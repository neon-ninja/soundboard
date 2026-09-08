import json, glob, re, collections

docs = {}
for p in glob.glob("ig_transcripts/*.json"):
    vid = p.split("/")[-1][:-5]
    docs[vid] = json.load(open(p))

# n-gram mining over segment texts (character-based, Mandarin)
counts = collections.Counter()
where = collections.defaultdict(list)
for vid, d in docs.items():
    for seg in d["segments"]:
        t = re.sub(r"[\s,。，!！?？~、.]", "", seg["text"])
        for n in range(2, 8):
            for i in range(len(t)-n+1):
                g = t[i:i+n]
                counts[g] += 1
                if len(where[g]) < 8:
                    where[g].append((vid, seg["start"], seg["text"][:40]))

# report n-grams appearing in >= 4 reels, prefer longer
seen_docs = {g: len({v for v,_,_ in ws}) for g,ws in where.items()}
cands = [(g,c) for g,c in counts.items() if seen_docs.get(g,0) >= 4 and c >= 6]
cands.sort(key=lambda x: (-len(x[0]), -x[1]))
shown = []
for g, c in cands:
    if any(g in s for s in shown): continue  # skip substrings of already-shown longer grams
    shown.append(g)
    print(f"{c:4d}x in {seen_docs[g]:2d} reels | {g} | e.g. {where[g][0][0]} @ {where[g][0][1]}")
    if len(shown) >= 60: break
