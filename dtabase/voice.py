import edge_tts
import asyncio

# Narration Script for Database YouTube Short
SCRIPT = """
Where does your data actually go when you save it?

A database. The brain of your application.

A database is an organized collection of data stored on a computer.

Think of it like a filing cabinet. Each drawer holds different information, neatly organized and easy to find.

Data is organized in tables. Tables have columns, which define what kind of information you're storing. And rows, which are individual records.

There are four basic operations you can perform. Create: add new data. Read: retrieve existing data. Update: modify data. And Delete: remove data. Together, these are called CRUD operations.

Where is all this data actually stored? On your hard drive or SSD. The beauty of databases? Data stays safe, even when the power is turned off.

Let's recap. Databases organize data in tables. Tables have columns and rows. CRUD operations let you manage your data. And everything is stored permanently on disk.

That's how databases work. Simple, powerful, essential.
"""

VOICE = "en-US-GuyNeural"
OUTPUT_FILE = "database_narration.mp3"

async def generate_audio():
    communicate = edge_tts.Communicate(SCRIPT, VOICE)
    await communicate.save(OUTPUT_FILE)
    print(f"✅ Audio saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(generate_audio())
