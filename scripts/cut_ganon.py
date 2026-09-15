import json, subprocess, urllib.request, uuid
import os
KEY = os.environ.get("GROQ_API_KEY") or open("groq.key").read().strip()
AF = 'loudnorm=I=-16:TP=-1.5:LRA=11'
SRC = "yt/EGDR4AOIp3g.webm"
CLIPS = [
 ("ganon-suavemente",        22.85, 24.30),   # sung: "Suavemente!"
 ("ganon-suavemente-besame", 22.85, 26.05),   # sung: "Suavemente, bésame"
 ("ganon-a-ver-si-te-gusta", 53.20, 54.95),   # ¡A ver si te gusta esto!
 ("ganon-toma",              59.15, 59.90),   # ¡Toma!
 ("ganon-ni-siquiera",       66.55, 68.75),   # Ni siquiera he comenzado
 ("ganon-que-pasa",          76.20, 77.90),   # ¿Qué pasa?
 ("ganon-tienes-miedo",      78.05, 79.75),   # ¿Tienes miedo?
]
def groq(fpath):
    b = uuid.uuid4().hex; body = b""
    for k, v in [("model","whisper-large-v3"),("response_format","json"),("language","es")]:
        body += f"--{b}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
    body += (f"--{b}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"c.mp3\"\r\nContent-Type: audio/mpeg\r\n\r\n").encode() + open(fpath,"rb").read() + f"\r\n--{b}--\r\n".encode()
    req = urllib.request.Request("https://api.groq.com/openai/v1/audio/transcriptions", data=body,
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": f"multipart/form-data; boundary={b}", "User-Agent": "curl/8.5.0"})
    with urllib.request.urlopen(req, timeout=120) as r: return json.load(r)["text"].strip()
for name, s, e in CLIPS:
    out = f"clips_ganon/{name}.mp3"
    subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',f'{s:.3f}','-i',SRC,'-t',f'{e-s:.3f}','-vn','-af',AF,'-ar','44100','-b:a','128k',out], check=True)
    print(f"{name:26s} {e-s:4.2f}s → {groq(out)[:50]}")
