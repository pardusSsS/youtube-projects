import asyncio
import edge_tts
import os

# Seslendirilecek Metinler
SCRIPTS = {
    "Part1": "Modern naval warfare happens beyond the horizon. But how does a warship detect a fighter jet moving at supersonic speeds before it's even visible?",
    "Part2": "Meet the Aegis-class destroyer. This floating fortress is equipped with the world's most advanced phased array radar system, capable of tracking hundreds of targets simultaneously.",
    "Part3": "Unlike traditional radars that mechanically rotate, a phased array uses thousands of small emitters. By shifting the phase of each signal, we can steer the beam electronically in milliseconds.",
    "Part4": "It all starts here in the signal generator. We create high-frequency electromagnetic pulses. Precision timing is critical for accurate ranging.",
    "Part5": "The target: a fifth-generation fighter. Its shape is strictly designed to deflect radar waves away from the source, minimizing its radar cross-section.",
    "Part6": "Electromagnetic waves travel at the speed of light, 300,000 kilometers per second. As they propagate, the electric and magnetic fields oscillate perpendicular to the direction of travel.",
    "Part7": "The pulse leaves the ship, traversing kilometers of empty space. As it travels, it expands, distributing its energy over a larger and larger area, following the inverse square law.",
    "Part8": "When the wave hits the target, most of it scatteres into space. But a tiny fraction is reflected back towards the source. This is the echo we are hunting for.",
    "Part9": "The intensity of this reflection depends on the material's properties. The reflection coefficient, gamma, tells us how much energy bounces back. Conductive surfaces reflect strongly, while stealth coatings absorb the energy.",
    "Part10": "The Radar Cross Section, or sigma, quantifies how visible the object is to radar. A large cargo plane has a huge RCS, while a stealth fighter appears as small as a bird.",
    "Part11": "The signal must travel to the target and back. This two-way journey means the received power drops with the fourth power of distance. We receive only a whisper of the original shout.",
    "Part12": "The radar measures range, azimuth, and elevation. Using spherical coordinates, we can pinpoint the target's exact location in 3D space relative to the ship.",
    "Part13": "If the target is moving, the frequency of the reflected wave changes. This is the Doppler effect. Approaching targets compress the wave, increasing the frequency.",
    "Part14": "By analyzing this frequency shift, we calculate the target's radial velocity. We know not just where it is, but exactly how fast it is closing in on us.",
    "Part15": "The raw signal is buried in noise from the ocean and atmosphere. We use Constant False Alarm Rate processing to dynamically adjust the threshold and filter out the clutter.",
    "Part16": "Is it a friend or foe? By analyzing the specific radar signature and speed profile, the system classifies the target type instantly.",
    "Part17": "Welcome to the Combat Information Center. Here, on the tactical display, commanders verify the track and make split-second decisions based on the sensor data.",
    "Part18": "We don't rely on just one sensor. We fuse data from primary radar, secondary radar, and infrared sensors to create a single, high-confidence fused track.",
    "Part19": "Let's review the full sequence. Transmit. Propagate. Reflect. Receive. Process. Track. A complex chain of physics and engineering executing in milliseconds.",
    "Part20": "From simple radio waves to sophisticated digital processing, naval radar is the unblinking eye of the fleet. Ensuring safety through science."
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
