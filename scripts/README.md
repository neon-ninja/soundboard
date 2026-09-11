# Clip-making pipeline

These are the scripts used to find and cut the soundboard's voice clips.
They expect this working layout (paths are relative to the directory you
run them from):

```
subs/<video-id>.en.json3   # YouTube auto-captions, word-level timestamps
vids/<video-id>.webm       # episode video/audio (Internet Archive mirrors)
clips*/                    # output MP3s
```

## Pipeline

1. **Fetch transcripts** — for each episode's YouTube ID:

   ```bash
   yt-dlp --skip-download --write-auto-subs --sub-langs en \
          --sub-format json3 -o "subs/%(id)s.%(ext)s" <video-url>
   ```

2. **Find source media** — `ia_survey.py` searches Internet Archive items
   for Aphmau uploads; `ia_list_files.py` lists an item's files with the
   original YouTube IDs parsed out of the filenames (so transcript
   timestamps line up with the mirrored media — verify with `ffprobe`
   duration vs. the last caption timestamp).

3. **Search for phrases** — `phrase_search.py` (catchphrases),
   `sleep_search.py` (sleep/bedtime words), and `imp_search.py`
   (imperative bedtime commands) flatten each `json3` transcript into a
   word list with per-word times and print every phrase match with its
   timestamp and surrounding context.

4. **Cut clips** — `cut_clips.py` (original 19), `cut_sleep.py`
   (Sleepy Time section), and `cut_imp.py` ("Time for bed, you two!")
   each hold a table of (name, video, phrase, approximate time, padding).
   They re-locate the phrase in the transcript, set the clip end at the
   word following the phrase, then cut with ffmpeg: trailing-silence trim,
   loudness normalisation to −16 LUFS, 128 kbps MP3 output.

The search scripts are read-only and safe to re-run; the cut scripts
overwrite their output MP3s.

## Instagram / Mandarin pipeline (思思 section)

Reels have no captions, so this pipeline transcribes them locally:

1. Download reels with `yt-dlp --cookies <cookies.txt> -a <url-list>`
   (a logged-in Instagram session is required; cookies are never committed).
2. `transcribe_groq.py` — Groq-hosted whisper-large-v3 transcription of
   every downloaded reel (16 kHz mono MP3 uploads, word + segment
   timestamps). Needs `GROQ_API_KEY`. This replaced the original
   `transcribe_all.py` (local faster-whisper small/medium on CPU), whose
   garbled output caused several mis-cut and mislabelled clips.
3. `mine_phrases.py` — character n-gram mining across all transcripts to
   surface phrases repeated in many reels.
4. `cut_groq.py` — clip table cut at large-v3 word boundaries, then each
   MP3 is sent back through Groq to confirm it transcribes to the intended
   phrase. (`cut_zh.py` is the older table used with the local models.)
   `groq_search.py REGEX` greps the transcripts with word-level times.
5. `verify_wide.py` — sanity-checks a cut by re-transcribing a ±2.5 s
   window around it and asserting the phrase is present; clips that
   failed this check were re-cut from other occurrences or dropped.

## Last Asylum: Plague (Asylum board)

`extract_asylum_sfx.py` extracts the battle win/loss jingles and a dozen
short interaction effects (chest open, coins, level-up, unlocks…) from the
game's Wwise soundbank (APK download via apkeep, DIDX/DATA carving,
vgmstream decode, ffmpeg loudnorm). The extracted audio is the game
developer's copyrighted material, so the repo ships the tooling only:
run the script locally and the Asylum board's buttons light up.
`sounds/game-*.mp3` is gitignored; committing the results is your
decision to make, not this repo's default.
