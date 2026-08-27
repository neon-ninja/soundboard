import json, subprocess

d = json.load(open('subs/gSrIBEgrxSU.en.json3'))
times, toks = [], []
for ev in d.get('events', []):
    t0 = ev.get('tStartMs', 0)
    for seg in ev.get('segs', []) or []:
        w = seg.get('utf8', '').strip()
        if not w or w == '\n': continue
        times.append((t0 + seg.get('tOffsetMs', 0)) / 1000.0)
        toks.append(w.lower())

pw = "time for bed you two".split()
for i in range(len(toks) - len(pw) + 1):
    if toks[i:i+len(pw)] == pw:
        start = times[i] - 0.25
        end_idx = i + len(pw)
        end = (times[end_idx] if end_idx < len(times) else times[-1] + 1.0) + 0.20
        dur = min(end - start, 3.5)
        print(f"cut {start:.2f}s +{dur:.2f}s | ctx:", ' '.join(toks[max(0,i-4):i+len(pw)+4]))
        subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',f'{start:.3f}','-i','vids/gSrIBEgrxSU.webm',
                        '-t',f'{dur:.3f}','-vn',
                        '-af','areverse,silenceremove=start_periods=1:start_duration=0.35:start_threshold=-42dB,areverse,loudnorm=I=-16:TP=-1.5:LRA=11',
                        '-ar','44100','-b:a','128k','clips_sleep/time-for-bed.mp3'], check=True)
        break
