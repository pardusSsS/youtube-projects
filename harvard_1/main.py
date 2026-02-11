from manim import *
import numpy as np

# ============================================================================
# HARVARD ENTRANCE EXAM: lim(n→∞) (n!)^(1/n) / n = 1/e
# 20-Part Educational Animation
# ============================================================================

# Color Palette - Vibrant Space Tech
DEEP_NAVY = "#020B1F"
ELECTRIC_CYAN = "#00F0FF"
NEON_PINK = "#FF0055"
VIBRANT_ORANGE = "#FF9F00"
TEXT_WHITE = "#FFFFFF"
SUBTLE_NAVY = "#1E2A45"

config.background_color = DEEP_NAVY


# ============================================================================
# PART 1: THE HOOK (3-6 seconds)
# ============================================================================
class Part1(Scene):
    """Dramatic title reveal - instant attention grabber"""
    
    def construct(self):
        # Main title with glow effect
        title = Text("HARVARD", font_size=96, color=VIBRANT_ORANGE, weight=BOLD)
        subtitle = Text("ENTRANCE EXAM", font_size=64, color=ELECTRIC_CYAN)
        subtitle.next_to(title, DOWN, buff=0.4)
        
        challenge = Text("CHALLENGE", font_size=48, color=NEON_PINK)
        challenge.next_to(subtitle, DOWN, buff=0.5)
        
        title_group = VGroup(title, subtitle, challenge)
        title_group.move_to(ORIGIN)
        
        # Create glow effect with shadow copies
        title_glow = title.copy().set_color(VIBRANT_ORANGE).set_opacity(0.3)
        title_glow.scale(1.05)
        
        # Fast dramatic entrance
        self.play(
            FadeIn(title_glow, scale=2),
            FadeIn(title, scale=1.5),
            run_time=0.5
        )
        self.play(
            FadeIn(subtitle, shift=UP * 0.5),
            run_time=0.4
        )
        self.play(
            FadeIn(challenge, shift=UP * 0.3),
            Flash(challenge, color=NEON_PINK, line_length=0.3),
            run_time=0.6
        )
        
        # Quick pulse effect
        self.play(
            title_group.animate.scale(1.1),
            rate_func=there_and_back,
            run_time=0.5
        )
        
        self.wait(0.5)
        
        # Fade out title group completely before showing formula
        self.play(
            FadeOut(title_group),
            FadeOut(title_glow),
            run_time=0.6
        )
        
        # Show the formula prominently centered
        formula_hint = MathTex(
            r"\lim_{n \to \infty} \frac{\sqrt[n]{n!}}{n} = \, ?",
            font_size=80,
            color=TEXT_WHITE
        )
        formula_hint.move_to(ORIGIN)
        
        # Box around formula
        formula_box = SurroundingRectangle(formula_hint, color=ELECTRIC_CYAN, buff=0.3, stroke_width=2)
        
        self.play(
            Write(formula_hint),
            run_time=1.2
        )
        
        self.play(
            Create(formula_box),
            Flash(formula_hint, color=ELECTRIC_CYAN, line_length=0.5),
            run_time=0.8
        )
        
        self.wait(1)


# ============================================================================
# PART 2: PROBLEM PRESENTATION (15-20 seconds)
# ============================================================================
class Part2(Scene):
    """Display the limit problem with clean LaTeX"""
    
    def construct(self):
        # Header
        header = Text("The Challenge", font_size=48, color=ELECTRIC_CYAN)
        header.to_edge(UP, buff=0.5)
        
        self.play(Write(header), run_time=1)
        
        # Build the complete formula - larger and centered
        formula = MathTex(
            r"\lim_{n \to \infty}",
            r"\frac{\sqrt[n]{n!}}{n}",
            r"= \, ?",
            font_size=72
        )
        formula[0].set_color(TEXT_WHITE)
        formula[1].set_color(TEXT_WHITE)
        formula[2].set_color(VIBRANT_ORANGE)
        
        formula.move_to(UP * 0.5)
        
        # Animate each piece
        self.play(FadeIn(formula[0], shift=RIGHT), run_time=1.5)
        self.wait(0.8)
        
        self.play(Write(formula[1]), run_time=2)
        self.wait(0.8)
        
        self.play(
            FadeIn(formula[2], scale=1.5),
            Flash(formula[2], color=VIBRANT_ORANGE),
            run_time=1.5
        )
        
        self.wait(0.5)
        
        # ANNOTATION 1: Factorial (n!) - point to it from the RIGHT side
        # Create annotation box and label on the right
        factorial_label = Text("Factorial: n!", font_size=32, color=NEON_PINK)
        factorial_label.move_to(RIGHT * 4.5 + UP * 1.5)
        
        # Arrow pointing from label to the n! in formula
        factorial_arrow = Arrow(
            start=factorial_label.get_left(),
            end=formula[1].get_right() + UP * 0.3,
            color=NEON_PINK,
            stroke_width=3,
            buff=0.2
        )
        
        factorial_desc = Text(
            "n! = 1 × 2 × 3 × ... × n",
            font_size=24,
            color=NEON_PINK
        ).set_opacity(0.9)
        factorial_desc.next_to(factorial_label, DOWN, buff=0.2)
        
        self.play(
            Write(factorial_label),
            Create(factorial_arrow),
            run_time=1.2
        )
        self.play(FadeIn(factorial_desc), run_time=0.8)
        self.wait(1)
        
        # ANNOTATION 2: n-th Root - point to it from the LEFT side
        root_label = Text("n-th Root", font_size=32, color=ELECTRIC_CYAN)
        root_label.move_to(LEFT * 4.5 + DOWN * 0.5)
        
        root_arrow = Arrow(
            start=root_label.get_right(),
            end=formula[1].get_left() + DOWN * 0.2,
            color=ELECTRIC_CYAN,
            stroke_width=3,
            buff=0.2
        )
        
        root_desc = MathTex(
            r"\sqrt[n]{x} = x^{\frac{1}{n}}",
            font_size=28,
            color=ELECTRIC_CYAN
        )
        root_desc.next_to(root_label, DOWN, buff=0.2)
        
        self.play(
            Write(root_label),
            Create(root_arrow),
            run_time=1.2
        )
        self.play(FadeIn(root_desc), run_time=0.8)
        self.wait(1)
        
        # ANNOTATION 3: Denominator n - point from below
        denom_label = Text("Divided by n", font_size=28, color=VIBRANT_ORANGE)
        denom_label.move_to(DOWN * 2.2)
        
        denom_arrow = Arrow(
            start=denom_label.get_top(),
            end=formula[1].get_bottom() + DOWN * 0.1,
            color=VIBRANT_ORANGE,
            stroke_width=3,
            buff=0.15
        )
        
        self.play(
            Write(denom_label),
            Create(denom_arrow),
            run_time=1
        )
        self.wait(1)
        
        # Question text at the bottom
        question = Text(
            "What value does this approach as n → ∞?",
            font_size=34,
            color=TEXT_WHITE
        )
        question.to_edge(DOWN, buff=0.5)
        
        self.play(Write(question), run_time=1.5)
        self.wait(2.5)


# ============================================================================
# PART 3: WHAT IS FACTORIAL? (15-20 seconds)
# ============================================================================
class Part3(Scene):
    """Visual breakdown of n! = 1 × 2 × 3 × ... × n"""
    
    def construct(self):
        # Header
        header = Text("What is Factorial?", font_size=48, color=ELECTRIC_CYAN)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        # n! definition - higher position
        definition = MathTex(
            r"n! = 1 \times 2 \times 3 \times \cdots \times n",
            font_size=52,
            color=TEXT_WHITE
        )
        definition.move_to(UP * 1.8)
        
        # Add box around definition
        def_box = SurroundingRectangle(definition, color=ELECTRIC_CYAN, buff=0.15, stroke_width=2)
        
        self.play(Write(definition), Create(def_box), run_time=2)
        self.wait(0.8)
        
        # Example section - on the left side
        example_label = Text("Example: 5!", font_size=32, color=VIBRANT_ORANGE)
        example_label.move_to(LEFT * 4.5 + UP * 0.5)
        
        self.play(FadeIn(example_label), run_time=0.8)
        
        # Build the multiplication as a single MathTex for better alignment
        multiplication = MathTex(
            r"1 \times 2 \times 3 \times 4 \times 5",
            font_size=48,
            color=ELECTRIC_CYAN
        )
        multiplication.move_to(LEFT * 1.5 + DOWN * 0.3)
        
        equals_result = MathTex(
            r"= 120",
            font_size=56,
            color=VIBRANT_ORANGE
        )
        equals_result.next_to(multiplication, RIGHT, buff=0.4)
        
        self.play(Write(multiplication), run_time=2)
        self.wait(0.5)
        
        self.play(
            Write(equals_result),
            Flash(equals_result, color=VIBRANT_ORANGE, line_length=0.3),
            run_time=1.2
        )
        
        self.wait(0.8)
        
        # Show compact 5! notation on the right side
        notation = MathTex(r"5! = 120", font_size=48, color=VIBRANT_ORANGE)
        notation.move_to(RIGHT * 4 + DOWN * 0.3)
        
        box = SurroundingRectangle(notation, color=VIBRANT_ORANGE, buff=0.15, stroke_width=2)
        
        arrow = Arrow(
            start=equals_result.get_right() + RIGHT * 0.3,
            end=notation.get_left() + LEFT * 0.3,
            color=VIBRANT_ORANGE,
            stroke_width=3,
            buff=0.1
        )
        
        self.play(
            Create(arrow),
            Write(notation),
            Create(box),
            run_time=1.5
        )
        
        self.wait(1)
        
        # Growth indication - clear at the bottom
        growth_box = Rectangle(
            width=10, height=0.9,
            color=NEON_PINK,
            fill_opacity=0.1,
            stroke_width=2
        )
        growth_box.move_to(DOWN * 2.5)
        
        growth_text = Text(
            "Factorial grows EXTREMELY fast!",
            font_size=30,
            color=NEON_PINK
        )
        growth_text.move_to(growth_box.get_center())
        
        self.play(
            Create(growth_box),
            Write(growth_text),
            run_time=1.5
        )
        
        # Add emphasis animation
        self.play(
            growth_box.animate.scale(1.05),
            growth_text.animate.scale(1.05),
            rate_func=there_and_back,
            run_time=0.8
        )
        
        self.wait(2)


# ============================================================================
# PART 4: UNDERSTANDING THE N-TH ROOT (15-20 seconds)
# ============================================================================
class Part4(Scene):
    """Explain the n-th root concept with examples"""
    
    def construct(self):
        # Header
        header = Text("The n-th Root", font_size=48, color=ELECTRIC_CYAN)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        # Definition - positioned higher
        definition = MathTex(
            r"\sqrt[n]{x} = x^{\frac{1}{n}}",
            font_size=60,
            color=TEXT_WHITE
        )
        definition.move_to(UP * 2)
        
        # Add glow box around definition
        def_box = SurroundingRectangle(definition, color=ELECTRIC_CYAN, buff=0.2, stroke_width=2)
        
        self.play(Write(definition), Create(def_box), run_time=2)
        self.wait(0.8)
        
        # Examples - arranged in a 2-column grid layout
        examples_header = Text("Examples:", font_size=32, color=VIBRANT_ORANGE)
        examples_header.move_to(UP * 0.6 + LEFT * 4.5)
        
        self.play(FadeIn(examples_header), run_time=0.5)
        
        # Left column examples
        example1 = MathTex(
            r"\sqrt[2]{16} = 4",
            font_size=40,
            color=ELECTRIC_CYAN
        )
        example1.move_to(LEFT * 3 + UP * 0)
        
        example2 = MathTex(
            r"\sqrt[3]{27} = 3",
            font_size=40,
            color=ELECTRIC_CYAN
        )
        example2.move_to(LEFT * 3 + DOWN * 0.8)
        
        # Right column examples
        example3 = MathTex(
            r"\sqrt[4]{81} = 3",
            font_size=40,
            color=ELECTRIC_CYAN
        )
        example3.move_to(RIGHT * 3 + UP * 0)
        
        example4 = MathTex(
            r"\sqrt[5]{32} = 2",
            font_size=40,
            color=ELECTRIC_CYAN
        )
        example4.move_to(RIGHT * 3 + DOWN * 0.8)
        
        # Animate examples appearing in pairs
        self.play(
            Write(example1),
            Write(example3),
            run_time=1.5
        )
        self.wait(0.8)
        
        self.play(
            Write(example2),
            Write(example4),
            run_time=1.5
        )
        self.wait(0.8)
        
        # Key insight at the bottom - clear of all examples
        insight_box = Rectangle(
            width=9, height=1,
            color=VIBRANT_ORANGE,
            fill_opacity=0.15,
            stroke_width=3
        )
        insight_box.move_to(DOWN * 2.5)
        
        insight_text = Text(
            "Higher roots make large numbers smaller!",
            font_size=30,
            color=VIBRANT_ORANGE
        )
        insight_text.move_to(insight_box.get_center())
        
        self.play(
            Create(insight_box),
            Write(insight_text),
            run_time=1.5
        )
        
        # Pulse effect on insight
        self.play(
            insight_box.animate.scale(1.05),
            rate_func=there_and_back,
            run_time=0.8
        )
        
        self.wait(2.5)


# ============================================================================
# PART 5: INITIAL EXPLORATION (15-20 seconds)
# ============================================================================
class Part5(Scene):
    """Try computing for small n values"""
    
    def construct(self):
        # Header
        header = Text("Let's Explore Small Values", font_size=44, color=ELECTRIC_CYAN)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        # Formula reminder
        formula = MathTex(
            r"a_n = \frac{\sqrt[n]{n!}}{n}",
            font_size=48,
            color=TEXT_WHITE
        )
        formula.move_to(UP * 1.8)
        self.play(Write(formula), run_time=1.5)
        
        # Create table
        table_data = [
            ("n", "n!", "\\sqrt[n]{n!}", "a_n"),
            ("1", "1", "1", "1.000"),
            ("2", "2", "1.41", "0.707"),
            ("3", "6", "1.82", "0.606"),
            ("4", "24", "2.21", "0.553"),
            ("5", "120", "2.61", "0.522"),
            ("10", "3628800", "4.53", "0.453"),
        ]
        
        # Build table manually for better control
        rows = []
        start_y = 0.8
        
        for i, row in enumerate(table_data):
            row_mobjects = []
            for j, item in enumerate(row):
                if i == 0:
                    # Header row
                    cell = MathTex(item, font_size=32, color=VIBRANT_ORANGE)
                else:
                    color = ELECTRIC_CYAN if j == 3 else TEXT_WHITE
                    cell = MathTex(item, font_size=28, color=color)
                
                x_pos = -4.5 + j * 2.5
                y_pos = start_y - i * 0.6
                cell.move_to([x_pos, y_pos, 0])
                row_mobjects.append(cell)
            rows.append(row_mobjects)
        
        # Animate table
        # Show header
        for cell in rows[0]:
            self.play(FadeIn(cell), run_time=0.3)
        
        self.wait(0.5)
        
        # Show data rows with animation
        for row in rows[1:]:
            for cell in row:
                self.play(FadeIn(cell, shift=UP * 0.2), run_time=0.2)
            self.wait(0.3)
        
        # Draw trend arrow
        arrow = Arrow(
            start=[3.5, 0.2, 0],
            end=[3.5, -2.2, 0],
            color=NEON_PINK,
            stroke_width=3
        )
        trend_label = Text("Decreasing!", font_size=28, color=NEON_PINK)
        trend_label.next_to(arrow, RIGHT, buff=0.2)
        
        self.play(
            Create(arrow),
            Write(trend_label),
            run_time=1.5
        )
        
        # Question
        question = Text(
            "Does it approach a specific value?",
            font_size=36,
            color=VIBRANT_ORANGE
        )
        question.to_edge(DOWN, buff=0.5)
        
        self.play(Write(question), run_time=1.5)
        self.wait(3)


# ============================================================================
# PART 6: INTRODUCING STIRLING (15-20 seconds)
# ============================================================================
class Part6(Scene):
    """Introduce Stirling's approximation"""
    
    def construct(self):
        # Need a powerful tool
        intro_text = Text(
            "We need a powerful mathematical tool...",
            font_size=40,
            color=TEXT_WHITE
        )
        intro_text.move_to(UP * 2)
        
        self.play(Write(intro_text), run_time=2)
        self.wait(1)
        
        # Stirling's name appears dramatically
        name = Text("STIRLING'S", font_size=72, color=ELECTRIC_CYAN, weight=BOLD)
        subtitle = Text("APPROXIMATION", font_size=56, color=VIBRANT_ORANGE)
        subtitle.next_to(name, DOWN, buff=0.3)
        
        name_group = VGroup(name, subtitle)
        name_group.move_to(ORIGIN)
        
        self.play(
            FadeOut(intro_text),
            run_time=0.5
        )
        
        self.play(
            FadeIn(name, scale=1.5),
            run_time=1
        )
        self.play(
            FadeIn(subtitle, shift=UP * 0.3),
            Flash(name_group, color=ELECTRIC_CYAN, line_length=0.5),
            run_time=1
        )
        
        self.wait(1)
        
        # Historical note
        history = Text(
            "James Stirling (1692-1770)",
            font_size=32,
            color=SUBTLE_NAVY
        ).set_color(TEXT_WHITE).set_opacity(0.7)
        history.to_edge(DOWN, buff=2)
        
        self.play(FadeIn(history), run_time=1)
        
        # Why it's useful
        use_text = Text(
            "Approximates n! for large n",
            font_size=36,
            color=NEON_PINK
        )
        use_text.to_edge(DOWN, buff=0.8)
        
        self.play(
            name_group.animate.shift(UP * 1),
            FadeIn(use_text, shift=UP),
            run_time=1.5
        )
        
        self.wait(3)
        
        # Teaser of the formula
        teaser = MathTex(
            r"n! \approx \sqrt{2\pi n} \left(\frac{n}{e}\right)^n",
            font_size=52,
            color=TEXT_WHITE
        )
        teaser.move_to(DOWN * 0.5)
        
        self.play(
            FadeIn(teaser, scale=0.8),
            run_time=2
        )
        
        self.wait(3)


# ============================================================================
# PART 7: STIRLING'S FORMULA (15-20 seconds)
# ============================================================================
class Part7(Scene):
    """Display Stirling's formula in detail"""
    
    def construct(self):
        # Header
        header = Text("Stirling's Approximation", font_size=44, color=ELECTRIC_CYAN)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        # Main formula - positioned higher
        formula = MathTex(
            r"n!", r"\approx", r"\sqrt{2\pi n}", r"\left(\frac{n}{e}\right)^n",
            font_size=60
        )
        formula[0].set_color(NEON_PINK)
        formula[1].set_color(TEXT_WHITE)
        formula[2].set_color(ELECTRIC_CYAN)
        formula[3].set_color(VIBRANT_ORANGE)
        
        formula.move_to(UP * 1.5)
        
        # Add surrounding box
        formula_box = SurroundingRectangle(formula, color=TEXT_WHITE, buff=0.25, stroke_width=1)
        
        self.play(Write(formula[0]), run_time=1)
        self.play(Write(formula[1]), run_time=0.5)
        self.play(Write(formula[2]), run_time=1.5)
        self.play(Write(formula[3]), run_time=1.5)
        self.play(Create(formula_box), run_time=0.5)
        
        self.wait(0.8)
        
        # Annotations positioned on the SIDES, not overlapping below
        # Left annotation for sqrt term
        left_label = Text("Correction\nfactor", font_size=24, color=ELECTRIC_CYAN)
        left_label.move_to(LEFT * 5 + DOWN * 0.3)
        
        left_arrow = Arrow(
            start=left_label.get_right(),
            end=formula[2].get_left() + LEFT * 0.1,
            color=ELECTRIC_CYAN,
            stroke_width=3,
            buff=0.2
        )
        
        self.play(
            Write(left_label),
            Create(left_arrow),
            run_time=1.2
        )
        self.wait(0.8)
        
        # Right annotation for main term
        right_label = Text("Main growth\nterm", font_size=24, color=VIBRANT_ORANGE)
        right_label.move_to(RIGHT * 5 + DOWN * 0.3)
        
        right_arrow = Arrow(
            start=right_label.get_left(),
            end=formula[3].get_right() + RIGHT * 0.1,
            color=VIBRANT_ORANGE,
            stroke_width=3,
            buff=0.2
        )
        
        self.play(
            Write(right_label),
            Create(right_arrow),
            run_time=1.2
        )
        self.wait(0.8)
        
        # Key insight about e - in a clear bottom section
        e_section = VGroup()
        
        e_note = MathTex(
            r"e \approx 2.71828...",
            font_size=44,
            color=VIBRANT_ORANGE
        )
        e_note.move_to(DOWN * 1.5)
        
        e_box = SurroundingRectangle(e_note, color=VIBRANT_ORANGE, buff=0.15, stroke_width=2)
        
        self.play(
            Write(e_note),
            Create(e_box),
            run_time=1.5
        )
        
        self.wait(0.8)
        
        # Accuracy note at the very bottom
        accuracy = Text(
            "Becomes more accurate as n → ∞",
            font_size=26,
            color=TEXT_WHITE
        ).set_opacity(0.9)
        accuracy.move_to(DOWN * 2.8)
        
        self.play(FadeIn(accuracy), run_time=1)
        
        self.wait(2.5)


# ============================================================================
# PART 8: SUBSTITUTION (15-20 seconds)
# ============================================================================
class Part8(Scene):
    """Replace n! with Stirling approximation in the limit"""
    
    def construct(self):
        # Header
        header = Text("Substituting Stirling's Formula", font_size=44, color=ELECTRIC_CYAN)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        # Original limit
        original = MathTex(
            r"\lim_{n \to \infty} \frac{\sqrt[n]{n!}}{n}",
            font_size=52,
            color=TEXT_WHITE
        )
        original.move_to(UP * 1.5)
        
        self.play(Write(original), run_time=2)
        self.wait(1)
        
        # Arrow and substitution step
        arrow1 = MathTex(r"\downarrow", font_size=48, color=NEON_PINK)
        arrow1.move_to(UP * 0.5)
        
        step_label = Text("Replace n! with Stirling's", font_size=28, color=NEON_PINK)
        step_label.next_to(arrow1, RIGHT, buff=0.3)
        
        self.play(
            FadeIn(arrow1),
            Write(step_label),
            run_time=1
        )
        
        # Substituted formula
        substituted = MathTex(
            r"\lim_{n \to \infty} \frac{\sqrt[n]{\sqrt{2\pi n} \left(\frac{n}{e}\right)^n}}{n}",
            font_size=44,
            color=TEXT_WHITE
        )
        substituted.move_to(DOWN * 0.8)
        
        self.play(Write(substituted), run_time=3)
        self.wait(1)
        
        # Highlight the key insight
        insight = Text(
            "Now we can simplify the n-th root!",
            font_size=32,
            color=VIBRANT_ORANGE
        )
        insight.to_edge(DOWN, buff=1)
        
        self.play(
            Write(insight),
            Flash(substituted, color=ELECTRIC_CYAN, line_length=0.3),
            run_time=1.5
        )
        
        self.wait(4)


# ============================================================================
# PART 9: SPLIT THE N-TH ROOT (15-20 seconds)
# ============================================================================
class Part9(Scene):
    """Show property: (AB)^(1/n) = A^(1/n) × B^(1/n)"""
    
    def construct(self):
        # Header
        header = Text("Splitting the Root", font_size=44, color=ELECTRIC_CYAN)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        # Property
        property_text = MathTex(
            r"\sqrt[n]{A \cdot B} = \sqrt[n]{A} \cdot \sqrt[n]{B}",
            font_size=52,
            color=VIBRANT_ORANGE
        )
        property_text.move_to(UP * 1.5)
        
        box = SurroundingRectangle(property_text, color=VIBRANT_ORANGE, buff=0.2)
        
        self.play(
            Write(property_text),
            Create(box),
            run_time=2
        )
        self.wait(1)
        
        # Apply to our expression
        before = MathTex(
            r"\sqrt[n]{\sqrt{2\pi n} \cdot \left(\frac{n}{e}\right)^n}",
            font_size=44,
            color=TEXT_WHITE
        )
        before.move_to(UP * 0.2)
        
        self.play(Write(before), run_time=2)
        
        # Arrow
        arrow = MathTex(r"\downarrow", font_size=48, color=NEON_PINK)
        arrow.move_to(DOWN * 0.5)
        
        self.play(FadeIn(arrow), run_time=0.5)
        
        # Split result
        after = MathTex(
            r"\sqrt[n]{\sqrt{2\pi n}}", r"\cdot", r"\sqrt[n]{\left(\frac{n}{e}\right)^n}",
            font_size=44
        )
        after[0].set_color(ELECTRIC_CYAN)
        after[1].set_color(TEXT_WHITE)
        after[2].set_color(VIBRANT_ORANGE)
        after.move_to(DOWN * 1.3)
        
        self.play(Write(after), run_time=2)
        self.wait(1)
        
        # Labels
        label1 = Text("Part A", font_size=24, color=ELECTRIC_CYAN)
        label1.next_to(after[0], DOWN, buff=0.3)
        
        label2 = Text("Part B", font_size=24, color=VIBRANT_ORANGE)
        label2.next_to(after[2], DOWN, buff=0.3)
        
        self.play(
            FadeIn(label1),
            FadeIn(label2),
            run_time=1
        )
        
        self.wait(4)


# ============================================================================
# PART 10: SIMPLIFY PART A (15-20 seconds)
# ============================================================================
class Part10(Scene):
    """Show sqrt(2πn)^(1/n) → 1 as n → ∞"""
    
    def construct(self):
        # Header
        header = Text("Simplifying Part A", font_size=44, color=ELECTRIC_CYAN)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        # Part A
        part_a = MathTex(
            r"\sqrt[n]{\sqrt{2\pi n}} = (2\pi n)^{\frac{1}{2n}}",
            font_size=48,
            color=ELECTRIC_CYAN
        )
        part_a.move_to(UP * 1.5)
        
        self.play(Write(part_a), run_time=2)
        self.wait(1)
        
        # Key insight
        insight = MathTex(
            r"\text{As } n \to \infty, \quad \frac{1}{2n} \to 0",
            font_size=44,
            color=VIBRANT_ORANGE
        )
        insight.move_to(UP * 0.3)
        
        self.play(Write(insight), run_time=1.5)
        self.wait(1)
        
        # Therefore
        therefore = MathTex(
            r"\therefore \quad (2\pi n)^{\frac{1}{2n}} \to 1",
            font_size=52,
            color=NEON_PINK
        )
        therefore.move_to(DOWN * 0.8)
        
        self.play(
            Write(therefore),
            Flash(therefore, color=NEON_PINK),
            run_time=2
        )
        
        self.wait(1)
        
        # Visual: create a simple graph
        axes = Axes(
            x_range=[0, 50, 10],
            y_range=[0, 2, 0.5],
            x_length=6,
            y_length=2.5,
            axis_config={"color": SUBTLE_NAVY},
            tips=False
        )
        axes.to_edge(DOWN, buff=0.8)
        
        # Function
        def func(n):
            if n <= 0:
                return 2
            return (2 * np.pi * n) ** (1 / (2 * n))
        
        graph = axes.plot(
            func,
            x_range=[1, 50],
            color=ELECTRIC_CYAN,
            stroke_width=3
        )
        
        # Asymptote at y=1
        asymptote = DashedLine(
            axes.c2p(0, 1),
            axes.c2p(50, 1),
            color=VIBRANT_ORANGE,
            stroke_width=2
        )
        
        label_one = MathTex(r"1", font_size=28, color=VIBRANT_ORANGE)
        label_one.next_to(axes.c2p(0, 1), LEFT, buff=0.2)
        
        self.play(Create(axes), run_time=1)
        self.play(
            Create(graph),
            Create(asymptote),
            Write(label_one),
            run_time=2
        )
        
        self.wait(3)


# ============================================================================
# PART 11: SIMPLIFY PART B (15-20 seconds)
# ============================================================================
class Part11(Scene):
    """Show ((n/e)^n)^(1/n) = n/e"""
    
    def construct(self):
        # Header
        header = Text("Simplifying Part B", font_size=44, color=VIBRANT_ORANGE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        # Part B - on the LEFT side
        part_b = MathTex(
            r"\sqrt[n]{\left(\frac{n}{e}\right)^n}",
            font_size=52,
            color=VIBRANT_ORANGE
        )
        part_b.move_to(LEFT * 4 + UP * 1)
        
        part_b_box = SurroundingRectangle(part_b, color=VIBRANT_ORANGE, buff=0.15, stroke_width=2)
        
        self.play(Write(part_b), Create(part_b_box), run_time=2)
        self.wait(0.8)
        
        # Property to use - CENTER TOP
        property_label = Text("Key Property:", font_size=28, color=ELECTRIC_CYAN)
        property_label.move_to(RIGHT * 2 + UP * 1.8)
        
        property_text = MathTex(
            r"\sqrt[n]{x^n} = x",
            font_size=48,
            color=ELECTRIC_CYAN
        )
        property_text.move_to(RIGHT * 2 + UP * 1)
        
        property_box = SurroundingRectangle(property_text, color=ELECTRIC_CYAN, buff=0.15, stroke_width=2)
        
        self.play(
            Write(property_label),
            Write(property_text),
            Create(property_box),
            run_time=1.5
        )
        self.wait(0.8)
        
        # Transformation arrow - horizontal
        transform_arrow = Arrow(
            start=LEFT * 1.5 + DOWN * 0.5,
            end=RIGHT * 1.5 + DOWN * 0.5,
            color=NEON_PINK,
            stroke_width=4,
            buff=0
        )
        
        apply_text = Text("Apply", font_size=24, color=NEON_PINK)
        apply_text.next_to(transform_arrow, UP, buff=0.1)
        
        self.play(
            Create(transform_arrow),
            Write(apply_text),
            run_time=1
        )
        self.wait(0.5)
        
        # Result - on the RIGHT side
        result = MathTex(
            r"= \frac{n}{e}",
            font_size=64,
            color=VIBRANT_ORANGE
        )
        result.move_to(RIGHT * 3.5 + DOWN * 0.5)
        
        result_box = SurroundingRectangle(result, color=VIBRANT_ORANGE, buff=0.2, stroke_width=3)
        
        self.play(
            Write(result),
            Create(result_box),
            Flash(result, color=VIBRANT_ORANGE, line_length=0.4),
            run_time=2
        )
        
        self.wait(1)
        
        # Final summary at the bottom - complete equation
        summary = MathTex(
            r"\sqrt[n]{\left(\frac{n}{e}\right)^n} = \frac{n}{e}",
            font_size=44,
            color=VIBRANT_ORANGE
        )
        summary.move_to(DOWN * 2.5)
        
        summary_box = SurroundingRectangle(summary, color=VIBRANT_ORANGE, buff=0.15, stroke_width=2)
        
        self.play(
            Write(summary),
            Create(summary_box),
            run_time=1.5
        )
        
        self.wait(2.5)


# ============================================================================
# PART 12: THE CANCELLATION (15-20 seconds)
# ============================================================================
class Part12(Scene):
    """Show (n/e) ÷ n = 1/e"""
    
    def construct(self):
        # Header
        header = Text("The Final Simplification", font_size=44, color=ELECTRIC_CYAN)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        # Show the complete derivation as a clean sequence
        # Step 1: Starting expression
        step1 = MathTex(
            r"\frac{\frac{n}{e}}{n}",
            font_size=64,
            color=TEXT_WHITE
        )
        step1.move_to(UP * 1.2)
        
        step1_label = Text("Starting with:", font_size=26, color=TEXT_WHITE)
        step1_label.next_to(step1, LEFT, buff=1)
        
        self.play(Write(step1_label), Write(step1), run_time=1.5)
        self.wait(1)
        
        # Step 2: Show equals and the simplified version
        equals1 = MathTex(r"=", font_size=64, color=TEXT_WHITE)
        equals1.next_to(step1, RIGHT, buff=0.5)
        
        step2 = MathTex(
            r"\frac{n}{e \cdot n}",
            font_size=64,
            color=ELECTRIC_CYAN
        )
        step2.next_to(equals1, RIGHT, buff=0.5)
        
        self.play(Write(equals1), Write(step2), run_time=1.5)
        self.wait(1)
        
        # Step 3: Show the cancellation with a brace and explanation
        cancel_text = Text("n cancels!", font_size=28, color=NEON_PINK)
        cancel_text.next_to(step2, DOWN, buff=0.8)
        
        # Draw a simple strikethrough over the whole fraction briefly
        strike = Line(
            step2.get_left() + LEFT * 0.1 + DOWN * 0.2,
            step2.get_right() + RIGHT * 0.1 + UP * 0.2,
            color=NEON_PINK,
            stroke_width=4
        )
        
        self.play(
            Write(cancel_text),
            Create(strike),
            run_time=1
        )
        self.wait(0.8)
        
        # Fade out everything and show clean result
        self.play(
            FadeOut(step1_label),
            FadeOut(step1),
            FadeOut(equals1),
            FadeOut(step2),
            FadeOut(strike),
            FadeOut(cancel_text),
            run_time=0.8
        )
        
        # Final clean result
        final_eq = MathTex(
            r"\lim_{n \to \infty} \frac{\sqrt[n]{n!}}{n} = \frac{1}{e}",
            font_size=52,
            color=VIBRANT_ORANGE
        )
        final_eq.move_to(UP * 0.5)
        
        result_box = SurroundingRectangle(final_eq, color=VIBRANT_ORANGE, buff=0.25, stroke_width=3)
        
        self.play(
            Write(final_eq),
            Create(result_box),
            run_time=2
        )
        
        # Emphasize the answer
        answer = MathTex(
            r"\frac{1}{e}",
            font_size=100,
            color=VIBRANT_ORANGE
        )
        answer.move_to(DOWN * 1.8)
        
        answer_box = SurroundingRectangle(answer, color=VIBRANT_ORANGE, buff=0.3, stroke_width=4)
        
        self.play(
            Write(answer),
            Create(answer_box),
            run_time=1.5
        )
        
        self.play(
            Flash(answer, color=VIBRANT_ORANGE, line_length=0.6, num_lines=20),
            run_time=1.5
        )
        
        self.wait(2)


# ============================================================================
# PART 13: THE ANSWER REVEALED (15-20 seconds)
# ============================================================================
class Part13(Scene):
    """Celebrate the answer 1/e with visual effects"""
    
    def construct(self):
        # Grand reveal
        result_text = Text("THE ANSWER", font_size=56, color=ELECTRIC_CYAN)
        result_text.to_edge(UP, buff=1)
        
        self.play(Write(result_text), run_time=1)
        
        # Main formula
        formula = MathTex(
            r"\lim_{n \to \infty} \frac{\sqrt[n]{n!}}{n} = \frac{1}{e}",
            font_size=64,
            color=TEXT_WHITE
        )
        formula.move_to(UP * 0.5)
        
        self.play(Write(formula), run_time=2)
        
        # Highlight the answer
        answer_box = SurroundingRectangle(
            formula[0][-3:],  # 1/e part
            color=VIBRANT_ORANGE,
            buff=0.2,
            stroke_width=4
        )
        
        self.play(
            Create(answer_box),
            Flash(formula, color=VIBRANT_ORANGE, line_length=0.4),
            run_time=1.5
        )
        
        self.wait(1)
        
        # Numerical value
        numerical = MathTex(
            r"\frac{1}{e} \approx 0.3679",
            font_size=56,
            color=VIBRANT_ORANGE
        )
        numerical.move_to(DOWN * 1)
        
        self.play(Write(numerical), run_time=2)
        
        # Add celebratory dots (simple confetti effect)
        dots = VGroup()
        for _ in range(30):
            dot = Dot(
                point=[
                    np.random.uniform(-6, 6),
                    np.random.uniform(-3, 3),
                    0
                ],
                radius=0.05,
                color=np.random.choice([ELECTRIC_CYAN, NEON_PINK, VIBRANT_ORANGE])
            )
            dots.add(dot)
        
        self.play(
            LaggedStartMap(FadeIn, dots, lag_ratio=0.05),
            run_time=2
        )
        
        # Victory text
        victory = Text(
            "Harvard Challenge: SOLVED! ✓",
            font_size=40,
            color=ELECTRIC_CYAN
        )
        victory.to_edge(DOWN, buff=1)
        
        self.play(
            Write(victory),
            run_time=1.5
        )
        
        self.wait(3)


# ============================================================================
# PART 14: GRAPH VERIFICATION (15-20 seconds)
# ============================================================================
class Part14(Scene):
    """Plot the sequence converging to 1/e"""
    
    def construct(self):
        # Header
        header = Text("Visual Verification", font_size=44, color=ELECTRIC_CYAN)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        # Create axes
        axes = Axes(
            x_range=[0, 25, 5],
            y_range=[0, 1.2, 0.2],
            x_length=10,
            y_length=5,
            axis_config={
                "color": SUBTLE_NAVY,
                "include_numbers": True,
                "font_size": 24
            },
            tips=False
        )
        axes.move_to(DOWN * 0.3)
        
        x_label = MathTex(r"n", font_size=32, color=TEXT_WHITE)
        x_label.next_to(axes.x_axis, RIGHT, buff=0.2)
        
        y_label = MathTex(r"a_n", font_size=32, color=TEXT_WHITE)
        y_label.next_to(axes.y_axis, UP, buff=0.2)
        
        self.play(
            Create(axes),
            Write(x_label),
            Write(y_label),
            run_time=2
        )
        
        # Calculate sequence values
        import math
        def a_n(n):
            if n <= 0:
                return 1
            factorial = math.factorial(int(n))
            return (factorial ** (1/n)) / n
        
        # Plot points
        points = VGroup()
        x_values = list(range(1, 21))
        
        for n in x_values:
            value = a_n(n)
            point = Dot(
                axes.c2p(n, value),
                radius=0.08,
                color=ELECTRIC_CYAN
            )
            points.add(point)
        
        self.play(
            LaggedStartMap(FadeIn, points, lag_ratio=0.1),
            run_time=3
        )
        
        # 1/e asymptote
        one_over_e = 1 / np.e
        asymptote = DashedLine(
            axes.c2p(0, one_over_e),
            axes.c2p(25, one_over_e),
            color=VIBRANT_ORANGE,
            stroke_width=3
        )
        
        asymptote_label = MathTex(
            r"y = \frac{1}{e} \approx 0.368",
            font_size=28,
            color=VIBRANT_ORANGE
        )
        asymptote_label.next_to(asymptote, RIGHT, buff=0.2)
        asymptote_label.shift(LEFT * 3 + DOWN * 0.3)
        
        self.play(
            Create(asymptote),
            Write(asymptote_label),
            run_time=2
        )
        
        # Annotation
        annotation = Text(
            "Points approach 1/e as n increases!",
            font_size=28,
            color=NEON_PINK
        )
        annotation.to_edge(DOWN, buff=0.3)
        
        self.play(Write(annotation), run_time=1.5)
        
        self.wait(4)


# ============================================================================
# PART 15: NUMERICAL CHECK (15-20 seconds)
# ============================================================================
class Part15(Scene):
    """Table of values showing convergence"""
    
    def construct(self):
        # Header
        header = Text("Numerical Verification", font_size=44, color=ELECTRIC_CYAN)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        # Target value
        target = MathTex(
            r"\frac{1}{e} = 0.367879441...",
            font_size=44,
            color=VIBRANT_ORANGE
        )
        target.move_to(UP * 1.5)
        
        self.play(Write(target), run_time=1.5)
        
        # Calculate actual values using log to avoid overflow
        import math
        def a_n(n):
            # Use Stirling's approximation via log: log(n!) ≈ n*log(n) - n + 0.5*log(2*pi*n)
            # Then: (n!)^(1/n) / n = exp(log(n!)/n) / n
            if n <= 20:
                # For small n, use direct calculation
                factorial = math.factorial(n)
                return (factorial ** (1/n)) / n
            else:
                # For large n, use log approach: log(n!) = sum(log(k) for k in 1..n)
                log_factorial = sum(math.log(k) for k in range(1, n + 1))
                return math.exp(log_factorial / n) / n
        
        # Create data rows
        data = [
            (10, a_n(10)),
            (50, a_n(50)),
            (100, a_n(100)),
            (500, a_n(500)),
        ]
        
        # Build table
        table_header = MathTex(
            r"n", r"\quad", r"a_n = \frac{\sqrt[n]{n!}}{n}",
            font_size=36,
            color=ELECTRIC_CYAN
        )
        table_header.move_to(UP * 0.5)
        
        self.play(Write(table_header), run_time=1)
        
        # Add rows with calculator-style animation
        rows = []
        start_y = -0.2
        
        for i, (n, val) in enumerate(data):
            n_text = MathTex(str(n), font_size=36, color=TEXT_WHITE)
            n_text.move_to([-2, start_y - i * 0.7, 0])
            
            val_text = MathTex(f"{val:.10f}...", font_size=32, color=ELECTRIC_CYAN)
            val_text.move_to([2, start_y - i * 0.7, 0])
            
            rows.append((n_text, val_text))
        
        for n_text, val_text in rows:
            self.play(
                FadeIn(n_text),
                run_time=0.3
            )
            # Calculator effect - show digits appearing
            self.play(
                Write(val_text),
                run_time=1
            )
            self.wait(0.5)
        
        # Highlight convergence
        arrow = Arrow(
            start=[4, 0.5, 0],
            end=[4, -2.5, 0],
            color=NEON_PINK,
            stroke_width=3
        )
        
        converge_text = MathTex(
            r"\to 0.3678...",
            font_size=32,
            color=NEON_PINK
        )
        converge_text.next_to(arrow, RIGHT, buff=0.2)
        
        self.play(
            Create(arrow),
            Write(converge_text),
            run_time=1.5
        )
        
        self.wait(3)


# ============================================================================
# PART 16: EULER'S NUMBER SPOTLIGHT (15-20 seconds)
# ============================================================================
class Part16(Scene):
    """Explain e = 2.71828..."""
    
    def construct(self):
        # Header
        header = Text("Euler's Number", font_size=48, color=ELECTRIC_CYAN)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        # Big e with value - centered
        big_e = MathTex(r"e", font_size=160, color=VIBRANT_ORANGE)
        value = MathTex(
            r"= 2.71828182845...",
            font_size=44,
            color=TEXT_WHITE
        )
        
        e_group = VGroup(big_e, value).arrange(RIGHT, buff=0.4)
        e_group.move_to(UP * 0.5)
        
        self.play(
            FadeIn(big_e, scale=0.5),
            run_time=1.2
        )
        self.play(Write(value), run_time=1.5)
        self.wait(0.8)
        
        # Fade out e group to show definitions
        self.play(
            e_group.animate.scale(0.6).move_to(UP * 2.3 + LEFT * 3),
            run_time=0.8
        )
        
        # Definitions - now have full screen
        def1 = MathTex(r"e = \lim_{n \to \infty} \left(1 + \frac{1}{n}\right)^n", font_size=38, color=ELECTRIC_CYAN)
        def2 = MathTex(r"e = \sum_{n=0}^{\infty} \frac{1}{n!}", font_size=38, color=NEON_PINK)
        def3 = MathTex(r"\frac{d}{dx} e^x = e^x", font_size=38, color=VIBRANT_ORANGE)
        
        definitions = VGroup(def1, def2, def3)
        definitions.arrange(DOWN, buff=0.6, aligned_edge=LEFT)
        definitions.move_to(DOWN * 0.3)
        
        for defn in definitions:
            self.play(FadeIn(defn, shift=RIGHT * 0.2), run_time=0.8)
            self.wait(0.4)
        
        # Why it appears here
        explanation = Text(
            "e naturally appears in growth and factorial problems!",
            font_size=26,
            color=TEXT_WHITE
        )
        explanation.to_edge(DOWN, buff=0.5)
        
        self.play(Write(explanation), run_time=1.5)
        
        self.wait(2)


# ============================================================================
# PART 17: WHY THIS MATTERS (15-20 seconds)
# ============================================================================
class Part17(Scene):
    """Applications and significance"""
    
    def construct(self):
        # Header
        header = Text("Why This Matters", font_size=48, color=ELECTRIC_CYAN)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        # Application areas
        apps = VGroup(
            VGroup(
                Text("📊 Probability", font_size=36, color=VIBRANT_ORANGE),
                Text("Stirling's approx in statistics", font_size=24, color=TEXT_WHITE)
            ).arrange(DOWN, buff=0.2),
            
            VGroup(
                Text("🔢 Combinatorics", font_size=36, color=NEON_PINK),
                Text("Counting large arrangements", font_size=24, color=TEXT_WHITE)
            ).arrange(DOWN, buff=0.2),
            
            VGroup(
                Text("📈 Asymptotic Analysis", font_size=36, color=ELECTRIC_CYAN),
                Text("Algorithm complexity", font_size=24, color=TEXT_WHITE)
            ).arrange(DOWN, buff=0.2),
        )
        
        apps.arrange(DOWN, buff=0.8, aligned_edge=LEFT)
        apps.move_to(LEFT * 2)
        
        for app in apps:
            self.play(FadeIn(app, shift=RIGHT * 0.5), run_time=1)
            self.wait(0.5)
        
        # Connection illustration
        connection = Text(
            "This limit connects factorials to e!",
            font_size=32,
            color=VIBRANT_ORANGE
        )
        connection.to_edge(DOWN, buff=1)
        
        # Formula reminder
        formula = MathTex(
            r"n! \sim \sqrt{2\pi n} \left(\frac{n}{e}\right)^n",
            font_size=40,
            color=TEXT_WHITE
        )
        formula.move_to(RIGHT * 2.5)
        
        self.play(
            Write(formula),
            Write(connection),
            run_time=2
        )
        
        self.wait(4)


# ============================================================================
# PART 18: ALTERNATIVE APPROACH (15-20 seconds)
# ============================================================================
class Part18(Scene):
    """Mention logarithm approach briefly"""
    
    def construct(self):
        # Header
        header = Text("Alternative Approach", font_size=44, color=ELECTRIC_CYAN)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        # Idea - positioned higher
        idea = Text(
            "We could also use logarithms:",
            font_size=32,
            color=TEXT_WHITE
        )
        idea.move_to(UP * 2)
        
        self.play(Write(idea), run_time=1)
        self.wait(0.5)
        
        # Step 1: Take log of both sides
        step1 = MathTex(
            r"\ln(a_n) = \ln\left(\frac{\sqrt[n]{n!}}{n}\right)",
            font_size=40,
            color=TEXT_WHITE
        )
        step1.move_to(UP * 0.8)
        
        self.play(Write(step1), run_time=1.5)
        self.wait(1)
        
        # Step 2: Expand - show then fade step1
        step2 = MathTex(
            r"= \frac{1}{n} \ln(n!) - \ln(n)",
            font_size=40,
            color=ELECTRIC_CYAN
        )
        step2.move_to(DOWN * 0.2)
        
        self.play(Write(step2), run_time=1.5)
        self.wait(0.8)
        
        # Fade out previous steps to make room
        self.play(
            FadeOut(idea),
            FadeOut(step1),
            step2.animate.move_to(UP * 1.5),
            run_time=0.8
        )
        
        # Step 3: Use sum formula
        step3 = MathTex(
            r"= \frac{1}{n} \sum_{k=1}^{n} \ln(k) - \ln(n)",
            font_size=42,
            color=VIBRANT_ORANGE
        )
        step3.move_to(UP * 0.3)
        
        self.play(Write(step3), run_time=1.5)
        self.wait(1)
        
        # Conclusion box
        conclusion_box = Rectangle(
            width=9, height=0.9,
            color=NEON_PINK,
            fill_opacity=0.1,
            stroke_width=2
        )
        conclusion_box.move_to(DOWN * 1)
        
        conclusion = Text(
            "This sum → -1 using integral approximation",
            font_size=28,
            color=NEON_PINK
        )
        conclusion.move_to(conclusion_box.get_center())
        
        self.play(
            Create(conclusion_box),
            Write(conclusion),
            run_time=1.5
        )
        self.wait(1)
        
        # Final result - clear at bottom
        final = MathTex(
            r"\therefore \ln(a_n) \to -1 \Rightarrow a_n \to e^{-1} = \frac{1}{e}",
            font_size=38,
            color=VIBRANT_ORANGE
        )
        final.move_to(DOWN * 2.5)
        
        final_box = SurroundingRectangle(final, color=VIBRANT_ORANGE, buff=0.15, stroke_width=2)
        
        self.play(
            Write(final),
            Create(final_box),
            run_time=2
        )
        
        self.wait(2.5)


# ============================================================================
# PART 19: SUMMARY (15-20 seconds)
# ============================================================================
class Part19(Scene):
    """Recap key steps with visual summary"""
    
    def construct(self):
        # Header
        header = Text("Summary", font_size=56, color=ELECTRIC_CYAN)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        # Steps with checkmarks - CENTERED on screen
        steps = VGroup(
            VGroup(
                MathTex(r"\checkmark", font_size=36, color=NEON_PINK),
                Text("Used Stirling's Approximation", font_size=26, color=TEXT_WHITE)
            ).arrange(RIGHT, buff=0.3),
            
            VGroup(
                MathTex(r"\checkmark", font_size=36, color=NEON_PINK),
                Text("Split the n-th root", font_size=26, color=TEXT_WHITE)
            ).arrange(RIGHT, buff=0.3),
            
            VGroup(
                MathTex(r"\checkmark", font_size=36, color=NEON_PINK),
                Text("Showed correction term → 1", font_size=26, color=TEXT_WHITE)
            ).arrange(RIGHT, buff=0.3),
            
            VGroup(
                MathTex(r"\checkmark", font_size=36, color=NEON_PINK),
                Text("Simplified (n/e)ⁿ under radical", font_size=26, color=TEXT_WHITE)
            ).arrange(RIGHT, buff=0.3),
            
            VGroup(
                MathTex(r"\checkmark", font_size=36, color=NEON_PINK),
                Text("Cancelled n terms", font_size=26, color=TEXT_WHITE)
            ).arrange(RIGHT, buff=0.3),
        )
        
        steps.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        steps.move_to(ORIGIN)  # Center the steps
        
        for step in steps:
            self.play(FadeIn(step, shift=RIGHT * 0.3), run_time=0.6)
            self.wait(0.3)
        
        self.wait(1)
        
        # Fade out steps to show final answer
        self.play(
            FadeOut(steps),
            run_time=0.8
        )
        
        # Final answer - large and centered
        result_label = Text("Final Answer:", font_size=36, color=TEXT_WHITE)
        result_label.move_to(UP * 1.6)
        
        answer = MathTex(
            r"\frac{1}{e}",
            font_size=120,
            color=VIBRANT_ORANGE
        )
        answer.move_to(DOWN * 0.5)
        
        answer_box = SurroundingRectangle(answer, color=VIBRANT_ORANGE, buff=0.35, stroke_width=4)
        
        approx = MathTex(
            r"\approx 0.368",
            font_size=40,
            color=TEXT_WHITE
        )
        approx.next_to(answer_box, DOWN, buff=0.4)
        
        self.play(
            Write(result_label),
            Write(answer),
            Create(answer_box),
            run_time=2
        )
        self.play(Write(approx), run_time=1)
        
        self.play(
            Flash(answer, color=VIBRANT_ORANGE, line_length=0.6, num_lines=20),
            run_time=1.5
        )
        
        self.wait(2.5)


# ============================================================================
# PART 20: OUTRO (15-20 seconds)
# ============================================================================
class Part20(Scene):
    """Final answer and closing"""
    
    def construct(self):
        # Final presentation
        problem = MathTex(
            r"\lim_{n \to \infty} \frac{\sqrt[n]{n!}}{n}",
            font_size=56,
            color=TEXT_WHITE
        )
        problem.move_to(UP * 2)
        
        self.play(Write(problem), run_time=2)
        
        # Equals with dramatic pause
        equals = MathTex(r"=", font_size=72, color=TEXT_WHITE)
        equals.move_to(UP * 0.5)
        
        self.play(FadeIn(equals, scale=1.5), run_time=1)
        self.wait(0.5)
        
        # Big answer reveal
        answer = MathTex(
            r"\frac{1}{e}",
            font_size=90,
            color=VIBRANT_ORANGE
        )
        answer.move_to(DOWN * 0.8)
        
        # Glow background
        glow = Circle(
            radius=2,
            color=VIBRANT_ORANGE,
            fill_opacity=0.1,
            stroke_width=0
        )
        glow.move_to(answer.get_center())
        
        self.play(
            FadeIn(glow),
            FadeIn(answer, scale=0.5),
            run_time=2
        )
        
        self.play(
            Flash(answer, color=VIBRANT_ORANGE, line_length=0.6, num_lines=20),
            glow.animate.scale(1.5).set_opacity(0),
            run_time=1.5
        )
        
        # Harvard badge text
        badge = Text(
            "HARVARD CHALLENGE: COMPLETE",
            font_size=36,
            color=ELECTRIC_CYAN
        )
        badge.to_edge(DOWN, buff=1.5)
        
        box = SurroundingRectangle(badge, color=ELECTRIC_CYAN, buff=0.2)
        
        self.play(
            Write(badge),
            Create(box),
            run_time=1.5
        )
        
        self.wait(1)
        
        # Subscribe CTA with subtle animation
        cta = Text(
            "Like & Subscribe for more math challenges!",
            font_size=28,
            color=NEON_PINK
        )
        cta.to_edge(DOWN, buff=0.5)
        
        self.play(
            FadeIn(cta, shift=UP * 0.2),
            run_time=1
        )
        
        # Gentle pulse on everything
        all_elements = VGroup(problem, equals, answer, badge, box, cta)
        
        self.play(
            all_elements.animate.scale(1.02),
            rate_func=there_and_back,
            run_time=2
        )
        
        self.wait(3)
