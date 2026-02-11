import asyncio
import edge_tts
import os

# Single narration script — ~50 seconds (~125 words at normal pace)
SCRIPTS = {
    "Full": (
        "Push a tumbler toy as hard as you like. It always bounces back. Why? "
        "The secret is a heavy weight hidden in the base. "
        "This pulls the center of mass very low. "
        "When the toy tilts, gravity creates a restoring torque that always pushes it back upright. "
        "We can see this on an energy curve. "
        "The lowest point is at zero tilt, so nature always pulls the toy back to its most stable position. "
        "But why does the rocking stop? Friction and air resistance steal a little energy each swing. "
        "The oscillations shrink until the toy stands perfectly still. "
        "Low center of mass, restoring torque, energy minimum, and damping. "
        "Four simple physics principles that make a toy unbeatable."
    ),
}

VOICE = "en-US-GuyNeural"

async def generate_voiceover():
    if not os.path.exists("voiceovers"):
        os.makedirs("voiceovers")

    print(f"--- Generating Voiceover: {VOICE} ---")

    for part, text in SCRIPTS.items():
        filename = f"voiceovers/{part}.mp3"
        print(f"Processing: {part}...")

        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(filename)

    print("\n--- DONE! ---")
    print("Check the 'voiceovers' folder.")

if __name__ == "__main__":
    asyncio.run(generate_voiceover())
