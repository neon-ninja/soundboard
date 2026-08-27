import json, glob, re, sys

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

phrases = [
    "what the", "oh my gosh", "oh my god", "are you kidding", "wait what",
    "no no no", "so cute", "i can't even", "oh no", "seriously",
    "let's go", "shut up", "leave me alone", "i love you", "what is that",
    "excuse me", "get out", "oh my", "stop it", "you're the worst",
    "i hate you", "best friend", "what are you doing", "why are you",
    "that's adorable", "huh", "what do you want",
]

results = {}
for path in sorted(glob.glob('subs/*.en.json3')):
    vid = path.split('/')[-1].split('.en.json3')[0]
    words = load_words(path)
    toks = [w for _, w in words]
    for ph in phrases:
        pw = ph.split()
        for i in range(len(toks) - len(pw) + 1):
            if toks[i:i+len(pw)] == [w for w in pw]:
                t = words[i][0]
                end = words[min(i+len(pw), len(words)-1)][0]
                ctx = ' '.join(toks[max(0,i-4):i+len(pw)+5])
                results.setdefault(ph, []).append((vid, t/1000, (end-words[i][0])/1000, ctx))

for ph in phrases:
    hits = results.get(ph, [])
    print(f"### {ph}: {len(hits)} hits")
    for vid, t, dur, ctx in hits[:6]:
        print(f"   {vid} @ {t:8.1f}s | {ctx[:90]}")
