"""
Narration for the Short: "What Is a Range-Doppler Map?"

Generates one MP3 per scene with edge-tts, then measures every clip with ffprobe
and writes `voiceovers/durations.json`.  short.py reads that file so each Manim
scene pads itself out to exactly the length of its narration -- that is what
keeps picture and voice locked together without any hand-tuned waits.

    python voice.py
"""

import asyncio
import json
import os
import subprocess

import edge_tts

VOICE = "en-US-GuyNeural"
RATE = "+6%"          # Shorts want pace
OUT_DIR = "voiceovers"

SCRIPTS = {
    "Short1": """
A radar stares at the sky and hands you a single picture. Not a blip, a picture.
This is the range-Doppler map.
""",

    "Short2": """
The raw data is just a table. Range down the rows, pulse number across the
columns. Hundreds of pulses in one look.
""",

    "Short3": """
Pick one row. The target is there every pulse, but its phase creeps. That creep
is a frequency, and an F F T reads it out as speed.
""",

    "Short4": """
Do that for every row, and the table becomes a map. Range up the side, velocity
across, brightness for echo strength.
""",

    "Short5": """
Now it reads like a chart. High and right, far away, closing fast. Everything at
zero velocity is clutter, so cut that column and it is gone.
""",

    "Short6": """
But the velocity axis wraps. Past lambda P R F over four, a fast target folds
into the clutter and vanishes. Every modern radar builds this map.
""",
}


async def synth():
    os.makedirs(OUT_DIR, exist_ok=True)
    print(f"--- Seslendirme baslıyor: {VOICE} ({len(SCRIPTS)} parca, rate {RATE}) ---")
    for part, text in SCRIPTS.items():
        path = os.path.join(OUT_DIR, f"{part}.mp3")
        clean = " ".join(text.split())
        print(f"  isleniyor: {part} ({len(clean.split())} kelime)")
        await edge_tts.Communicate(clean, VOICE, rate=RATE).save(path)


def probe(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", path],
        capture_output=True, text=True, check=True)
    return round(float(out.stdout.strip()), 3)


def write_durations():
    durations = {}
    for p in SCRIPTS:
        path = os.path.join(OUT_DIR, f"{p}.mp3")
        if os.path.exists(path):
            durations[p] = probe(path)
    with open(os.path.join(OUT_DIR, "durations.json"), "w") as f:
        json.dump(durations, f, indent=2)
    print("\n--- Sure raporu ---")
    for p, d in durations.items():
        print(f"  {p:<8} {d:7.2f} s")
    tot = sum(durations.values())
    print(f"  {'TOPLAM':<8} {tot:7.2f} s  ({tot/60:.2f} dk konusma)")
    return durations


if __name__ == "__main__":
    asyncio.run(synth())
    write_durations()
    print("--- TAMAMLANDI ---")
