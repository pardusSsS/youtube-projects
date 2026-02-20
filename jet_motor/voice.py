import asyncio
import edge_tts
import os

# Narration Scripts for "How a Jet Engine Works in 1 Minute" — YouTube Short
SCRIPTS = {
    "JetEngineShort": """
How does a jet engine work?
Let's break it down in sixty seconds.

A jet engine has four key stages: the fan, the compressor, the combustion chamber, and the turbine.

Stage one: Intake and Fan.
A massive fan at the front sucks in enormous amounts of air.
About ninety percent of this air bypasses the core and provides thrust directly.

Stage two: the Compressor.
Multiple rows of spinning blades squeeze the remaining air into a much smaller space.
The pressure ratio can reach thirty to one, dramatically increasing the air's density.

Stage three: Combustion.
Jet fuel is injected into the compressed air and ignited.
Temperatures soar to around seventeen hundred degrees Celsius, causing the gases to expand violently.

Stage four: Turbine and Exhaust.
The hot, high-speed gases slam into the turbine blades, spinning them at tremendous speed.
The turbine is connected by a shaft to the front fan, keeping the entire cycle going.
The remaining gas blasts out the exhaust nozzle, generating thrust.

This is Newton's Third Law in action.
For every action, there is an equal and opposite reaction.
Gas pushes backward; the aircraft pushes forward.

Suck, squeeze, bang, blow. That's a jet engine.

Like and subscribe for more!
"""
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
