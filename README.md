# Aphmau Soundboard 🐾

A fan-made mobile-friendly soundboard webapp featuring short voice clips of
common phrases from Aphmau's *MyStreet: Phoenix Drop High* Minecraft roleplay
series — including a full collection of six different "What the—?!" variants.

## Run it

It's a static site — no build step. Either open `index.html` directly, or serve
the folder:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Features

- **19 sound clips** organised into three sections: the "WHAT THE—?!"
  collection, Classics, and Maximum Sass
- **Web Audio API** playback for low-latency, overlapping sounds, with an
  `<audio>` element fallback
- **Mobile-first design**: big touch targets, tap animations, haptic feedback
  (vibration) on supported devices, safe-area insets for notched phones
- **Random button** (🎲) that plays a surprise clip

## How the clips were made

1. Episode audio was sourced with `yt-dlp` (episodes of *MyStreet: Phoenix
   Drop High*, which are archived on the Internet Archive).
2. Word-level transcripts (YouTube auto-generated captions in `json3` format)
   were fetched with `yt-dlp --write-auto-subs --sub-format json3`.
3. A Python script searched the transcripts for target phrases ("what the",
   "oh my gosh", "are you kidding me", …) and computed precise start/end
   timestamps from the word timings.
4. `ffmpeg` cut each clip with a little padding and applied loudness
   normalisation (`loudnorm I=-16`) so every button plays at a consistent
   volume, exporting 128 kbps MP3s.

## Credits

All voice clips are from [Aphmau](https://www.youtube.com/@Aphmau)'s
*MyStreet: Phoenix Drop High* series and remain the property of their
respective owners. This is a non-commercial fan project for personal
entertainment.
