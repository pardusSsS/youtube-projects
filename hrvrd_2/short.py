from manim import *
import numpy as np

# ============================================================================
# INTEGRAL SOLUTION: ∫ 1/(x⁴ + x) dx
# 1-Minute YouTube Short
# ============================================================================

# Color Palette
DEEP_NAVY = "#020B1F"
ELECTRIC_CYAN = "#00F0FF"
NEON_PINK = "#FF0055"
VIBRANT_ORANGE = "#FF9F00"
TEXT_WHITE = "#FFFFFF"
SUBTLE_NAVY = "#1E2A45"
SOFT_GREEN = "#00E676"

# YouTube Shorts Configuration (9:16)
config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 14.0
config.frame_width = 14.0 * (1080 / 1920)
config.background_color = DEEP_NAVY


class IntegralShort(Scene):
    """Solve ∫ 1/(x⁴ + x) dx in 1 minute — YouTube Short"""

    def construct(self):
        # =================================================================
        # SECTION 1: HOOK — Show the problem (0-3s)
        # =================================================================
        hook_label = Text("Can you solve this?", font_size=36, color=NEON_PINK)
        hook_label.to_edge(UP, buff=1.0)

        integral = MathTex(
            r"\int \frac{1}{x^4 + x} \, dx",
            font_size=64, color=TEXT_WHITE
        ).move_to(UP * 1)

        timer = Text("in 1 minute.", font_size=30, color=ELECTRIC_CYAN)
        timer.next_to(integral, DOWN, buff=0.8)

        self.play(FadeIn(hook_label, shift=DOWN * 0.3), run_time=0.5)
        self.play(Write(integral), run_time=1.0)
        self.play(FadeIn(timer, shift=UP * 0.2), run_time=0.5)
        self.wait(0.8)

        self.play(
            FadeOut(hook_label), FadeOut(timer),
            integral.animate.scale(0.7).to_edge(UP, buff=0.6),
            run_time=0.6
        )

        # Keep integral at top as reference throughout
        top_integral = integral

        # Box around reference integral
        ref_box = SurroundingRectangle(top_integral, color=ELECTRIC_CYAN, buff=0.15, stroke_width=1.5)
        self.play(Create(ref_box), run_time=0.3)

        # =================================================================
        # SECTION 2: FACTOR THE DENOMINATOR (3-11s)
        # =================================================================
        step1_label = Text("Step 1: Factor", font_size=32, color=VIBRANT_ORANGE)
        step1_label.move_to(UP * 2)
        self.play(FadeIn(step1_label, shift=RIGHT * 0.3), run_time=0.5)

        factor1 = MathTex(
            r"x^4 + x", r"=", r"x(x^3 + 1)",
            font_size=44
        ).move_to(UP * 0.5)
        factor1[0].set_color(TEXT_WHITE)
        factor1[2].set_color(ELECTRIC_CYAN)
        self.play(Write(factor1), run_time=1.5)
        self.wait(0.8)

        factor2 = MathTex(
            r"= x(x+1)(x^2 - x + 1)",
            font_size=40, color=SOFT_GREEN
        ).next_to(factor1, DOWN, buff=0.5)
        self.play(Write(factor2), run_time=1.5)
        self.wait(0.5)

        # Highlight the full factorization
        factor2_box = SurroundingRectangle(factor2, color=SOFT_GREEN, buff=0.12, stroke_width=2)
        self.play(Create(factor2_box), run_time=0.4)
        self.wait(0.8)

        # Clean up
        self.play(
            FadeOut(step1_label), FadeOut(factor1),
            FadeOut(factor2_box),
            factor2.animate.scale(0.8).move_to(UP * 2),
            run_time=0.5
        )

        # =================================================================
        # SECTION 3: PARTIAL FRACTIONS SETUP (11-20s)
        # =================================================================
        step2_label = Text("Step 2: Partial Fractions", font_size=30, color=VIBRANT_ORANGE)
        step2_label.move_to(UP * 0.8)
        self.play(FadeIn(step2_label, shift=RIGHT * 0.3), run_time=0.5)

        pf_setup = MathTex(
            r"\frac{1}{x(x+1)(x^2-x+1)}",
            font_size=34, color=TEXT_WHITE
        ).move_to(DOWN * 0.2)
        self.play(Write(pf_setup), run_time=1.2)
        self.wait(0.5)

        pf_eq = MathTex(
            r"= \frac{A}{x} + \frac{B}{x+1} + \frac{Cx+D}{x^2-x+1}",
            font_size=32, color=ELECTRIC_CYAN
        ).next_to(pf_setup, DOWN, buff=0.5)
        self.play(Write(pf_eq), run_time=1.8)
        self.wait(1.0)

        # Clean up
        self.play(
            FadeOut(step2_label), FadeOut(pf_setup), FadeOut(factor2),
            pf_eq.animate.scale(0.85).move_to(UP * 2.2),
            run_time=0.5
        )

        # =================================================================
        # SECTION 4: FIND COEFFICIENTS (20-33s)
        # =================================================================
        step3_label = Text("Find A, B, C, D", font_size=30, color=VIBRANT_ORANGE)
        step3_label.move_to(UP * 0.8)
        self.play(FadeIn(step3_label, shift=RIGHT * 0.3), run_time=0.4)

        # A via x=0
        find_a = MathTex(r"x = 0 \Rightarrow", r"A = 1", font_size=38)
        find_a[0].set_color(TEXT_WHITE)
        find_a[1].set_color(SOFT_GREEN)
        find_a.move_to(DOWN * 0.0)
        self.play(Write(find_a), run_time=1.0)
        self.wait(0.5)

        # B via x=-1
        find_b = MathTex(r"x = -1 \Rightarrow", r"B = -\frac{1}{3}", font_size=38)
        find_b[0].set_color(TEXT_WHITE)
        find_b[1].set_color(SOFT_GREEN)
        find_b.next_to(find_a, DOWN, buff=0.5)
        self.play(Write(find_b), run_time=1.0)
        self.wait(0.5)

        # C, D by comparing coefficients
        find_cd = MathTex(
            r"C = -\frac{2}{3}, \quad D = \frac{1}{3}",
            font_size=38, color=SOFT_GREEN
        ).next_to(find_b, DOWN, buff=0.5)
        compare_label = Text("(comparing coefficients)", font_size=20, color=TEXT_WHITE)
        compare_label.set_opacity(0.7)
        compare_label.next_to(find_cd, DOWN, buff=0.2)
        self.play(Write(find_cd), FadeIn(compare_label), run_time=1.2)
        self.wait(1.0)

        # Clean up
        self.play(
            FadeOut(step3_label), FadeOut(compare_label), FadeOut(pf_eq),
            FadeOut(find_a), FadeOut(find_b),
            find_cd.animate.scale(0.8).move_to(UP * 2.2),
            run_time=0.5
        )

        # =================================================================
        # SECTION 5: WRITE SEPARATED INTEGRALS (33-42s)
        # =================================================================
        step4_label = Text("Step 3: Integrate", font_size=30, color=VIBRANT_ORANGE)
        step4_label.move_to(UP * 0.8)
        self.play(FadeIn(step4_label, shift=RIGHT * 0.3), run_time=0.4)

        int1 = MathTex(
            r"\int \frac{1}{x}\,dx",
            font_size=34, color=ELECTRIC_CYAN
        ).move_to(UP * 0.0 + LEFT * 0.5)

        int2 = MathTex(
            r"- \frac{1}{3}\int \frac{1}{x+1}\,dx",
            font_size=34, color=NEON_PINK
        ).next_to(int1, DOWN, buff=0.5)

        int3 = MathTex(
            r"- \frac{1}{3}\int \frac{2x - 1}{x^2 - x + 1}\,dx",
            font_size=32, color=VIBRANT_ORANGE
        ).next_to(int2, DOWN, buff=0.5)

        self.play(Write(int1), run_time=1.0)
        self.play(Write(int2), run_time=1.0)
        self.play(Write(int3), run_time=1.2)
        self.wait(0.8)

        # Note about the third integral
        note = MathTex(
            r"\frac{d}{dx}(x^2 - x + 1) = 2x - 1",
            font_size=26, color=TEXT_WHITE
        ).set_opacity(0.8)
        note.next_to(int3, DOWN, buff=0.4)
        note_box = SurroundingRectangle(note, color=VIBRANT_ORANGE, buff=0.1, stroke_width=1.5)
        self.play(FadeIn(note), Create(note_box), run_time=0.8)
        self.wait(1.0)

        # Clean up
        self.play(
            FadeOut(step4_label), FadeOut(find_cd),
            FadeOut(int1), FadeOut(int2), FadeOut(int3),
            FadeOut(note), FadeOut(note_box),
            run_time=0.5
        )

        # =================================================================
        # SECTION 6: RESULT (42-50s)
        # =================================================================
        step5_label = Text("Result:", font_size=32, color=VIBRANT_ORANGE)
        step5_label.move_to(UP * 1.5)
        self.play(FadeIn(step5_label), run_time=0.3)

        result_line1 = MathTex(
            r"\ln|x|",
            r"- \frac{1}{3}\ln|x+1|",
            font_size=36
        ).move_to(UP * 0.3)
        result_line1[0].set_color(ELECTRIC_CYAN)
        result_line1[1].set_color(NEON_PINK)

        result_line2 = MathTex(
            r"- \frac{1}{3}\ln|x^2-x+1| + C",
            font_size=36, color=VIBRANT_ORANGE
        ).next_to(result_line1, DOWN, buff=0.4)

        self.play(Write(result_line1), run_time=1.5)
        self.play(Write(result_line2), run_time=1.2)
        self.wait(1.0)

        # =================================================================
        # SECTION 7: SIMPLIFY TO CLEAN FORM (50-58s)
        # =================================================================
        simplify_label = Text("Simplify:", font_size=28, color=SOFT_GREEN)
        simplify_label.next_to(result_line2, DOWN, buff=0.7)

        # Since (x+1)(x²-x+1) = x³+1
        note2 = MathTex(
            r"(x+1)(x^2-x+1) = x^3+1",
            font_size=26, color=TEXT_WHITE
        ).set_opacity(0.7)
        note2.next_to(simplify_label, DOWN, buff=0.3)

        self.play(FadeIn(simplify_label), FadeIn(note2), run_time=0.8)
        self.wait(0.8)

        # Clean everything for final answer
        self.play(
            FadeOut(step5_label),
            FadeOut(result_line1), FadeOut(result_line2),
            FadeOut(simplify_label), FadeOut(note2),
            FadeOut(top_integral), FadeOut(ref_box),
            run_time=0.5
        )

        # =================================================================
        # SECTION 8: FINAL ANSWER (58-60s)
        # =================================================================
        final_label = Text("ANSWER", font_size=40, color=ELECTRIC_CYAN)
        final_label.move_to(UP * 3)
        self.play(Write(final_label), run_time=0.5)

        final_answer = MathTex(
            r"\int \frac{1}{x^4+x}\,dx = \frac{1}{3}\ln\!\left|\frac{x^3}{x^3+1}\right| + C",
            font_size=38, color=VIBRANT_ORANGE
        ).move_to(UP * 0.5)

        answer_box = SurroundingRectangle(
            final_answer, color=VIBRANT_ORANGE,
            buff=0.25, stroke_width=3, corner_radius=0.15
        )

        self.play(Write(final_answer), run_time=2.0)
        self.play(
            Create(answer_box),
            Flash(final_answer, color=VIBRANT_ORANGE, line_length=0.4, num_lines=16),
            run_time=1.0
        )

        # Subscribe CTA
        cta = Text("Like & Subscribe!", font_size=28, color=NEON_PINK)
        cta.move_to(DOWN * 3)
        self.play(FadeIn(cta, shift=UP * 0.2), run_time=0.6)

        # Gentle pulse
        self.play(
            VGroup(final_answer, answer_box).animate.scale(1.03),
            rate_func=there_and_back, run_time=1.0
        )
        self.wait(2)
