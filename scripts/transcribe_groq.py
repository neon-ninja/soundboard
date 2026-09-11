#!/usr/bin/env python3
"""Transcribe every reel in ig_vids/ with Groq whisper-large-v3 (word timestamps).
Reads the API key from $GROQ_API_KEY (or a local groq.key file, gitignored). Output: ig_transcripts_groq/<id>.json"""
import glob, json, os, subprocess, sys, time, urllib.request, uuid

KEY = os.environ.get("GROQ_API_KEY") or open("groq.key").read().strip()
URL = "https://api.groq.com/openai/v1/audio/transcriptions"
os.makedirs("ig_transcripts_groq", exist_ok=True)
os.makedirs("groq_audio", exist_ok=True)

def multipart(fields, fpath):
    b = uuid.uuid4().hex
    body = b""
    for k, v in fields:
        body += f"--{b}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
    body += (f"--{b}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{os.path.basename(fpath)}\"\r\n"
             f"Content-Type: audio/mpeg\r\n\r\n").encode() + open(fpath, "rb").read() + f"\r\n--{b}--\r\n".encode()
    return body, f"multipart/form-data; boundary={b}"

def transcribe(fpath):
    fields = [("model", "whisper-large-v3"), ("response_format", "verbose_json"),
              ("timestamp_granularities[]", "word"), ("timestamp_granularities[]", "segment"), ("language", "zh")]
    body, ctype = multipart(fields, fpath)
    for attempt in range(8):
        req = urllib.request.Request(URL, data=body, headers={"Authorization": f"Bearer {KEY}", "Content-Type": ctype, "User-Agent": "curl/8.5.0"})
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")[:200]
            wait = e.headers.get("retry-after")
            wait = float(wait) if wait else min(600, 30 * (2 ** attempt))
            print(f"  HTTP {e.code}: {msg} — waiting {wait:.0f}s", flush=True)
            time.sleep(wait)
        except Exception as e:
            print(f"  error {e} — waiting 30s", flush=True); time.sleep(30)
    return None

files = sorted(glob.glob("ig_vids/*.mp4"))
for i, f in enumerate(files, 1):
    vid = os.path.basename(f)[:-4]
    out = f"ig_transcripts_groq/{vid}.json"
    if os.path.exists(out): continue
    # Groq caps uploads at 25 MB: 16 kHz mono MP3 at 48 kbps keeps even 20-min lives ~7 MB
    flac = f"groq_audio/{vid}.mp3"
    if not os.path.exists(flac):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f, "-vn", "-ar", "16000", "-ac", "1", "-b:a", "48k", flac], check=True)
    print(f"[{i}/{len(files)}] {vid} ({os.path.getsize(flac)/1e6:.1f} MB)", flush=True)
    res = transcribe(flac)
    if res is None:
        print("  FAILED", flush=True); continue
    json.dump({"duration": res.get("duration"), "text": res.get("text"),
               "segments": [{"start": s["start"], "end": s["end"], "text": s["text"]} for s in res.get("segments", [])],
               "words": res.get("words", [])}, open(out, "w"), ensure_ascii=False)
    time.sleep(2)
print("ALL DONE", flush=True)
