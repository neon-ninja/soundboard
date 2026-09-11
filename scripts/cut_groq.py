#!/usr/bin/env python3
"""Cut clips at large-v3 word boundaries and verify each via Groq whisper-large-v3."""
import json, os, subprocess, sys, urllib.request, uuid
KEY = os.environ.get("GROQ_API_KEY") or open("groq.key").read().strip()
AF = 'loudnorm=I=-16:TP=-1.5:LRA=11'
CLIPS = [
 # name, vid, start, end
 ("zh-kakashi",           "DaR6T6VyiI0", 0.86, 2.62),
 ("zh-kashi-shang",       "Dc3t2xfysR0", 6.20, 7.48),
 ("zh-kashi-zhenbang",    "Db3LiWSSZuo", 7.76, 9.14),
 ("zh-zhen-guai",         "Db3LiWSSZuo", 71.38, 72.96),
 ("zh-guai-guai-guai",    "Dc_UWTqS5TB", 60.44, 61.58),
 ("zh-sun-wukong",        "DcJClRZyWq7", 5.94, 7.40),
 ("zh-zhu-bajie",         "DcItKJCywa4", 77.82, 78.98),
 ("zh-kashi-woshou",      "DcItKJCywa4", 76.00, 77.22),
 ("zh-kashi-zuo",         "Dc0zOnFSVyc", 53.74, 55.12),
 ("zh-qu-xiang-zeng-xing","DcYypNtSDEa", 34.82, 36.62),   # sung take
 ("zh-gei-ni-chi",        "Dc87tC1Sgxj", 58.55, 59.94),
 ("zh-wo-shi-dijia",      "Db571mnS4ad", 34.75, 36.55),   # sung take (hummed intro)
 ("zh-xiexie-guanzhu",    "Dcs3tPNyft1", 1035.12, 1036.66),
 ("zh-xiexie-xiongdi",    "Dcs3tPNyft1", 755.28, 756.49),
 ("zh-xiexie-dajia",      "DcnrwfqSgWr", 530.42, 532.52),
 ("zh-wa-sai",            "DcnrwfqSgWr", 121.20, 122.20),
 ("zh-chaoji-wudi",       "DcjQiHbyoEd", 264.00, 267.20),
 ("zh-hao-da-de-huo",      "Dcf1pPSyi8l", 627.52, 628.98),
 ("zh-shide-shide",       "DcnlNSSytWY", 633.28, 635.10),
 ("zh-kandaole-ma",       "DctL9n5Sj0V", 314.75, 316.05),
 ("zh-duoshao-qian",      "DctL9n5Sj0V", 359.53, 360.55),
 ("zh-gei-dajia-kan",     "DctL9n5Sj0V", 284.70, 285.90),
 ("zh-hao-xiang-ya",      "Dcgd6JUSUS3", 79.32, 81.55),
]
def groq(fpath):
    b = uuid.uuid4().hex
    body = b""
    for k, v in [("model","whisper-large-v3"),("response_format","json"),("language","zh"),("prompt","卡卡西，孙悟空，猪八戒，真乖，去香增腥，我是迪迦，谢谢关注，超级无敌，好大的火呀")]:
        body += f"--{b}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
    body += (f"--{b}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"c.mp3\"\r\nContent-Type: audio/mpeg\r\n\r\n").encode() + open(fpath,"rb").read() + f"\r\n--{b}--\r\n".encode()
    req = urllib.request.Request("https://api.groq.com/openai/v1/audio/transcriptions", data=body,
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": f"multipart/form-data; boundary={b}", "User-Agent": "curl/8.5.0"})
    with urllib.request.urlopen(req, timeout=120) as r: return json.load(r)["text"]
only = set(sys.argv[1:])
for name, vid, s, e in CLIPS:
    if only and name not in only: continue
    out = f"clips_zh/{name}.mp3"
    subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',f'{s:.3f}','-i',f'ig_vids/{vid}.mp4','-t',f'{e-s:.3f}',
                    '-vn','-af',AF,'-ar','44100','-b:a','128k',out], check=True)
    try: heard = groq(out)
    except Exception as ex: heard = f"(verify error: {ex})"
    print(f"{name:24s} {e-s:4.2f}s → {heard.strip()[:40]}")
