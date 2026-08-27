import json, subprocess, os

def load_words(vid):
    d = json.load(open(f'subs/{vid}.en.json3'))
    words = []
    for ev in d.get('events', []):
        t0 = ev.get('tStartMs', 0)
        for seg in ev.get('segs', []) or []:
            w = seg.get('utf8', '').strip()
            if not w or w == '\n': continue
            words.append((t0 + seg.get('tOffsetMs', 0)) / 1000.0)
            wordlist.append(w.lower())
    return words

cache = {}
def words_of(vid):
    if vid not in cache:
        global wordlist
        wordlist = []
        times = load_words(vid)
        cache[vid] = (times, list(wordlist))
    return cache[vid]

# name, vid, phrase, approx_t, extra_words_after, lead_pad, tail_pad
CLIPS = [
 ("what-the-1",       "1VdB6zwZ2QQ", "what the", 27.7, 0, 0.20, 0.15),
 ("what-the-2",       "1VdB6zwZ2QQ", "what the", 74.8, 0, 0.20, 0.15),
 ("what-the-3",       "1VdB6zwZ2QQ", "what the", 415.1, 0, 0.20, 0.20),
 ("what-the-4",       "4kAejvdDWsc", "what the", 465.7, 0, 0.20, 0.15),
 ("what-the-5",       "4kAejvdDWsc", "what the", 650.2, 0, 0.20, 0.15),
 ("what-the-6",       "6CkxS22FMkI", "what the", 426.7, 0, 0.20, 0.15),
 ("oh-my-gosh",       "38QBRLxaF18", "oh my gosh", 236.6, 0, 0.20, 0.15),
 ("are-you-kidding-me","38QBRLxaF18", "are you kidding me", 607.5, 0, 0.20, 0.15),
 ("wait-what",        "4kAejvdDWsc", "wait wait wait what", 53.5, 0, 0.20, 0.15),
 ("no-no-no",         "4kAejvdDWsc", "no no no", 379.8, 0, 0.20, 0.15),
 ("sos-cute",         "4kAejvdDWsc", "she's so cute", 205.0, 0, 0.20, 0.20),
 ("oh-no-you-dont",   "38QBRLxaF18", "oh no you don't young lady", 962.0, 0, 0.20, 0.15),
 ("leave-me-alone",   "1VdB6zwZ2QQ", "leave me alone", 510.0, 0, 0.20, 0.20),
 ("excuse-me",        "1VdB6zwZ2QQ", "excuse me what do you want", 494.1, 0, 0.20, 0.15),
 ("what-is-that",     "1VdB6zwZ2QQ", "what is that", 579.7, 0, 0.20, 0.20),
 ("shut-up",          "1VdB6zwZ2QQ", "shut up", 759.8, 0, 0.20, 0.25),
 ("get-out",          "6CkxS22FMkI", "get out", 97.9, 1, 0.20, 0.15),
 ("stop-it",          "6CkxS22FMkI", "zane stop it", 653.5, 0, 0.20, 0.20),
 ("lets-go",          "38QBRLxaF18", "let's go now", 109.2, 0, 0.20, 0.15),
]

os.makedirs('clips', exist_ok=True)
report = []
for name, vid, phrase, approx, extra, lead, tail in CLIPS:
    times, toks = words_of(vid)
    pw = phrase.split()
    best = None
    for i in range(len(toks) - len(pw) + 1):
        if toks[i:i+len(pw)] == pw and abs(times[i] - approx) < 3.0:
            best = i; break
    if best is None:
        report.append((name, "NOT FOUND")); continue
    end_idx = best + len(pw) + extra
    start = max(0, times[best] - lead)
    end = (times[end_idx] if end_idx < len(times) else times[-1] + 1.0) + tail
    dur = min(end - start, 4.0)
    out = f'clips/{name}.mp3'
    subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',f'{start:.3f}','-i',f'vids/{vid}.webm',
                    '-t',f'{dur:.3f}','-vn','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-ar','44100','-b:a','128k',out], check=True)
    report.append((name, f"{start:.2f}s +{dur:.2f}s from {vid}"))
for r in report: print(*r)
