import asyncio
import edge_tts
import os

# Seslendirilecek Metinler
SCRIPTS = {

    # ─────────────────────────────────────────────────────────────────────────
    # Part1: The Hook – Radar Antennas Revealed
    # Role: Hook  |  Duration: 3 – 6 s  |  ~55 words
    # ─────────────────────────────────────────────────────────────────────────
    "Part1": """
        In the blink of an eye, radar antennas shape the way we see the world  —  from tracking aircraft at 40,000 feet to mapping storm cells hundreds of kilometres away. This is not just engineering; it is physics in action. Welcome to a complete visual breakdown of every major radar antenna type on the planet.
    """,

    # ─────────────────────────────────────────────────────────────────────────
    # Part2: What Is a Radar Antenna?
    # Role: Foundation  |  Duration: 13 – 20 s  |  ~105 words
    # ─────────────────────────────────────────────────────────────────────────
    "Part2": """
        A radar antenna is the interface between the electronic world and the electromagnetic spectrum. It performs two critical jobs: first, it radiates a precisely shaped beam of radio-frequency energy outward; second, it captures the faint echo that returns after that energy bounces off a distant object. The antenna does not generate the signal  —  the transmitter does that. Nor does it interpret the returning echo  —  the receiver handles processing. The antenna simply converts guided electrical energy into a propagating wave, and back again. That conversion efficiency, and the shape of the beam it produces, are the two parameters that define every radar antenna's performance.
    """,

    # ─────────────────────────────────────────────────────────────────────────
    # Part3: Classification of Radar Antennas
    # Role: Taxonomy  |  Duration: 15 – 22 s  |  ~113 words
    # ─────────────────────────────────────────────────────────────────────────
    "Part3": """
        Radar antennas are not a single device  —  they are a family of designs, each optimised for a different mission. We can broadly classify them into four major categories that cover nearly every application in the real world. Parabolic reflector antennas concentrate energy using a curved dish. Phased array antennas steer a beam electronically, with no moving parts. Slot array antennas radiate through precision-cut openings in a metal waveguide. Horn antennas flare a waveguide into an open aperture, radiating a controlled cone of energy. Each category has its own physics, its own strengths, and its own ideal use case. Over the next sections, we will pull each one apart  —  layer by layer.
    """,

    # ─────────────────────────────────────────────────────────────────────────
    # Part4: Type 1 – Parabolic Reflector Antenna
    # Role: Deep Dive – Parabolic  |  Duration: 16 – 23 s  |  ~124 words
    # ─────────────────────────────────────────────────────────────────────────
    "Part4": """
        The parabolic reflector is the oldest and most recognisable radar antenna on Earth. You have seen it on airports, navy ships, and weather stations. At its core, the design is elegantly simple: a large, concave dish made of metal, with a small feed horn positioned at its focal point. The transmitter sends energy into the feed horn, which radiates it toward the dish. The dish then reflects all of that energy into a narrow, focused beam  —  much like a satellite dish focuses television signals. Because the dish is physically large, it gathers a correspondingly large amount of returning echo, giving parabolic antennas exceptionally high gain. The trade-off is mechanical: to point the beam at a new target, the entire dish must physically rotate.
    """,

    # ─────────────────────────────────────────────────────────────────────────
    # Part5: Parabolic Focusing – The Physics Behind the Dish
    # Role: Physics Explainer  |  Duration: 17 – 24 s  |  ~135 words
    # ─────────────────────────────────────────────────────────────────────────
    "Part5": """
        The reason a parabolic dish works so well comes down to one elegant property of the parabola as a mathematical curve. Every ray of energy that arrives parallel to the central axis of the dish  —  no matter how far from the centre  —  will reflect and pass through exactly one point: the focal point. This is not an approximation. It is a geometric certainty. In a radar context, this works in reverse during transmission: energy emitted from the feed at the focus reflects off the dish and exits as a perfectly parallel beam. During reception, an incoming parallel wavefront from a distant target reflects off the dish and converges precisely at the feed, maximising the signal captured by the receiver. This dual-use geometry is what makes the parabolic reflector so powerful and so enduring.
    """,

    # ─────────────────────────────────────────────────────────────────────────
    # Part6: Type 2 – Phased Array Antenna
    # Role: Deep Dive – Phased Array  |  Duration: 15 – 22 s  |  ~124 words
    # ─────────────────────────────────────────────────────────────────────────
    "Part6": """
        The phased array is where radar engineering takes a dramatic leap forward. Instead of one big dish that physically moves, a phased array uses dozens  —  or thousands  —  of small, individual antenna elements arranged in a flat panel. Each element can transmit and receive on its own. The breakthrough lies in the electronics behind each element: a phase shifter. By precisely controlling the tiny time delay  —  the phase  —  of the signal at each element, the array can constructively add all those individual signals into one powerful, steered beam  —  pointed in any direction the electronics demand, with no mechanical movement whatsoever. This is why phased arrays dominate modern fighter jets, destroyers, and early-warning systems: they can redirect a beam in microseconds.
    """,

    # ─────────────────────────────────────────────────────────────────────────
    # Part7: Electronic Beam Steering – How Phase Controls Direction
    # Role: Physics Explainer  |  Duration: 18 – 25 s  |  ~150 words
    # ─────────────────────────────────────────────────────────────────────────
    "Part7": """
        To understand how a phased array steers its beam, think about waves on water. If every ripple starts at exactly the same moment across a long straight edge, the resulting wavefront moves straight out, perpendicular to the edge. Now imagine you delay the start of each ripple by a tiny amount as you move along the edge. The wavefront tilts. The more delay you add, the more the beam tilts. That is precisely what a phased array does with radio waves. When all elements transmit in phase  —  zero phase difference  —  the beam points straight ahead. When a progressive phase shift is applied  —  each element shifted by a fixed increment relative to its neighbour  —  the beam rotates smoothly to a new angle. Reverse the progression and the beam steers the other way. The entire scan can sweep 120 degrees or more, all without a single moving part.
    """,

    # ─────────────────────────────────────────────────────────────────────────
    # Part8: Type 3 – Slot Array Antenna
    # Role: Deep Dive – Slot Array  |  Duration: 16 – 23 s  |  ~132 words
    # ─────────────────────────────────────────────────────────────────────────
    "Part8": """
        The slot array antenna is a masterclass in compact, integrated radar design. It starts with a waveguide  —  a hollow metal channel that guides electromagnetic energy along its length without loss. Precision slots  —  narrow rectangular openings  —  are machined into the wall of the waveguide at exact intervals. Each slot acts as a tiny radiating element: as the guided wave passes a slot, a small fraction of its energy leaks out and radiates into free space. By controlling the size, spacing, and orientation of each slot, engineers shape the radiation pattern of the entire antenna. Slot arrays are extraordinarily flat and can be flush-mounted into aircraft fuselages or ship hulls. They are also highly efficient because the waveguide itself acts as the transmission line  —  no cables, no connectors, minimal loss.
    """,

    # ─────────────────────────────────────────────────────────────────────────
    # Part9: Type 4 – Horn Antenna
    # Role: Deep Dive – Horn  |  Duration: 15 – 22 s  |  ~125 words
    # ─────────────────────────────────────────────────────────────────────────
    "Part9": """
        The horn antenna is one of the simplest and most versatile radar antennas in existence. Picture a waveguide  —  that hollow metal channel we just discussed  —  but instead of ending abruptly, it flares open gradually into a wide rectangular or conical mouth. That flared opening is the horn. As the guided wave travels from the narrow waveguide into the wider horn, it spreads out and radiates into free space in a controlled, forward-directed cone. The wider the mouth, the narrower and more directional the beam becomes. Horn antennas are exceptionally broadband  —  they work well across a wide range of frequencies without redesign. For this reason, they are the gold standard for calibrating other antennas and are used extensively in laboratory and field measurements.
    """,

    # ─────────────────────────────────────────────────────────────────────────
    # Part10: Beam Pattern Comparison – All Four Types Side by Side
    # Role: Comparative Analysis  |  Duration: 18 – 25 s  |  ~149 words
    # ─────────────────────────────────────────────────────────────────────────
    "Part10": """
        Now that we have met all four antenna types individually, it is time to place them next to each other and compare the one parameter that matters most in radar: the beam pattern. The parabolic reflector produces the narrowest beam of all  —  a razor-thin pencil of energy. That narrow beam means exceptional angular resolution, but it also means the antenna can only look in one direction at a time. The phased array produces a beam of similar width, but here is the key difference: it can be steered electronically to any angle almost instantaneously. The slot array fans its energy over a wider arc  —  useful when you need to illuminate a broad sector without mechanical scanning. And the horn antenna produces the widest beam of the four, trading directivity for simplicity and bandwidth. Each beam width is a deliberate engineering trade-off between resolution, coverage, speed, and cost.
    """,

    # ─────────────────────────────────────────────────────────────────────────
    # Part11: Antenna Gain and Directivity
    # Role: Core Concept  |  Duration: 17 – 24 s  |  ~132 words
    # ─────────────────────────────────────────────────────────────────────────
    "Part11": """
        Gain and directivity are the two numbers that every radar engineer looks at first when evaluating an antenna. Directivity tells you how much more power an antenna radiates in its peak direction compared to a hypothetical isotropic radiator  —  an ideal point source that would radiate equally in every direction. Gain goes one step further: it folds in the antenna's real-world losses. An antenna with 90 percent efficiency and a directivity of 30 dB has a gain of about 29 dB. In the radar range equation, gain appears squared  —  doubling the antenna's gain quadruples the effective power in the link budget. This is why large-aperture antennas like parabolic reflectors dominate long-range radar: their physical size translates directly into gain, and gain is the single most powerful lever for extending detection range.
    """,

    # ─────────────────────────────────────────────────────────────────────────
    # Part12: Signal Polarization
    # Role: Core Concept  |  Duration: 16 – 23 s  |  ~137 words
    # ─────────────────────────────────────────────────────────────────────────
    "Part12": """
        Every electromagnetic wave has a polarization  —  the direction in which its electric field oscillates as it travels through space. A linearly polarised wave oscillates in a single plane: think of a rope being shaken up and down. A circularly polarised wave traces a helix as it propagates: the electric field rotates continuously, like a corkscrew. Why does this matter for radar? Because when a wave bounces off a target, its polarization often changes. By comparing the polarization of the transmitted pulse with that of the returning echo, a radar system can distinguish rain droplets from aircraft, or classify the shape and orientation of a target. The antenna itself defines what polarization is transmitted, and how sensitively different polarizations are received. Modern weather radars and military systems use dual-polarization antennas to extract maximum information from every echo.
    """,

    # ─────────────────────────────────────────────────────────────────────────
    # Part13: The Radar Range Equation
    # Role: Mathematical Core  |  Duration: 18 – 25 s  |  ~143 words
    # ─────────────────────────────────────────────────────────────────────────
    "Part13": """
        All of the physics we have discussed so far  —  gain, beam width, polarization  —  comes together in one equation: the radar range equation. It tells you the maximum distance at which a radar system can reliably detect a target. Maximum range scales with the fourth root of transmit power. Double the power, and range increases by only about 19 percent. But gain appears squared inside that fourth root  —  so doubling the antenna's gain increases range by about 41 percent. The target's radar cross-section  —  essentially how 'visible' it is to radar  —  also sits inside the equation. And the minimum detectable power of the receiver sets the noise floor that all returning echoes must exceed. The antenna's gain is the single most impactful parameter the designer can control. That is why so much radar engineering effort goes into maximising antenna performance.
    """,

    # ─────────────────────────────────────────────────────────────────────────
    # Part14: Frequency Bands and Antenna Selection
    # Role: Applied Engineering  |  Duration: 17 – 24 s  |  ~144 words
    # ─────────────────────────────────────────────────────────────────────────
    "Part14": """
        Radar systems do not operate at a single frequency  —  they are spread across a wide spectrum, and the choice of frequency fundamentally changes the antenna that must be used. At lower frequencies  —  the L-band around one to two gigahertz  —  wavelengths are long, antennas must be large, but the signals penetrate weather and foliage exceptionally well, making these bands ideal for long-range surveillance. As you move up to S-band and C-band, antennas become more manageable in size, and resolution improves. X-band, at eight to twelve gigahertz, is the sweet spot for many military and weather applications: the antenna is compact, the resolution is sharp, and the atmospheric absorption is still tolerable. At Ku-band and above, antennas shrink further, but atmospheric losses become severe, limiting range. The antenna type and its physical size are dictated by the frequency. You cannot separate the two.
    """,

    # ─────────────────────────────────────────────────────────────────────────
    # Part15: Antenna Efficiency and Losses
    # Role: Engineering Detail  |  Duration: 16 – 23 s  |  ~148 words
    # ─────────────────────────────────────────────────────────────────────────
    "Part15": """
        No antenna is perfect. Between the power that enters the antenna and the power that actually radiates into space, a series of loss mechanisms quietly erode performance. Ohmic loss is the simplest: the metal of the antenna has finite conductivity, so some energy is converted to heat as it flows through the structure. Impedance mismatch loss occurs when the antenna's input impedance does not precisely match the transmission line feeding it; the mismatched portion of the signal reflects back instead of radiating. Polarization loss arises when the antenna's polarization does not perfectly align with the incoming signal. There are also aperture taper losses and spillover losses in dish antennas. Antenna efficiency  —  the ratio of radiated power to input power  —  is the number that captures all of these losses in one figure. Top-tier radar antennas routinely achieve efficiencies above 60 percent; poor designs may fall below 40.
    """,

    # ─────────────────────────────────────────────────────────────────────────
    # Part16: Sidelobe Levels
    # Role: Engineering Detail  |  Duration: 17 – 24 s  |  ~149 words
    # ─────────────────────────────────────────────────────────────────────────
    "Part16": """
        A radar antenna's beam is not a perfect, clean pencil of light. In reality, alongside the main lobe  —  the intended beam  —  the antenna also radiates smaller lobes of energy in unintended directions. These are called sidelobes. Sidelobes are a serious problem. They can pick up strong echoes from nearby objects  —  buildings, terrain, ships  —  and feed them back into the receiver as false targets or clutter that masks the real return. Sidelobe level is measured in decibels below the peak of the main lobe. A conventional antenna might have sidelobes at minus 13 dB; a carefully tapered design can push them to minus 25 dB or lower. Low-sidelobe antennas are critical in cluttered environments  —  airborne radar over cities, or naval radar in coastal waters. The phased array and slot array are particularly well suited to sidelobe suppression because their element-level amplitudes can be individually controlled.
    """,

    # ─────────────────────────────────────────────────────────────────────────
    # Part17: Synthetic Aperture Radar (SAR)
    # Role: Advanced Application  |  Duration: 18 – 25 s  |  ~141 words
    # ─────────────────────────────────────────────────────────────────────────
    "Part17": """
        Synthetic Aperture Radar is one of the most ingenious ideas ever applied to antenna design. The fundamental limitation of a real antenna is its physical size: a larger aperture means a narrower beam and better resolution. SAR breaks that limitation entirely. An aircraft or satellite flies along a straight path, transmitting radar pulses and recording the returns at every point along the route. Because the platform is moving, each pulse is transmitted from a slightly different position. A sophisticated signal processor then stitches all those returns together, treating the flight path as if it were one giant antenna  —  many times longer than the aircraft itself. The result is resolution that rivals optical imaging, achieved with an antenna that fits inside a small pod on the aircraft's wing. SAR is the technology behind satellite images of coastlines, farmland, and disaster zones.
    """,

    # ─────────────────────────────────────────────────────────────────────────
    # Part18: MIMO Radar Systems
    # Role: Advanced Application  |  Duration: 17 – 24 s  |  ~135 words
    # ─────────────────────────────────────────────────────────────────────────
    "Part18": """
        MIMO  —  Multiple-Input, Multiple-Output  —  radar is the next frontier in antenna array technology. A conventional phased array transmits one beam at a time from all its elements in unison. A MIMO radar does something fundamentally different: each transmit element radiates an independent, uniquely coded waveform simultaneously. On the receive side, a separate array of elements captures all returning echoes. Because each transmit signal is uniquely coded, the receiver can untangle which echo came from which transmitter. This creates a virtual array  —  a grid of effective elements far larger than either the physical transmit or receive array alone. The result is dramatically improved angular resolution, better ability to track multiple targets simultaneously, and greater resilience against jamming. MIMO radar is already deployed in advanced military systems and is being adopted in automotive and communications.
    """,

    # ─────────────────────────────────────────────────────────────────────────
    # Part19: Key Takeaways
    # Role: Summary  |  Duration: 16 – 23 s  |  ~113 words
    # ─────────────────────────────────────────────────────────────────────────
    "Part19": """
        Let us bring everything together. The parabolic reflector is the workhorse of long-range radar: high gain, proven reliability, but mechanically steered. The phased array is the speed champion: electronic steering in microseconds, ideal for fast-moving threats and multi-target environments. The slot array is the integrator's favourite: ultra-flat, flush-mountable, and highly efficient. The horn antenna is the generalist: broadband, predictable, and the calibration standard of the industry. Beneath all four types lie the same physical principles  —  gain, directivity, polarization, sidelobes  —  and the same governing equation: the radar range equation. Choosing the right antenna is not about which type is 'best.' It is about matching the antenna's characteristics precisely to the mission's demands.
    """,

    # ─────────────────────────────────────────────────────────────────────────
    # Part20: Outro – The Future of Radar Antennas
    # Role: Closing  |  Duration: 13 – 20 s  |  ~111 words
    # ─────────────────────────────────────────────────────────────────────────
    "Part20": """
        Radar antennas have evolved from simple rotating dishes to electronically steered arrays, synthetic apertures, and MIMO systems  —  each generation sharper, faster, and more capable than the last. The physics has not changed: Maxwell's equations still govern every wave that leaves an antenna and every echo that returns. But the engineering imagination applied to those equations keeps pushing the boundaries. Active electronically scanned arrays are shrinking. Conformal antennas are wrapping around curved aircraft surfaces. Metamaterial elements are bending waves in ways that were once considered impossible. The radar antenna is not a solved problem. It is an evolving frontier  —  and understanding its fundamentals is the key to navigating that frontier.
    """,
}

VOICE = "en-US-GuyNeural"

async def generate_voiceover():
    if not os.path.exists("voiceovers"):
        os.makedirs("voiceovers")

    print(f"--- Seslendirme Başlıyor: {VOICE} ---")

    for part, text in SCRIPTS.items():
        filename = f"voiceovers/{part}.mp3"
        print(f"İşleniyor: {part}...")
        
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(filename)
    
    print("\n--- İŞLEM TAMAMLANDI! ---")
    print("'voiceovers' klasörünü kontrol et.")

if __name__ == "__main__":
    asyncio.run(generate_voiceover())
