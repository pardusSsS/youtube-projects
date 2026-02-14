import asyncio
import edge_tts
import os

SCRIPTS = {
    "Full": (
        # Section 1 — Intro (~6.6s)
        "How does a soccer ball curve into the goal? "
        "The answer lies in spin. "

        # Section 2 — Magnus Effect (~9.8s)
        "When a ball spins in flight, it drags the air around it. "
        "One side speeds up, the other slows down. "
        "This creates a pressure difference, and a sideways force appears. "
        "This is the Magnus effect. "

        # Section 3 — Curved Free Kick (~11.1s)
        "In a free kick, a spinning ball doesn't travel in a straight line. "
        "The Magnus force bends its path around the wall of defenders "
        "and into the corner of the goal. "
        "The ball's acceleration combines gravity and the Magnus force. "

        # Section 4 — Angular Momentum (~10.4s)
        "The spin also keeps the ball stable in flight. "
        "Angular momentum acts like a gyroscope, "
        "locking the spin axis in place so the curve stays predictable. "
        "The faster the spin, the greater the stability. "

        # Section 5 — Drag & Spin Decay (~10.6s)
        "But nothing lasts forever. "
        "Air resistance slows the ball and friction reduces its spin. "
        "Both decay over time. "
        "As the spin weakens, the curve straightens out near the end of its flight. "

        # Section 6 — Goal Moment (~10.2s)
        "Put it all together and you get the perfect free kick. "
        "The ball launches with speed and spin, curves through the air, "
        "and bends into the top corner. Goal! "

        # Section 7 — Outro (~9.7s)
        "Magnus effect, curved trajectory, angular momentum, and drag. "
        "Four physics principles behind every beautiful goal."
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
