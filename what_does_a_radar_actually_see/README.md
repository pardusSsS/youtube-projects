# What Does a Radar Actually See? | From Chirp to Detection

A ~10.6 minute explainer built with Manim + edge-tts and assembled with ffmpeg.

    output/what_does_a_radar_actually_see.mp4    1920×1080 60fps
    output/what_does_a_radar_actually_see.srt    sentence-level subtitles
    output/youtube_description.txt               description + chapters
    output/thumbnail.png                         1280×720 YouTube thumbnail

## The idea

A radar does not see a car. For one chirp it sees a few hundred samples of a
single wobbling voltage, and every reflector in the beam is summed into that
one line. Sixteen scenes follow what happens to it:

    beat frequency   f_b = 2 S R / c        delay becomes a tone
    range bin        ΔR  = c / 2B           bandwidth alone decides
    velocity         v   = λ · f_d / 2      phase drift across chirps
    angle            ψ   = 2π d sinθ / λ    phase step across antennas
    detection        thr = α · mean(training cells)      CFAR

Three Fourier transforms and an adaptive threshold, and the wiggle has become a
tracked object. The last scene is the whole chain in one strip.

## How audio and picture stay locked

Timing is **derived**, never hand-tuned:

1. `voice.py` synthesises one MP3 per scene and measures each one with ffprobe,
   writing `voiceovers/durations.json`.
2. Every scene in `main.py` subclasses `NarratedScene`. Its last statement is
   `self.fill()`, which reads that JSON, compares the narration length against
   `self.renderer.time` (how much animation has actually played), and waits out
   exactly the difference plus a 0.6 s tail.
3. `build.py` muxes each scene with its MP3, topping the audio up with silence
   (`apad`) so the track ends precisely with the picture.

Each scene is choreographed once at a natural rhythm and then stretched by a
single per-scene number in `TEMPO`, which scales `PACE` (every `run_time`),
`BEAT` (the hold after each substantial reveal) and `WAIT_SCALE` together. A
scene is therefore linear in its tempo: render, read the pad from the sync
report, multiply, done. Every scene currently lands within about two seconds of
its narration.

## Nothing overlaps, and that is enforced

Two mechanisms, not one.

**Zones.** The frame is carved into named rectangles — `HEADER`, `BODY`,
`LCOL`/`RCOL`, `TOPBAND`/`BOTBAND`, `FOOT` — and text blocks are placed with
`Zone.fit()`, which shrinks a block until it fits inside its zone with padding.
Two blocks in disjoint zones cannot collide. `FOOT` is reserved for the one-line
caption and never holds anything else.

**An audit that runs while rendering.** `NarratedScene` overrides `play()` and
`wait()`; after every one it walks the visible `Text` mobjects, tests all pairs
of bounding boxes with a 0.05-unit tolerance, and prints

    [LAYOUT] Part3 OVERLAP: "TX" x "RX(echo)" (dx=0.10 dy=0.15)
    [LAYOUT] Part10 OFFSCREEN: "range→" x[-7.13,-6.91] y[-0.62,0.32]

for anything that touches or drifts past the frame edge. `build.py` collects
those lines out of the render log and reprints them in the final summary, so a
clash cannot quietly ship. The current build reports none. Set
`RADAR_LAYOUT_CHECK=0` to skip the audit.

## Build

    python build.py                  # voice + 1080p60 render + mux + concat + SRT
    python build.py --quality m      # 720p30 draft, much faster
    python build.py --quality l      # 480p15, for layout and timing checks
    python build.py --skip-voice     # reuse existing voiceovers/
    python build.py --only Part7     # iterate on one scene

Requires `manim`, `edge-tts` and `ffmpeg` on PATH. In this repo the toolchain
lives in the shared virtualenv one level up:

    ../.venv-video/bin/python build.py

**No LaTeX is used.** `MathTex`/`DecimalNumber` are avoided deliberately, since
they shell out to `latex`. Every formula is a Pango `Text` built from Unicode
glyphs.

## Thumbnail

    python -m manim -s -r 1280,720 --media_dir media thumbnail.py Thumbnail
    cp media/images/thumbnail/Thumbnail*.png output/thumbnail.png

## Files

    voice.py      narration for all sixteen scenes + edge-tts + duration measurement
    main.py       the zone system, the layout audit, the shared builders, Part1 … Part16
    thumbnail.py  the 1280×720 thumbnail, rendered as one Manim still
    build.py      the pipeline, the sync report, SRT and the description
    voiceovers/   generated MP3s and durations.json     (gitignored)
    media/        Manim's render tree                   (gitignored)
    work/         per-scene muxed segments              (gitignored)
    output/       the finished files                    (gitignored)

## Scene map

     1  the question — you see a car, it sees a voltage
     2  the chirp: 77 GHz, 1 GHz of sweep, 40 μs
     3  the echo is the same ramp, delayed by 2R/c
     4  the mixer: delay becomes a beat frequency
     5  what actually lands in memory — one messy line
     6  the range FFT, and ΔR = c/2B
     7  a tall peak is not a big object: 1/R⁴ and RCS
     8  128 chirps in a frame, and 0.8 mm of phase
     9  the Doppler FFT across slow time
    10  the range-Doppler map
    11  the angle FFT across the receive array, and MIMO
    12  the data cube: 256 × 128 × 8 complex numbers
    13  noise, clutter, and why a fixed threshold fails
    14  CFAR: guard cells, training cells, α
    15  detections → clusters → tracks, and what is missing
    16  the whole chain, from chirp to detection
