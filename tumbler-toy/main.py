from manim import *
import numpy as np

# Vibrant Space Tech Color Palette
DEEP_NAVY = "#020B1F"
ELECTRIC_CYAN = "#00F0FF"
NEON_PINK = "#FF0055"
VIBRANT_ORANGE = "#FF9F00"
SUBTLE_NAVY = "#1E2A45"

# YouTube Shorts Configuration (9:16 aspect ratio)
config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 14.0
config.frame_width = 14.0 * (1080 / 1920)  # ~7.875
config.background_color = DEEP_NAVY


# ─── Helper: build a tumbler toy shape ──────────────────────────────
def build_tumbler(scale=1.0):
    """Return a VGroup representing the tumbler toy (cross-section view).
    The toy is centred at the bottom of the hemisphere.
    """
    s = scale

    # Bottom heavy hemisphere (weighted base)
    bottom_arc = Arc(
        radius=1.2 * s, start_angle=PI, angle=PI,
        color=ELECTRIC_CYAN, stroke_width=3
    )
    bottom_arc.set_fill(ELECTRIC_CYAN, opacity=0.25)

    # Close the hemisphere with a line
    bottom_line = Line(
        bottom_arc.get_start(), bottom_arc.get_end(),
        color=ELECTRIC_CYAN, stroke_width=3
    )

    # Upper body (elliptical / egg shape)
    upper_body = Ellipse(
        width=1.8 * s, height=2.4 * s,
        color=NEON_PINK, stroke_width=3
    )
    upper_body.set_fill(NEON_PINK, opacity=0.15)
    upper_body.move_to(bottom_line.get_center() + UP * 1.2 * s)

    # Eyes
    eye_l = Dot(point=upper_body.get_center() + LEFT * 0.3 * s + UP * 0.3 * s,
                radius=0.08 * s, color=WHITE)
    eye_r = Dot(point=upper_body.get_center() + RIGHT * 0.3 * s + UP * 0.3 * s,
                radius=0.08 * s, color=WHITE)

    # Smile
    smile = Arc(
        radius=0.25 * s, start_angle=-PI * 0.8, angle=PI * 0.6,
        color=WHITE, stroke_width=2 * s
    )
    smile.move_to(upper_body.get_center() + DOWN * 0.1 * s)

    # Weight inside hemisphere (dark circle representing heavy mass)
    weight = Circle(radius=0.55 * s, color=VIBRANT_ORANGE, stroke_width=2)
    weight.set_fill(VIBRANT_ORANGE, opacity=0.5)
    weight.move_to(bottom_arc.get_center() + DOWN * 0.25 * s)

    toy = VGroup(bottom_arc, bottom_line, upper_body, eye_l, eye_r, smile, weight)
    return toy


# ─── Main Scene ─────────────────────────────────────────────────────
class TumblerToyShort(Scene):
    """How Does a Tumbler Toy Stay Balanced? — YouTube Shorts Version"""

    def construct(self):
        self.section_1_intro()
        self.section_2_center_of_mass()
        self.section_3_torque()
        self.section_4_potential_energy()
        self.section_5_damped_oscillation()
        self.section_6_outro()

    # ── Section 1 — Intro ───────────────────────────────────────────
    def section_1_intro(self):
        # Title
        title = Text("Tumbler Toy", font_size=56, color=ELECTRIC_CYAN, weight=BOLD)
        title.to_edge(UP, buff=0.8)

        question = Text("Why doesn't it fall over?", font_size=34, color=WHITE)
        question.next_to(title, DOWN, buff=0.4)

        # Build toy
        toy = build_tumbler(scale=1.1)
        toy.move_to(DOWN * 0.5)

        # Ground line
        ground = Line(LEFT * 4, RIGHT * 4, color=SUBTLE_NAVY, stroke_width=2)
        ground.move_to(toy.get_bottom() + DOWN * 0.05)

        # Animations
        self.play(Write(title), run_time=1.0)
        self.play(FadeIn(question, shift=DOWN), run_time=0.8)
        self.play(FadeIn(ground), DrawBorderThenFill(toy), run_time=1.5)
        self.wait(0.3)

        # Push the toy (tilt and snap back)
        pivot = toy.get_bottom()
        self.play(Rotate(toy, angle=PI / 6, about_point=pivot), run_time=0.6)
        self.play(Rotate(toy, angle=-PI / 6, about_point=pivot), run_time=0.4)
        self.play(Rotate(toy, angle=-PI / 8, about_point=pivot), run_time=0.4)
        self.play(Rotate(toy, angle=PI / 8, about_point=pivot), run_time=0.3)
        self.wait(0.5)

        # Transition
        self.play(
            FadeOut(title), FadeOut(question), FadeOut(toy), FadeOut(ground),
            run_time=0.6
        )

    # ── Section 2 — Center of Mass ─────────────────────────────────
    def section_2_center_of_mass(self):
        # Section title
        sec_title = Text("Center of Mass", font_size=48, color=ELECTRIC_CYAN, weight=BOLD)
        sec_title.to_edge(UP, buff=0.7)

        # Explanation text
        desc = Text(
            "The heavy base keeps the\ncenter of mass LOW",
            font_size=26, color=WHITE, line_spacing=1.3
        )
        desc.next_to(sec_title, DOWN, buff=0.4)

        # Cross-section tumbler
        toy = build_tumbler(scale=1.3)
        toy.move_to(DOWN * 0.3)

        # Center of mass dot
        com_dot = Dot(color=VIBRANT_ORANGE, radius=0.12)
        com_pos = toy[6].get_center() + UP * 0.15  # just above the weight
        com_dot.move_to(com_pos)

        com_label = MathTex("CM", font_size=30, color=VIBRANT_ORANGE)
        com_label.next_to(com_dot, RIGHT, buff=0.2)

        # Dashed line to show height of CM
        dash = DashedLine(
            start=com_dot.get_center() + LEFT * 1.8,
            end=com_dot.get_center() + RIGHT * 1.8,
            color=VIBRANT_ORANGE, stroke_width=2
        )

        # Formula
        formula = MathTex(
            r"y_{cm} = \frac{\sum m_i \, y_i}{\sum m_i}",
            font_size=36, color=NEON_PINK
        )
        formula.to_edge(DOWN, buff=1.8)

        # Animations
        self.play(Write(sec_title), run_time=0.8)
        self.play(FadeIn(desc, shift=DOWN), run_time=0.7)
        self.play(DrawBorderThenFill(toy), run_time=1.2)
        self.play(
            FadeIn(com_dot, scale=2),
            Write(com_label),
            Create(dash),
            run_time=1.0
        )
        self.play(Write(formula), run_time=1.2)
        self.wait(1.5)

        # Transition
        self.play(
            *[FadeOut(m) for m in [sec_title, desc, toy, com_dot, com_label, dash, formula]],
            run_time=0.6
        )

    # ── Section 3 — Torque & Restoring Force ───────────────────────
    def section_3_torque(self):
        sec_title = Text("Restoring Torque", font_size=48, color=ELECTRIC_CYAN, weight=BOLD)
        sec_title.to_edge(UP, buff=0.7)

        # Tilted toy (simplified diagram)
        pivot = DOWN * 1.5
        toy = build_tumbler(scale=1.0)
        toy.move_to(pivot + UP * 1.2)
        toy.rotate(PI / 5, about_point=pivot)

        # Ground
        ground = Line(LEFT * 4, RIGHT * 4, color=SUBTLE_NAVY, stroke_width=2)
        ground.move_to(pivot)

        # Contact point
        contact = Dot(pivot, color=WHITE, radius=0.08)

        # Center of mass
        com_pos = toy[6].get_center() + UP * 0.15
        com_dot = Dot(com_pos, color=VIBRANT_ORANGE, radius=0.12)

        # Gravity arrow from CM
        gravity_arrow = Arrow(
            com_pos, com_pos + DOWN * 1.5,
            color=NEON_PINK, stroke_width=4, buff=0
        )
        g_label = MathTex("mg", font_size=28, color=NEON_PINK)
        g_label.next_to(gravity_arrow, RIGHT, buff=0.15)

        # Lever arm 'd' — horizontal distance from pivot to CM
        d_line = DashedLine(
            pivot, pivot + RIGHT * (com_pos[0] - pivot[0]),
            color=ELECTRIC_CYAN, stroke_width=3
        )
        # Vertical portion
        d_vert = DashedLine(
            pivot + RIGHT * (com_pos[0] - pivot[0]),
            com_pos,
            color=ELECTRIC_CYAN, stroke_width=3
        )
        d_label = MathTex("d", font_size=28, color=ELECTRIC_CYAN)
        d_label.next_to(d_line, DOWN, buff=0.15)

        # Angle theta
        angle_arc = Arc(
            radius=0.6, start_angle=PI / 2, angle=-PI / 2 + PI / 5,
            color=VIBRANT_ORANGE, stroke_width=3
        )
        angle_arc.move_arc_center_to(pivot)
        theta_label = MathTex(r"\theta", font_size=28, color=VIBRANT_ORANGE)
        theta_label.next_to(angle_arc, UP + RIGHT, buff=0.1)

        # Torque formula
        formula = MathTex(
            r"\tau = m g \cdot d \sin\theta",
            font_size=36, color=NEON_PINK
        )
        formula.to_edge(DOWN, buff=1.5)

        note = Text("→ always pushes back to center!", font_size=22, color=WHITE)
        note.next_to(formula, DOWN, buff=0.3)

        # Animations
        self.play(Write(sec_title), run_time=0.8)
        self.play(
            FadeIn(ground), FadeIn(contact),
            DrawBorderThenFill(toy),
            run_time=1.0
        )
        self.play(FadeIn(com_dot, scale=2), run_time=0.5)
        self.play(
            GrowArrow(gravity_arrow), Write(g_label),
            run_time=0.8
        )
        self.play(
            Create(d_line), Create(d_vert), Write(d_label),
            run_time=0.8
        )
        self.play(
            Create(angle_arc), Write(theta_label),
            run_time=0.7
        )
        self.play(Write(formula), run_time=1.0)
        self.play(FadeIn(note, shift=UP), run_time=0.6)
        self.wait(1.5)

        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=0.6
        )

    # ── Section 4 — Potential Energy ───────────────────────────────
    def section_4_potential_energy(self):
        sec_title = Text("Potential Energy", font_size=48, color=ELECTRIC_CYAN, weight=BOLD)
        sec_title.to_edge(UP, buff=0.7)

        desc = Text("Energy is lowest at the bottom", font_size=26, color=WHITE)
        desc.next_to(sec_title, DOWN, buff=0.35)

        # Create U(θ) plot
        axes = Axes(
            x_range=[-PI / 2, PI / 2, PI / 4],
            y_range=[0, 1.2, 0.5],
            x_length=6.0,
            y_length=3.5,
            axis_config={"color": WHITE, "stroke_width": 2},
            tips=False,
        )
        axes.move_to(DOWN * 0.5)

        x_label = MathTex(r"\theta", font_size=28, color=WHITE)
        x_label.next_to(axes.x_axis, RIGHT, buff=0.2)
        y_label = MathTex(r"U(\theta)", font_size=28, color=WHITE)
        y_label.next_to(axes.y_axis, UP, buff=0.2)

        # U(θ) = 1 - cos(θ)  (normalised)
        graph = axes.plot(
            lambda t: 1 - np.cos(t),
            x_range=[-PI / 2, PI / 2],
            color=NEON_PINK, stroke_width=3
        )

        # Dot that rolls along the curve
        tracker = ValueTracker(-PI / 3)
        dot = always_redraw(lambda: Dot(
            axes.c2p(tracker.get_value(), 1 - np.cos(tracker.get_value())),
            color=VIBRANT_ORANGE, radius=0.12
        ))

        # Minimum label
        min_label = MathTex(r"\text{min}", font_size=22, color=ELECTRIC_CYAN)
        min_label.next_to(axes.c2p(0, 0), DOWN, buff=0.25)

        # Formula
        formula = MathTex(
            r"U(\theta) = m g R (1 - \cos\theta)",
            font_size=34, color=NEON_PINK
        )
        formula.to_edge(DOWN, buff=1.3)

        # Animations
        self.play(Write(sec_title), run_time=0.8)
        self.play(FadeIn(desc, shift=DOWN), run_time=0.6)
        self.play(Create(axes), Write(x_label), Write(y_label), run_time=1.0)
        self.play(Create(graph), run_time=1.2)
        self.play(FadeIn(dot, scale=2), run_time=0.5)

        # Roll the dot
        self.play(tracker.animate.set_value(PI / 3), run_time=1.2, rate_func=smooth)
        self.play(tracker.animate.set_value(-PI / 4), run_time=1.0, rate_func=smooth)
        self.play(tracker.animate.set_value(0), run_time=0.8, rate_func=smooth)

        self.play(Write(min_label), run_time=0.4)
        self.play(Write(formula), run_time=1.0)
        self.wait(1.0)

        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=0.6
        )

    # ── Section 5 — Damped Oscillation ─────────────────────────────
    def section_5_damped_oscillation(self):
        sec_title = Text("Damped Oscillation", font_size=44, color=ELECTRIC_CYAN, weight=BOLD)
        sec_title.to_edge(UP, buff=0.7)

        desc = Text("It rocks less each time\nuntil it stops", font_size=24, color=WHITE,
                     line_spacing=1.3)
        desc.next_to(sec_title, DOWN, buff=0.35)

        # θ(t) vs t graph
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[-1, 1, 0.5],
            x_length=6.0,
            y_length=3.0,
            axis_config={"color": WHITE, "stroke_width": 2},
            tips=False,
        )
        axes.move_to(DOWN * 0.3)

        x_label = MathTex("t", font_size=28, color=WHITE)
        x_label.next_to(axes.x_axis, RIGHT, buff=0.2)
        y_label = MathTex(r"\theta(t)", font_size=28, color=WHITE)
        y_label.next_to(axes.y_axis, UP, buff=0.2)

        # Damped oscillation: θ₀ e^{-γt} cos(ωt)
        gamma = 0.5
        omega = 4.0
        theta0 = 0.8

        osc_graph = axes.plot(
            lambda t: theta0 * np.exp(-gamma * t) * np.cos(omega * t),
            x_range=[0, 6],
            color=NEON_PINK, stroke_width=3
        )

        # Envelope curves
        env_upper = axes.plot(
            lambda t: theta0 * np.exp(-gamma * t),
            x_range=[0, 6],
            color=VIBRANT_ORANGE, stroke_width=2, stroke_opacity=0.5
        )
        env_lower = axes.plot(
            lambda t: -theta0 * np.exp(-gamma * t),
            x_range=[0, 6],
            color=VIBRANT_ORANGE, stroke_width=2, stroke_opacity=0.5
        )

        # Formula
        formula = MathTex(
            r"\theta(t) = \theta_0 \, e^{-\gamma t} \cos(\omega t)",
            font_size=32, color=NEON_PINK
        )
        formula.to_edge(DOWN, buff=1.3)

        # Animations
        self.play(Write(sec_title), run_time=0.8)
        self.play(FadeIn(desc, shift=DOWN), run_time=0.6)
        self.play(Create(axes), Write(x_label), Write(y_label), run_time=1.0)
        self.play(
            Create(env_upper), Create(env_lower),
            run_time=0.8
        )
        self.play(Create(osc_graph), run_time=2.0)
        self.play(Write(formula), run_time=1.0)
        self.wait(1.5)

        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=0.6
        )

    # ── Section 6 — Outro / Summary ────────────────────────────────
    def section_6_outro(self):
        # Recap title
        title = Text("The Secret?", font_size=52, color=ELECTRIC_CYAN, weight=BOLD)
        title.to_edge(UP, buff=0.8)

        # Key bullet points
        bullets = VGroup(
            Text("① Low center of mass", font_size=28, color=WHITE),
            Text("② Restoring torque", font_size=28, color=WHITE),
            Text("③ Energy minimum at θ = 0", font_size=28, color=WHITE),
            Text("④ Damping stops oscillation", font_size=28, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=1.2)
        bullets.next_to(title, DOWN, buff=0.8)

        # Mini formulas
        formulas = VGroup(
            MathTex(r"y_{cm} = \frac{\sum m_i y_i}{\sum m_i}", font_size=26, color=NEON_PINK),
            MathTex(r"\tau = m g d \sin\theta", font_size=26, color=NEON_PINK),
            MathTex(r"U = m g R (1-\cos\theta)", font_size=26, color=NEON_PINK),
            MathTex(r"\theta(t)=\theta_0 e^{-\gamma t}\cos\omega t", font_size=26, color=NEON_PINK),
        )
        for f, b in zip(formulas, bullets):
            f.next_to(b, DOWN, buff=0.35, aligned_edge=LEFT)

        # Small tumbler at bottom rocking gently
        toy = build_tumbler(scale=0.7)
        toy.to_edge(DOWN, buff=1.0)
        pivot = toy.get_bottom()

        # Animations
        self.play(Write(title), run_time=0.8)
        for b, f in zip(bullets, formulas):
            self.play(FadeIn(b, shift=RIGHT), run_time=0.5)
            self.play(Write(f), run_time=0.5)

        self.play(DrawBorderThenFill(toy), run_time=0.8)

        # Gentle rocking loop
        for _ in range(3):
            self.play(
                Rotate(toy, angle=PI / 12, about_point=pivot),
                run_time=0.5, rate_func=smooth
            )
            self.play(
                Rotate(toy, angle=-PI / 12, about_point=pivot),
                run_time=0.5, rate_func=smooth
            )

        self.wait(1.5)
