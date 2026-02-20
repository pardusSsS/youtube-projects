from manim import *
import numpy as np

# ============================================================================
# HOW A JET ENGINE WORKS — in 1 Minute
# YouTube Short (9:16)
# ============================================================================

# Color Palette
DEEP_NAVY = "#020B1F"
ELECTRIC_CYAN = "#00F0FF"
NEON_PINK = "#FF0055"
VIBRANT_ORANGE = "#FF9F00"
TEXT_WHITE = "#FFFFFF"
SUBTLE_NAVY = "#1E2A45"
SOFT_GREEN = "#00E676"
FLAME_RED = "#FF3D00"
HOT_YELLOW = "#FFD600"

# YouTube Shorts Configuration (9:16)
config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 14.0
config.frame_width = 14.0 * (1080 / 1920)

config.background_color = DEEP_NAVY


class JetEngineShort(Scene):
    """How a Jet Engine Works in 1 minute — YouTube Short"""

    # ── helper: draw a simplified jet-engine cross-section ──────────────
    def build_engine(self):
        """Return a VGroup that represents a stylised jet-engine diagram."""
        # Outer nacelle (rounded rectangle)
        nacelle = RoundedRectangle(
            width=6.0, height=2.4, corner_radius=0.5,
            stroke_color=ELECTRIC_CYAN, stroke_width=2.5,
            fill_color=SUBTLE_NAVY, fill_opacity=0.6,
        )

        # Section divider lines
        line1 = DashedLine(
            start=UP * 1.2, end=DOWN * 1.2,
            dash_length=0.1, color=ELECTRIC_CYAN
        ).shift(LEFT * 1.2)
        line2 = DashedLine(
            start=UP * 1.2, end=DOWN * 1.2,
            dash_length=0.1, color=ELECTRIC_CYAN
        ).shift(RIGHT * 0.3)
        line3 = DashedLine(
            start=UP * 1.2, end=DOWN * 1.2,
            dash_length=0.1, color=ELECTRIC_CYAN
        ).shift(RIGHT * 1.8)

        # Fan blades (left-most section)
        fan_center = Dot(ORIGIN, radius=0.08, color=TEXT_WHITE).shift(LEFT * 2.1)
        fan_blades = VGroup()
        for angle in range(0, 360, 45):
            blade = Line(ORIGIN, UP * 0.9, stroke_width=3, color=TEXT_WHITE)
            blade.rotate(angle * DEGREES, about_point=ORIGIN)
            blade.shift(LEFT * 2.1)
            fan_blades.add(blade)

        # Compressor chevrons
        comp = VGroup()
        for i in range(3):
            chev = VGroup(
                Line(UP * 0.7, ORIGIN, stroke_width=2, color=ELECTRIC_CYAN),
                Line(ORIGIN, DOWN * 0.7, stroke_width=2, color=ELECTRIC_CYAN),
            ).shift(LEFT * (0.6 - i * 0.35))
            comp.add(chev)

        # Combustion flame shapes
        flames = VGroup()
        for dy in np.linspace(-0.5, 0.5, 3):
            flame = Polygon(
                LEFT * 0.15 + UP * dy,
                RIGHT * 0.35 + UP * (dy + 0.12),
                RIGHT * 0.35 + UP * (dy - 0.12),
                fill_color=FLAME_RED, fill_opacity=0.85,
                stroke_width=0,
            )
            flames.add(flame)
        flames.shift(RIGHT * 1.05)

        # Turbine blades
        turbine_center = Dot(ORIGIN, radius=0.06, color=TEXT_WHITE).shift(RIGHT * 2.2)
        turbine_blades = VGroup()
        for angle in range(0, 360, 60):
            blade = Line(ORIGIN, UP * 0.7, stroke_width=2.5, color=VIBRANT_ORANGE)
            blade.rotate(angle * DEGREES, about_point=ORIGIN)
            blade.shift(RIGHT * 2.2)
            turbine_blades.add(blade)

        # Exhaust nozzle (cone)
        nozzle = Polygon(
            RIGHT * 3.0 + UP * 1.2,
            RIGHT * 3.0 + DOWN * 1.2,
            RIGHT * 3.8 + DOWN * 0.6,
            RIGHT * 3.8 + UP * 0.6,
            stroke_color=ELECTRIC_CYAN, stroke_width=2,
            fill_color=SUBTLE_NAVY, fill_opacity=0.4,
        )

        engine = VGroup(
            nacelle, line1, line2, line3,
            fan_center, fan_blades,
            comp, flames,
            turbine_center, turbine_blades,
            nozzle,
        )
        return engine

    # ── helper: section labels inside engine ────────────────────────────
    def section_labels(self):
        labels = VGroup(
            Text("FAN", font_size=16, color=HOT_YELLOW).move_to(LEFT * 2.1 + DOWN * 1.7),
            Text("COMPRESSOR", font_size=13, color=HOT_YELLOW).move_to(LEFT * 0.3 + DOWN * 1.7),
            Text("COMBUSTION", font_size=13, color=HOT_YELLOW).move_to(RIGHT * 1.05 + DOWN * 1.7),
            Text("TURBINE", font_size=14, color=HOT_YELLOW).move_to(RIGHT * 2.2 + DOWN * 1.7),
        )
        return labels

    # ── main construct ──────────────────────────────────────────────────
    def construct(self):
        # =================================================================
        # SECTION 1 — HOOK (0-3s)
        # =================================================================
        hook = Text("How does a Jet Engine work?", font_size=34, color=NEON_PINK)
        hook.to_edge(UP, buff=1.2)

        subtitle = Text("in 1 minute.", font_size=28, color=ELECTRIC_CYAN)
        subtitle.next_to(hook, DOWN, buff=0.6)

        # Small jet icon (triangle)
        jet_icon = Triangle(fill_color=TEXT_WHITE, fill_opacity=0.9, stroke_width=0)
        jet_icon.scale(0.35).rotate(-PI / 2).next_to(subtitle, DOWN, buff=1.0)

        self.play(FadeIn(hook, shift=DOWN * 0.3), run_time=0.6)
        self.play(Write(subtitle), run_time=0.7)
        self.play(FadeIn(jet_icon, scale=0.5), run_time=0.5)
        self.wait(0.7)

        self.play(
            FadeOut(hook), FadeOut(subtitle), FadeOut(jet_icon),
            run_time=0.5,
        )

        # =================================================================
        # SECTION 2 — OVERVIEW: 4 STAGES (3-8s)
        # =================================================================
        title = Text("4 Key Stages", font_size=34, color=VIBRANT_ORANGE)
        title.to_edge(UP, buff=0.6)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.4)

        engine = self.build_engine()
        engine.scale(0.85).move_to(UP * 0.5)
        self.play(FadeIn(engine, shift=LEFT * 0.5), run_time=1.2)
        self.wait(0.5)

        labels = self.section_labels()
        labels.scale(0.85).shift(UP * 0.5)
        self.play(
            *[FadeIn(l, shift=UP * 0.15) for l in labels],
            run_time=0.8,
        )
        self.wait(1.0)

        # Move engine + labels up, keep as reference
        self.play(
            FadeOut(title),
            VGroup(engine, labels).animate.scale(0.65).to_edge(UP, buff=0.4),
            run_time=0.6,
        )
        ref_group = VGroup(engine, labels)
        ref_box = SurroundingRectangle(ref_group, color=ELECTRIC_CYAN, buff=0.15, stroke_width=1.5)
        self.play(Create(ref_box), run_time=0.3)

        # =================================================================
        # SECTION 3 — STAGE 1: INTAKE & FAN (8-18s)
        # =================================================================
        s1_label = Text("Stage 1 — Intake & Fan", font_size=28, color=VIBRANT_ORANGE)
        s1_label.move_to(UP * 1.5)
        self.play(FadeIn(s1_label, shift=RIGHT * 0.3), run_time=0.4)

        # Air arrows entering
        air_arrows = VGroup()
        for dy in np.linspace(-0.6, 0.6, 4):
            arr = Arrow(
                LEFT * 3.5 + UP * dy, LEFT * 1.5 + UP * dy,
                buff=0, stroke_width=3, color=ELECTRIC_CYAN,
                max_tip_length_to_length_ratio=0.2,
            )
            air_arrows.add(arr)
        air_arrows.move_to(DOWN * 0.5)

        air_text = MathTex(r"\text{Air} \;\longrightarrow", font_size=34, color=ELECTRIC_CYAN)
        air_text.next_to(air_arrows, LEFT, buff=0.0)

        self.play(
            *[GrowArrow(a) for a in air_arrows],
            FadeIn(air_text, shift=RIGHT * 0.2),
            run_time=1.0,
        )
        self.wait(0.3)

        fan_desc = Text(
            "Large fan blades suck in\nmassive amounts of air.",
            font_size=22, color=TEXT_WHITE, line_spacing=1.3,
        ).move_to(DOWN * 2.5)
        self.play(FadeIn(fan_desc, shift=UP * 0.2), run_time=0.8)
        self.wait(1.5)

        # Bypass note
        bypass = MathTex(
            r"\approx 90\%\;\text{bypass air}",
            font_size=26, color=SOFT_GREEN,
        ).next_to(fan_desc, DOWN, buff=0.5)
        self.play(Write(bypass), run_time=0.8)
        self.wait(1.0)

        self.play(
            FadeOut(s1_label), FadeOut(air_arrows), FadeOut(air_text),
            FadeOut(fan_desc), FadeOut(bypass),
            run_time=0.5,
        )

        # =================================================================
        # SECTION 4 — STAGE 2: COMPRESSOR (18-28s)
        # =================================================================
        s2_label = Text("Stage 2 — Compressor", font_size=28, color=VIBRANT_ORANGE)
        s2_label.move_to(UP * 1.5)
        self.play(FadeIn(s2_label, shift=RIGHT * 0.3), run_time=0.4)

        # Pressure visualisation: shrinking volume
        box_big = Rectangle(
            width=3.0, height=2.0,
            stroke_color=ELECTRIC_CYAN, stroke_width=2,
        ).move_to(DOWN * 0.8 + LEFT * 1.5)
        box_small = Rectangle(
            width=1.5, height=1.0,
            stroke_color=SOFT_GREEN, stroke_width=3,
        ).move_to(DOWN * 0.8 + RIGHT * 1.5)

        dots_big = VGroup(*[
            Dot(radius=0.04, color=TEXT_WHITE).move_to(
                box_big.get_center() + np.array([
                    np.random.uniform(-1.2, 1.2),
                    np.random.uniform(-0.7, 0.7), 0
                ])
            ) for _ in range(20)
        ])
        dots_small = VGroup(*[
            Dot(radius=0.04, color=TEXT_WHITE).move_to(
                box_small.get_center() + np.array([
                    np.random.uniform(-0.5, 0.5),
                    np.random.uniform(-0.3, 0.3), 0
                ])
            ) for _ in range(20)
        ])

        arrow_comp = Arrow(
            box_big.get_right(), box_small.get_left(),
            buff=0.15, color=VIBRANT_ORANGE, stroke_width=3,
        )

        self.play(FadeIn(box_big), FadeIn(dots_big), run_time=0.6)
        self.play(GrowArrow(arrow_comp), run_time=0.5)
        self.play(FadeIn(box_small), FadeIn(dots_small), run_time=0.6)
        self.wait(0.3)

        comp_desc = Text(
            "Multiple rotating blades\nsqueeze the air tightly.",
            font_size=22, color=TEXT_WHITE, line_spacing=1.3,
        ).move_to(DOWN * 3.0)
        self.play(FadeIn(comp_desc, shift=UP * 0.2), run_time=0.6)
        self.wait(0.5)

        pressure_eq = MathTex(
            r"P_2 \gg P_1",
            font_size=38, color=SOFT_GREEN,
        ).next_to(comp_desc, DOWN, buff=0.5)
        self.play(Write(pressure_eq), run_time=0.8)
        self.wait(1.2)

        # Pressure ratio
        ratio = MathTex(
            r"\frac{P_2}{P_1} \approx 30{:}1",
            font_size=36, color=ELECTRIC_CYAN,
        ).next_to(pressure_eq, DOWN, buff=0.4)
        self.play(Write(ratio), run_time=0.8)
        self.wait(1.0)

        self.play(
            FadeOut(s2_label), FadeOut(box_big), FadeOut(box_small),
            FadeOut(dots_big), FadeOut(dots_small), FadeOut(arrow_comp),
            FadeOut(comp_desc), FadeOut(pressure_eq), FadeOut(ratio),
            run_time=0.5,
        )

        # =================================================================
        # SECTION 5 — STAGE 3: COMBUSTION (28-42s)
        # =================================================================
        s3_label = Text("Stage 3 — Combustion", font_size=28, color=VIBRANT_ORANGE)
        s3_label.move_to(UP * 1.5)
        self.play(FadeIn(s3_label, shift=RIGHT * 0.3), run_time=0.4)

        # Fuel + Air → Ignition
        fuel_tex = MathTex(r"\text{Fuel}", font_size=34, color=HOT_YELLOW)
        plus = MathTex(r"+", font_size=34, color=TEXT_WHITE)
        air_tex = MathTex(r"\text{Compressed Air}", font_size=34, color=ELECTRIC_CYAN)
        eq_row = VGroup(fuel_tex, plus, air_tex).arrange(RIGHT, buff=0.3)
        eq_row.move_to(DOWN * 0.2)

        self.play(Write(eq_row), run_time=1.0)
        self.wait(0.5)

        ignite_arrow = Arrow(
            eq_row.get_bottom(), eq_row.get_bottom() + DOWN * 1.0,
            buff=0.15, color=FLAME_RED, stroke_width=4,
        )
        ignite_text = Text("IGNITE!", font_size=30, color=FLAME_RED)
        ignite_text.next_to(ignite_arrow, DOWN, buff=0.2)

        self.play(GrowArrow(ignite_arrow), run_time=0.4)
        self.play(
            FadeIn(ignite_text, scale=1.5),
            Flash(ignite_text, color=FLAME_RED, line_length=0.3, num_lines=12),
            run_time=0.8,
        )
        self.wait(0.5)

        temp_eq = MathTex(
            r"T \approx 1\,700\;°C",
            font_size=36, color=HOT_YELLOW,
        ).next_to(ignite_text, DOWN, buff=0.6)
        self.play(Write(temp_eq), run_time=0.8)
        self.wait(0.4)

        comb_desc = Text(
            "Hot expanding gases\nshoot out at high speed.",
            font_size=22, color=TEXT_WHITE, line_spacing=1.3,
        ).next_to(temp_eq, DOWN, buff=0.5)
        self.play(FadeIn(comb_desc, shift=UP * 0.2), run_time=0.6)
        self.wait(1.5)

        self.play(
            FadeOut(s3_label), FadeOut(eq_row),
            FadeOut(ignite_arrow), FadeOut(ignite_text),
            FadeOut(temp_eq), FadeOut(comb_desc),
            run_time=0.5,
        )

        # =================================================================
        # SECTION 6 — STAGE 4: TURBINE & EXHAUST (42-52s)
        # =================================================================
        s4_label = Text("Stage 4 — Turbine & Exhaust", font_size=26, color=VIBRANT_ORANGE)
        s4_label.move_to(UP * 1.5)
        self.play(FadeIn(s4_label, shift=RIGHT * 0.3), run_time=0.4)

        # Energy flow diagram
        turb_desc = Text(
            "Hot gases spin the turbine,\nwhich drives the front fan.",
            font_size=22, color=TEXT_WHITE, line_spacing=1.3,
        ).move_to(DOWN * 0.3)
        self.play(FadeIn(turb_desc, shift=UP * 0.2), run_time=0.8)
        self.wait(1.0)

        # Feedback loop
        loop_arrow_text = MathTex(
            r"\text{Turbine} \;\xrightarrow{\text{shaft}}\; \text{Fan}",
            font_size=30, color=SOFT_GREEN,
        ).next_to(turb_desc, DOWN, buff=0.6)
        self.play(Write(loop_arrow_text), run_time=1.0)
        self.wait(0.8)

        # Thrust equation
        thrust_eq = MathTex(
            r"F = \dot{m}\,(v_e - v_0)",
            font_size=38, color=ELECTRIC_CYAN,
        ).next_to(loop_arrow_text, DOWN, buff=0.6)
        thrust_label = Text("Thrust", font_size=22, color=VIBRANT_ORANGE)
        thrust_label.next_to(thrust_eq, DOWN, buff=0.2)

        self.play(Write(thrust_eq), run_time=1.2)
        self.play(FadeIn(thrust_label), run_time=0.4)
        self.wait(1.2)

        self.play(
            FadeOut(s4_label), FadeOut(turb_desc),
            FadeOut(loop_arrow_text),
            FadeOut(thrust_eq), FadeOut(thrust_label),
            run_time=0.5,
        )

        # =================================================================
        # SECTION 7 — NEWTON'S 3RD LAW (52-57s)
        # =================================================================
        newton_label = Text("Newton's 3rd Law", font_size=30, color=VIBRANT_ORANGE)
        newton_label.move_to(UP * 1.5)
        self.play(FadeIn(newton_label), run_time=0.4)

        newton_eq = MathTex(
            r"F_{\text{action}} = -\,F_{\text{reaction}}",
            font_size=40, color=NEON_PINK,
        ).move_to(DOWN * 0.2)
        self.play(Write(newton_eq), run_time=1.0)
        self.wait(0.5)

        newton_desc = Text(
            "Gas pushes backward →\nPlane pushes forward!",
            font_size=24, color=TEXT_WHITE, line_spacing=1.3,
        ).next_to(newton_eq, DOWN, buff=0.7)
        self.play(FadeIn(newton_desc, shift=UP * 0.2), run_time=0.6)
        self.wait(1.0)

        # Clean everything for finale
        self.play(
            FadeOut(newton_label), FadeOut(newton_eq), FadeOut(newton_desc),
            FadeOut(ref_group), FadeOut(ref_box),
            run_time=0.5,
        )

        # =================================================================
        # SECTION 8 — FINALE & CTA (57-60s)
        # =================================================================
        final_label = Text("JET ENGINE", font_size=42, color=ELECTRIC_CYAN)
        final_label.move_to(UP * 3)
        self.play(Write(final_label), run_time=0.5)

        summary = MathTex(
            r"\text{Suck} \;\rightarrow\; \text{Squeeze} \;\rightarrow\; "
            r"\text{Bang} \;\rightarrow\; \text{Blow}",
            font_size=30, color=VIBRANT_ORANGE,
        ).move_to(UP * 0.5)

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

        # Subscribe CTA
        cta = Text("Like & Subscribe!", font_size=28, color=NEON_PINK)
        cta.move_to(DOWN * 3)
        self.play(FadeIn(cta, shift=UP * 0.2), run_time=0.5)

        # Gentle pulse
        self.play(
            VGroup(summary, summary_box).animate.scale(1.03),
            rate_func=there_and_back, run_time=1.0,
        )
        self.wait(2)
