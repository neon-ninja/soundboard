import json, subprocess, time, sys

items = [
 "20251015_20251015_0920",
 "ep.-30-dont-tell-aaron-pt.-2-mom-ro-meave-minecraft-my-street-e-aphmau-20160226-1920x-1080",
 "2-want-to-start-anime-club-my-street-upsidedown-stories-hai-o-5zm-mdj-m",
 "5-weekend-friends-my-street-phoenix-drop-high-ep.-5-minecraft-roleplay-tdcfeppjyb-e",
 "the-decoration-fight-minecraft-my-street-ep.-7-minecraft-roleplay-720p-60fps-h-264-128kbit-aac",
 "Aphmau-YandereSimulator",
]

def fetch(url, tries=4):
    for i in range(tries):
        r = subprocess.run(["curl","-s","--max-time","60",url], capture_output=True, text=True)
        if r.stdout.strip():
            try: return json.loads(r.stdout)
            except Exception: pass
        time.sleep(3)
    return None

for it in items:
    d = fetch(f"https://archive.org/metadata/{it}")
    if not d or not d.get('files'):
        print(f"=== {it}: FAILED/EMPTY"); continue
    m = d.get('metadata',{})
    print(f"=== {it} | unavailable={d.get('servers_unavailable')} | {str(m.get('title'))[:60]}")
    print("   orig:", str(m.get('originalurl',''))[:80])
    vids = [f for f in d['files'] if f['name'].endswith(('.mp4','.mkv','.webm','.m4a','.mp3'))]
    subs = [f for f in d['files'] if f['name'].endswith(('.vtt','.srt','.json3'))]
    print(f"   {len(vids)} media, {len(subs)} sub files")
    for f in vids[:6]:
        print("   ", round(int(f.get('size',0))/1e6,1),"MB |", f['name'][:90])
    for f in subs[:4]:
        print("   SUB:", f['name'][:90])
