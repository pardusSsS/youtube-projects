# What Is a Range-Doppler Map?

A vertical YouTube Short built with Manim + edge-tts and assembled with ffmpeg.

    output/short_what_is_a_range_doppler_map.mp4    1080×1920 60fps, 0:58, 5.3 MB
    output/short_what_is_a_range_doppler_map.srt    sentence-level subtitles

## The idea

A radar dwell does not return a blip. It returns a **table**: range down the
rows (fast time, one row per range gate) and pulse number across the columns
(slow time). Run an FFT along each row and the second axis stops being time and
becomes velocity — because a target's echo phase creeps from pulse to pulse, and
a creep is a frequency:

    v  =  λ · f_d / 2

Six scenes carry that from raw table to finished map, then to the two things the
map gives you for free and the one thing it takes away:

- everything not moving piles into the zero-Doppler column, so clutter
  rejection is a column mask
- the velocity axis is a DFT axis, so it **wraps**: past |v| = λ·PRF/4 a fast
  target folds back into the clutter and disappears

## How audio and picture stay locked

Timing is **derived**, never hand-tuned:

1. `voice.py` synthesises one MP3 per scene and measures each with ffprobe,
   writing `voiceovers/durations.json`.
2. Every scene in `short.py` subclasses `NarratedShort`. Its last statement is
   `self.fill()`, which reads that JSON, compares the narration length against
   `self.renderer.time` (how much animation has actually played), and waits out
   exactly the difference plus a 0.35 s tail.
3. `build.py` muxes each scene with its MP3, topping the audio up with silence
   (`apad`) so the track ends precisely with the picture.

Change a line of narration and the picture re-times itself on the next build.
The render log prints a per-scene sync report; anything over a 3 s pad is
flagged `<-- LONG PAD`, meaning that scene needs more animation, not more
waiting. Current build: every scene's silent tail is between 0.33 s and 0.80 s.

## Rendering 9:16 in Manim

Two things matter. Manim derives pixels-per-unit from `frame_width` alone and
never adjusts it for a tall canvas, so a vertical render silently letterboxes
the scene into a middle band; `short.py` pins `frame_height = 8.0` and
`frame_width = 4.5` to make the 1080×1920 frame exactly 4.5 × 8 units. And the
frame is then only 4.5 units across, so every text block goes through `fit()`,
which shrinks anything wider than 4.05 units. Content is also kept above
y = −3.0, clear of the Shorts title overlay.

**No LaTeX is used.** `MathTex`/`DecimalNumber` are avoided deliberately, since
they shell out to `latex`. All formulas are Pango `Text` with Unicode glyphs,
and the live velocity readout in scene 6 goes through `live_text()`.

## Build

    python build.py                  # voice + 1080×1920 60fps + mux + concat + SRT
    python build.py --quality m      # 720×1280 30fps draft, much faster
    python build.py --quality l      # 480×854 15fps, for layout checks
    python build.py --skip-voice     # reuse existing voiceovers/
    python build.py --only Short3    # iterate on one scene

Requires `manim`, `edge-tts` and `ffmpeg` on PATH. In this repo the toolchain
lives in the shared virtualenv one level up:

    ../.venv-video/bin/python build.py

## Files

    voice.py     narration + edge-tts synthesis + duration measurement
    short.py     palette, shared builders, and the six scenes (Short1 … Short6)
    build.py     the pipeline, plus the sync report and SRT generation
    voiceovers/  generated MP3s and durations.json     (gitignored)
    media/       Manim's render tree                   (gitignored)
    work/        per-scene muxed segments              (gitignored)
    output/      the finished files                    (gitignored)

## Scene map

    1  the hook — a dwell hands you a picture, not a blip
    2  the raw table: range down the rows, pulse number across
    3  one row, phase creeping pulse to pulse, FFT → speed
    4  every row, one FFT → the map, and how to read its three axes
    5  reading blips, and clutter rejection as a column mask
    6  the axis wraps — |v| < λ·PRF/4, and folding into the clutter
