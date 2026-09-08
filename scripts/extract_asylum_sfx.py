#!/usr/bin/env python3
"""Extract the battle win/loss jingles from Last Asylum: Plague (com.phs.global).

Run this yourself, on your own machine — the extracted audio is the game
developer's copyrighted material, so this repo ships the tooling only,
never the sounds. Whether extracting and hosting them is OK is your call
to make (and your jurisdiction's), not this script's.

Steps it performs:
 1. Downloads the game XAPK from APKPure via `apkeep`
    (https://github.com/EFForg/apkeep), unless --xapk is given.
 2. Unzips the asset pack and locates the Wwise soundbanks (scene_2024.bnk
    and sfx_2024.bnk).
 3. Parses each bank's DIDX/DATA sections and carves out the embedded .wem
    media files listed in TARGETS below — battle win/loss jingles plus a
    dozen short interaction effects (chest open, rewards, coins, level-up,
    unlocks, UI click…), all identified via the game's SoundbanksInfo.json.
 4. Decodes them with vgmstream-cli (https://vgmstream.org) and encodes
    loudness-normalised MP3s with ffmpeg into sounds/game-*.mp3.

Prerequisites on PATH: apkeep (step 1 only), vgmstream-cli, ffmpeg.

Usage:
    python3 scripts/extract_asylum_sfx.py [--xapk path/to/com.phs.global.xapk]

The soundboard's Asylum board picks the files up automatically once they
exist. sounds/game-*.mp3 is gitignored by default; remove that line from
.gitignore yourself if you decide to commit them.
"""
import argparse, os, shutil, struct, subprocess, sys, tempfile, zipfile

PACKAGE = "com.phs.global"
BANK_DIR = "assets/CustomDatas/Audio/GeneratedSoundBanks/Android"
# bank file -> {wwise media id: output basename}
# ids/names come from the game's own SoundbanksInfo.json (event -> media map)
TARGETS = {
    "scene_2024.bnk": {
        910607432: "game-battle-win",     # win_ver_18.wav          ~1.0s
        1020441531: "game-battle-loss",   # lose_3_ver_2.wav        ~1.3s
    },
    "sfx_2024.bnk": {
        777978140: "game-chest-open",     # box_open_ver_18.wav     ~1.0s
        495340830: "game-get-reward",     # get_reward_ver_17.wav   ~2.9s
        91809598: "game-get-coin",        # item_fly_get_coin       ~0.5s
        315840682: "game-get-star",       # item_fly_get_star       ~1.3s
        1073572823: "game-level-up",      # menu_fade_in_level_up_3 ~1.7s
        235607711: "game-hero-unlock",    # eft_unlock_ver_7.wav    ~0.5s
        175008223: "game-feature-unlock", # feature_unlock_ver_18   ~2.7s
        235809080: "game-build-finish",   # eft_level_up_2_ver_18   ~2.4s
        885733322: "game-click",          # common_click_ver_18     ~0.1s
        239329685: "game-map-unlock",     # eft_map_unlock_ver_18   ~1.4s
    },
}
LOUDNORM = "loudnorm=I=-16:TP=-1.5:LRA=11"


def need(tool):
    if not shutil.which(tool):
        sys.exit(f"error: `{tool}` not found on PATH — see the docstring for install links")


def download_xapk(workdir):
    need("apkeep")
    print(f"downloading {PACKAGE} via apkeep…")
    subprocess.run(["apkeep", "-a", PACKAGE, "-d", "apk-pure", workdir], check=True)
    path = os.path.join(workdir, f"{PACKAGE}.xapk")
    if not os.path.exists(path):
        sys.exit("error: apkeep did not produce the expected .xapk")
    return path


def carve_bank(bank_bytes, wanted_ids):
    """Parse Wwise .bnk sections; return {media_id: wem_bytes} for wanted_ids."""
    out, pos = {}, 0
    didx, data = None, None
    while pos + 8 <= len(bank_bytes):
        tag = bank_bytes[pos:pos + 4]
        size = struct.unpack_from("<I", bank_bytes, pos + 4)[0]
        body = bank_bytes[pos + 8:pos + 8 + size]
        if tag == b"DIDX":
            didx = body
        elif tag == b"DATA":
            data = body
        pos += 8 + size
    if didx is None or data is None:
        sys.exit("error: bank has no DIDX/DATA sections — format changed?")
    for i in range(0, len(didx), 12):
        media_id, offset, length = struct.unpack_from("<III", didx, i)
        if media_id in wanted_ids:
            out[media_id] = data[offset:offset + length]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--xapk", help="already-downloaded .xapk (skips apkeep)")
    ap.add_argument("--outdir", default="sounds", help="output directory (default: sounds/)")
    args = ap.parse_args()

    need("vgmstream-cli")
    need("ffmpeg")
    os.makedirs(args.outdir, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        xapk = args.xapk or download_xapk(tmp)
        print("unpacking asset pack…")
        with zipfile.ZipFile(xapk) as z:
            with z.open("abPack1.apk") as inner:
                inner_path = os.path.join(tmp, "abPack1.apk")
                with open(inner_path, "wb") as f:
                    shutil.copyfileobj(inner, f)
        with zipfile.ZipFile(inner_path) as z:
            for bank_file, targets in TARGETS.items():
                bank = z.read(f"{BANK_DIR}/{bank_file}")
                print(f"carving {len(targets)} wems from {bank_file}…")
                wems = carve_bank(bank, set(targets))
                missing = set(targets) - set(wems)
                if missing:
                    sys.exit(f"error: media ids not found in {bank_file}: {missing}")
                for media_id, name in targets.items():
                    wem = os.path.join(tmp, f"{media_id}.wem")
                    wav = os.path.join(tmp, f"{media_id}.wav")
                    with open(wem, "wb") as f:
                        f.write(wems[media_id])
                    subprocess.run(["vgmstream-cli", "-o", wav, wem], check=True,
                                   stdout=subprocess.DEVNULL)
                    out = os.path.join(args.outdir, f"{name}.mp3")
                    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav,
                                    "-af", LOUDNORM, "-ar", "44100", "-b:a", "128k", out],
                                   check=True)
                    print(f"  wrote {out}")

    print("done — reload the soundboard and the Asylum board will light up.")


if __name__ == "__main__":
    main()
