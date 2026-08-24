# How Radar Measures Distance AND Speed

A ~10.6 minute narrated explainer, built with Manim + edge-tts and assembled with ffmpeg.

    output/how_radar_measures_distance_and_speed.mp4    1920×1080, 60 fps
    output/how_radar_measures_distance_and_speed.srt    sentence-level subtitles

## The idea

Two measurements, two entirely different mechanisms:

    range     R  =  c · Δt / 2         time of flight
    velocity  v  =  λ · f_d / 2        Doppler shift

Twenty scenes walk from the first transmitted pulse to range-Doppler maps,
blind speeds and FMCW chirps, with the real equations and the real trade-offs.

## How audio and picture stay locked

This is the part worth knowing about. Timing is **derived**, never hand-tuned:

1. `voice.py` synthesises one MP3 per scene and measures each one with ffprobe,
   writing `voiceovers/durations.json`.
2. Every scene in `main.py` subclasses `NarratedScene`. Its last statement is
   `self.fill()`, which reads that JSON, compares the narration length against
   `self.renderer.time` (how much animation has actually played), and waits out
   exactly the difference plus a 0.6 s tail.
3. `build.py` muxes each scene with its MP3, topping the audio up with silence
   (`apad`) so the track ends precisely with the picture.

Change a line of narration and the picture re-times itself on the next build.
The render log prints a per-scene sync report; anything over a 5 s pad is
flagged `<-- LONG PAD`, meaning that scene needs more animation, not more waiting.

## Build

    python build.py                  # voice + 1080p60 render + mux + concat + SRT
    python build.py --quality m      # 720p30 draft, much faster
    python build.py --skip-voice     # reuse existing voiceovers/
    python build.py --only Part7     # iterate on one scene

Requires `manim`, `edge-tts` and `ffmpeg` on PATH. Note that **no LaTeX is
used** — `MathTex`/`DecimalNumber` are avoided deliberately, since they shell
out to `latex`. All formulas are Pango `Text` with Unicode glyphs, and live
numeric readouts go through the `live_text()` helper.

## Files

    voice.py     narration scripts + edge-tts synthesis + duration measurement
    main.py      20 Manim scenes (Part1 … Part20) and the shared visual language
    build.py     the pipeline, plus the sync report and SRT generation
    voiceovers/  generated MP3s and durations.json     (gitignored)
    media/       Manim's render tree                   (gitignored)
    work/        per-scene muxed segments              (gitignored)
    output/      the finished MP4 and SRT              (gitignored)

## Scene map

     1  hook — two answers from one echo         11  radial velocity only, v·cosθ
     2  the pulse and the speed of light         12  pulse-to-pulse phase
     3  round-trip time → range                  13  slow time → FFT → velocity
     4  worked example, 100 μs → 15 km           14  the range-Doppler map
     5  range resolution, ΔR = cτ/2              15  clutter rejection / MTI
     6  PRF and ambiguous range                  16  Doppler ambiguity, blind speeds
     7  why range differencing fails             17  the PRF dilemma
     8  the Doppler effect                       18  FMCW chirp radar
     9  f_d = 2·v_r/λ and the factor of 2        19  where this shows up
    10  how big the shift actually is            20  recap and outro
