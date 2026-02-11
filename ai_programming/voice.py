import asyncio
import edge_tts
import os

# Narration Scripts for AI Programming Animation
SCRIPTS = {
    "Part1": """
Can machines really think in code?
Today, we're diving deep into how AI writes software.
It's not magic, it's mathematics, and by the end of this video, you'll understand exactly how it works.
""",

    "Part2": """
At the heart of every code-writing AI is a neural network.
Think of it as an artificial brain made up of billions of tiny components called parameters.
These neurons are arranged in layers, each one processing information and passing it forward.
When data flows through this network, patterns emerge.
The AI learns to recognize what good code looks like from billions of examples.
One goal: understanding the language of programming.
""",

    "Part3": """
The secret behind modern AI is called the Transformer architecture.
It has two main parts: an Encoder that reads and understands input, and a Decoder that generates output.
Inside each part, you'll find three key building blocks.
Embeddings convert words and code into numbers.
Self-Attention helps the model understand context by looking at relationships between tokens.
Feed-Forward layers process this information further.
The magic happens when these components work together, allowing the AI to understand and generate code.
""",

    "Part4": """
How does an AI learn to code? By reading massive amounts of existing code.
The training data comes from places like GitHub, StackOverflow, and documentation.
Code snippets flow into the AI model, and with each example, it gets a little bit smarter.
We're talking about billions of lines of code from every programming language imaginable.
The AI doesn't memorize code. Instead, it learns patterns, syntax rules, and programming concepts.
""",

    "Part5": """
Before the AI can understand code, it needs to break it down into smaller pieces called tokens.
Take a simple print statement. The AI doesn't see it as one unit.
Instead, it splits it into individual tokens: the function name, parentheses, quotes, and words.
Each token gets assigned a unique numerical ID.
This tokenization process is how the AI converts human-readable code into numbers it can process.
""",

    "Part6": """
Once code is tokenized, each token needs to be placed into a mathematical space.
This is called embedding.
Imagine a three-dimensional universe where every programming concept has a specific location.
Similar tokens cluster together. Keywords like 'def' and 'function' end up close to each other.
Print statements group with other output functions.
Loop keywords like 'for' and 'while' form their own neighborhood.
This spatial arrangement helps the AI understand the relationships between different code elements.
""",

    "Part7": """
The Attention mechanism is what makes modern AI so powerful.
It answers one critical question: which tokens should I focus on right now?
The system uses three matrices: Query, Key, and Value.
Query asks: what am I looking for?
Key answers: what do I contain?
Value provides: what information do I carry?
These work together through a formula that calculates relevance between every pair of tokens.
This allows the AI to understand context, no matter how far apart related code elements are.
""",

    "Part8": """
Let's see attention in action.
When the AI looks at a function definition, it pays different amounts of attention to each token.
The word 'def' strongly attends to the colon at the end, they define a function together.
It also pays attention to the function name and parameters.
These attention weights, shown as bars, represent how important each connection is.
Higher weights mean stronger relevance.
This is how the AI understands that 'def' and colon belong together, even with tokens in between.
""",

    "Part9": """
One attention head isn't enough. The AI uses multiple heads working in parallel.
Each head learns to recognize different patterns.
One might focus on syntax relationships.
Another tracks variable references.
A third might detect function calls.
After all heads process the input, their outputs are combined into a single representation.
This multi-headed approach gives the AI a richer, more nuanced understanding of code.
""",

    "Part10": """
Between attention layers, the AI uses Feed-Forward Networks.
Think of them as processing stations that transform the data.
Input flows in, gets expanded to four times its size in a hidden layer, then compressed back down.
An activation function called GELU adds non-linearity, allowing the network to learn complex patterns.
This expansion and compression cycle helps the AI extract and refine the features it needs.
""",

    "Part11": """
The Transformer doesn't just have one layer. It stacks many layers on top of each other.
Each layer adds more understanding.
Early layers might learn basic syntax.
Middle layers understand function structures.
Deep layers grasp complex patterns like algorithms and design patterns.
As data flows through these stacked layers, the AI's understanding deepens with every step.
More layers generally mean more sophisticated understanding.
""",

    "Part12": """
There's a limit to how much code the AI can see at once. This is called the Context Window.
Modern models can handle anywhere from eight thousand to over one hundred thousand tokens.
Only the tokens within this window can influence each other.
The window can be thought of as the AI's working memory.
If your code is longer than the context window, the AI can't see all of it at once.
Understanding this limitation is key to working effectively with AI coding assistants.
""",

    "Part13": """
When generating code, the AI predicts one token at a time.
Given the code so far, it calculates the probability of what comes next.
In our example, after 'return a', the plus sign has seventy-five percent probability.
Other operators like multiplication, subtraction, and division have much lower chances.
The AI picks the most likely token, adds it to the output, and repeats.
This probability-based prediction is how AI writes code that makes sense.
""",

    "Part14": """
Temperature is a setting that controls how creative the AI gets.
With low temperature, the AI plays it safe, picking only the most likely tokens. This produces focused, predictable code.
Medium temperature balances between safety and creativity.
High temperature allows the AI to take risks, sometimes choosing unexpected tokens.
This can lead to creative solutions, but also more errors.
For code generation, lower temperatures are usually preferred for reliability.
""",

    "Part15": """
Code generation is an autoregressive process, meaning each new token depends on all previous ones.
The cycle goes like this: encode the current context, apply attention to understand relationships, predict the next token, then sample from the probability distribution.
This cycle repeats for every single token.
Watch as the AI builds a Fibonacci function one piece at a time.
Each token is the result of the entire pipeline running from start to finish.
""",

    "Part16": """
The AI doesn't just randomly string tokens together. It learns proper syntax.
Bracket matching ensures every opening parenthesis has its closing partner.
Indentation rules are understood, like the four-space convention in Python.
Keywords are recognized and used correctly.
The AI picks up these syntax rules from the billions of examples it trained on.
This is why AI-generated code usually runs without syntax errors.
""",

    "Part17": """
Beyond syntax, the AI understands what code means. This is semantic understanding.
It tracks variables throughout their lifecycle.
When 'name' appears as a parameter, the AI knows it's a string that will be used later.
It understands that 'message' stores the result of string concatenation.
It even infers that the return type matches the variable type.
This semantic awareness helps the AI write code that not only looks correct but actually works.
""",

    "Part18": """
Training an AI to code involves serious mathematics.
The Cross-Entropy Loss measures how wrong the AI's predictions are.
Gradient Descent is the optimization algorithm that minimizes this loss.
Imagine a landscape where height represents error.
The AI starts somewhere on this surface and gradually rolls downhill.
With each training step, it adjusts billions of parameters to reduce the error.
Eventually, it finds the minimum, the point where it makes the best predictions possible.
""",

    "Part19": """
Let's see the complete pipeline in action.
A prompt enters the system.
Tokenization breaks it into pieces.
Embedding converts tokens to vectors.
Attention processes relationships.
Prediction generates probabilities.
And finally, output emerges.
What goes in as 'Write hello world' comes out as actual working code.
Each stage transforms the data, building from raw text to functional code.
This is the journey every prompt takes through an AI coding assistant.
""",

    "Part20": """
So where is AI coding headed?
Today, we have single-file code generation.
Soon, AI will understand entire projects, all files and their relationships.
The future holds autonomous software development, where AI builds complete applications from a description.
The code you imagine, AI can create.
Thanks for watching! Subscribe for more deep dives into the technology shaping our future.
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
