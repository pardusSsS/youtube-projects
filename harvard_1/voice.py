# Professional English Narration Scripts for Harvard Entrance Exam Animation
# Each script is proportional to the scene's duration (15-20 seconds each)

SCRIPTS = {
    "Part1": """
Welcome to one of the most challenging problems from the Harvard entrance exam.
Today, we're going to solve the limit of the n-th root of n factorial, divided by n, as n approaches infinity.
This elegant problem combines factorials, roots, and limits into a beautiful mathematical puzzle.
Let's uncover the answer step by step.
""",

    "Part2": """
Let's break down what we're dealing with.
In the numerator, we have the n-th root of n factorial.
The n-th root extracts a value such that when multiplied by itself n times, it gives n factorial.
In the denominator, we simply divide by n.
Understanding each component is key to solving this limit.
""",

    "Part3": """
What exactly is a factorial?
N factorial, written as n exclamation point, means multiplying all integers from one up to n.
For example, five factorial equals one times two times three times four times five, which is one hundred twenty.
The important thing to remember: factorial grows extremely fast, faster than exponential functions.
""",

    "Part4": """
Now let's understand N-th roots.
The n-th root of x equals x raised to the power of one over n.
For example, the square root of sixteen is four, the cube root of twenty-seven is three.
The key insight is that n-th roots "slow down" the growth of large numbers.
This will be crucial when we deal with our factorial expression.
""",

    "Part5": """
To solve this limit, we'll need a powerful tool: Stirling's Approximation.
This remarkable formula tells us that n factorial is approximately equal to the square root of two pi n, times n over e, all raised to the n-th power.
Named after James Stirling, this approximation becomes incredibly accurate for large values of n.
""",

    "Part6": """
Let's verify how accurate Stirling's approximation really is.
For n equals ten, the actual value of ten factorial is three million, six hundred twenty-eight thousand, eight hundred.
Stirling's approximation gives us three million, five hundred ninety-eight thousand.
That's already ninety-nine percent accurate, and it only gets better as n increases.
""",

    "Part7": """
Let's examine the components of Stirling's formula more closely.
The square root of two pi n is called the correction factor. It fine-tunes our approximation.
The main growth term is n over e, raised to the n-th power.
Here, e is Euler's number, approximately two point seven one eight.
As n approaches infinity, this approximation becomes essentially exact.
""",

    "Part8": """
Now we apply Stirling's formula to our limit.
We replace n factorial with its approximation: square root of two pi n, times n over e to the n-th power.
Then we take the n-th root of this entire expression and divide by n.
This substitution transforms our complex limit into something more manageable.
""",

    "Part9": """
Let's use the product rule for n-th roots.
The n-th root of a product equals the product of the n-th roots.
This allows us to split our expression into two separate parts.
Part A contains the correction factor: the n-th root of square root of two pi n.
Part B contains the main term: the n-th root of n over e to the n-th power.
""",

    "Part10": """
Let's evaluate Part A: the n-th root of square root of two pi n.
We can rewrite this as two pi n raised to the power of one over two n.
As n approaches infinity, this expression approaches one.
Why? Because any finite base raised to a power approaching zero equals one.
So Part A contributes a factor of one to our final answer.
""",

    "Part11": """
Now for Part B: the n-th root of n over e, raised to the n-th power.
Here's a key property: the n-th root of x to the n-th power simply equals x.
The root and the power cancel each other perfectly.
Therefore, Part B simplifies directly to n over e.
""",

    "Part12": """
Now we combine our results for the final simplification.
We have one from Part A, times n over e from Part B, all divided by n.
The fraction n over e, divided by n, simplifies beautifully.
The n in the numerator cancels with the n in the denominator.
We're left with just one over e.
""",

    "Part13": """
And there it is: the answer to our Harvard entrance exam problem.
The limit equals one over e.
This is approximately zero point three six eight.
A beautifully simple answer to what seemed like a complex problem.
The number e appears once again in an unexpected place.
""",

    "Part14": """
Let's verify our answer by computing the expression for increasing values of n.
For n equals five, we get approximately zero point four seven.
For n equals fifty, we get zero point three seven seven.
For n equals five hundred, we get zero point three six nine.
The values are clearly converging toward one over e, which is zero point three six eight.
""",

    "Part15": """
Why does one over e appear as our answer?
The number e emerges naturally because of how factorial growth relates to exponential growth.
E is the unique base where the rate of growth equals the function itself.
When we extract the n-th root of n factorial and scale by n, e naturally surfaces.
It's another example of e's fundamental role in mathematics.
""",

    "Part16": """
Let's visualize what's happening geometrically.
Stirling's approximation connects factorial to exponential growth.
The n-th root operation extracts the "average" multiplicative factor.
Dividing by n normalizes the growth rate.
The result is the natural scaling constant: one over e.
""",

    "Part17": """
This problem connects several important mathematical concepts.
Factorials, which count permutations and appear throughout combinatorics.
N-th roots, which measure geometric averages.
Limits, which describe behavior at infinity.
And Stirling's approximation, which bridges discrete and continuous mathematics.
""",

    "Part18": """
There's actually an alternative approach using logarithms.
Take the natural log of both sides and apply log properties.
The sum of logarithms from one to n, divided by n, minus log n.
This sum approaches negative one as n goes to infinity.
Therefore, the original expression approaches e to the negative one, which is one over e.
""",

    "Part19": """
Let's summarize what we've accomplished.
We used Stirling's approximation to handle the factorial.
We split the n-th root into two manageable parts.
The correction term approached one.
The main term simplified to n over e.
Finally, the division cancelled the n, leaving one over e.
""",

    "Part20": """
And that concludes our solution to this Harvard entrance exam challenge.
The limit of the n-th root of n factorial, divided by n, equals exactly one over e.
Mathematics reveals elegant answers when we apply the right tools.
Thank you for watching. If you enjoyed this problem, like and subscribe for more mathematical journeys.
"""
}


def get_script(part_name: str) -> str:
    """Get the narration script for a specific part."""
    return SCRIPTS.get(part_name, "").strip()


def get_all_scripts() -> dict:
    """Get all narration scripts."""
    return {k: v.strip() for k, v in SCRIPTS.items()}


if __name__ == "__main__":
    # Print all scripts with their lengths
    for part, script in SCRIPTS.items():
        word_count = len(script.split())
        print(f"{part}: {word_count} words")
