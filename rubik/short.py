from manim import *
import numpy as np

# ============================================================================
# THE LOGIC & ALGORITHMS BEHIND THE RUBIK'S CUBE — in 1 Minute
# YouTube Short (9:16)
# ============================================================================

# Color Palette (matching project style)
DEEP_NAVY = "#020B1F"
ELECTRIC_CYAN = "#00F0FF"
NEON_PINK = "#FF0055"
VIBRANT_ORANGE = "#FF9F00"
TEXT_WHITE = "#FFFFFF"
SUBTLE_NAVY = "#1E2A45"
SOFT_GREEN = "#00E676"
FLAME_RED = "#FF3D00"
HOT_YELLOW = "#FFD600"

# Rubik's face colors
RUBIK_WHITE = "#FFFFFF"
RUBIK_YELLOW = "#FFD600"
RUBIK_RED = "#FF3D00"
RUBIK_ORANGE = "#FF9F00"
RUBIK_BLUE = "#0055FF"
RUBIK_GREEN = "#00E676"

# YouTube Shorts Configuration (9:16)
config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 14.0
config.frame_width = 14.0 * (1080 / 1920)

config.background_color = DEEP_NAVY


class RubikCubeShort(Scene):
    """The Logic & Algorithms Behind the Rubik's Cube — YouTube Short"""

    # ── helper: draw a single face of a Rubik's cube (3×3 grid) ─────────
    def build_face(self, colors, cell_size=0.55, gap=0.06):
        """Return a VGroup representing a 3×3 Rubik's face with given colors."""
        face = VGroup()
        for row in range(3):
            for col in range(3):
                cell = Square(
                    side_length=cell_size,
                    fill_color=colors[row * 3 + col],
                    fill_opacity=0.95,
                    stroke_color=TEXT_WHITE,
                    stroke_width=1.5,
                )
                cell.move_to(
                    RIGHT * (col - 1) * (cell_size + gap)
                    + DOWN * (row - 1) * (cell_size + gap)
                )
                face.add(cell)
        return face

    # ── helper: 3-face isometric cube view ──────────────────────────────
    def build_cube_isometric(self):
        """Draw a simplified 3-face isometric Rubik's cube."""
        # Front face (red)
        front = self.build_face([RUBIK_RED] * 9, cell_size=0.5, gap=0.05)

        # Top face (white) — skewed
        top = self.build_face([RUBIK_WHITE] * 9, cell_size=0.5, gap=0.05)
        top.rotate(-15 * DEGREES, axis=RIGHT)
        top.apply_matrix([[1, 0.5, 0], [0, 0.6, 0], [0, 0, 1]])
        top.next_to(front, UP, buff=0.02)

        # Right face (blue) — skewed
        right_face = self.build_face([RUBIK_BLUE] * 9, cell_size=0.5, gap=0.05)
        right_face.apply_matrix([[0.6, 0, 0], [0.5, 1, 0], [0, 0, 1]])
        right_face.next_to(front, RIGHT, buff=0.02)

        cube = VGroup(front, top, right_face)
        return cube

    # ── helper: draw scrambled face ─────────────────────────────────────
    def build_scrambled_face(self):
        all_colors = [RUBIK_RED, RUBIK_BLUE, RUBIK_GREEN,
                      RUBIK_WHITE, RUBIK_YELLOW, RUBIK_ORANGE]
        random_colors = [all_colors[i % 6] for i in
                         [3, 0, 5, 2, 1, 4, 0, 5, 2]]
        return self.build_face(random_colors)

    # ── helper: notation move arrows ────────────────────────────────────
    def build_move_notation(self):
        """Show the 6 basic moves: U, D, L, R, F, B."""
        moves = ["U", "D", "L", "R", "F", "B"]
        colors = [RUBIK_WHITE, RUBIK_YELLOW, RUBIK_ORANGE,
                  RUBIK_RED, RUBIK_GREEN, RUBIK_BLUE]
        group = VGroup()
        for i, (move, color) in enumerate(zip(moves, colors)):
            box = RoundedRectangle(
                width=0.85, height=0.85, corner_radius=0.12,
                fill_color=color, fill_opacity=0.8,
                stroke_color=TEXT_WHITE, stroke_width=1.5,
            )
            label = Text(move, font_size=24, color=DEEP_NAVY, weight=BOLD)
            label.move_to(box)
            pair = VGroup(box, label)
            group.add(pair)
        group.arrange_in_grid(rows=2, cols=3, buff=0.15)
        return group

    # ── main construct ──────────────────────────────────────────────────
    def construct(self):
        # =================================================================
        # SECTION 1 — HOOK (0–3s)
        # =================================================================
        hook = Text(
            "How does a Rubik's Cube\nactually work?",
            font_size=32, color=NEON_PINK, line_spacing=1.3,
        )
        hook.to_edge(UP, buff=1.5)

        subtitle = Text("The logic & algorithms.", font_size=26, color=ELECTRIC_CYAN)
        subtitle.next_to(hook, DOWN, buff=0.6)

        # Small cube icon
        cube_icon = self.build_face(
            [RUBIK_RED, RUBIK_BLUE, RUBIK_GREEN,
             RUBIK_WHITE, RUBIK_YELLOW, RUBIK_ORANGE,
             RUBIK_BLUE, RUBIK_GREEN, RUBIK_RED],
            cell_size=0.3, gap=0.04,
        )
        cube_icon.next_to(subtitle, DOWN, buff=0.8)

        self.play(FadeIn(hook, shift=DOWN * 0.3), run_time=0.6)
        self.play(Write(subtitle), run_time=0.7)
        self.play(FadeIn(cube_icon, scale=0.5), run_time=0.5)
        self.wait(0.7)

        self.play(
            FadeOut(hook), FadeOut(subtitle), FadeOut(cube_icon),
            run_time=0.5,
        )

        # =================================================================
        # SECTION 2 — THE SCALE OF THE PROBLEM (3–8s)
        # =================================================================
        title = Text("The Scale of the Problem", font_size=30, color=VIBRANT_ORANGE)
        title.to_edge(UP, buff=0.6)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.4)

        # Permutation count
        perm_eq = MathTex(
            r"43{,}252{,}003{,}274{,}489{,}856{,}000",
            font_size=28, color=ELECTRIC_CYAN,
        ).move_to(UP * 1.5)

        perm_label = Text(
            "possible configurations!",
            font_size=20, color=TEXT_WHITE,
        ).next_to(perm_eq, DOWN, buff=0.3)

        self.play(Write(perm_eq), run_time=1.2)
        self.play(FadeIn(perm_label, shift=UP * 0.15), run_time=0.5)
        self.wait(0.5)

        # Compact formula
        formula = MathTex(
            r"\frac{8! \cdot 3^8 \cdot 12! \cdot 2^{12}}{12}",
            font_size=36, color=SOFT_GREEN,
        ).move_to(DOWN * 0.5)

        approx = MathTex(
            r"\approx 4.3 \times 10^{19}",
            font_size=32, color=HOT_YELLOW,
        ).next_to(formula, DOWN, buff=0.4)

        self.play(Write(formula), run_time=1.0)
        self.play(Write(approx), run_time=0.8)
        self.wait(0.5)

        scale_desc = Text(
            "That's more than the number\nof grains of sand on Earth.",
            font_size=20, color=TEXT_WHITE, line_spacing=1.3,
        ).move_to(DOWN * 2.8)
        self.play(FadeIn(scale_desc, shift=UP * 0.2), run_time=0.6)
        self.wait(1.0)

        self.play(
            FadeOut(title), FadeOut(perm_eq), FadeOut(perm_label),
            FadeOut(formula), FadeOut(approx), FadeOut(scale_desc),
            run_time=0.5,
        )

        # =================================================================
        # SECTION 3 — NOTATION: THE LANGUAGE (8–14s)
        # =================================================================
        s2_label = Text("Move Notation", font_size=28, color=VIBRANT_ORANGE)
        s2_label.to_edge(UP, buff=0.6)
        self.play(FadeIn(s2_label, shift=RIGHT * 0.3), run_time=0.4)

        notation_grid = self.build_move_notation()
        notation_grid.move_to(UP * 1.2)
        self.play(
            *[FadeIn(m, scale=0.7) for m in notation_grid],
            run_time=1.0,
        )
        self.wait(0.5)

        # Explanation
        not_desc = Text(
            "Each letter = one 90° turn\nof a face.",
            font_size=22, color=TEXT_WHITE, line_spacing=1.3,
        ).move_to(DOWN * 0.8)
        self.play(FadeIn(not_desc, shift=UP * 0.2), run_time=0.6)
        self.wait(0.3)

        prime_desc = MathTex(
            r"R' = \text{reverse (counter-clockwise)}",
            font_size=26, color=ELECTRIC_CYAN,
        ).move_to(DOWN * 2.0)
        double_desc = MathTex(
            r"R2 = \text{double turn (180°)}",
            font_size=26, color=ELECTRIC_CYAN,
        ).next_to(prime_desc, DOWN, buff=0.3)

        self.play(Write(prime_desc), run_time=0.7)
        self.play(Write(double_desc), run_time=0.7)
        self.wait(1.0)

        self.play(
            FadeOut(s2_label), FadeOut(notation_grid), FadeOut(not_desc),
            FadeOut(prime_desc), FadeOut(double_desc),
            run_time=0.5,
        )

        # =================================================================
        # SECTION 4 — GROUP THEORY: THE MATH (14–22s)
        # =================================================================
        s3_label = Text("Group Theory — The Math", font_size=28, color=VIBRANT_ORANGE)
        s3_label.to_edge(UP, buff=0.6)
        self.play(FadeIn(s3_label, shift=RIGHT * 0.3), run_time=0.4)

        # Group definition
        group_def = MathTex(
            r"\text{Rubik's Group: } G = \langle U, D, L, R, F, B \rangle",
            font_size=26, color=ELECTRIC_CYAN,
        ).move_to(UP * 1.5)
        self.play(Write(group_def), run_time=1.0)
        self.wait(0.3)

        # Properties
        props = VGroup(
            MathTex(r"\bullet\; \text{Closure: } A \cdot B \in G", font_size=22, color=TEXT_WHITE),
            MathTex(r"\bullet\; \text{Identity: } I \cdot A = A", font_size=22, color=TEXT_WHITE),
            MathTex(r"\bullet\; \text{Inverse: } R \cdot R' = I", font_size=22, color=TEXT_WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 0.2)

        self.play(
            *[FadeIn(p, shift=RIGHT * 0.2) for p in props],
            run_time=1.0,
        )
        self.wait(0.5)

        group_desc = Text(
            "Every move sequence is\na permutation of 54 stickers.",
            font_size=20, color=SOFT_GREEN, line_spacing=1.3,
        ).move_to(DOWN * 2.5)
        self.play(FadeIn(group_desc, shift=UP * 0.2), run_time=0.6)
        self.wait(1.5)

        self.play(
            FadeOut(s3_label), FadeOut(group_def),
            FadeOut(props), FadeOut(group_desc),
            run_time=0.5,
        )

        # =================================================================
        # SECTION 5 — GOD'S NUMBER (22–30s)
        # =================================================================
        s4_label = Text("God's Number", font_size=30, color=VIBRANT_ORANGE)
        s4_label.to_edge(UP, buff=0.6)
        self.play(FadeIn(s4_label, shift=RIGHT * 0.3), run_time=0.4)

        # Big 20
        big_20 = Text("20", font_size=100, color=NEON_PINK, weight=BOLD)
        big_20.move_to(UP * 0.8)
        self.play(FadeIn(big_20, scale=0.3), run_time=0.8)
        self.wait(0.3)

        # Glow ring
        glow = Circle(radius=1.2, stroke_color=NEON_PINK, stroke_width=4)
        glow.move_to(big_20)
        self.play(Create(glow), run_time=0.5)
        self.play(
            glow.animate.scale(1.3).set_stroke(opacity=0),
            run_time=0.8,
        )
        self.remove(glow)

        god_desc = Text(
            "Every possible scramble can be\nsolved in 20 moves or fewer.",
            font_size=20, color=TEXT_WHITE, line_spacing=1.3,
        ).move_to(DOWN * 1.0)
        self.play(FadeIn(god_desc, shift=UP * 0.2), run_time=0.7)
        self.wait(0.5)

        proven = Text(
            "Proven in 2010 with\n35 CPU-years of computation.",
            font_size=18, color=ELECTRIC_CYAN, line_spacing=1.3,
        ).move_to(DOWN * 2.8)
        self.play(FadeIn(proven, shift=UP * 0.15), run_time=0.6)
        self.wait(1.5)

        self.play(
            FadeOut(s4_label), FadeOut(big_20),
            FadeOut(god_desc), FadeOut(proven),
            run_time=0.5,
        )

        # =================================================================
        # SECTION 6 — SOLVING ALGORITHMS: CFOP (30–45s)
        # =================================================================
        s5_label = Text("CFOP — The Speed-Solver's Method", font_size=24, color=VIBRANT_ORANGE)
        s5_label.to_edge(UP, buff=0.6)
        self.play(FadeIn(s5_label, shift=RIGHT * 0.3), run_time=0.4)

        # CFOP steps as animated blocks
        steps_data = [
            ("C", "Cross", RUBIK_WHITE, "Solve the bottom\nedge pieces"),
            ("F", "F2L", SOFT_GREEN, "First Two Layers\nsimultaneously"),
            ("O", "OLL", HOT_YELLOW, "Orient Last Layer\n(top face yellow)"),
            ("P", "PLL", ELECTRIC_CYAN, "Permute Last Layer\n(final solve!)"),
        ]

        all_blocks = VGroup()
        for letter, name, color, desc_text in steps_data:
            # Letter circle
            circle = Circle(
                radius=0.4, fill_color=color, fill_opacity=0.85,
                stroke_color=TEXT_WHITE, stroke_width=1.5,
            )
            letter_t = Text(letter, font_size=28, color=DEEP_NAVY, weight=BOLD)
            letter_t.move_to(circle)

            name_t = Text(name, font_size=18, color=color, weight=BOLD)
            name_t.next_to(circle, RIGHT, buff=0.25)

            desc_t = Text(desc_text, font_size=14, color=TEXT_WHITE, line_spacing=1.2)
            desc_t.next_to(name_t, DOWN, buff=0.15, aligned_edge=LEFT)

            block = VGroup(circle, letter_t, name_t, desc_t)
            all_blocks.add(block)

        all_blocks.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        all_blocks.move_to(DOWN * 0.3)

        # Animate each step
        for i, block in enumerate(all_blocks):
            self.play(
                FadeIn(block[0], scale=0.5),  # circle
                FadeIn(block[1], scale=0.5),  # letter
                run_time=0.3,
            )
            self.play(
                FadeIn(block[2], shift=RIGHT * 0.2),  # name
                FadeIn(block[3], shift=UP * 0.1),      # description
                run_time=0.4,
            )
            if i < len(all_blocks) - 1:
                # Draw connecting arrow
                arr = Arrow(
                    block.get_bottom() + DOWN * 0.05,
                    block.get_bottom() + DOWN * 0.3,
                    buff=0, stroke_width=2, color=VIBRANT_ORANGE,
                    max_tip_length_to_length_ratio=0.5,
                )
                self.play(GrowArrow(arr), run_time=0.15)

        self.wait(1.0)

        # Algorithm count
        alg_count = MathTex(
            r"\text{OLL: 57 algorithms} \quad \text{PLL: 21 algorithms}",
            font_size=20, color=HOT_YELLOW,
        ).move_to(DOWN * 4.5)
        self.play(FadeIn(alg_count, shift=UP * 0.15), run_time=0.6)
        self.wait(1.0)

        self.play(
            FadeOut(s5_label), FadeOut(all_blocks),
            FadeOut(alg_count),
            *[FadeOut(m) for m in self.mobjects if m not in [s5_label, all_blocks, alg_count]],
            run_time=0.5,
        )

        # =================================================================
        # SECTION 7 — KOCIEMBA'S ALGORITHM (45–52s)
        # =================================================================
        s6_label = Text("Kociemba's Algorithm", font_size=28, color=VIBRANT_ORANGE)
        s6_label.to_edge(UP, buff=0.6)
        self.play(FadeIn(s6_label, shift=RIGHT * 0.3), run_time=0.4)

        # Two-phase approach
        phase1_box = RoundedRectangle(
            width=5.5, height=1.6, corner_radius=0.2,
            fill_color=SUBTLE_NAVY, fill_opacity=0.7,
            stroke_color=ELECTRIC_CYAN, stroke_width=2,
        ).move_to(UP * 1.0)

        p1_title = Text("Phase 1", font_size=22, color=ELECTRIC_CYAN, weight=BOLD)
        p1_title.move_to(phase1_box.get_top() + DOWN * 0.35)
        p1_desc = Text(
            "Reduce to a subgroup\nwhere only half-turns needed",
            font_size=16, color=TEXT_WHITE, line_spacing=1.2,
        )
        p1_desc.next_to(p1_title, DOWN, buff=0.15)

        phase2_box = RoundedRectangle(
            width=5.5, height=1.6, corner_radius=0.2,
            fill_color=SUBTLE_NAVY, fill_opacity=0.7,
            stroke_color=SOFT_GREEN, stroke_width=2,
        ).move_to(DOWN * 1.2)

        p2_title = Text("Phase 2", font_size=22, color=SOFT_GREEN, weight=BOLD)
        p2_title.move_to(phase2_box.get_top() + DOWN * 0.35)
        p2_desc = Text(
            "Solve from subgroup\nto the solved state",
            font_size=16, color=TEXT_WHITE, line_spacing=1.2,
        )
        p2_desc.next_to(p2_title, DOWN, buff=0.15)

        mid_arrow = Arrow(
            phase1_box.get_bottom(), phase2_box.get_top(),
            buff=0.15, color=VIBRANT_ORANGE, stroke_width=3,
        )

        self.play(FadeIn(phase1_box), FadeIn(p1_title), run_time=0.5)
        self.play(FadeIn(p1_desc, shift=UP * 0.1), run_time=0.4)
        self.play(GrowArrow(mid_arrow), run_time=0.3)
        self.play(FadeIn(phase2_box), FadeIn(p2_title), run_time=0.5)
        self.play(FadeIn(p2_desc, shift=UP * 0.1), run_time=0.4)
        self.wait(0.5)

        # Subgroup notation
        subgroup = MathTex(
            r"G_1 = \langle U, D, L2, R2, F2, B2 \rangle",
            font_size=24, color=HOT_YELLOW,
        ).move_to(DOWN * 3.5)
        self.play(Write(subgroup), run_time=0.8)
        self.wait(1.5)

        self.play(
            FadeOut(s6_label),
            FadeOut(phase1_box), FadeOut(p1_title), FadeOut(p1_desc),
            FadeOut(phase2_box), FadeOut(p2_title), FadeOut(p2_desc),
            FadeOut(mid_arrow), FadeOut(subgroup),
            run_time=0.5,
        )

        # =================================================================
        # SECTION 8 — FINALE & CTA (52–60s)
        # =================================================================
        final_label = Text("RUBIK'S CUBE", font_size=42, color=ELECTRIC_CYAN)
        final_label.move_to(UP * 3)
        self.play(Write(final_label), run_time=0.5)

        # Summary flow
        summary = MathTex(
            r"\text{Scramble} \;\rightarrow\; \text{Cross} \;\rightarrow\; "
            r"\text{F2L} \;\rightarrow\; \text{OLL} \;\rightarrow\; \text{PLL}",
            font_size=22, color=VIBRANT_ORANGE,
        ).move_to(UP * 0.8)

        summary_box = SurroundingRectangle(
            summary, color=VIBRANT_ORANGE,
            buff=0.25, stroke_width=3, corner_radius=0.15,
        )

        self.play(Write(summary), run_time=1.5)
        self.play(
            Create(summary_box),
            Flash(summary, color=VIBRANT_ORANGE, line_length=0.4, num_lines=16),
            run_time=0.8,
        )
        self.wait(0.3)

        # Final cube — solved face
        solved_face = self.build_face([RUBIK_RED] * 9, cell_size=0.45, gap=0.04)
        solved_face.move_to(DOWN * 1.5)
        self.play(FadeIn(solved_face, scale=0.5), run_time=0.6)

        # Solved label
        solved_text = Text("Solved.", font_size=26, color=SOFT_GREEN, weight=BOLD)
        solved_text.next_to(solved_face, DOWN, buff=0.4)
        self.play(Write(solved_text), run_time=0.5)
        self.wait(0.5)

        # Subscribe CTA
        cta = Text("Like & Subscribe!", font_size=28, color=NEON_PINK)
        cta.move_to(DOWN * 4.5)
        self.play(FadeIn(cta, shift=UP * 0.2), run_time=0.5)

        # Gentle pulse
        self.play(
            VGroup(summary, summary_box).animate.scale(1.03),
            rate_func=there_and_back, run_time=1.0,
        )
        self.wait(2)
