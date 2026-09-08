import json, glob, os
from faster_whisper import WhisperModel

model = WhisperModel("small", device="cpu", compute_type="int8")
os.makedirs("ig_transcripts", exist_ok=True)
files = sorted(glob.glob("ig_vids/*.mp4"))
for f in files:
    vid = os.path.basename(f)[:-4]
    out = f"ig_transcripts/{vid}.json"
    if os.path.exists(out): continue
    try:
        segs, info = model.transcribe(f, language="zh", word_timestamps=True, vad_filter=True)
        data = []
        for s in segs:
            data.append({"start": round(s.start,2), "end": round(s.end,2), "text": s.text,
                         "words": [{"w": w.word, "s": round(w.start,2), "e": round(w.end,2)} for w in (s.words or [])]})
        json.dump({"duration": info.duration, "segments": data}, open(out,"w"), ensure_ascii=False)
        print(vid, "ok", len(data), "segs")
    except Exception as e:
        print(vid, "FAIL", e)
