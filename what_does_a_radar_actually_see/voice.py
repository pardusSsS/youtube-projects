"""
Narration for: "What Does a Radar Actually See? | From Chirp to Detection"

Generates one MP3 per scene with edge-tts, then measures every clip with
ffprobe and writes `voiceovers/durations.json`.  main.py reads that file so
each Manim scene pads itself out to exactly the length of its narration --
that is what keeps picture and voice locked together without hand-tuned waits.

    python voice.py
"""

import asyncio
import json
import os
import subprocess

import edge_tts

VOICE = "en-US-GuyNeural"
RATE = "-4%"          # a touch slower: this is a dense, signal-processing topic
OUT_DIR = "voiceovers"

SCRIPTS = {
    "Part1": """
Point a radar at a car and ask what it sees. Not a car. Not a shape. Not even a
dot. What it sees is a voltage. One wiggling line, buried in noise, sampled a
few million times a second. Every radar picture you have ever looked at, the
blips, the tracks, the neat boxes drawn around vehicles, sits at the far end of
a long chain of processing that begins with that wiggle. In the next ten
minutes we are going to walk that entire chain, one stage at a time, from the
transmitted chirp all the way to a finished detection.
""",

    "Part2": """
It starts with the chirp. A modern radar of this kind does not fire a short
pulse. It transmits continuously, and it sweeps. The frequency climbs in a
straight line, starting at seventy seven gigahertz and covering one gigahertz
of bandwidth in about forty microseconds. Plot frequency against time and you
get a ramp. That ramp is a ruler. Because the transmitted frequency is
different at every single instant, the moment a copy of it comes back, the
radar can work out how long ago it left. The chirp writes a timestamp onto the
air itself.
""",

    "Part3": """
The echo is that same ramp, delayed. It goes out, it strikes a car, a sliver of
the energy scatters back, and it arrives as a faint copy of the chirp, shifted
to the right in time by two R over c. Put that car thirty metres away and the
delay is two hundred nanoseconds. Two hundred billionths of a second. Nothing
you could timestamp directly without absurd hardware. So the radar never tries.
Instead of measuring the delay, it measures a difference in frequency, and that
turns out to be the same information.
""",

    "Part4": """
Here is the trick that makes the whole thing work. The receiver takes the echo
and multiplies it by the chirp being transmitted at that very moment. That
component is a mixer. Both signals are ramps with the same slope, and one is
delayed, so at every instant they sit a constant distance apart in frequency.
That constant is the beat frequency, and it equals the slope of the ramp times
the delay, which is two times slope times range, over c. Range has become a
tone. Our car at thirty metres gives a beat of five megahertz.
""",

    "Part5": """
So what actually lands in memory? For one chirp, a few hundred samples of a
single wobbling voltage. That is the raw truth the radar has to work with. And
it is not one clean tone. Every object inside the beam contributes its own beat
frequency simultaneously. The car ahead, the guardrail, the road surface, a
sign, a truck two lanes over, all summed into one line, sitting on a floor of
thermal noise. Put it on an oscilloscope and it tells you essentially nothing.
There is no target in there that a human eye can find.
""",

    "Part6": """
Now take a Fourier transform along that chirp. A sum of tones becomes a set of
peaks, and because beat frequency is proportional to range, that frequency axis
is a range axis. This is the range F F T, and what comes out is a row of range
bins. How wide is one bin? Only the bandwidth decides. Delta R equals c over
two B. One gigahertz of sweep gives you fifteen centimetres. Not the power, not
the antenna, not how long you stare. If you want to separate two things
standing close together, sweep wider. And notice what just happened. A brutally hard timing problem
became an easy frequency problem. That is the entire reason chirps exist.
""",

    "Part7": """
Be careful how you read the height of a peak, though. It is not the size of the
object. Received power falls off as one over range to the fourth. Double the
distance and you keep one sixteenth of the echo. Sitting on top of that is
radar cross section, which depends on geometry and material rather than on how
large something looks. A flat truck tailgate square on to you can reflect like
a building. A pedestrian scatters energy in every direction and sends back
almost nothing. A tall peak means a strong reflector. It does not mean a big
object.
""",

    "Part8": """
One chirp gives you range. To get speed, the radar sends a burst of them.
Typically one hundred and twenty eight chirps, back to back, forty microseconds
apart, and that burst is called a frame. If the target is moving, it sits at a
very slightly different range on every chirp. Far too little to change range
bins. A car closing at twenty metres per second moves less than a millimetre
between chirps. But the wavelength up here is only four millimetres. So that
millimetre is enormous, and it shows up in the phase of the peak.
""",

    "Part9": """
Line those hundred and twenty eight complex samples up, one per chirp, and the
phase rotates steadily, turn after turn. A steady rotation is a frequency. So
we run a second Fourier transform, this time across chirps, along what
engineers call slow time. Out of it comes Doppler frequency, and from that,
velocity: v equals lambda f d over two. The whole frame lasts about five
milliseconds, and that duration alone fixes the velocity resolution, roughly
forty centimetres per second. Stare longer and you can split targets moving at
more nearly the same speed.
""",

    "Part10": """
Do that for every range bin, and the frame stops being a table of voltages and
becomes an image. Range down one axis, velocity across the other, brightness
for echo strength. This is the range Doppler map, and it is the closest thing
there is to what a radar actually sees. Everything stationary, the road,
barriers, signs, parked cars, piles into the zero velocity column. A vehicle
you are closing on sits off to one side. One picture, and range and speed are
read straight off the two axes. Look at the map and the scene is already half
interpreted, before a single decision has been made.
""",

    "Part11": """
Two dimensions down, one to go. Which direction did it come from? For that you
need more than one receiving antenna. A wavefront arriving at an angle reaches
one antenna slightly before it reaches the next, and that extra path, d sine
theta, becomes a constant phase step from element to element across the array.
A constant step is, once again, a frequency. So a third Fourier transform, this
time across antennas, turns phase into angle. Modern chips also transmit from
several antennas in turn to synthesise a much larger array. That is M I M O.
""",

    "Part12": """
Now stack everything up. Once per frame, the radar produces a three dimensional
grid of complex numbers. Range, by velocity, by angle. And it fills that grid
several dozen times a second. This is the honest answer to our question. A
radar does not see objects. It sees a cube of energy, in which the vast
majority of cells hold nothing but noise, and a handful hold the sum of
everything that reflected from one particular range, moving at one particular
speed, lying in one particular direction. Nothing in that cube is labelled. There are
no edges, no objects and no meaning. Only numbers, waiting to be judged.
""",

    "Part13": """
That noise is not something you get to ignore. Every receiver has a thermal
noise floor, set by temperature, by bandwidth and by its own noise figure. And
every real scene is stuffed with clutter. The road surface, the guardrail,
rain, a manhole cover. Now try to draw one fixed threshold across the whole
map. Close in, where the clutter is strong, you drown in false alarms. Far out,
where the echoes are weak, you sail straight over the target you actually
needed to see. One number cannot do both jobs. What matters is never the raw power. It is the
signal to noise ratio, the height of a peak above its own surroundings.
""",

    "Part14": """
So the threshold has to move. The standard answer is C F A R, constant false
alarm rate. For every cell in the map, look at a ring of neighbouring cells.
Skip a few guard cells immediately around it, so a strong target cannot raise
its own bar. Average the rest to estimate the local noise and clutter level,
and multiply by a factor chosen for the false alarm rate you are willing to
accept. A cell is only declared a detection if it beats its own neighbourhood.
The threshold breathes with the scene. Cell averaging is the simplest version,
and there is a whole family of variants tuned for different kinds of clutter.
""",

    "Part15": """
What survives is a detection list. Range, velocity, angle and signal to noise
ratio, a few hundred points in a frame. Cluster the points that belong to the
same thing and you have objects. Follow those objects from frame to frame with
a tracker, and at last you get the boxes and the arrows you would recognise.
But notice what was never in there. No colour, no texture, no outline.
Multipath can hang a ghost target under a bridge. And at a hundred metres, one
degree of beam width is still nearly two metres across. The radar is not seeing
the world. It is inferring it, from reflections and a great deal of arithmetic.
""",

    "Part16": """
So here is the whole chain. A ramp goes out. A delayed copy comes back. A mixer
turns that delay into a tone. One Fourier transform turns the tone into range.
A second turns phase drift across chirps into speed. A third turns phase across
antennas into angle. C F A R decides what is real, clustering builds objects,
and a tracker gives them a history. From chirp to detection. Everything a radar
knows about the world, it built out of a wiggling voltage. And if you take one idea away from all of this, let it be that almost every
stage in the chain is a Fourier transform, trading one axis for another. Thanks
for watching.
""",
}


async def synth():
    os.makedirs(OUT_DIR, exist_ok=True)
    print(f"--- Seslendirme baslıyor: {VOICE} ({len(SCRIPTS)} parca, rate {RATE}) ---")
    for part, text in SCRIPTS.items():
        clean = " ".join(text.split())
        path = os.path.join(OUT_DIR, f"{part}.mp3")
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
