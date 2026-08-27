import json, subprocess, time, re
def fetch(url, tries=5):
    for i in range(tries):
        r = subprocess.run(["curl","-s","--max-time","60",url], capture_output=True, text=True)
        if r.stdout.strip():
            try:
                d=json.loads(r.stdout)
                if d.get('files'): return d
            except Exception: pass
        time.sleep(3)
    return None
it="5-weekend-friends-my-street-phoenix-drop-high-ep.-5-minecraft-roleplay-tdcfeppjyb-e"
d=fetch(f"https://archive.org/metadata/{it}")
print("nfiles:", len(d['files']), "dir:", d.get("dir"), "server:", d.get("server"))
for f in d['files']:
    n=f['name']
    if n.endswith(('.mp4','.mkv','.webm')):
        m=re.search(r'\[([A-Za-z0-9_-]{11})\]', n)
        print(round(int(f.get('size',0))/1e6,1),"MB |", (m.group(1) if m else "NO-ID"), "|", n)
