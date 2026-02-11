import asyncio
import edge_tts
import os

# Seslendirilecek Metinler
SCRIPTS = {
    "Part1": """
        How do computers actually understand the code we write? Let's find out.
    """,
    
    "Part2": """
        When we write code, we use human-readable programming languages. 
        These languages use words, symbols, and structures that make sense to us.
        We can read them, understand them, and reason about them.
        But here's the problem: computers don't speak our language.
    """,
    
    "Part3": """
        Computers only understand one thing: binary. 
        Zeros and ones. Machine code.
        Everything a computer does is ultimately represented as sequences of binary digits.
        This is the only language processors can execute directly.
        So how do we bridge this massive gap between human code and machine code?
    """,
    
    "Part4": """
        This is the translation problem at the heart of computing.
        On one side, we have human-written code that's easy for us to read and write.
        On the other side, we have binary machine code that only processors understand.
        Between them lies a complex journey of transformation.
        The question is: what steps are needed to cross this divide?
    """,
    
    "Part5": """
        The answer is a translation pipeline. A series of stages that gradually transforms our code.
        It starts with source code and ends with machine code.
        Each stage has a specific job: the lexer, the parser, the compiler or interpreter, and finally code generation.
        Think of it like a factory assembly line, where each station adds another layer of transformation.
        By the end, what started as human-readable text becomes executable binary instructions.
    """,
    
    "Part6": """
        The first step is lexical analysis, also called tokenization.
        The lexer reads your source code character by character and groups them into meaningful units called tokens.
        Take this simple line: x equals ten plus five.
        The lexer breaks it down into individual tokens: x is an identifier, equals is an operator, ten is a number, plus is an operator, and five is a number.
        Each token is labeled with its type, creating a stream of categorized pieces that the next stage can work with.
    """,
    
    "Part7": """
        These tokens form a stream, a sequence that flows through the pipeline.
        Each token carries information about what it represents: is it a variable name, an operator, a number, or a keyword?
        This token stream is the output of the lexer and the input for the next stage.
        Think of it like breaking down a sentence into individual words and labeling each one as a noun, verb, or adjective.
        The structure is starting to emerge.
    """,
    
    "Part8": """
        Next comes syntax analysis, or parsing.
        The parser takes the stream of tokens and organizes them into a tree structure called a parse tree.
        This tree represents the grammatical structure of your code.
        For our example, the root is the assignment operation. The left branch is the variable x. The right branch is the addition operation.
        And that addition has its own branches: the numbers ten and five.
        The parser ensures your code follows the rules of the programming language's grammar.
    """,
    
    "Part9": """
        The parse tree is then refined into an Abstract Syntax Tree, or AST.
        This is a cleaner, more structured representation of your code's meaning.
        Unlike the parse tree, the AST strips away unnecessary details and focuses on the logical structure.
        Here we can see the hierarchy in three dimensions: the assignment at the top, the variable and operation below, and the operands at the bottom.
        The AST is the foundation for all the analysis and transformations that follow.
    """,
    
    "Part10": """
        Now we enter semantic analysis, where the computer checks if your code actually makes sense.
        Is the variable declared? Are the types compatible? Is the scope valid? Could this cause an error like division by zero?
        The semantic analyzer verifies these rules.
        For example, if you're assigning an integer value to an integer variable, it checks that the types match.
        If they don't, you get a type error. This stage catches logical mistakes that aren't visible in the syntax alone.
    """,
    
    "Part11": """
        After semantic analysis, the code is converted into an intermediate representation, or IR.
        This is a middle ground between high-level code and low-level machine code.
        Our simple statement x equals ten plus five becomes a series of three-address instructions: 
        load ten into t1, load five into t2, add them into t3, store t3 into x.
        Then this IR can be translated into assembly language with specific processor instructions.
        IR makes it easier to optimize and target different types of processors.
    """,
    
    "Part12": """
        Before final code generation, the optimizer gets to work.
        It analyzes the intermediate code looking for improvements.
        Our example has four separate operations, but the optimizer realizes ten plus five is always fifteen.
        So it performs constant folding, replacing all those steps with a single instruction: x equals fifteen.
        Optimization makes code faster, smaller, and more efficient without changing what it does.
        This is where the magic of compiler intelligence really shines.
    """,
    
    "Part13": """
        Next is code generation, where IR is translated into assembly language.
        The code generator acts like a machine, taking intermediate instructions and converting them into the specific assembly commands for your target processor.
        Different processors have different instruction sets, so this stage is platform-specific.
        The gears turn, processing each IR instruction and outputting the corresponding assembly code.
        This is where we start speaking the processor's language.
    """,
    
    "Part14": """
        Assembly language is a human-readable form of machine code.
        Each instruction corresponds directly to a processor operation.
        MOV R1, 10 means load the value ten into register one.
        ADD R3, R1, R2 means add the values in registers one and two, and store the result in register three.
        Registers are tiny, super-fast storage locations inside the CPU.
        Assembly is the last step before raw binary, and it's still readable if you know what you're looking for.
    """,
    
    "Part15": """
        The final translation: assembly to machine code.
        Each assembly instruction is converted into binary.
        MOV R1, 10 becomes a specific sequence of ones and zeros that the processor can decode.
        This binary code is what actually gets loaded into the CPU.
        The processor reads these binary instructions, decodes them, and executes them.
        This is the language the hardware truly understands: pure binary, streaming into the chip.
    """,
    
    "Part16": """
        Inside the CPU, the magic happens.
        The processor has different components: the ALU handles arithmetic and logic, the control unit manages instruction flow, and registers hold data.
        When machine code arrives, data flows from registers into the ALU.
        The control unit tells the ALU what operation to perform.
        The result flows back out and is stored.
        This three-dimensional dance of data happens billions of times per second in modern processors.
    """,
    
    "Part17": """
        Every instruction goes through the CPU cycle: fetch, decode, execute.
        First, fetch the instruction from memory.
        Second, decode it to understand what operation is needed.
        Third, execute the operation using the ALU and registers.
        Then the cycle repeats with the next instruction.
        This loop runs continuously, processing millions of instructions every second.
        It's the heartbeat of computation, happening over and over at incredible speed.
    """,
    
    "Part18": """
        Not all languages follow the same path. There are two major approaches: compiled and interpreted.
        Compiled languages like C and C++ go through the entire pipeline ahead of time.
        Source code becomes an executable file full of machine code, which runs directly on the processor.
        Interpreted languages like Python and JavaScript take a different route.
        The interpreter reads and executes the code line by line, translating on the fly.
        There's a loop: interpret a line, execute it, move to the next. Each approach has trade-offs in speed and flexibility.
    """,
    
    "Part19": """
        Let's trace the complete journey from top to bottom.
        It starts with source code that you write.
        The lexer breaks it into tokens.
        The parser builds an abstract syntax tree.
        Semantic analysis checks for errors.
        Intermediate representation simplifies the structure.
        The optimizer makes it faster.
        Code generation creates assembly.
        The assembler produces machine code.
        And finally, the CPU executes it.
        Every line of code you write travels this entire pipeline before it runs.
    """,
    
    "Part20": """
        From human to machine. That's the journey.
        Computers don't understand code directly. They need multiple translation layers to bridge the gap.
        Lexer, parser, compiler, assembly, CPU. Each step transforms the code closer to machine language.
        Every program, every app, every website goes through this process.
        Understanding this pipeline doesn't just teach you how computers work.
        It empowers you to write better code, debug more effectively, and create with confidence.
        Because now you know: the path from your mind to the machine.
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
