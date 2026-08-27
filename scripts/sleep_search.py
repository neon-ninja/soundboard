import json, glob

def load_words(path):
    d = json.load(open(path))
    words = []
    for ev in d.get('events', []):
        t0 = ev.get('tStartMs', 0)
        for seg in ev.get('segs', []) or []:
            w = seg.get('utf8', '').strip()
            if not w or w == '\n': continue
            words.append((t0 + seg.get('tOffsetMs', 0), w.lower()))
    return words

phrases = ["good night", "goodnight", "go to sleep", "go to bed", "time for bed",
           "i'm so tired", "so tired", "i'm tired", "sleepy", "wake up", "woke up",
           "take a nap", "nap", "sleepover", "slumber party", "sweet dreams",
           "dream", "pajamas", "sleep", "bedtime", "stay up", "in bed", "asleep"]

for path in sorted(glob.glob('subs/*.en.json3')):
    vid = path.split('/')[-1].split('.en.json3')[0]
    words = load_words(path)
    toks = [w for _, w in words]
    for ph in phrases:
        pw = ph.split()
        for i in range(len(toks) - len(pw) + 1):
            if toks[i:i+len(pw)] == pw:
                t = words[i][0]/1000
                ctx = ' '.join(toks[max(0,i-5):i+len(pw)+6])
                print(f"{ph:15s} {vid} @ {t:7.1f}s | {ctx[:95]}")
