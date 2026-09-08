import subprocess, os
CLIPS = [
 ("zh-full-intro",      "DcQ8DjWy9Lv", 0.35, 7.00),
 ("zh-hey-boy",         "Dc5QOG3SyyM", 0.30, 2.05),
 ("zh-listen-to-me",    "Dc5QOG3SyyM", 2.10, 3.55),
 ("zh-i-wanna-tell-you","Dc5QOG3SyyM", 6.25, 7.75),
 ("zh-xiexie-guanzhu",  "Dcs3tPNyft1", 754.05, 755.05),
 ("zh-xiexie-xiongdi",  "Dcs3tPNyft1", 754.95, 756.45),
 ("zh-xiexie-dajia",    "DcnrwfqSgWr", 530.85, 532.40),
 ("zh-wa-sai",          "DcnrwfqSgWr", 120.95, 122.35),
 ("zh-chaoji-wudi",     "DcjQiHbyoEd", 264.25, 268.10),
 ("zh-hao-xiang-ya",    "Dcgd6JUSUS3", 79.10, 81.60),
 ("zh-gei-ni-chi",      "Dcs3tPNyft1", 507.60, 508.75),
 ("zh-wo-lai-shishi",   "Dcgd6JUSUS3", 111.70, 114.20),
 ("zh-hen-you-weidao",  "Dcgd6JUSUS3", 114.40, 115.60),
 ("zh-shide-shide",     "DcfQZZ2Ssnj", 3.25, 4.35),
 ("zh-kandaole-ma",     "DctL9n5Sj0V", 314.80, 316.10),
 ("zh-duoshao-qian",    "DctL9n5Sj0V", 359.30, 360.70),
 ("zh-gei-dajia-kan",   "DctL9n5Sj0V", 283.60, 285.85),
]
os.makedirs("clips_zh", exist_ok=True)
for name, vid, start, end in CLIPS:
    out = f"clips_zh/{name}.mp3"
    subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',f'{start:.3f}','-i',f'ig_vids/{vid}.mp4',
                    '-t',f'{end-start:.3f}','-vn',
                    '-af','areverse,silenceremove=start_periods=1:start_duration=0.35:start_threshold=-42dB,areverse,loudnorm=I=-16:TP=-1.5:LRA=11',
                    '-ar','44100','-b:a','128k',out], check=True)
    print(name, f"{end-start:.2f}s")
