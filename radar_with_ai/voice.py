import asyncio
import edge_tts
import os

# Seslendirilecek Metinler
SCRIPTS = {
    "Part1": "Two revolutionary technologies merge into one. Artificial Intelligence meets Radar. This fusion is transforming detection, tracking, and defense. Watch how AI makes the invisible, visible.",
    
    "Part2": "A radar system works like a high-tech echo chamber. The transmitter sends radio waves. The antenna directs them toward targets. Waves bounce back from objects like aircraft. The receiver catches these returns. Signal processors analyze the data. Detection algorithms identify real targets. AI can enhance every single one of these steps, transforming basic radar into an intelligent system.",
    
    "Part3": "Raw radar signals are incredibly noisy. Ground clutter, weather interference, and electronic noise contaminate everything. Traditional filters help, but AI neural networks are game changers. This three-dimensional network learns to recognize noise versus real targets. Multiple layers process the messy input, each learning different patterns. The output is clean and clear. AI doesn't just filter, it understands.",
    
    "Part4": "Teaching AI to clean signals requires massive training data. We collect raw I-Q samples, the basic building blocks of radar. We create spectrograms showing frequency changes over time. We generate range-Doppler maps displaying distance and velocity. We gather noise patterns from real environments. Clear weather, storms, urban clutter, ocean returns. Millions of diverse examples teach AI to handle anything.",
    
    "Part5": "Once signals are clean, AI performs detection. Is there actually a target? Birds can look like drones. Weather mimics aircraft. Convolutional neural networks excel here. These three-dimensional layers process information progressively. First layers see raw patterns. Deeper layers recognize complex features. Final layers make confident decisions: aircraft, drone, or bird. All in milliseconds.",
    
    "Part6": "Detection AI needs mountains of labeled data. Imagine a radar screen with dozens of blips. Each needs identification. That's a commercial aircraft with large radar cross-section. That's a small drone. That's just a bird with wing-flapping signatures. Those are ground clutter returns. We need hundreds of thousands of labeled examples across different ranges, angles, and weather conditions. Only then can AI distinguish targets accurately.",
    
    "Part7": "Detection isn't enough. We need classification. What type exactly? Passenger plane? Fighter jet? Stealth bomber? Small drone? This requires deeper networks. Early layers detect shapes and movements. Middle layers recognize jet engine modulation signatures. Deep layers combine everything into final classification. The AI has learned millions of examples. It knows fighters differ from bombers. It recognizes unique drone rotor signatures.",
    
    "Part8": "Classification AI needs incredibly rich data. RCS profiles showing how reflections change with target rotation. Micro-Doppler signatures from helicopter blades and jet engines. Polarization data showing wave orientation changes. Multi-band fusion from X-band, S-band, L-band radar. We use data augmentation, adding synthetic noise and variations. The more diverse our training data, the more accurate our AI becomes in real-world scenarios.",
    
    "Part9": "Targets are moving. We need tracking and prediction. Where will that aircraft be in five seconds? LSTM neural networks have memory. These connected cells represent time steps. Hidden states flow between them, carrying past movement patterns. By learning how aircraft maneuver, AI predicts future positions with remarkable accuracy. It handles straight paths, curves, and sudden evasive maneuvers. This is understanding motion, not just following dots.",
    
    "Part10": "Tracking AI requires sequential trajectory data. Linear motion from steady aircraft. Curved paths from changing helicopters. Aggressive maneuvers from fighter jets. For each, we need position, velocity, and acceleration over time. Hundreds of flight paths in different conditions. The AI learns commercial aircraft turn gradually while fighters change direction rapidly. It learns physics: objects can't teleport or exceed acceleration limits. Predictions become realistic and reliable.",
    
    "Part11": "AI can optimize the radar itself through reinforcement learning. The radar adjusts pulse width, repetition frequency, bandwidth, and power. The AI agent learns optimal settings for each situation. Small drone? High bandwidth for resolution. Distant aircraft? Adjusted PRF to avoid ambiguities. The agent receives rewards for good performance. Over thousands of iterations, it learns perfect settings for every scenario, becoming an expert radar operator.",
    
    "Part12": "Optimization training happens in simulation. Virtual worlds with multiple targets at different speeds. Ground clutter, sea clutter, rain, snow. Interference from jamming and multipath. Sensor constraints on power and bandwidth. The AI experiments with different parameters and observes results. The reward function balances detection probability, false alarms, power, and bandwidth. After weeks of millions of scenarios, AI makes optimal decisions faster than any human.",
    
    "Part13": "Interference is radar's constant enemy. Jamming signals, electronic warfare, unintentional interference from other systems. Autoencoders solve this elegantly. The encoder compresses noisy signals into compact representations capturing only essentials. The narrow latent space forces learning what truly matters. The decoder reconstructs clean signals. During training, AI learns to preserve targets while discarding interference. It's adaptive noise-canceling for radar.",
    
    "Part14": "Interference mitigation needs paired training examples. Clean signal plus interference equals noisy signal. We create millions of these pairs with varying interference types, strengths, and patterns. Narrowband jamming, broadband noise, electronic warfare chaos. The AI inputs noisy signals and outputs clean ones. We simulate every documented jamming technique. When new interference appears in real deployment, AI recognizes it as another removable noise pattern.",
    
    "Part15": "Modern radar uses beamforming, focusing energy precisely like a spotlight. With antenna arrays, AI calculates optimal weights for each element in real-time. It considers target locations and interference directions. Then it shapes beams to maximize target signals while creating nulls toward jamming. Watch the beam steer and adapt thousands of times per second. Maximum sensitivity toward threats, zero reception from interference. Three-dimensional noise-canceling for radar.",
    
    "Part16": "Here's the complete AI-enhanced radar pipeline. Seven AI systems work simultaneously. Preprocessing cleans data. Detection identifies targets. Classification determines types. Tracking predicts positions. Beamforming optimizes antennas. Waveform optimization adjusts transmission. Interference mitigation removes jamming. Notice the feedback loops connecting everything. Detection informs beamforming. Tracking guides waveform optimization. It's one intelligent organism producing actionable intelligence in real-time.",
    
    "Part17": "Building these systems requires serious infrastructure. GPU clusters with eight A100s for parallel training. One hundred terabytes storage for training data. Half a terabyte RAM. One hundred gigabit networking between GPUs. Software includes PyTorch, CUDA, MLflow, and distributed training frameworks. Each model takes two to four weeks of continuous training. Multiply by seven systems. The scale is massive, but results are worth it: radar that sees farther, clearer, smarter.",
    
    "Part18": "Deployment brings extreme challenges. AI must run on edge devices like Jetson AGX, smartphone-sized embedded GPUs. Requirements are brutal: inference under fifty milliseconds, one hundred frames per second, less than thirty watts power. We use model compression. Quantization reduces precision. Pruning removes connections. Knowledge distillation teaches small networks to mimic large ones. Deployed models are ten times smaller while maintaining ninety-five percent accuracy. Powerful, fast, efficient AI at the edge.",
    
    "Part19": "The future brings exciting possibilities. Federated learning lets radars train together without sharing sensitive data. Few-shot learning recognizes new threats from handful of examples. Neural architecture search automates network design. Quantum machine learning promises unprecedented processing power. But challenges remain. Adversarial robustness against spoofing. Explainability for trust. Data scarcity for rare events. Ever-tighter real-time constraints. These will define the next decade of AI-radar research.",
    
    "Part20": "Seven AI systems integrated into one platform. Signal processing, detection, classification, tracking, beamforming, waveform optimization, interference mitigation. All coordinated by the central AI core. Each trained on millions of examples. Each using specialized architectures. Each processing real-time on edge hardware. Together they create revolutionary capability: radar that doesn't just detect, it understands. It adapts, learns, and decides faster than humans. This is intelligent sensing. The future is here."
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
