import subprocess
from faster_whisper import WhisperModel

CASES = [
 ("zh-gei-ni-chi",     "Dc87tC1Sgxj", 55.50, 58.50, "给你吃"),
 ("zh-wo-lai-shishi",  "Dcgd6JUSUS3", 111.75, 113.10, "我来试试"),
 ("zh-hen-you-weidao", "Dcgd6JUSUS3", 114.45, 115.75, "有味道"),
 ("zh-shide-shide",    "Dcs3tPNyft1", 658.45, 659.45, "是的是的"),
]
model = WhisperModel("small", device="cpu", compute_type="int8")
for name, vid, start, end, phrase in CASES:
    ws, we = max(0, start - 2.5), end + 2.5
    subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',f'{ws:.2f}','-i',f'ig_vids/{vid}.mp4',
                    '-t',f'{we-ws:.2f}','-vn','-ar','16000','-ac','1',f'/tmp/w_{name}.wav'], check=True)
    segs, _ = model.transcribe(f'/tmp/w_{name}.wav', language="zh", beam_size=5, word_timestamps=True)
    text = ""
    words = []
    for s in segs:
        text += s.text
        for w in (s.words or []):
            words.append((round(ws + 0, 2), w.word, round(ws + w.start, 2)))
    print(name, "| window text:", text.strip()[:80])
    hit = phrase in text.replace(" ", "")
    print("   phrase present:", hit)
    if hit:
        # locate phrase start time within window
        joined = ""
        for _, w, t in words:
            joined += w
            if phrase[:2] in joined[-len(phrase)*2:]:
                print("   near t≈", t)
                break
