#!/usr/bin/env python3
"""
Build "How Radar Measures Distance AND Speed" end to end.

    python build.py                # full 1080p60 build
    python build.py --quality m    # faster 720p30 draft
    python build.py --skip-voice   # reuse existing voiceovers/
    python build.py --only Part3   # rebuild a single scene

Pipeline
    1. voice.py  -> voiceovers/PartN.mp3 + durations.json
    2. manim     -> one silent MP4 per scene; each scene reads durations.json
                    and pads its own tail so picture length == narration length
    3. ffmpeg    -> mux each scene with its MP3 (audio silence-padded to the
                    exact video length), then concatenate all twenty
    4. SRT       -> sentence-level subtitles on the real timeline
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
VOICE_DIR = os.path.join(HERE, "voiceovers")
WORK_DIR = os.path.join(HERE, "work")
OUT_DIR = os.path.join(HERE, "output")
MEDIA_DIR = os.path.join(HERE, "media")
FINAL = os.path.join(OUT_DIR, "how_radar_measures_distance_and_speed.mp4")
SRT = os.path.join(OUT_DIR, "how_radar_measures_distance_and_speed.srt")

PARTS = [f"Part{i}" for i in range(1, 21)]
QUALITY_DIR = {"l": "480p15", "m": "720p30", "h": "1080p60", "k": "2160p60"}

PY = sys.executable


def run(cmd, **kw):
    print("  $", " ".join(str(c) for c in cmd[:6]), "..." if len(cmd) > 6 else "")
    return subprocess.run(cmd, check=True, **kw)


def probe(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", path],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


# ------------------------------------------------------------------ 1. voice
def step_voice(skip):
    if skip and os.path.exists(os.path.join(VOICE_DIR, "durations.json")):
        print("\n[1/4] seslendirme atlandi (mevcut voiceovers/ kullanilacak)")
        return
    print("\n[1/4] seslendirme uretiliyor (edge-tts)")
    run([PY, os.path.join(HERE, "voice.py")], cwd=HERE)


# ------------------------------------------------------------------ 2. manim
def step_render(quality, only):
    print(f"\n[2/4] sahneler render ediliyor (-q{quality})")
    parts = [only] if only else PARTS
    cmd = [PY, "-m", "manim", f"-q{quality}", "--disable_caching",
           "--media_dir", MEDIA_DIR, os.path.join(HERE, "main.py"), *parts]
    run(cmd, cwd=HERE)


def scene_path(part, quality):
    return os.path.join(MEDIA_DIR, "videos", "main", QUALITY_DIR[quality], f"{part}.mp4")


# ------------------------------------------------------------------ 3. mux
def step_mux(quality):
    print("\n[3/4] ses + goruntu birlestiriliyor")
    os.makedirs(WORK_DIR, exist_ok=True)
    segments, report = [], []

    for part in PARTS:
        vid = scene_path(part, quality)
        aud = os.path.join(VOICE_DIR, f"{part}.mp3")
        if not os.path.exists(vid):
            raise SystemExit(f"eksik sahne: {vid} (once render et)")
        vd, ad = probe(vid), probe(aud)
        out = os.path.join(WORK_DIR, f"{part}_av.mp4")
        # apad tops the narration up with silence to the exact picture length,
        # so audio never runs past the cut and never gets truncated either.
        run(["ffmpeg", "-y", "-loglevel", "error",
             "-i", vid, "-i", aud,
             "-filter_complex", "[1:a]apad,aresample=async=1[a]",
             "-map", "0:v:0", "-map", "[a]",
             "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
             "-shortest", "-movflags", "+faststart", out])
        segments.append(out)
        report.append((part, vd, ad, vd - ad))
        print(f"    {part:<7} video {vd:6.2f}s  ses {ad:6.2f}s  sessiz kuyruk {vd-ad:5.2f}s")

    print("\n  --- senkron raporu ---")
    worst = max(report, key=lambda r: abs(r[3]))
    total = sum(r[1] for r in report)
    print(f"  en buyuk sapma : {worst[0]}  {worst[3]:+.2f}s")
    print(f"  toplam sure    : {total:.2f}s  ({total/60:.2f} dk)")
    return segments, report


# ------------------------------------------------------------------ 4. concat
def step_concat(segments):
    print("\n[4/4] birlestiriliyor")
    os.makedirs(OUT_DIR, exist_ok=True)
    listfile = os.path.join(WORK_DIR, "concat.txt")
    with open(listfile, "w") as f:
        for s in segments:
            f.write(f"file '{s}'\n")
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
         "-i", listfile, "-c", "copy", "-movflags", "+faststart", FINAL])
    return FINAL


# ------------------------------------------------------------------ subtitles
def ts(seconds):
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def step_subtitles(report):
    """Split each narration block into sentences, timed proportionally to length."""
    sys.path.insert(0, HERE)
    from voice import SCRIPTS

    def cues(text, limit=92):
        """Sentences, further split at commas so no cue overruns a comfortable read."""
        out = []
        for sent in re.split(r"(?<=[.?!])\s+", text):
            sent = sent.strip()
            if not sent:
                continue
            while len(sent) > limit:
                cut = sent.rfind(", ", 0, limit)
                if cut < limit // 2:
                    cut = sent.find(" ", limit)
                    if cut == -1:
                        break
                out.append(sent[:cut + 1].strip())
                sent = sent[cut + 1:].strip()
            if sent:
                out.append(sent)
        return out

    lines, idx, clock = [], 1, 0.0
    for part, vdur, adur, _ in report:
        text = " ".join(SCRIPTS[part].split())
        sentences = cues(text)
        chars = sum(len(s) for s in sentences) or 1
        t = clock
        for s in sentences:
            span = adur * len(s) / chars
            lines.append(f"{idx}\n{ts(t)} --> {ts(t + span)}\n{s}\n")
            idx += 1
            t += span
        clock += vdur

    with open(SRT, "w") as f:
        f.write("\n".join(lines))
    print(f"  altyazi: {SRT}  ({idx-1} satir)")


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quality", default="h", choices=list(QUALITY_DIR))
    ap.add_argument("--skip-voice", action="store_true")
    ap.add_argument("--skip-render", action="store_true")
    ap.add_argument("--only", help="render a single scene, e.g. Part7")
    args = ap.parse_args()

    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            raise SystemExit(f"{tool} bulunamadi — PATH'e ekle (brew install ffmpeg)")

    step_voice(args.skip_voice)
    if not args.skip_render:
        step_render(args.quality, args.only)
    if args.only:
        print("\ntek sahne render edildi; tam cikti icin --only olmadan calistir")
        return
    segments, report = step_mux(args.quality)
    final = step_concat(segments)
    step_subtitles(report)

    dur = probe(final)
    size = os.path.getsize(final) / 1e6
    print("\n=== TAMAMLANDI ===")
    print(f"  {final}")
    print(f"  sure {dur:.1f}s ({dur/60:.2f} dk)  ·  {size:.1f} MB")


if __name__ == "__main__":
    main()
