# How Radar Measures Distance AND Speed

Two deliverables from one system, built with Manim + edge-tts and assembled with
ffmpeg: a ~10.7 minute explainer and a vertical Short cut from the same material.

    output/how_radar_measures_distance_and_speed.mp4    1920×1080 60fps, 10:44
    output/how_radar_measures_distance_and_speed.srt    sentence-level subtitles
    output/thumbnail.png                                1280×720 YouTube thumbnail
    output/youtube_description.txt                      description + chapters

    output/short_how_can_radar_know_your_speed.mp4      1080×1920 60fps, 0:56
    output/short_how_can_radar_know_your_speed.srt      subtitles

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

## The Short

`short.py` is the vertical cut: "How Can Radar Know Your Speed?", six scenes,
0:56, built on the same `fill()` machinery. It answers one question only — the
Doppler shift — and drops range entirely.

    python build.py --short

Two things matter when rendering 9:16 in Manim. It derives pixels-per-unit from
`frame_width` alone and never adjusts it for a tall canvas, so a vertical render
silently letterboxes the scene into a middle band; `short.py` pins
`frame_height = 8.0` and `frame_width = 4.5` to make the 1080×1920 frame exactly
4.5 × 8 units. And the frame is then only 4.5 units across, so every text block
goes through `fit()`, which shrinks anything wider than 4.05 units. Content is
also kept above y = −3.0, clear of the Shorts title overlay.

## Build

    python build.py                  # voice + 1080p60 render + mux + concat + SRT
    python build.py --short          # the vertical Short instead
    python build.py --quality m      # 720p30 draft, much faster
    python build.py --skip-voice     # reuse existing voiceovers/
    python build.py --only Part7     # iterate on one scene

`voice.py` takes an argument — `long`, `short` or `all` (default) — so you can
resynthesise one deliverable's narration without touching the other. Both write
into a single `voiceovers/durations.json`.

Requires `manim`, `edge-tts` and `ffmpeg` on PATH. Note that **no LaTeX is
used** — `MathTex`/`DecimalNumber` are avoided deliberately, since they shell
out to `latex`. All formulas are Pango `Text` with Unicode glyphs, and live
numeric readouts go through the `live_text()` helper.

## Thumbnail

`thumbnail.py` is a single still frame rendered through Manim, importing the
palette and the `dish()` / `plane()` builders from `main.py` so the thumbnail
and the opening shot share one visual language.

    python -m manim -s -r 1280,720 --media_dir media thumbnail.py Thumbnail
    cp media/images/thumbnail/Thumbnail*.png output/thumbnail.png

1280×720, ~128 KB — well inside YouTube's 2 MB limit. The bottom-right corner
is kept clear of content, since YouTube stamps the duration badge there.

## Files

    voice.py     narration for both cuts + edge-tts synthesis + duration measurement
    main.py      20 Manim scenes (Part1 … Part20) and the shared visual language
    short.py     6 vertical scenes (Short1 … Short6) for the Short
    thumbnail.py the 1280×720 thumbnail, rendered as one Manim still
    build.py     the pipeline, plus the sync report and SRT generation
    voiceovers/  generated MP3s and durations.json     (gitignored)
    media/       Manim's render tree                   (gitignored)
    work/long/   per-scene muxed segments, long video  (gitignored)
    work/short/  per-scene muxed segments, Short       (gitignored)
    output/      the finished files                    (gitignored)

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

## Short scene map

    1  the hook — a speed gun clocks you, but never ranged you
    2  the Doppler effect, a source squeezing its own wavefronts
    3  the same thing happening to the echo off your car
    4  f_d = 2v/λ, and where the factor of 2 comes from
    5  the actual numbers at 24 GHz: 4.8 kHz for a car, 160 Hz for a walker
    6  the catch — v·cosθ, and why they never aim it sideways
