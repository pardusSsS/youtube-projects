import asyncio
import edge_tts
import os

# Narration Script for "The Logic & Algorithms Behind the Rubik's Cube" — YouTube Short
SCRIPTS = {
    "RubikCubeShort": """
How does a Rubik's Cube actually work?

It has over forty-three quintillion possible states — more than grains of sand on Earth.

Six letters describe every move: U, D, L, R, F, and B — each a ninety-degree face turn.

Mathematically, the cube is a group. Every move sequence is a permutation of fifty-four stickers, with inverses and closure.

God's Number is twenty. Any scramble, solved in twenty moves or fewer — proven in twenty-ten.

Speed-solvers use CFOP: Cross, F-two-L, O-L-L, then P-L-L. That's seventy-eight algorithms combined.

Computers use Kociemba's two-phase algorithm — reducing the cube to a subgroup, then solving to the final state.

From toy to deep mathematics — that's the Rubik's Cube.

Like and subscribe for more!
"""
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

    print("\n--- COMPLETE! ---")
    print("Check the 'voiceovers' folder.")

if __name__ == "__main__":
    asyncio.run(generate_voiceover())
