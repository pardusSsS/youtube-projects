"""
Narration for: "How Radar Measures Distance AND Speed"

Generates one MP3 per scene with edge-tts, then measures every clip with
ffprobe and writes `voiceovers/durations.json`.  main.py reads that file so
each Manim scene pads itself out to exactly the length of its narration --
that is what keeps picture and voice locked together.
"""

import asyncio
import json
import os
import subprocess

import edge_tts

VOICE = "en-US-GuyNeural"
RATE = "-4%"          # a touch slower: this is a dense, formula-heavy topic
OUT_DIR = "voiceovers"

SCRIPTS = {
    "Part1": """
Radar does something remarkable. From a single burst of radio energy, bounced
off an object kilometres away, it recovers two completely different quantities.
How far away that object is. And how fast it is closing on you.
Two answers, two entirely separate pieces of physics. Distance comes from time.
Speed comes from frequency. In the next ten minutes we will build both of them
from the ground up, with the real equations, and the real trade-offs that
radar engineers fight with every single day.
""",

    "Part2": """
Everything starts with a pulse. The transmitter generates a short burst of
radio frequency energy, and the antenna launches it into space. That burst
travels at the speed of light. Three hundred million metres per second.
In free space this speed is fixed. It does not depend on the transmitter, the
weather, or the target. And that constant is the key to everything, because a
speed you already know turns a measurement of time into a measurement of
distance.
""",

    "Part3": """
So we start a clock. At time zero the pulse leaves the antenna. It races out,
strikes the target, and a tiny fraction of the energy scatters back. When that
echo arrives, we stop the clock. Call the elapsed time delta t. The pulse
covered the distance twice, out and back, so the range is c times delta t,
divided by two. That division by two is the whole trick. Miss it, and every
target in your display sits at twice its true distance.
""",

    "Part4": """
Let us put numbers on it. Suppose the echo returns one hundred microseconds
after transmission. Multiply three times ten to the eight by one hundred
microseconds and you get thirty thousand metres of total travel. Halve it, and
the target is fifteen kilometres away. A useful rule of thumb falls out of
this. Radio waves cover roughly one kilometre of range for every six and a
half microseconds of round trip delay. Twelve point three microseconds per
nautical mile.
""",

    "Part5": """
But how finely can we measure that range? That depends on the pulse. A pulse
of width tau occupies a stretch of space c times tau long. Two targets closer
together than half of that return overlapping echoes, and they merge into a
single blip. So range resolution equals c tau over two. A one microsecond
pulse gives you one hundred and fifty metres. Shorten the pulse to ten
nanoseconds and resolution improves to one and a half metres. Sharper pulses,
sharper picture.
""",

    "Part6": """
Now, the catch. Short pulses carry less energy, so they see less far. And we
cannot simply fire pulses as fast as we like, because the radar must wait for
the echo before sending the next one. The gap between pulses is the pulse
repetition interval. Anything beyond c divided by twice the pulse repetition
frequency returns after the next pulse has already gone out, and gets
displayed at a completely wrong, much shorter range. That is a second time
around echo.
""",

    "Part7": """
So far we have distance. What about speed? The obvious idea is to measure the
range twice and divide the change by the time between them. It works, but it
is poor. If your range accuracy is fifteen metres, and your measurements are a
tenth of a second apart, your velocity error is a hundred and fifty metres per
second. Useless for anything fast. We need something far more sensitive. And
the wave itself is about to hand it to us.
""",

    "Part8": """
Listen to a siren pass you on the street. Approaching, the pitch is high.
Receding, it drops. The source is squeezing its own wavefronts together in
front of it and stretching them out behind. That is the Doppler effect, and it
works exactly the same way for radio waves striking a moving target. A closing
target compresses the reflected wave, raising its frequency. A receding target
stretches it, lowering the frequency.
""",

    "Part9": """
The shift is called the Doppler frequency, and for radar it is two times the
radial velocity divided by the wavelength. Where does that factor of two come
from? The target sees a compressed wave arriving, and then, acting as a moving
source, it re-radiates a compressed wave back. The shift is applied twice, once
on the way in and once on the way out. Positive Doppler means closing.
Negative Doppler means opening.
""",

    "Part10": """
Numbers again. Take an X band radar at ten gigahertz. Its wavelength is three
centimetres. An aircraft closing at three hundred metres per second produces a
Doppler shift of twenty kilohertz. Perfectly measurable. Now an automotive
radar at twenty four gigahertz, wavelength one point two five centimetres,
watching a car approaching at thirty metres per second, sees four point eight
kilohertz. Even a person walking at one metre per second is a clean one
hundred and sixty hertz.
""",

    "Part11": """
There is an important limitation hiding in that equation. Doppler responds
only to radial velocity, the component straight along the line of sight.
A target moving at velocity v at an angle theta to the beam gives you v times
cosine theta. So an aircraft flying directly at the radar shows its full
speed. One crossing perpendicular to the beam, at any speed at all, shows
zero Doppler. Tangential motion is invisible to Doppler. It looks exactly like
a stationary object.
""",

    "Part12": """
How do we actually extract a twenty kilohertz shift from a ten gigahertz
carrier? Not by measuring the frequency directly. We measure phase. Each pulse
in a train is sampled at the same range bin, and if the target is moving, its
range changes very slightly between pulses. That tiny change rotates the phase
of the echo by a fixed amount every pulse. The phase steps around in a circle
at exactly the Doppler rate.
""",

    "Part13": """
Line up those pulse to pulse samples and you have a slowly varying signal.
Engineers call this slow time, as opposed to the fast time within one pulse.
Take a Fourier transform along slow time, and the steady phase rotation
becomes a sharp peak in a frequency spectrum. That peak's position is the
Doppler frequency. Its width is set by how long you looked. Longer coherent
processing intervals give finer velocity resolution.
""",

    "Part14": """
Now combine the two. Arrange the returns as a matrix. Along one axis, fast
time, which is range. Along the other, slow time, which is pulse number.
Fourier transform every column and you get the range Doppler map, the single
most important picture in modern radar. Each target appears as a bright spot.
Its horizontal position gives velocity, its vertical position gives range.
Distance and speed, read from one image, simultaneously.
""",

    "Part15": """
That map does something else valuable. Ground clutter, hills, buildings, sea
surface, is stationary, so it all piles up at zero Doppler in one narrow
column. A moving target indication filter simply notches that column out. The
mountain that was swamping your receiver disappears, and the aircraft flying in
front of it survives. This is why a Doppler radar can pull a small aeroplane
out of a return ten thousand times stronger.
""",

    "Part16": """
But Doppler has an ambiguity of its own. We sample the phase once per pulse, so
the pulse repetition frequency is our sampling rate, and Nyquist applies. The
unambiguous velocity span is lambda times the pulse repetition frequency
divided by four, either side of zero. Beyond it, velocities fold back and a
fast target masquerades as a slow one. Worse, a target whose Doppler lands
exactly on a multiple of the pulse repetition frequency vanishes into the
clutter notch. That is a blind speed.
""",

    "Part17": """
And here is the dilemma at the heart of pulse Doppler radar. Low pulse
repetition frequency gives you unambiguous range, but ambiguous velocity. High
pulse repetition frequency gives you unambiguous velocity, but ambiguous range.
You cannot have both from one waveform, because the two limits multiply out to
a constant. Real radars escape the trap by staggering, transmitting several
different pulse repetition frequencies and resolving each ambiguity against the
others.
""",

    "Part18": """
There is another route entirely. Instead of short pulses, sweep the frequency
continuously. A frequency modulated continuous wave radar transmits a chirp.
The echo returns delayed, so at any instant it is at a slightly different
frequency from what is being transmitted, and mixing the two produces a beat
tone proportional to range. A moving target shifts that beat as well, so sweep
up and then down. Range shifts both beats the same way, Doppler shifts them
oppositely. Solve the pair, and you separate the two.
""",

    "Part19": """
This is the physics behind an enormous amount of technology. The police speed
gun is pure Doppler with no ranging at all. Weather radar maps rainfall from
echo strength and reads wind and rotation from Doppler, which is how tornado
warnings are issued. Your car's adaptive cruise control is an FMCW radar
tracking range and closing rate hundreds of times a second. Air traffic
control, marine navigation, and every modern air defence system rest on the
same two equations.
""",

    "Part20": """
So, two measurements, two mechanisms. Range comes from time of flight. c delta
t over two. Speed comes from the Doppler shift. lambda f d over two. One is
timing, the other is frequency, and a range Doppler map delivers both at once
from the same received data. Every limitation we met, resolution, ambiguous
range, blind speeds, traces back to a single choice, the waveform. Get the
waveform right and the radar sees everything. Thanks for watching.
""",
}


async def synth():
    os.makedirs(OUT_DIR, exist_ok=True)
    print(f"--- Seslendirme baslıyor: {VOICE} (rate {RATE}) ---")
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
    durations = {p: probe(os.path.join(OUT_DIR, f"{p}.mp3")) for p in SCRIPTS}
    with open(os.path.join(OUT_DIR, "durations.json"), "w") as f:
        json.dump(durations, f, indent=2)
    total = sum(durations.values())
    print("\n--- Sure raporu ---")
    for p, d in durations.items():
        print(f"  {p:<7} {d:7.2f} s")
    print(f"  {'TOPLAM':<7} {total:7.2f} s  ({total/60:.2f} dk konusma)")
    return durations


if __name__ == "__main__":
    asyncio.run(synth())
    write_durations()
    print("\n--- TAMAMLANDI ---")
