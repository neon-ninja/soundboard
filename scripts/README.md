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
