import json, subprocess, os

cache = {}
def words_of(vid):
    if vid not in cache:
        d = json.load(open(f'subs/{vid}.en.json3'))
        times, toks = [], []
        for ev in d.get('events', []):
            t0 = ev.get('tStartMs', 0)
            for seg in ev.get('segs', []) or []:
                w = seg.get('utf8', '').strip()
                if not w or w == '\n': continue
                times.append((t0 + seg.get('tOffsetMs', 0)) / 1000.0)
                toks.append(w.lower())
        cache[vid] = (times, toks)
    return cache[vid]

# name, vid, phrase, approx_t, extra_words_after, lead_pad, tail_pad
CLIPS = [
 ("slumber-party",   "DN_1itWH9-M", "this is the bestest slumber party ever", 927.0, 0, 0.20, 0.20),
 ("first-sleepover", "DN_1itWH9-M", "remember this is my first sleepover", 167.5, 0, 0.20, 0.20),
 ("take-a-nap",      "UOFwXXmSFf8", "i was about to take a nap", 253.6, 0, 0.20, 0.15),
 ("wake-up",         "UOFwXXmSFf8", "hey hey wake up", 669.4, 0, 0.20, 0.20),
 ("good-night",      "SeHDnlZ91mg", "have a good night", 56.7, 0, 0.20, 0.25),
 ("go-to-bed",       "SeHDnlZ91mg", "i have to go to bed", 383.6, 0, 0.20, 0.20),
 ("back-to-sleep",   "SnPzuLqA5TY", "go back to sleep i'm really really tired", 175.4, 0, 0.20, 0.20),
 ("pajamas",         "SnPzuLqA5TY", "i'm still in my pajamas", 280.5, 0, 0.20, 0.20),
 ("fell-asleep",     "Rn0GIgk6ZJw", "i almost fell asleep", 114.0, 0, 0.25, 0.20),
 ("right-to-sleep",  "4kAejvdDWsc", "she fell right to sleep", 341.7, 0, 0.20, 0.20),
]

os.makedirs('clips_sleep', exist_ok=True)
for name, vid, phrase, approx, extra, lead, tail in CLIPS:
    times, toks = words_of(vid)
    pw = phrase.split()
    best = None
    for i in range(len(toks) - len(pw) + 1):
        if toks[i:i+len(pw)] == pw and abs(times[i] - approx) < 3.0:
            best = i; break
    if best is None:
        print(name, "NOT FOUND"); continue
    end_idx = best + len(pw) + extra
    start = max(0, times[best] - lead)
    end = (times[end_idx] if end_idx < len(times) else times[-1] + 1.0) + tail
    dur = min(end - start, 4.5)
    out = f'clips_sleep/{name}.mp3'
    subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',f'{start:.3f}','-i',f'vids/{vid}.webm',
                    '-t',f'{dur:.3f}','-vn','-af','areverse,silenceremove=start_periods=1:start_duration=0.35:start_threshold=-42dB,areverse,loudnorm=I=-16:TP=-1.5:LRA=11','-ar','44100','-b:a','128k',out], check=True)
    print(f"{name}: {start:.2f}s +{dur:.2f}s from {vid}")
