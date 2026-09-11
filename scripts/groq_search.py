#!/usr/bin/env python3
"""Search Groq whisper-large-v3 transcripts. Usage: groq_search.py REGEX [maxlen]"""
import glob, json, re, sys
pat = re.compile(sys.argv[1], re.I)
maxlen = int(sys.argv[2]) if len(sys.argv) > 2 else 40
for p in sorted(glob.glob("ig_transcripts_groq/*.json")):
    vid = p.split("/")[-1][:-5]
    d = json.load(open(p))
    words = d.get("words", [])
    for seg in d["segments"]:
        t = seg["text"].strip()
        if pat.search(t) and len(t) <= maxlen:
            # word-level times inside this segment
            ws = [w for w in words if seg["start"] - 0.05 <= w["start"] <= seg["end"] + 0.05]
            wtxt = " ".join(f"{w['word']}@{w['start']:.2f}" for w in ws[:16])
            print(f"{vid} [{seg['start']:8.2f}-{seg['end']:8.2f}] {t[:60]}")
            print(f"     {wtxt[:150]}")
