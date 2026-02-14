from manim import *
import numpy as np

# ─── Vibrant Space Tech Color Palette ────────────────────────────────
DEEP_NAVY = "#020B1F"
ELECTRIC_CYAN = "#00F0FF"
NEON_PINK = "#FF0055"
VIBRANT_ORANGE = "#FF9F00"
SUBTLE_NAVY = "#1E2A45"
GRASS_GREEN = "#2ECC71"
GOAL_WHITE = "#F0F0F0"
GOLD = "#FFD700"
CELEBRATION_YELLOW = "#FFEB3B"

# YouTube Shorts Configuration (9:16 aspect ratio)
config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 14.0
config.frame_width = 14.0 * (1080 / 1920)  # ~7.875
config.background_color = DEEP_NAVY


# ─── Helper: build a soccer ball ────────────────────────────────────
def build_soccer_ball(radius=0.8, color=WHITE):
    """Return a VGroup representing a soccer ball with panel pattern."""
    ball = Circle(radius=radius, color=color, stroke_width=3)
    ball.set_fill(color, opacity=0.15)

    # Pentagon patterns on the ball surface
    panels = VGroup()
    pentagon_positions = [
        ORIGIN,
        UP * radius * 0.55,
        DOWN * radius * 0.55,
        LEFT * radius * 0.5 + UP * radius * 0.2,
        RIGHT * radius * 0.5 + UP * radius * 0.2,
        LEFT * radius * 0.5 + DOWN * radius * 0.2,
        RIGHT * radius * 0.5 + DOWN * radius * 0.2,
    ]
    for pos in pentagon_positions:
        p = RegularPolygon(n=5, color=SUBTLE_NAVY, stroke_width=1.5)
        p.scale(radius * 0.18)
        p.set_fill(SUBTLE_NAVY, opacity=0.6)
        p.move_to(pos)
        panels.add(p)

    soccer = VGroup(ball, panels)
    return soccer


def build_goal_front(width=5.0, height=3.5, center=ORIGIN):
    """Return a VGroup representing goal posts with net (front view)."""
    hw, hh = width / 2, height / 2
    base_y = center[1] - hh

    left_post = Line(
        np.array([center[0] - hw, base_y, 0]),
        np.array([center[0] - hw, center[1] + hh, 0]),
        color=GOAL_WHITE, stroke_width=6
    )
    right_post = Line(
        np.array([center[0] + hw, base_y, 0]),
        np.array([center[0] + hw, center[1] + hh, 0]),
        color=GOAL_WHITE, stroke_width=6
    )
    crossbar = Line(
        np.array([center[0] - hw, center[1] + hh, 0]),
        np.array([center[0] + hw, center[1] + hh, 0]),
        color=GOAL_WHITE, stroke_width=6
    )
    ground = Line(
        np.array([center[0] - hw - 0.5, base_y, 0]),
        np.array([center[0] + hw + 0.5, base_y, 0]),
        color=GRASS_GREEN, stroke_width=3
    )

    # Net mesh
    net = VGroup()
    step = 0.35
    nx = int(width / step)
    ny = int(height / step)
    for i in range(1, nx):
        x = center[0] - hw + i * step
        net.add(Line(
            np.array([x, base_y, 0]),
            np.array([x, center[1] + hh, 0]),
            color=GOAL_WHITE, stroke_width=0.7, stroke_opacity=0.25
        ))
    for j in range(1, ny):
        y = base_y + j * step
        net.add(Line(
            np.array([center[0] - hw, y, 0]),
            np.array([center[0] + hw, y, 0]),
            color=GOAL_WHITE, stroke_width=0.7, stroke_opacity=0.25
        ))

    goal = VGroup(net, ground, left_post, right_post, crossbar)
    return goal


def build_pitch_lines():
    """Return subtle pitch markings for atmosphere."""
    lines = VGroup()
    # Center circle
    cc = Circle(radius=1.0, color=GRASS_GREEN, stroke_width=1.5, stroke_opacity=0.3)
    # Center line
    cl = Line(UP * 7, DOWN * 7, color=GRASS_GREEN, stroke_width=1, stroke_opacity=0.15)
    lines.add(cc, cl)
    return lines


def create_star_burst(center, num_rays=12, inner_r=0.3, outer_r=1.5, color=GOLD):
    """Create a starburst celebration effect."""
    rays = VGroup()
    for i in range(num_rays):
        angle = i * TAU / num_rays
        start = center + inner_r * np.array([np.cos(angle), np.sin(angle), 0])
        end = center + outer_r * np.array([np.cos(angle), np.sin(angle), 0])
        ray = Line(start, end, color=color, stroke_width=3, stroke_opacity=0.8)
        rays.add(ray)
    return rays


# ─── Main Scene ─────────────────────────────────────────────────────
class SoccerSpinShort(Scene):
    """The Physics of a Goal ⚽ — YouTube Shorts Version"""

    def construct(self):
        self.section_1_intro()
        self.section_2_magnus_effect()
        self.section_3_curved_trajectory()
        self.section_4_angular_momentum()
        self.section_5_drag_and_decay()
        self.section_6_goal_moment()
        self.section_7_outro()

    # ── Section 1 — Intro ───────────────────────────────────────────
    def section_1_intro(self):
        # Title
        title = Text("The Physics of a Goal", font_size=50, color=ELECTRIC_CYAN, weight=BOLD)
        title.to_edge(UP, buff=0.8)

        question = Text("How does spin curve the ball?", font_size=30, color=WHITE)
        question.next_to(title, DOWN, buff=0.5)

        # Build goal at center-bottom
        goal = build_goal_front(width=5.0, height=3.0, center=DOWN * 2.0)

        # Ball starts from bottom-left corner
        ball = build_soccer_ball(radius=0.6)
        ball.move_to(LEFT * 3.5 + DOWN * 5.5)

        # Curved path — ball curves into the top corner of the goal
        path = CubicBezier(
            LEFT * 3.5 + DOWN * 5.5,
            LEFT * 2.0 + DOWN * 3.0,
            RIGHT * 0.0 + DOWN * 0.5,
            RIGHT * 1.5 + DOWN * 1.0,  # top-right corner of goal
        )
        path_trail = path.copy().set_color(NEON_PINK).set_stroke(width=2.5, opacity=0.4)

        # Animations
        self.play(Write(title), run_time=1.0)
        self.play(FadeIn(question, shift=DOWN), run_time=0.8)
        self.play(FadeIn(goal, shift=UP), run_time=1.0)
        self.play(FadeIn(ball, scale=0.5), run_time=0.4)

        # Ball curves into goal
        self.play(
            Create(path_trail),
            MoveAlongPath(ball, path),
            Rotate(ball, angle=6 * PI),
            run_time=2.0,
            rate_func=smooth
        )

        # Goal flash effect
        flash_rect = FullScreenRectangle(color=GOLD, fill_opacity=0.0, stroke_width=0)
        self.add(flash_rect)
        self.play(
            flash_rect.animate.set_fill(opacity=0.15),
            ball.animate.scale(1.3),
            run_time=0.25
        )
        self.play(
            flash_rect.animate.set_fill(opacity=0.0),
            ball.animate.scale(1 / 1.3),
            run_time=0.25
        )
        self.remove(flash_rect)
        self.wait(0.3)

        # Transition
        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=0.6
        )

    # ── Section 2 — Magnus Effect ───────────────────────────────────
    def section_2_magnus_effect(self):
        sec_title = Text("The Magnus Effect", font_size=46, color=ELECTRIC_CYAN, weight=BOLD)
        sec_title.to_edge(UP, buff=0.7)

        desc = Text(
            "Spin creates a pressure\ndifference → lateral force",
            font_size=24, color=WHITE, line_spacing=1.3
        )
        desc.next_to(sec_title, DOWN, buff=0.35)

        # Ball cross-section
        ball_center = DOWN * 0.3
        ball = Circle(radius=1.2, color=WHITE, stroke_width=3)
        ball.set_fill(WHITE, opacity=0.08)
        ball.move_to(ball_center)

        # Spin direction — curved arrow around ball
        spin_arc = Arc(
            radius=1.5, start_angle=PI / 4, angle=PI,
            color=VIBRANT_ORANGE, stroke_width=4
        )
        spin_arc.move_arc_center_to(ball_center)
        spin_tip = Triangle(color=VIBRANT_ORANGE, fill_color=VIBRANT_ORANGE, fill_opacity=1)
        spin_tip.scale(0.12)
        spin_tip.move_to(spin_arc.get_end())
        spin_tip.rotate(spin_arc.get_angle() + PI / 2)
        spin_label = MathTex(r"\omega", font_size=32, color=VIBRANT_ORANGE)
        spin_label.next_to(spin_arc, UP, buff=0.15)

        # Airflow arrows — top (faster, closely spaced)
        fast_arrows = VGroup()
        for i in range(5):
            x_start = -2.5 + i * 0.6
            arr = Arrow(
                np.array([x_start, ball_center[1] + 2.0, 0]),
                np.array([x_start + 1.2, ball_center[1] + 2.0, 0]),
                color=ELECTRIC_CYAN, stroke_width=3, buff=0,
                max_tip_length_to_length_ratio=0.2
            )
            fast_arrows.add(arr)
        fast_label = Text("Fast airflow", font_size=18, color=ELECTRIC_CYAN)
        fast_label.next_to(fast_arrows, UP, buff=0.15)

        # Airflow arrows — bottom (slower, wider spaced)
        slow_arrows = VGroup()
        for i in range(3):
            x_start = -1.8 + i * 0.9
            arr = Arrow(
                np.array([x_start, ball_center[1] - 2.0, 0]),
                np.array([x_start + 0.7, ball_center[1] - 2.0, 0]),
                color=NEON_PINK, stroke_width=3, buff=0,
                max_tip_length_to_length_ratio=0.2
            )
            slow_arrows.add(arr)
        slow_label = Text("Slow airflow", font_size=18, color=NEON_PINK)
        slow_label.next_to(slow_arrows, DOWN, buff=0.15)

        # Pressure labels
        low_p = Text("Low P", font_size=20, color=ELECTRIC_CYAN)
        low_p.next_to(ball, UP, buff=0.3)
        high_p = Text("High P", font_size=20, color=NEON_PINK)
        high_p.next_to(ball, DOWN, buff=0.3)

        # Magnus force arrow (perpendicular — upward)
        magnus_arrow = Arrow(
            ball_center, ball_center + UP * 2.0,
            color=GRASS_GREEN, stroke_width=5, buff=0.1,
            max_tip_length_to_length_ratio=0.15
        )
        fm_label = MathTex(r"\vec{F}_M", font_size=30, color=GRASS_GREEN)
        fm_label.next_to(magnus_arrow, RIGHT, buff=0.15)

        # Formula
        formula = MathTex(
            r"F_M = \frac{1}{2} C_L \, \rho \, A \, v^2",
            font_size=34, color=NEON_PINK
        )
        formula.to_edge(DOWN, buff=1.5)

        # Animations
        self.play(Write(sec_title), run_time=0.8)
        self.play(FadeIn(desc, shift=DOWN), run_time=0.7)
        self.play(DrawBorderThenFill(ball), run_time=0.8)
        self.play(
            Create(spin_arc), FadeIn(spin_tip), Write(spin_label),
            run_time=0.8
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in fast_arrows], lag_ratio=0.15),
            FadeIn(fast_label),
            run_time=1.0
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in slow_arrows], lag_ratio=0.15),
            FadeIn(slow_label),
            run_time=1.0
        )
        self.play(
            FadeIn(low_p, scale=1.3), FadeIn(high_p, scale=1.3),
            run_time=0.6
        )
        self.play(
            GrowArrow(magnus_arrow), Write(fm_label),
            run_time=0.8
        )
        self.play(Write(formula), run_time=1.2)
        self.wait(1.5)

        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=0.6
        )

    # ── Section 3 — Curved Free-Kick Trajectory ────────────────────
    def section_3_curved_trajectory(self):
        sec_title = Text("Curved Free Kick", font_size=46, color=ELECTRIC_CYAN, weight=BOLD)
        sec_title.to_edge(UP, buff=0.7)

        # Top-down pitch view axes
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[-3, 3, 1],
            x_length=6.5,
            y_length=5.0,
            axis_config={"color": WHITE, "stroke_width": 2},
            tips=False,
        )
        axes.move_to(DOWN * 0.5)

        x_label = Text("Distance", font_size=18, color=WHITE)
        x_label.next_to(axes.x_axis, DOWN, buff=0.2)
        y_label = Text("Lateral", font_size=18, color=WHITE)
        y_label.next_to(axes.y_axis, LEFT, buff=0.2)

        # Goal representation on graph — vertical line segment at x=10
        goal_line = Line(
            axes.c2p(10, 1.0), axes.c2p(10, 2.8),
            color=GOAL_WHITE, stroke_width=5
        )
        goal_cap_top = Dot(axes.c2p(10, 2.8), color=GOAL_WHITE, radius=0.08)
        goal_cap_bot = Dot(axes.c2p(10, 1.0), color=GOAL_WHITE, radius=0.08)
        goal_label = Text("GOAL", font_size=16, color=GOLD, weight=BOLD)
        goal_label.next_to(goal_line, RIGHT, buff=0.15)

        # Net behind goal (subtle)
        goal_net = VGroup()
        for j in range(5):
            y = 1.0 + j * 0.45
            goal_net.add(Line(
                axes.c2p(10, y), axes.c2p(10.5, y),
                color=GOAL_WHITE, stroke_width=0.5, stroke_opacity=0.2
            ))
        for i in range(3):
            x = 10 + i * 0.25
            goal_net.add(Line(
                axes.c2p(x, 1.0), axes.c2p(x, 2.8),
                color=GOAL_WHITE, stroke_width=0.5, stroke_opacity=0.2
            ))

        # Straight trajectory (no spin) — dashed
        straight_path = axes.plot(
            lambda x: 0, x_range=[0, 10],
            color=WHITE, stroke_width=2
        )
        straight_path = DashedVMobject(straight_path, num_dashes=20)
        no_spin_label = Text("No spin", font_size=16, color=WHITE)
        no_spin_label.next_to(axes.c2p(10, 0), RIGHT, buff=0.2)

        # Curved trajectory (with spin)
        def curved_y(x):
            return 2.2 * np.sin(x * PI / 10) * (x / 10) ** 0.8

        curved_path = axes.plot(
            curved_y, x_range=[0, 10],
            color=NEON_PINK, stroke_width=3
        )
        spin_label = Text("With spin", font_size=16, color=NEON_PINK)
        spin_label.next_to(axes.c2p(8, curved_y(8)), UP, buff=0.2)

        # Animated ball along curved path
        tracker = ValueTracker(0)
        ball_dot = always_redraw(lambda: Dot(
            axes.c2p(tracker.get_value(), curved_y(tracker.get_value())),
            color=VIBRANT_ORANGE, radius=0.15
        ))

        # Wall of defenders at x=3
        wall = VGroup()
        for k in range(3):
            defender = Rectangle(
                width=0.25, height=0.6,
                color=NEON_PINK, fill_color=NEON_PINK, fill_opacity=0.3,
                stroke_width=2
            )
            defender.move_to(axes.c2p(3, -0.6 + k * 0.65))
            wall.add(defender)
        wall_label = Text("Wall", font_size=14, color=NEON_PINK)
        wall_label.next_to(wall, DOWN, buff=0.15)

        # Formula
        formula = MathTex(
            r"\vec{a} = \vec{g} + \frac{\vec{F}_M}{m}",
            font_size=34, color=NEON_PINK
        )
        formula.to_edge(DOWN, buff=1.3)

        # Animations
        self.play(Write(sec_title), run_time=0.8)
        self.play(
            Create(axes), Write(x_label), Write(y_label),
            run_time=1.0
        )
        self.play(
            Create(goal_line), FadeIn(goal_cap_top), FadeIn(goal_cap_bot),
            FadeIn(goal_net), Write(goal_label),
            run_time=0.8
        )
        self.play(
            LaggedStart(*[FadeIn(d, scale=0.5) for d in wall], lag_ratio=0.15),
            FadeIn(wall_label),
            run_time=0.6
        )
        self.play(Create(straight_path), FadeIn(no_spin_label), run_time=0.8)
        self.play(Create(curved_path), FadeIn(spin_label), run_time=1.0)
        self.play(FadeIn(ball_dot, scale=2), run_time=0.4)

        # Ball travels along curve
        self.play(
            tracker.animate.set_value(10),
            run_time=2.5,
            rate_func=linear
        )

        # Goal flash when ball reaches the goal
        goal_flash = goal_line.copy().set_color(GOLD).set_stroke(width=10, opacity=0.6)
        self.play(
            FadeIn(goal_flash),
            goal_label.animate.set_color(CELEBRATION_YELLOW),
            run_time=0.3
        )
        self.play(FadeOut(goal_flash), run_time=0.3)

        self.play(Write(formula), run_time=1.0)
        self.wait(1.0)

        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=0.6
        )

    # ── Section 4 — Angular Momentum ───────────────────────────────
    def section_4_angular_momentum(self):
        sec_title = Text("Angular Momentum", font_size=44, color=ELECTRIC_CYAN, weight=BOLD)
        sec_title.to_edge(UP, buff=0.7)

        desc = Text(
            "Spin gives the ball\ngyroscopic stability",
            font_size=24, color=WHITE, line_spacing=1.3
        )
        desc.next_to(sec_title, DOWN, buff=0.35)

        # Ball in centre
        ball_center = DOWN * 0.2
        ball = build_soccer_ball(radius=1.0)
        ball.move_to(ball_center)

        # Spin axis — dashed vertical
        spin_axis = DashedLine(
            ball_center + DOWN * 1.8,
            ball_center + UP * 1.8,
            color=VIBRANT_ORANGE, stroke_width=2, dash_length=0.15
        )
        axis_label = Text("Spin axis", font_size=18, color=VIBRANT_ORANGE)
        axis_label.next_to(spin_axis, RIGHT, buff=0.15)

        # Angular velocity vector ω
        omega_arrow = Arrow(
            ball_center, ball_center + UP * 2.0,
            color=VIBRANT_ORANGE, stroke_width=4, buff=0.1,
            max_tip_length_to_length_ratio=0.15
        )
        omega_label = MathTex(r"\vec{\omega}", font_size=32, color=VIBRANT_ORANGE)
        omega_label.next_to(omega_arrow.get_end(), RIGHT, buff=0.15)

        # Angular momentum vector L
        L_arrow = Arrow(
            ball_center + RIGHT * 0.3,
            ball_center + UP * 2.5 + RIGHT * 0.3,
            color=GRASS_GREEN, stroke_width=4, buff=0.1,
            max_tip_length_to_length_ratio=0.15
        )
        L_label = MathTex(r"\vec{L}", font_size=32, color=GRASS_GREEN)
        L_label.next_to(L_arrow.get_end(), RIGHT, buff=0.15)

        # Orbit ring to visualise spin
        orbit_ring = Circle(radius=1.3, color=VIBRANT_ORANGE, stroke_width=1.5, stroke_opacity=0.3)
        orbit_ring.move_to(ball_center)

        # Formulas
        formula1 = MathTex(r"L = I \, \omega", font_size=36, color=NEON_PINK)
        formula2 = MathTex(r"I_{\text{sphere}} = \frac{2}{5} m r^2", font_size=34, color=NEON_PINK)
        formulas = VGroup(formula1, formula2).arrange(DOWN, buff=0.4)
        formulas.to_edge(DOWN, buff=1.3)

        note = Text("→ spin axis stays stable in flight!", font_size=20, color=WHITE)
        note.next_to(formulas, DOWN, buff=0.3)

        # Animations
        self.play(Write(sec_title), run_time=0.8)
        self.play(FadeIn(desc, shift=DOWN), run_time=0.6)
        self.play(DrawBorderThenFill(ball), run_time=1.0)
        self.play(Create(spin_axis), FadeIn(axis_label), run_time=0.6)
        self.play(FadeIn(orbit_ring), run_time=0.3)
        self.play(
            GrowArrow(omega_arrow), Write(omega_label),
            run_time=0.8
        )
        self.play(
            GrowArrow(L_arrow), Write(L_label),
            run_time=0.8
        )

        # Ball spinning with orbit ring pulsing
        self.play(
            Rotate(ball, angle=2 * PI, about_point=ball_center),
            orbit_ring.animate.set_stroke(opacity=0.7),
            run_time=1.5,
            rate_func=linear
        )
        self.play(orbit_ring.animate.set_stroke(opacity=0.3), run_time=0.3)

        self.play(Write(formula1), run_time=0.8)
        self.play(Write(formula2), run_time=0.8)
        self.play(FadeIn(note, shift=UP), run_time=0.5)
        self.wait(1.0)

        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=0.6
        )

    # ── Section 5 — Drag & Spin Decay ──────────────────────────────
    def section_5_drag_and_decay(self):
        sec_title = Text("Drag & Spin Decay", font_size=44, color=ELECTRIC_CYAN, weight=BOLD)
        sec_title.to_edge(UP, buff=0.7)

        desc = Text(
            "Air resistance slows the ball\nand reduces its spin",
            font_size=22, color=WHITE, line_spacing=1.3
        )
        desc.next_to(sec_title, DOWN, buff=0.35)

        # ω(t) graph
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 1.2, 0.5],
            x_length=6.0,
            y_length=3.0,
            axis_config={"color": WHITE, "stroke_width": 2},
            tips=False,
        )
        axes.move_to(DOWN * 0.5)

        x_label = MathTex("t", font_size=26, color=WHITE)
        x_label.next_to(axes.x_axis, RIGHT, buff=0.2)
        y_label = MathTex(r"\omega(t)", font_size=26, color=WHITE)
        y_label.next_to(axes.y_axis, UP, buff=0.2)

        beta = 0.5
        omega0 = 1.0

        decay_graph = axes.plot(
            lambda t: omega0 * np.exp(-beta * t),
            x_range=[0, 6],
            color=NEON_PINK, stroke_width=3
        )

        # ω₀ reference line
        omega0_line = DashedLine(
            axes.c2p(0, omega0), axes.c2p(6, omega0),
            color=VIBRANT_ORANGE, stroke_width=2, dash_length=0.15
        )
        omega0_label = MathTex(r"\omega_0", font_size=24, color=VIBRANT_ORANGE)
        omega0_label.next_to(axes.c2p(0, omega0), LEFT, buff=0.15)

        # Shaded area under curve
        area = axes.get_area(decay_graph, x_range=[0, 6], color=NEON_PINK, opacity=0.1)

        # Moving dot
        t_tracker = ValueTracker(0)
        trace_dot = always_redraw(lambda: Dot(
            axes.c2p(t_tracker.get_value(),
                     omega0 * np.exp(-beta * t_tracker.get_value())),
            color=VIBRANT_ORANGE, radius=0.1
        ))

        # Formulas
        drag_formula = MathTex(
            r"F_D = \frac{1}{2} C_D \, \rho \, A \, v^2",
            font_size=30, color=NEON_PINK
        )
        spin_formula = MathTex(
            r"\omega(t) = \omega_0 \, e^{-\beta t}",
            font_size=30, color=NEON_PINK
        )
        formulas = VGroup(drag_formula, spin_formula).arrange(DOWN, buff=0.35)
        formulas.to_edge(DOWN, buff=1.0)

        note = Text("Spin decays → curve straightens", font_size=20, color=WHITE)
        note.next_to(formulas, DOWN, buff=0.25)

        # Animations
        self.play(Write(sec_title), run_time=0.8)
        self.play(FadeIn(desc, shift=DOWN), run_time=0.6)
        self.play(
            Create(axes), Write(x_label), Write(y_label),
            run_time=1.0
        )
        self.play(
            Create(omega0_line), Write(omega0_label),
            run_time=0.6
        )
        self.play(Create(decay_graph), FadeIn(area), run_time=1.5)
        self.play(FadeIn(trace_dot, scale=2), run_time=0.4)
        self.play(
            t_tracker.animate.set_value(6),
            run_time=2.0,
            rate_func=linear
        )
        self.play(Write(drag_formula), run_time=0.8)
        self.play(Write(spin_formula), run_time=0.8)
        self.play(FadeIn(note, shift=UP), run_time=0.5)
        self.wait(1.0)

        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=0.6
        )

    # ── Section 6 — Goal Moment! ───────────────────────────────────
    def section_6_goal_moment(self):
        """Full side-view free kick → goal with celebration."""
        sec_title = Text("The Perfect Goal", font_size=48, color=GOLD, weight=BOLD)
        sec_title.to_edge(UP, buff=0.7)

        # Build front-view goal
        goal_center = RIGHT * 0.0 + UP * 0.5
        goal = build_goal_front(width=5.5, height=3.5, center=goal_center)

        # Grass field
        grass = Rectangle(
            width=config.frame_width + 1, height=3.0,
            color=GRASS_GREEN, fill_color=GRASS_GREEN, fill_opacity=0.08,
            stroke_width=0
        )
        grass.move_to(DOWN * 4.0)

        # Ball — start small (far away), will scale up
        ball = build_soccer_ball(radius=0.25)
        ball.move_to(DOWN * 3.0)

        # Velocity and spin labels
        v_label = MathTex(r"v = 30\,\text{m/s}", font_size=22, color=ELECTRIC_CYAN)
        v_label.next_to(ball, DOWN, buff=0.3)
        spin_info = MathTex(r"\omega = 10\,\text{rad/s}", font_size=22, color=VIBRANT_ORANGE)
        spin_info.next_to(v_label, DOWN, buff=0.2)

        # Trajectory: ball flies from bottom-center, curves to top-right corner
        kick_path = CubicBezier(
            DOWN * 3.0,
            DOWN * 1.5 + LEFT * 0.8,
            UP * 0.5 + RIGHT * 1.2,
            goal_center + RIGHT * 1.8 + UP * 1.0,  # top-right corner
        )
        trail = TracedPath(
            ball.get_center,
            stroke_color=NEON_PINK,
            stroke_width=2.5,
            stroke_opacity=0.5
        )

        # "GOAL!" celebration text
        goal_text = Text("GOAL!", font_size=72, color=GOLD, weight=BOLD)
        goal_text.move_to(UP * 4.5)

        # Starburst effect
        burst = create_star_burst(
            center=goal_center + RIGHT * 1.8 + UP * 1.0,
            num_rays=16, inner_r=0.2, outer_r=2.0, color=GOLD
        )

        # Celebration particles
        particles = VGroup()
        np.random.seed(42)
        for _ in range(20):
            dot = Dot(
                point=goal_center + np.array([
                    np.random.uniform(-3, 3),
                    np.random.uniform(-2, 3),
                    0
                ]),
                radius=np.random.uniform(0.03, 0.08),
                color=np.random.choice([GOLD, CELEBRATION_YELLOW, ELECTRIC_CYAN, NEON_PINK]),
            )
            particles.add(dot)

        # Net ripple lines (radiate from hit point)
        ripple1 = Circle(
            radius=0.3, color=GOAL_WHITE, stroke_width=2, stroke_opacity=0.6
        ).move_to(goal_center + RIGHT * 1.8 + UP * 1.0)
        ripple2 = ripple1.copy()
        ripple3 = ripple1.copy()

        # Animations
        self.play(Write(sec_title), run_time=0.8)
        self.play(FadeIn(grass), FadeIn(goal, shift=DOWN * 0.3), run_time=1.0)
        self.play(
            FadeIn(ball, scale=0.3),
            FadeIn(v_label), FadeIn(spin_info),
            run_time=0.6
        )
        self.wait(0.3)

        # Kick! — ball flies along path, scaling up as it approaches
        self.add(trail)
        self.play(
            FadeOut(v_label), FadeOut(spin_info),
            run_time=0.2
        )
        self.play(
            MoveAlongPath(ball, kick_path),
            ball.animate.scale(3.0),
            Rotate(ball, angle=8 * PI),
            run_time=1.8,
            rate_func=rate_functions.ease_in_quad
        )

        # === GOAL CELEBRATION ===
        # Net ripple
        self.play(
            ripple1.animate.scale(4).set_stroke(opacity=0),
            ripple2.animate.scale(6).set_stroke(opacity=0),
            ripple3.animate.scale(8).set_stroke(opacity=0),
            run_time=0.8,
            rate_func=linear
        )
        self.remove(ripple1, ripple2, ripple3)

        # Flash
        flash = FullScreenRectangle(color=GOLD, fill_opacity=0.0, stroke_width=0)
        self.add(flash)
        self.play(
            flash.animate.set_fill(opacity=0.2),
            run_time=0.15
        )
        self.play(
            flash.animate.set_fill(opacity=0.0),
            run_time=0.15
        )
        self.remove(flash)

        # Starburst + GOAL text
        self.play(
            FadeIn(burst, scale=0.3),
            FadeIn(goal_text, scale=0.5),
            run_time=0.5
        )
        # Starburst expands and fades
        self.play(
            burst.animate.scale(1.5).set_stroke(opacity=0),
            run_time=0.8,
            rate_func=smooth
        )
        self.remove(burst)

        # Confetti particles float in
        self.play(
            LaggedStart(
                *[FadeIn(p, shift=DOWN * np.random.uniform(0.5, 2.0))
                  for p in particles],
                lag_ratio=0.05
            ),
            run_time=1.0
        )
        self.wait(0.5)

        # Particles drift and fade
        self.play(
            *[p.animate.shift(DOWN * np.random.uniform(0.5, 1.5)).set_opacity(0)
              for p in particles],
            FadeOut(goal_text),
            run_time=1.0
        )

        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=0.6
        )

    # ── Section 7 — Outro / Summary ────────────────────────────────
    def section_7_outro(self):
        # Title
        title = Text("The Science of a Goal", font_size=48, color=ELECTRIC_CYAN, weight=BOLD)
        title.to_edge(UP, buff=0.8)

        # Key bullet points
        bullets = VGroup(
            Text("① Magnus Effect", font_size=26, color=WHITE),
            Text("② Curved Trajectory", font_size=26, color=WHITE),
            Text("③ Angular Momentum", font_size=26, color=WHITE),
            Text("④ Drag & Spin Decay", font_size=26, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=1.1)
        bullets.next_to(title, DOWN, buff=0.7)

        # Mini formulas
        formulas = VGroup(
            MathTex(r"F_M = \tfrac{1}{2}C_L \rho A v^2", font_size=24, color=NEON_PINK),
            MathTex(r"\vec{a} = \vec{g} + \frac{\vec{F}_M}{m}", font_size=24, color=NEON_PINK),
            MathTex(r"L = I\omega", font_size=24, color=NEON_PINK),
            MathTex(r"\omega(t) = \omega_0 e^{-\beta t}", font_size=24, color=NEON_PINK),
        )
        for f, b in zip(formulas, bullets):
            f.next_to(b, DOWN, buff=0.3, aligned_edge=LEFT)

        # Small goal + ball at bottom
        mini_goal = build_goal_front(width=3.0, height=2.0, center=DOWN * 4.5)
        mini_ball = build_soccer_ball(radius=0.35)
        mini_ball.move_to(DOWN * 4.5)

        # Animations
        self.play(Write(title), run_time=0.8)
        for b, f in zip(bullets, formulas):
            self.play(FadeIn(b, shift=RIGHT), run_time=0.45)
            self.play(Write(f), run_time=0.45)

        self.play(FadeIn(mini_goal), DrawBorderThenFill(mini_ball), run_time=0.8)

        # Gentle ball rock
        center_pt = mini_ball.get_center()
        for _ in range(3):
            self.play(
                Rotate(mini_ball, angle=PI / 3, about_point=center_pt),
                run_time=0.5, rate_func=smooth
            )
            self.play(
                Rotate(mini_ball, angle=-PI / 3, about_point=center_pt),
                run_time=0.5, rate_func=smooth
            )

        self.wait(1.5)
