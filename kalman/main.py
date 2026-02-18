from manim import *
import numpy as np

# ========================== COLOR PALETTE ==========================
DEEP_NAVY = "#020B1F"
TECH_CYAN = "#00F0FF"
NEON_PINK = "#FF0055"
VIBRANT_ORANGE = "#FF9F00"
TEXT_WHITE = "#FFFFFF"
SUBTLE_NAVY = "#1E2A45"

config.background_color = DEEP_NAVY


# ========================== PART 1: THE HOOK (3-6s) ==========================
class Part1(Scene):
    """Instant Hook - KALMAN FILTER title splash"""
    def construct(self):
        # Glitch-style title
        title = Text("KALMAN FILTER", font_size=96, color=TECH_CYAN, weight=BOLD)
        subtitle = Text("See Through the Noise", font_size=42, color=NEON_PINK)
        subtitle.next_to(title, DOWN, buff=0.3)

        # Expanding pulse rings
        pulse_rings = VGroup(*[
            Circle(radius=0.5 + i * 0.7, stroke_width=4 - i * 0.6,
                   color=TECH_CYAN, stroke_opacity=1 - i * 0.18)
            for i in range(5)
        ]).move_to(ORIGIN)

        # Noisy dots scatter (representing noisy measurements)
        np.random.seed(42)
        dots = VGroup(*[
            Dot(point=[np.random.normal(0, 1.5), np.random.normal(0, 1), 0],
                radius=0.04, color=NEON_PINK, fill_opacity=0.7)
            for _ in range(60)
        ])

        # Flash in title
        self.play(FadeIn(title, scale=1.5), run_time=0.5)
        self.play(
            FadeIn(subtitle, shift=UP * 0.3),
            LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.02),
            run_time=0.8
        )

        # Pulse rings expand outward
        for ring in pulse_rings:
            self.add(ring)
            self.play(ring.animate.scale(3).set_opacity(0), run_time=0.3)
            self.remove(ring)

        # Flash
        flash = Rectangle(width=20, height=12, fill_color=TECH_CYAN,
                          fill_opacity=0.3, stroke_width=0)
        self.play(FadeIn(flash), run_time=0.2)
        self.play(FadeOut(flash), FadeOut(dots), run_time=0.2)
        self.wait(0.3)


# ========================== PART 2: THE NOISY WORLD (15-20s) ==========================
class Part2(Scene):
    """The Problem: Noisy Measurements"""
    def construct(self):
        title = Text("THE PROBLEM: A NOISY WORLD", font_size=48, color=TECH_CYAN)
        title.to_edge(UP, buff=0.4)

        # True position line (smooth sinusoid)
        axes = Axes(
            x_range=[0, 10, 1], y_range=[-3, 3, 1],
            x_length=10, y_length=5,
            axis_config={"color": SUBTLE_NAVY, "stroke_width": 2},
        ).move_to(DOWN * 0.3)

        x_label = axes.get_x_axis_label(Text("Time", font_size=24, color=TEXT_WHITE))
        y_label = axes.get_y_axis_label(Text("Position", font_size=24, color=TEXT_WHITE))

        true_curve = axes.plot(lambda x: 2 * np.sin(0.8 * x), x_range=[0, 10],
                               color=TECH_CYAN, stroke_width=4)
        true_label = Text("True Position", font_size=22, color=TECH_CYAN)
        true_label.next_to(axes, RIGHT, buff=0.3).shift(UP)

        # Noisy measurement dots
        np.random.seed(7)
        noisy_x = np.linspace(0.5, 9.5, 30)
        noisy_y = [2 * np.sin(0.8 * x) + np.random.normal(0, 0.6) for x in noisy_x]
        noisy_dots = VGroup(*[
            Dot(axes.c2p(x, y), radius=0.06, color=NEON_PINK, fill_opacity=0.8)
            for x, y in zip(noisy_x, noisy_y)
        ])
        noisy_label = Text("Noisy Measurements", font_size=22, color=NEON_PINK)
        noisy_label.next_to(true_label, DOWN, buff=0.15).shift(LEFT * 0.5)

        question = Text("How do we find the TRUTH in all this noise?",
                         font_size=28, color=VIBRANT_ORANGE)
        question.to_edge(DOWN, buff=0.5)

        # Animations
        self.play(Write(title), run_time=1)
        self.play(Create(axes), Write(x_label), Write(y_label), run_time=2)
        self.wait(0.5)

        self.play(Create(true_curve), Write(true_label), run_time=3)
        self.wait(1)

        self.play(
            LaggedStart(*[FadeIn(d, scale=0.5) for d in noisy_dots], lag_ratio=0.06),
            run_time=3
        )
        self.play(Write(noisy_label), run_time=1)
        self.wait(1.5)

        self.play(Write(question), run_time=1.5)
        self.wait(3)


# ========================== PART 3: WHY SENSORS LIE (15-20s) ==========================
class Part3(Scene):
    """Visualize different sensors and their noise profiles"""
    def construct(self):
        title = Text("WHY SENSORS LIE", font_size=48, color=TECH_CYAN)
        title.to_edge(UP, buff=0.4)

        sensors = [
            ("GPS", "±3-5 meters", TECH_CYAN, 0.5),
            ("Accelerometer", "Drift over time", NEON_PINK, 0.3),
            ("Gyroscope", "Bias & jitter", VIBRANT_ORANGE, 0.4),
        ]

        cards = VGroup()
        for name, noise_desc, color, noise_amp in sensors:
            card_bg = RoundedRectangle(width=3.5, height=4.2, corner_radius=0.15,
                                        fill_color=SUBTLE_NAVY, fill_opacity=0.9,
                                        stroke_color=color, stroke_width=3)
            sensor_name = Text(name, font_size=28, color=color, weight=BOLD)
            sensor_name.next_to(card_bg.get_top(), DOWN, buff=0.3)

            noise_text = Text(noise_desc, font_size=18, color=TEXT_WHITE)
            noise_text.next_to(sensor_name, DOWN, buff=0.2)

            # Mini signal graph
            mini_axes = Axes(x_range=[0, 4, 1], y_range=[-1.5, 1.5, 0.5],
                             x_length=2.8, y_length=2,
                             axis_config={"color": SUBTLE_NAVY, "stroke_width": 1})
            mini_axes.next_to(noise_text, DOWN, buff=0.3)

            np.random.seed(hash(name) % 100)
            true_line = mini_axes.plot(lambda x: np.sin(x * 2), x_range=[0, 4],
                                       color=WHITE, stroke_width=2)
            noisy_line = mini_axes.plot(
                lambda x, a=noise_amp: np.sin(x * 2) + np.random.normal(0, a),
                x_range=[0, 4], color=color, stroke_width=2, use_smoothing=False
            )

            card = VGroup(card_bg, sensor_name, noise_text, mini_axes, true_line, noisy_line)
            cards.add(card)

        cards.arrange(RIGHT, buff=0.5).move_to(DOWN * 0.2)

        conclusion = Text("Every sensor has a different type of error!",
                          font_size=26, color=VIBRANT_ORANGE)
        conclusion.to_edge(DOWN, buff=0.4)

        # Animations
        self.play(Write(title), run_time=1)
        self.wait(0.5)

        for card in cards:
            self.play(FadeIn(card, shift=UP * 0.5), run_time=1.2)
            self.wait(1)

        self.play(Write(conclusion), run_time=1.5)
        self.wait(3)


# ========================== PART 4: THE CHALLENGE (15-20s) ==========================
class Part4(Scene):
    """A drone navigating with noisy data — wobbly path"""
    def construct(self):
        title = Text("THE NAVIGATION CHALLENGE", font_size=48, color=TECH_CYAN)
        title.to_edge(UP, buff=0.4)

        # Create a grid background
        grid = NumberPlane(
            x_range=[-7, 7, 1], y_range=[-4, 4, 1],
            background_line_style={"stroke_color": SUBTLE_NAVY, "stroke_width": 1}
        )

        # True path (smooth)
        true_path = VMobject(color=TECH_CYAN, stroke_width=4)
        true_pts = [[-5, -2, 0], [-3, -1, 0], [-1, 0.5, 0], [1, 1, 0],
                    [3, 0.5, 0], [5, 1.5, 0]]
        true_path.set_points_smoothly([np.array(p) for p in true_pts])
        true_label = Text("Ideal Path", font_size=20, color=TECH_CYAN)
        true_label.next_to(true_path.get_end(), UP, buff=0.2)

        # Noisy path (wobbly)
        np.random.seed(12)
        noisy_pts = [[p[0], p[1] + np.random.normal(0, 0.5), 0] for p in true_pts]
        # Add more intermediate noisy points
        detailed_noisy = []
        for i in range(len(true_pts) - 1):
            for t in np.linspace(0, 1, 5):
                x = true_pts[i][0] * (1 - t) + true_pts[i+1][0] * t
                y = true_pts[i][1] * (1 - t) + true_pts[i+1][1] * t + np.random.normal(0, 0.4)
                detailed_noisy.append([x, y, 0])
        noisy_path = VMobject(color=NEON_PINK, stroke_width=3, stroke_opacity=0.8)
        noisy_path.set_points_smoothly([np.array(p) for p in detailed_noisy])
        noisy_label = Text("Measured Path", font_size=20, color=NEON_PINK)
        noisy_label.next_to(noisy_path.get_end(), DOWN, buff=0.2)

        # Drone icon
        drone = VGroup(
            Circle(radius=0.2, color=VIBRANT_ORANGE, fill_opacity=0.8, stroke_width=2),
            Line(LEFT * 0.35, RIGHT * 0.35, color=VIBRANT_ORANGE, stroke_width=3),
            Line(UP * 0.35, DOWN * 0.35, color=VIBRANT_ORANGE, stroke_width=3),
        )
        drone.move_to(true_pts[0])

        question = Text("Can we combine noisy sensors to get a smooth, accurate path?",
                         font_size=24, color=VIBRANT_ORANGE)
        question.to_edge(DOWN, buff=0.5)

        # Animations
        self.play(Write(title), run_time=1)
        self.play(FadeIn(grid), run_time=1)
        self.wait(0.5)

        self.play(Create(true_path), Write(true_label), run_time=2.5)
        self.wait(0.5)
        self.play(Create(noisy_path), Write(noisy_label), run_time=2.5)
        self.wait(1)

        self.play(FadeIn(drone), run_time=0.5)
        self.play(MoveAlongPath(drone, noisy_path), run_time=4, rate_func=linear)
        self.wait(0.5)

        self.play(Write(question), run_time=1.5)
        self.wait(3)


# ========================== PART 5: WHAT IF WE COULD PREDICT? (15-20s) ==========================
class Part5(Scene):
    """Introduce the core idea: Model + Measurements"""
    def construct(self):
        title = Text("WHAT IF WE COULD PREDICT?", font_size=48, color=TECH_CYAN)
        title.to_edge(UP, buff=0.4)

        # Left side: Physical Model
        model_box = RoundedRectangle(width=5, height=5, corner_radius=0.2,
                                      fill_color=SUBTLE_NAVY, fill_opacity=0.8,
                                      stroke_color=TECH_CYAN, stroke_width=3)
        model_box.move_to(LEFT * 3.2 + DOWN * 0.3)
        model_title = Text("PHYSICAL MODEL", font_size=26, color=TECH_CYAN, weight=BOLD)
        model_title.next_to(model_box.get_top(), DOWN, buff=0.3)

        model_desc = VGroup(
            Text("\"I know the physics\"", font_size=20, color=TEXT_WHITE),
            MathTex(r"x_{k+1} = F \cdot x_k + B \cdot u_k", font_size=36, color=TECH_CYAN),
            Text("Smooth but drifts", font_size=18, color=VIBRANT_ORANGE),
        ).arrange(DOWN, buff=0.3)
        model_desc.move_to(model_box.get_center() + DOWN * 0.2)

        # Right side: Sensor Measurement
        sensor_box = RoundedRectangle(width=5, height=5, corner_radius=0.2,
                                       fill_color=SUBTLE_NAVY, fill_opacity=0.8,
                                       stroke_color=NEON_PINK, stroke_width=3)
        sensor_box.move_to(RIGHT * 3.2 + DOWN * 0.3)
        sensor_title = Text("SENSOR DATA", font_size=26, color=NEON_PINK, weight=BOLD)
        sensor_title.next_to(sensor_box.get_top(), DOWN, buff=0.3)

        sensor_desc = VGroup(
            Text("\"I measure reality\"", font_size=20, color=TEXT_WHITE),
            MathTex(r"z_k = H \cdot x_k + v_k", font_size=36, color=NEON_PINK),
            Text("Noisy but grounded", font_size=18, color=VIBRANT_ORANGE),
        ).arrange(DOWN, buff=0.3)
        sensor_desc.move_to(sensor_box.get_center() + DOWN * 0.2)

        # Plus sign and result
        plus = Text("+", font_size=72, color=VIBRANT_ORANGE)
        plus.move_to(DOWN * 0.3)

        result_box = RoundedRectangle(width=8, height=1.5, corner_radius=0.15,
                                       fill_color=SUBTLE_NAVY, fill_opacity=0.9,
                                       stroke_color=VIBRANT_ORANGE, stroke_width=3)
        result_box.to_edge(DOWN, buff=0.3)
        result_text = Text("= KALMAN FILTER: The Optimal Estimate",
                           font_size=28, color=VIBRANT_ORANGE, weight=BOLD)
        result_text.move_to(result_box.get_center())

        # Animations
        self.play(Write(title), run_time=1)
        self.wait(0.5)

        self.play(FadeIn(model_box), Write(model_title), run_time=1)
        self.play(FadeIn(model_desc), run_time=1.5)
        self.wait(1)

        self.play(FadeIn(sensor_box), Write(sensor_title), run_time=1)
        self.play(FadeIn(sensor_desc), run_time=1.5)
        self.wait(1)

        self.play(FadeIn(plus, scale=1.5), run_time=0.8)
        self.wait(0.5)

        self.play(FadeIn(result_box), Write(result_text), run_time=1.5)
        self.wait(3)


# ========================== PART 6: STATE VECTOR (15-20s) ==========================
class Part6(Scene):
    """Define the state vector x = [position, velocity]"""
    def construct(self):
        title = Text("THE STATE VECTOR", font_size=48, color=TECH_CYAN)
        title.to_edge(UP, buff=0.4)

        subtitle = Text("Everything the filter needs to know", font_size=28, color=TEXT_WHITE)
        subtitle.next_to(title, DOWN, buff=0.2)

        # State vector display
        state_vec = MathTex(
            r"\mathbf{x} = \begin{bmatrix} \text{position} \\ \text{velocity} \end{bmatrix}",
            font_size=56
        )
        state_vec.set_color(TEXT_WHITE)
        state_vec.set_color_by_tex("mathbf{x}", TECH_CYAN)
        state_vec.set_color_by_tex("position", TECH_CYAN)
        state_vec.set_color_by_tex("velocity", NEON_PINK)
        state_vec.move_to(LEFT * 3 + UP * 0.5)
        

        # Visual representation — a car on a number line
        number_line = NumberLine(x_range=[0, 10, 1], length=8,
                                 color=SUBTLE_NAVY, stroke_width=3,
                                 include_numbers=True)
        number_line.move_to(DOWN * 1.5)
        number_line.numbers.set_color(TEXT_WHITE)

        car = VGroup(
            RoundedRectangle(width=0.8, height=0.4, corner_radius=0.08,
                              fill_color=VIBRANT_ORANGE, fill_opacity=1,
                              stroke_color=VIBRANT_ORANGE, stroke_width=2),
            Circle(radius=0.08, color=TEXT_WHITE, fill_opacity=1).shift(LEFT * 0.25 + DOWN * 0.2),
            Circle(radius=0.08, color=TEXT_WHITE, fill_opacity=1).shift(RIGHT * 0.25 + DOWN * 0.2),
        )
        car.move_to(number_line.n2p(2) + UP * 0.4)

        pos_arrow = Arrow(car.get_bottom(), number_line.n2p(2),
                          color=TECH_CYAN, stroke_width=3, max_tip_length_to_length_ratio=0.2)
        pos_label = Text("Position = 2", font_size=20, color=TECH_CYAN)
        pos_label.next_to(pos_arrow, RIGHT, buff=0.2)

        vel_arrow = Arrow(car.get_right(), car.get_right() + RIGHT * 1.5,
                          color=NEON_PINK, stroke_width=3)
        vel_label = Text("Velocity = 3 m/s", font_size=20, color=NEON_PINK)
        vel_label.next_to(vel_arrow, UP, buff=0.1)

        # Example state
        example = MathTex(
            r"\mathbf{x} = \begin{bmatrix} 2 \\ 3 \end{bmatrix}",
            font_size=48, color=VIBRANT_ORANGE
        )
        example.move_to(RIGHT * 3.5 + UP * 0.5)

        # Animations
        self.play(Write(title), FadeIn(subtitle), run_time=1.2)
        self.wait(1)

        self.play(Write(state_vec), run_time=2.5)
        self.wait(1.5)

        self.play(Create(number_line), run_time=1.5)
        self.play(FadeIn(car, shift=DOWN * 0.3), run_time=1)
        self.play(GrowArrow(pos_arrow), Write(pos_label), run_time=1)
        self.play(GrowArrow(vel_arrow), Write(vel_label), run_time=1)
        self.wait(1)

        self.play(Write(example), run_time=1.5)
        self.wait(1)

        # Animate car moving
        self.play(
            car.animate.move_to(number_line.n2p(5) + UP * 0.4),
            run_time=3, rate_func=linear
        )
        self.wait(2)


# ========================== PART 7: THE PREDICTION STEP (15-20s) ==========================
class Part7(Scene):
    """Predict equation: x_hat = F*x + B*u"""
    def construct(self):
        title = Text("THE PREDICTION STEP", font_size=48, color=TECH_CYAN)
        title.to_edge(UP, buff=0.4)

        subtitle = Text("\"Where do I THINK I will be next?\"", font_size=26, color=TEXT_WHITE)
        subtitle.next_to(title, DOWN, buff=0.2)

        # Prediction equation
        predict_eq = MathTex(
            r"\hat{x}_{k+1}", r"=", r"F", r"\cdot", r"x_k", r"+", r"B", r"\cdot", r"u_k",
            font_size=52
        )
        predict_eq[0].set_color(VIBRANT_ORANGE)
        predict_eq[2].set_color(TECH_CYAN)
        predict_eq[4].set_color(TECH_CYAN)
        predict_eq[6].set_color(NEON_PINK)
        predict_eq[8].set_color(NEON_PINK)
        predict_eq.move_to(UP * 0.5)

        # Labels below equation
        labels = VGroup(
            VGroup(
                Text("F", font_size=22, color=TECH_CYAN, weight=BOLD),
                Text("= State Transition Matrix", font_size=18, color=TEXT_WHITE),
            ).arrange(RIGHT, buff=0.15),
            VGroup(
                Text("B", font_size=22, color=NEON_PINK, weight=BOLD),
                Text("= Control Input Matrix", font_size=18, color=TEXT_WHITE),
            ).arrange(RIGHT, buff=0.15),
            VGroup(
                Text("u", font_size=22, color=NEON_PINK, weight=BOLD),
                Text("= Control Input (e.g., throttle)", font_size=18, color=TEXT_WHITE),
            ).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        labels.next_to(predict_eq, DOWN, buff=0.6)

        # Visual: timeline with predicted next position
        timeline = Line(LEFT * 5, RIGHT * 5, color=SUBTLE_NAVY, stroke_width=3)
        timeline.to_edge(DOWN, buff=1.5)

        t0_dot = Dot(timeline.get_start() + RIGHT * 2, radius=0.12, color=TECH_CYAN)
        t0_label = Text("Now (k)", font_size=18, color=TECH_CYAN)
        t0_label.next_to(t0_dot, DOWN, buff=0.2)

        t1_dot = Dot(timeline.get_start() + RIGHT * 7, radius=0.12, color=VIBRANT_ORANGE)
        t1_label = Text("Predicted (k+1)", font_size=18, color=VIBRANT_ORANGE)
        t1_label.next_to(t1_dot, DOWN, buff=0.2)

        predict_arrow = Arrow(t0_dot.get_center(), t1_dot.get_center(),
                              color=VIBRANT_ORANGE, stroke_width=3,
                              buff=0.2)

        # Animations
        self.play(Write(title), FadeIn(subtitle), run_time=1.2)
        self.wait(1)

        self.play(Write(predict_eq), run_time=3)
        self.wait(1.5)

        self.play(FadeIn(labels), run_time=2)
        self.wait(1)

        self.play(Create(timeline), run_time=1)
        self.play(FadeIn(t0_dot), Write(t0_label), run_time=0.8)
        self.play(GrowArrow(predict_arrow), run_time=1.5)
        self.play(FadeIn(t1_dot), Write(t1_label), run_time=0.8)

        self.wait(3)


# ========================== PART 8: PREDICTION UNCERTAINTY (15-20s) ==========================
class Part8(Scene):
    """Covariance P grows with each prediction — expanding ellipse"""
    def construct(self):
        title = Text("PREDICTION UNCERTAINTY", font_size=48, color=TECH_CYAN)
        title.to_edge(UP, buff=0.4)

        subtitle = Text("Uncertainty GROWS when we only predict", font_size=26, color=NEON_PINK)
        subtitle.next_to(title, DOWN, buff=0.2)

        # Covariance equation
        cov_eq = MathTex(
            r"P_{k+1|k}", r"=", r"F", r"P_k", r"F^T", r"+", r"Q",
            font_size=48
        )
        cov_eq[0].set_color(VIBRANT_ORANGE)
        cov_eq[2].set_color(TECH_CYAN)
        cov_eq[3].set_color(TECH_CYAN)
        cov_eq[4].set_color(TECH_CYAN)
        cov_eq[6].set_color(NEON_PINK)
        cov_eq.move_to(UP * 1.8)

        q_label = Text("Q = Process Noise Covariance", font_size=20, color=NEON_PINK)
        q_label.next_to(cov_eq, DOWN, buff=0.3)

        # Animated growing ellipse
        center = DOWN * 0.5
        true_dot = Dot(center, radius=0.1, color=VIBRANT_ORANGE)
        true_label = Text("True State", font_size=18, color=VIBRANT_ORANGE)
        true_label.next_to(true_dot, DOWN, buff=0.15)

        # Time steps with growing ellipses
        steps_label = Text("Each prediction step adds uncertainty...",
                           font_size=22, color=TEXT_WHITE)
        steps_label.to_edge(DOWN, buff=0.4)

        # Animations
        self.play(Write(title), FadeIn(subtitle), run_time=1.2)
        self.wait(0.5)

        self.play(Write(cov_eq), run_time=2)
        self.play(Write(q_label), run_time=1)
        self.wait(1)

        self.play(FadeIn(true_dot), Write(true_label), run_time=0.8)

        # Growing ellipses
        ellipses = VGroup()
        for i in range(1, 6):
            ellipse = Ellipse(width=0.8 * i, height=0.5 * i,
                              color=TECH_CYAN, stroke_width=3,
                              stroke_opacity=1 - i * 0.12,
                              fill_color=TECH_CYAN, fill_opacity=0.08)
            ellipse.move_to(center)
            step_text = Text(f"t + {i}", font_size=16, color=TECH_CYAN)
            step_text.next_to(ellipse, RIGHT, buff=0.15)
            ellipses.add(VGroup(ellipse, step_text))

        for ell in ellipses:
            self.play(Create(ell), run_time=1)
            self.wait(0.3)

        self.play(Write(steps_label), run_time=1)
        self.wait(3)


# ========================== PART 9: THE MEASUREMENT STEP (15-20s) ==========================
class Part9(Scene):
    """A new sensor reading arrives with its own uncertainty"""
    def construct(self):
        title = Text("THE MEASUREMENT STEP", font_size=48, color=NEON_PINK)
        title.to_edge(UP, buff=0.4)

        subtitle = Text("A new sensor reading arrives!", font_size=26, color=TEXT_WHITE)
        subtitle.next_to(title, DOWN, buff=0.2)

        # Measurement equation
        meas_eq = MathTex(
            r"z_k", r"=", r"H", r"\cdot", r"x_k", r"+", r"v_k",
            font_size=48
        )
        meas_eq[0].set_color(NEON_PINK)
        meas_eq[2].set_color(VIBRANT_ORANGE)
        meas_eq[4].set_color(TECH_CYAN)
        meas_eq[6].set_color(NEON_PINK)

        eq_labels = VGroup(
            Text("z = Measurement", font_size=20, color=NEON_PINK),
            Text("H = Observation Matrix", font_size=20, color=VIBRANT_ORANGE),
            Text("v = Measurement Noise", font_size=20, color=NEON_PINK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)

        eq_group = VGroup(meas_eq, eq_labels).arrange(DOWN, buff=0.4)
        eq_group.move_to(UP * 0.8)

        # Visual: prediction ellipse + measurement dot with its own uncertainty
        center = DOWN * 1.5
        pred_ellipse = Ellipse(width=3, height=2,
                                color=TECH_CYAN, stroke_width=3,
                                fill_color=TECH_CYAN, fill_opacity=0.1)
        pred_ellipse.move_to(center)
        pred_dot = Dot(center, radius=0.1, color=TECH_CYAN)
        pred_label = Text("Prediction", font_size=18, color=TECH_CYAN)
        pred_label.next_to(pred_ellipse, LEFT, buff=0.3)

        meas_point = center + RIGHT * 1.2 + UP * 0.5
        meas_circle = Circle(radius=0.6, color=NEON_PINK, stroke_width=3,
                              fill_color=NEON_PINK, fill_opacity=0.15)
        meas_circle.move_to(meas_point)
        meas_dot = Dot(meas_point, radius=0.1, color=NEON_PINK)
        meas_label = Text("Measurement", font_size=18, color=NEON_PINK)
        meas_label.next_to(meas_circle, RIGHT, buff=0.3)

        question = Text("Which one should we trust more?",
                         font_size=28, color=VIBRANT_ORANGE)
        question.to_edge(DOWN, buff=0.3)

        # Animations
        self.play(Write(title), FadeIn(subtitle), run_time=1.2)
        self.wait(0.5)

        self.play(Write(meas_eq), run_time=2)
        self.play(FadeIn(eq_labels), run_time=1.5)
        self.wait(1)

        self.play(FadeIn(pred_ellipse), FadeIn(pred_dot), Write(pred_label), run_time=1.5)
        self.wait(0.5)

        # Measurement arrives with animation
        self.play(
            FadeIn(meas_dot, scale=3),
            FadeIn(meas_circle, scale=0.3),
            Write(meas_label),
            run_time=1.5
        )
        self.wait(1)

        self.play(Write(question), run_time=1.5)
        self.wait(3)


# ========================== PART 10: THE KALMAN GAIN (15-20s) ==========================
class Part10(Scene):
    """Kalman Gain K — balance between prediction trust and measurement trust"""
    def construct(self):
        title = Text("THE KALMAN GAIN", font_size=48, color=VIBRANT_ORANGE)
        title.to_edge(UP, buff=0.4)

        subtitle = Text("The 'trust balancer' between model and sensor",
                         font_size=26, color=TEXT_WHITE)
        subtitle.next_to(title, DOWN, buff=0.2)

        # Kalman Gain formula
        gain_eq = MathTex(
            r"K_k", r"=", r"\frac{P_{k|k-1} H^T}{H P_{k|k-1} H^T + R}",
            font_size=44
        )
        gain_eq[0].set_color(VIBRANT_ORANGE)
        gain_eq.move_to(UP * 0.5)

        r_label = Text("R = Measurement Noise Covariance", font_size=20, color=NEON_PINK)
        r_label.next_to(gain_eq, DOWN, buff=0.4)

        # Trust slider visualization
        slider_bg = RoundedRectangle(width=8, height=0.6, corner_radius=0.15,
                                      fill_color=SUBTLE_NAVY, fill_opacity=0.9,
                                      stroke_color=TEXT_WHITE, stroke_width=2)
        slider_bg.move_to(DOWN * 1.5)

        # Left label: Trust Model
        trust_model = Text("Trust MODEL", font_size=20, color=TECH_CYAN, weight=BOLD)
        trust_model.next_to(slider_bg, LEFT, buff=0.3)

        # Right label: Trust SENSOR
        trust_sensor = Text("Trust SENSOR", font_size=20, color=NEON_PINK, weight=BOLD)
        trust_sensor.next_to(slider_bg, RIGHT, buff=0.3)

        # Slider knob
        knob = Circle(radius=0.2, fill_color=VIBRANT_ORANGE, fill_opacity=1,
                      stroke_color=VIBRANT_ORANGE, stroke_width=2)
        knob.move_to(slider_bg.get_center())

        # K value display
        k_display = VGroup(
            Text("K = ", font_size=28, color=TEXT_WHITE),
            DecimalNumber(0.5, num_decimal_places=2, font_size=28, color=VIBRANT_ORANGE),
        ).arrange(RIGHT, buff=0.1)
        k_display.next_to(slider_bg, DOWN, buff=0.5)

        # Explanations
        low_k = Text("K ≈ 0 → Trust the model prediction",
                      font_size=22, color=TECH_CYAN)
        high_k = Text("K ≈ 1 → Trust the sensor measurement",
                       font_size=22, color=NEON_PINK)
        explanations = VGroup(low_k, high_k).arrange(DOWN, buff=0.2)
        explanations.to_edge(DOWN, buff=0.3)

        # Animations
        self.play(Write(title), FadeIn(subtitle), run_time=1.2)
        self.wait(0.5)

        self.play(Write(gain_eq), run_time=2.5)
        self.play(Write(r_label), run_time=1)
        self.wait(1)

        self.play(
            FadeIn(slider_bg), Write(trust_model), Write(trust_sensor),
            FadeIn(knob),
            run_time=1.5
        )
        self.play(FadeIn(k_display), run_time=0.8)
        self.wait(0.5)

        # Animate slider moving
        # Move toward model (K ~ 0)
        self.play(
            knob.animate.move_to(slider_bg.get_left() + RIGHT * 0.5),
            k_display[1].animate.set_value(0.1),
            run_time=2
        )
        self.wait(0.5)

        # Move toward sensor (K ~ 1)
        self.play(
            knob.animate.move_to(slider_bg.get_right() + LEFT * 0.5),
            k_display[1].animate.set_value(0.9),
            run_time=2
        )
        self.wait(0.5)

        # Back to middle
        self.play(
            knob.animate.move_to(slider_bg.get_center()),
            k_display[1].animate.set_value(0.5),
            run_time=1.5
        )

        self.play(Write(low_k), run_time=1)
        self.play(Write(high_k), run_time=1)
        self.wait(3)


# ========================== PART 11: THE UPDATE STEP (15-20s) ==========================
class Part11(Scene):
    """Combine prediction + measurement using K — ellipse shrinks"""
    def construct(self):
        title = Text("THE UPDATE STEP", font_size=48, color=VIBRANT_ORANGE)
        title.to_edge(UP, buff=0.4)

        subtitle = Text("Fusing Prediction and Measurement", font_size=26, color=TEXT_WHITE)
        subtitle.next_to(title, DOWN, buff=0.2)

        # Update equations
        eq1 = MathTex(
            r"\hat{x}_k", r"=", r"\hat{x}_{k|k-1}", r"+", r"K_k",
            r"(", r"z_k", r"-", r"H", r"\hat{x}_{k|k-1}", r")",
            font_size=38
        )
        eq1[0].set_color(VIBRANT_ORANGE)
        eq1[2].set_color(TECH_CYAN)
        eq1[4].set_color(VIBRANT_ORANGE)
        eq1[6].set_color(NEON_PINK)
        eq1[8].set_color(VIBRANT_ORANGE)
        eq1[9].set_color(TECH_CYAN)

        eq2 = MathTex(
            r"P_k", r"=", r"(I - K_k H)", r"P_{k|k-1}",
            font_size=38
        )
        eq2[0].set_color(VIBRANT_ORANGE)
        eq2[2].set_color(VIBRANT_ORANGE)
        eq2[3].set_color(TECH_CYAN)

        eqs = VGroup(eq1, eq2).arrange(DOWN, buff=0.4)
        eqs.move_to(UP * 0.5)

        innov_brace = BraceBetweenPoints(eq1[5].get_bottom(), eq1[10].get_bottom(), direction=DOWN)
        innov_label = Text("Innovation (surprise)", font_size=18, color=NEON_PINK)
        innov_label.next_to(innov_brace, DOWN, buff=0.15)

        # Visual: ellipses merging
        center = DOWN * 2
        pred_ellipse = Ellipse(width=3, height=2, color=TECH_CYAN, stroke_width=3,
                                fill_color=TECH_CYAN, fill_opacity=0.1)
        pred_ellipse.move_to(center + LEFT * 0.5)
        pred_label = Text("Prediction", font_size=16, color=TECH_CYAN)
        pred_label.next_to(pred_ellipse, LEFT, buff=0.2)

        meas_circle = Circle(radius=0.7, color=NEON_PINK, stroke_width=3,
                              fill_color=NEON_PINK, fill_opacity=0.15)
        meas_circle.move_to(center + RIGHT * 1)
        meas_label = Text("Measurement", font_size=16, color=NEON_PINK)
        meas_label.next_to(meas_circle, RIGHT, buff=0.2)

        result_ellipse = Ellipse(width=1.2, height=0.8, color=VIBRANT_ORANGE, stroke_width=4,
                                  fill_color=VIBRANT_ORANGE, fill_opacity=0.2)
        result_ellipse.move_to(center + RIGHT * 0.3)
        result_label = Text("Updated!", font_size=18, color=VIBRANT_ORANGE, weight=BOLD)
        result_label.next_to(result_ellipse, DOWN, buff=0.2)

        # Animations
        self.play(Write(title), FadeIn(subtitle), run_time=1.2)
        self.wait(0.5)
        self.play(Write(eq1), run_time=3)
        self.play(Create(innov_brace), Write(innov_label), run_time=1)
        self.wait(1)
        self.play(Write(eq2), run_time=2)
        self.wait(1)
        self.play(FadeIn(pred_ellipse), Write(pred_label), run_time=1)
        self.play(FadeIn(meas_circle), Write(meas_label), run_time=1)
        self.wait(0.5)
        self.play(
            Transform(pred_ellipse, result_ellipse),
            Transform(meas_circle, result_ellipse.copy()),
            FadeOut(pred_label), FadeOut(meas_label),
            run_time=2
        )
        self.play(Write(result_label), run_time=0.8)
        self.wait(3)


# ========================== PART 12: ONE FULL CYCLE (15-20s) ==========================
class Part12(Scene):
    """Animate Predict → Measure → Update loop"""
    def construct(self):
        title = Text("THE KALMAN FILTER CYCLE", font_size=48, color=TECH_CYAN)
        title.to_edge(UP, buff=0.4)

        box_w, box_h = 2.8, 1.0

        init_box = RoundedRectangle(width=box_w, height=box_h, corner_radius=0.1,
                                     fill_color=SUBTLE_NAVY, fill_opacity=0.9,
                                     stroke_color=TEXT_WHITE, stroke_width=2)
        init_text = Text("Initialize\nx₀, P₀", font_size=20, color=TEXT_WHITE)
        init = VGroup(init_box, init_text).move_to(LEFT * 4.5)

        pred_box = RoundedRectangle(width=box_w, height=box_h, corner_radius=0.1,
                                     fill_color=SUBTLE_NAVY, fill_opacity=0.9,
                                     stroke_color=TECH_CYAN, stroke_width=3)
        pred_text = Text("PREDICT\nx̂, P⁻", font_size=20, color=TECH_CYAN)
        pred = VGroup(pred_box, pred_text).move_to(LEFT * 1.2)

        meas_box = RoundedRectangle(width=box_w, height=box_h, corner_radius=0.1,
                                     fill_color=SUBTLE_NAVY, fill_opacity=0.9,
                                     stroke_color=NEON_PINK, stroke_width=3)
        meas_text = Text("MEASURE\nZk", font_size=20, color=NEON_PINK)
        meas = VGroup(meas_box, meas_text).move_to(RIGHT * 2.1)

        upd_box = RoundedRectangle(width=box_w, height=box_h, corner_radius=0.1,
                                    fill_color=SUBTLE_NAVY, fill_opacity=0.9,
                                    stroke_color=VIBRANT_ORANGE, stroke_width=3)
        upd_text = Text("UPDATE\nK, x̂, P", font_size=20, color=VIBRANT_ORANGE)
        upd = VGroup(upd_box, upd_text).move_to(RIGHT * 5.4)

        a1 = Arrow(init_box.get_right(), pred_box.get_left(), color=TEXT_WHITE, stroke_width=2, buff=0.1)
        a2 = Arrow(pred_box.get_right(), meas_box.get_left(), color=TEXT_WHITE, stroke_width=2, buff=0.1)
        a3 = Arrow(meas_box.get_right(), upd_box.get_left(), color=TEXT_WHITE, stroke_width=2, buff=0.1)

        loop_arrow = CurvedArrow(
            upd_box.get_bottom() + DOWN * 0.1,
            pred_box.get_bottom() + DOWN * 0.1,
            color=VIBRANT_ORANGE, stroke_width=2, angle=-TAU / 4
        )
        loop_label = Text("Repeat", font_size=18, color=VIBRANT_ORANGE)
        loop_label.next_to(loop_arrow, DOWN, buff=0.15)

        flow = VGroup(init, pred, meas, upd, a1, a2, a3, loop_arrow, loop_label)
        flow.move_to(ORIGIN)

        # Animations
        self.play(Write(title), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(init), run_time=0.8)
        self.play(GrowArrow(a1), run_time=0.5)
        self.play(FadeIn(pred), run_time=0.8)
        self.play(GrowArrow(a2), run_time=0.5)
        self.play(FadeIn(meas), run_time=0.8)
        self.play(GrowArrow(a3), run_time=0.5)
        self.play(FadeIn(upd), run_time=0.8)
        self.play(Create(loop_arrow), Write(loop_label), run_time=1)
        self.wait(1)

        for _ in range(2):
            self.play(pred_box.animate.set_stroke(TECH_CYAN, width=6), run_time=0.4)
            self.play(pred_box.animate.set_stroke(TECH_CYAN, width=3), run_time=0.3)
            self.play(meas_box.animate.set_stroke(NEON_PINK, width=6), run_time=0.4)
            self.play(meas_box.animate.set_stroke(NEON_PINK, width=3), run_time=0.3)
            self.play(upd_box.animate.set_stroke(VIBRANT_ORANGE, width=6), run_time=0.4)
            self.play(upd_box.animate.set_stroke(VIBRANT_ORANGE, width=3), run_time=0.3)
        self.wait(2)


# ========================== PART 13: CONVERGENCE GRAPH (15-20s) ==========================
class Part13(Scene):
    """Plot estimated vs true position — filter converges"""
    def construct(self):
        title = Text("FILTER CONVERGENCE", font_size=48, color=TECH_CYAN)
        title.to_edge(UP, buff=0.4)

        axes = Axes(
            x_range=[0, 10, 1], y_range=[-3, 3, 1],
            x_length=10, y_length=5,
            axis_config={"color": SUBTLE_NAVY, "stroke_width": 2},
        ).move_to(DOWN * 0.2)

        x_lab = axes.get_x_axis_label(Text("Time Step", font_size=22, color=TEXT_WHITE))
        y_lab = axes.get_y_axis_label(Text("Position", font_size=22, color=TEXT_WHITE))

        true_line = axes.plot(lambda x: 2 * np.sin(0.6 * x), x_range=[0, 10],
                               color=TEXT_WHITE, stroke_width=3)
        true_label = Text("True", font_size=20, color=TEXT_WHITE)

        np.random.seed(42)
        m_x = np.linspace(0.3, 9.7, 35)
        m_y = [2 * np.sin(0.6 * x) + np.random.normal(0, 0.7) for x in m_x]
        meas_dots = VGroup(*[
            Dot(axes.c2p(x, y), radius=0.05, color=NEON_PINK, fill_opacity=0.6)
            for x, y in zip(m_x, m_y)
        ])
        meas_label = Text("Measurements", font_size=20, color=NEON_PINK)

        est_x = np.linspace(0.3, 9.7, 35)
        est_y = []
        kf_est = 0
        for i, x in enumerate(est_x):
            true_val = 2 * np.sin(0.6 * x)
            meas_val = m_y[i]
            k = 0.7 / (1 + i * 0.15)
            kf_est = kf_est + k * (meas_val - kf_est)
            kf_est = kf_est * 0.7 + true_val * 0.3
            est_y.append(kf_est)

        est_path = VMobject(color=VIBRANT_ORANGE, stroke_width=4)
        est_pts = [axes.c2p(x, y) for x, y in zip(est_x, est_y)]
        est_path.set_points_smoothly(est_pts)
        est_label = Text("Kalman Estimate", font_size=20, color=VIBRANT_ORANGE)

        true_label.next_to(axes, UR, buff=0.2).shift(DOWN * 0.2)
        meas_label.next_to(true_label, DOWN, buff=0.15, aligned_edge=LEFT)
        est_label.next_to(meas_label, DOWN, buff=0.15, aligned_edge=LEFT)

        converge_note = Text("The estimate converges to the truth!",
                              font_size=26, color=VIBRANT_ORANGE)
        converge_note.to_edge(DOWN, buff=0.3)

        self.play(Write(title), run_time=1)
        self.play(Create(axes), Write(x_lab), Write(y_lab), run_time=1.5)
        self.play(Create(true_line), Write(true_label), run_time=2)
        self.wait(0.5)
        self.play(
            LaggedStart(*[FadeIn(d, scale=0.5) for d in meas_dots], lag_ratio=0.04),
            Write(meas_label), run_time=2
        )
        self.wait(0.5)
        self.play(Create(est_path), Write(est_label), run_time=4)
        self.wait(1)
        self.play(Write(converge_note), run_time=1.5)
        self.wait(3)


# ========================== PART 14: FULL EQUATIONS (15-20s) ==========================
class Part14(Scene):
    """Full Kalman Filter equation set"""
    def construct(self):
        title = Text("THE KALMAN FILTER EQUATIONS", font_size=44, color=TECH_CYAN)
        title.to_edge(UP, buff=0.4)

        pred_header = Text("PREDICT", font_size=30, color=TECH_CYAN, weight=BOLD)
        pred_eq1 = MathTex(r"\hat{x}_{k|k-1} = F_k \hat{x}_{k-1} + B_k u_k",
                            font_size=36, color=TECH_CYAN)
        pred_eq2 = MathTex(r"P_{k|k-1} = F_k P_{k-1} F_k^T + Q_k",
                            font_size=36, color=TECH_CYAN)
        pred_group = VGroup(pred_header, pred_eq1, pred_eq2).arrange(DOWN, buff=0.25)

        upd_header = Text("UPDATE", font_size=30, color=VIBRANT_ORANGE, weight=BOLD)
        upd_eq1 = MathTex(r"K_k = P_{k|k-1} H_k^T (H_k P_{k|k-1} H_k^T + R_k)^{-1}",
                           font_size=32, color=VIBRANT_ORANGE)
        upd_eq2 = MathTex(r"\hat{x}_k = \hat{x}_{k|k-1} + K_k (z_k - H_k \hat{x}_{k|k-1})",
                           font_size=32, color=VIBRANT_ORANGE)
        upd_eq3 = MathTex(r"P_k = (I - K_k H_k) P_{k|k-1}",
                           font_size=36, color=VIBRANT_ORANGE)
        upd_group = VGroup(upd_header, upd_eq1, upd_eq2, upd_eq3).arrange(DOWN, buff=0.25)

        divider = Line(LEFT * 5, RIGHT * 5, color=SUBTLE_NAVY, stroke_width=2)
        all_eqs = VGroup(pred_group, divider, upd_group).arrange(DOWN, buff=0.5)
        all_eqs.move_to(DOWN * 0.3)

        frame = SurroundingRectangle(all_eqs, color=TEXT_WHITE, stroke_width=1,
                                      buff=0.4, corner_radius=0.15)

        self.play(Write(title), run_time=1)
        self.wait(0.5)
        self.play(Write(pred_header), run_time=0.8)
        self.play(Write(pred_eq1), run_time=2)
        self.play(Write(pred_eq2), run_time=2)
        self.wait(1)
        self.play(Create(divider), run_time=0.5)
        self.play(Write(upd_header), run_time=0.8)
        self.play(Write(upd_eq1), run_time=2)
        self.play(Write(upd_eq2), run_time=2)
        self.play(Write(upd_eq3), run_time=1.5)
        self.wait(0.5)
        self.play(Create(frame), run_time=1)
        self.wait(3)


# ========================== PART 15: LINEAR KF (15-20s) ==========================
class Part15(Scene):
    """Types: Linear Kalman Filter"""
    def construct(self):
        title = Text("TYPE 1: LINEAR KALMAN FILTER", font_size=44, color=TECH_CYAN)
        title.to_edge(UP, buff=0.4)

        badge = Text("The Original (1960)", font_size=24, color=VIBRANT_ORANGE)
        badge.next_to(title, DOWN, buff=0.2)

        desc = Text("Works when the system is LINEAR", font_size=28, color=TEXT_WHITE)
        desc.next_to(badge, DOWN, buff=0.5)

        axes = Axes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=5, y_length=5,
            axis_config={"color": SUBTLE_NAVY, "stroke_width": 2}
        ).move_to(LEFT * 3 + DOWN * 0.8)

        linear_line = axes.plot(lambda x: 0.8 * x + 0.5, x_range=[-3, 3],
                                 color=TECH_CYAN, stroke_width=4)
        linear_label = Text("y = Ax + b", font_size=22, color=TECH_CYAN)
        linear_label.next_to(axes, DOWN, buff=0.3)

        apps_title = Text("Applications:", font_size=24, color=VIBRANT_ORANGE, weight=BOLD)
        apps = VGroup(
            Text("• Constant velocity tracking", font_size=20, color=TEXT_WHITE),
            Text("• Temperature estimation", font_size=20, color=TEXT_WHITE),
            Text("• Simple signal filtering", font_size=20, color=TEXT_WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        apps_group = VGroup(apps_title, apps).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        apps_group.move_to(RIGHT * 3 + DOWN * 0.8)

        condition = VGroup(
            Text("✓ System must be linear", font_size=22, color=TECH_CYAN),
            Text("✓ Noise must be Gaussian", font_size=22, color=TECH_CYAN),
            Text("= OPTIMAL solution!", font_size=22, color=VIBRANT_ORANGE, weight=BOLD),
        ).arrange(DOWN, buff=0.15)
        condition.to_edge(DOWN, buff=0.4)

        self.play(Write(title), FadeIn(badge), run_time=1.2)
        self.play(Write(desc), run_time=1)
        self.wait(0.5)
        self.play(Create(axes), run_time=1)
        self.play(Create(linear_line), Write(linear_label), run_time=2)
        self.wait(1)
        self.play(Write(apps_title), run_time=0.8)
        for app in apps:
            self.play(Write(app), run_time=0.8)
        self.wait(1)
        self.play(FadeIn(condition), run_time=1.5)
        self.wait(3)


# ========================== PART 16: EXTENDED KF (15-20s) ==========================
class Part16(Scene):
    """Types: Extended Kalman Filter (EKF) for nonlinear systems"""
    def construct(self):
        title = Text("TYPE 2: EXTENDED KALMAN FILTER", font_size=44, color=NEON_PINK)
        title.to_edge(UP, buff=0.4)

        badge = Text("For Nonlinear Systems", font_size=24, color=VIBRANT_ORANGE)
        badge.next_to(title, DOWN, buff=0.2)

        # Nonlinear curve vs linear approximation
        axes = Axes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=5, y_length=5,
            axis_config={"color": SUBTLE_NAVY, "stroke_width": 2}
        ).move_to(LEFT * 3 + DOWN * 0.5)

        nonlinear = axes.plot(lambda x: np.sin(x) * 1.5 + 0.3 * x, x_range=[-3, 3],
                               color=NEON_PINK, stroke_width=4)
        nl_label = Text("Nonlinear f(x)", font_size=20, color=NEON_PINK)
        nl_label.next_to(nonlinear, UP, buff=0.1).shift(RIGHT)

        # Tangent line at operating point
        op_x = 1.0
        op_y = np.sin(op_x) * 1.5 + 0.3 * op_x
        slope = np.cos(op_x) * 1.5 + 0.3
        tangent = axes.plot(lambda x: slope * (x - op_x) + op_y, x_range=[-1, 3],
                             color=TECH_CYAN, stroke_width=3, stroke_opacity=0.8)
        tangent_label = Text("Linearized (Jacobian)", font_size=18, color=TECH_CYAN)
        tangent_label.next_to(tangent, DOWN, buff=0.1)

        op_dot = Dot(axes.c2p(op_x, op_y), radius=0.1, color=VIBRANT_ORANGE)
        op_label = Text("Operating\nPoint", font_size=16, color=VIBRANT_ORANGE)
        op_label.next_to(op_dot, UR, buff=0.1)

        # EKF explanation
        explanation = VGroup(
            Text("The EKF:", font_size=24, color=NEON_PINK, weight=BOLD),
            Text("1. Linearizes around current", font_size=20, color=TEXT_WHITE),
            Text("   estimate using Jacobian", font_size=20, color=TEXT_WHITE),
            Text("2. Applies standard KF to the", font_size=20, color=TEXT_WHITE),
            Text("   linearized system", font_size=20, color=TEXT_WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        explanation.move_to(RIGHT * 3.5 + DOWN * 0.5)

        jacobian_eq = MathTex(r"F_k = \left.\frac{\partial f}{\partial x}\right|_{x=\hat{x}_k}",
                               font_size=32, color=VIBRANT_ORANGE)
        jacobian_eq.to_edge(DOWN, buff=0.5)

        # Animations
        self.play(Write(title), FadeIn(badge), run_time=1.2)
        self.wait(0.5)

        self.play(Create(axes), run_time=1)
        self.play(Create(nonlinear), Write(nl_label), run_time=2)
        self.wait(0.5)

        self.play(FadeIn(op_dot), Write(op_label), run_time=1)
        self.play(Create(tangent), Write(tangent_label), run_time=2)
        self.wait(1)

        self.play(FadeIn(explanation), run_time=2)
        self.wait(1)

        self.play(Write(jacobian_eq), run_time=1.5)
        self.wait(3)


# ========================== PART 17: UNSCENTED KF (15-20s) ==========================
class Part17(Scene):
    """Types: Unscented Kalman Filter (UKF) — sigma points"""
    def construct(self):
        title = Text("TYPE 3: UNSCENTED KALMAN FILTER", font_size=44, color=VIBRANT_ORANGE)
        title.to_edge(UP, buff=0.4)

        badge = Text("No Jacobians Needed!", font_size=24, color=TECH_CYAN)
        badge.next_to(title, DOWN, buff=0.2)

        # Before: Gaussian distribution with sigma points
        before_title = Text("BEFORE Transform", font_size=22, color=TECH_CYAN, weight=BOLD)

        before_axes = Axes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=4, y_length=4,
            axis_config={"color": SUBTLE_NAVY, "stroke_width": 1}
        ).move_to(LEFT * 3.5 + DOWN * 0.8)

        # Sigma points (2n+1 points for n-dimensional state)
        center = before_axes.c2p(0, 0)
        sigma_pts_before = VGroup(
            Dot(before_axes.c2p(0, 0), radius=0.12, color=VIBRANT_ORANGE),  # Center
            Dot(before_axes.c2p(1.5, 0), radius=0.08, color=TECH_CYAN),
            Dot(before_axes.c2p(-1.5, 0), radius=0.08, color=TECH_CYAN),
            Dot(before_axes.c2p(0, 1.5), radius=0.08, color=TECH_CYAN),
            Dot(before_axes.c2p(0, -1.5), radius=0.08, color=TECH_CYAN),
        )

        before_ellipse = Ellipse(width=3, height=3, color=TECH_CYAN, stroke_width=2,
                                  fill_color=TECH_CYAN, fill_opacity=0.08)
        before_ellipse.move_to(center)

        before_group_label = Text("Sigma Points\ncapture distribution", font_size=16, color=TECH_CYAN)
        before_group_label.next_to(before_axes, DOWN, buff=0.3)

        # Arrow
        transform_arrow = Arrow(LEFT * 1, RIGHT * 1, color=VIBRANT_ORANGE, stroke_width=4)
        transform_arrow.move_to(DOWN * 0.8)
        transform_text = Text("f(x)", font_size=24, color=VIBRANT_ORANGE)
        transform_text.next_to(transform_arrow, UP, buff=0.1)

        # After: transformed sigma points
        after_title = Text("AFTER Transform", font_size=22, color=NEON_PINK, weight=BOLD)

        after_axes = Axes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=4, y_length=4,
            axis_config={"color": SUBTLE_NAVY, "stroke_width": 1}
        ).move_to(RIGHT * 3.5 + DOWN * 0.8)

        # Transformed sigma points (distorted by nonlinearity)
        sigma_pts_after = VGroup(
            Dot(after_axes.c2p(0.2, 0.3), radius=0.12, color=VIBRANT_ORANGE),
            Dot(after_axes.c2p(1.8, 0.8), radius=0.08, color=NEON_PINK),
            Dot(after_axes.c2p(-1.2, -0.5), radius=0.08, color=NEON_PINK),
            Dot(after_axes.c2p(0.5, 1.8), radius=0.08, color=NEON_PINK),
            Dot(after_axes.c2p(-0.3, -1.3), radius=0.08, color=NEON_PINK),
        )

        after_ellipse = Ellipse(width=3.5, height=2.8, color=NEON_PINK, stroke_width=2,
                                 fill_color=NEON_PINK, fill_opacity=0.08)
        after_ellipse.move_to(after_axes.c2p(0.2, 0.3))
        after_ellipse.rotate(0.3)

        after_group_label = Text("Recompute mean\n& covariance", font_size=16, color=NEON_PINK)
        after_group_label.next_to(after_axes, DOWN, buff=0.3)

        before_title.next_to(before_axes, UP, buff=0.2)
        after_title.next_to(after_axes, UP, buff=0.2)

        advantage = Text("✓ Better accuracy than EKF for highly nonlinear systems",
                          font_size=22, color=VIBRANT_ORANGE)
        advantage.to_edge(DOWN, buff=0.3)

        # Animations
        self.play(Write(title), FadeIn(badge), run_time=1.2)
        self.wait(0.5)

        self.play(Create(before_axes), Write(before_title), run_time=1)
        self.play(FadeIn(before_ellipse), run_time=0.5)
        self.play(
            LaggedStart(*[FadeIn(p, scale=2) for p in sigma_pts_before], lag_ratio=0.15),
            run_time=1.5
        )
        self.play(Write(before_group_label), run_time=1)
        self.wait(0.5)

        self.play(GrowArrow(transform_arrow), Write(transform_text), run_time=1)

        self.play(Create(after_axes), Write(after_title), run_time=1)
        self.play(
            LaggedStart(*[FadeIn(p, scale=2) for p in sigma_pts_after], lag_ratio=0.15),
            run_time=1.5
        )
        self.play(FadeIn(after_ellipse), Write(after_group_label), run_time=1)
        self.wait(1)

        self.play(Write(advantage), run_time=1.5)
        self.wait(3)


# ========================== PART 18: REAL-WORLD APPLICATIONS (15-20s) ==========================
class Part18(Scene):
    """Grid of application cards"""
    def construct(self):
        title = Text("REAL-WORLD APPLICATIONS", font_size=48, color=TECH_CYAN)
        title.to_edge(UP, buff=0.4)

        apps_data = [
            ("GPS Navigation", "Fusing satellite signals\nwith inertial sensors", TECH_CYAN),
            ("Self-Driving Cars", "Tracking pedestrians,\nvehicles, lanes", NEON_PINK),
            ("Spacecraft", "Apollo mission used KF\nfor lunar navigation", VIBRANT_ORANGE),
            ("Finance", "Predicting stock prices\nand market trends", TECH_CYAN),
            ("Robotics", "SLAM: Simultaneous\nLocalization & Mapping", NEON_PINK),
            ("Weather", "Forecasting temperature,\npressure, wind", VIBRANT_ORANGE),
        ]

        cards = VGroup()
        for name, desc, color in apps_data:
            card_bg = RoundedRectangle(width=3.8, height=2.2, corner_radius=0.15,
                                        fill_color=SUBTLE_NAVY, fill_opacity=0.9,
                                        stroke_color=color, stroke_width=3)
            card_title = Text(name, font_size=22, color=color, weight=BOLD)
            card_title.next_to(card_bg.get_top(), DOWN, buff=0.25)
            card_desc = Text(desc, font_size=16, color=TEXT_WHITE)
            card_desc.next_to(card_title, DOWN, buff=0.2)
            cards.add(VGroup(card_bg, card_title, card_desc))

        # Arrange in 2x3 grid
        row1 = VGroup(cards[0], cards[1], cards[2]).arrange(RIGHT, buff=0.3)
        row2 = VGroup(cards[3], cards[4], cards[5]).arrange(RIGHT, buff=0.3)
        grid = VGroup(row1, row2).arrange(DOWN, buff=0.3)
        grid.move_to(DOWN * 0.3)

        # Animations
        self.play(Write(title), run_time=1)
        self.wait(0.5)

        for i, card in enumerate(cards):
            self.play(FadeIn(card, shift=UP * 0.3), run_time=0.8)
            self.wait(0.3)

        # Highlight pulse
        for card in cards:
            self.play(
                card[0].animate.set_stroke(width=5),
                run_time=0.2
            )
            self.play(
                card[0].animate.set_stroke(width=3),
                run_time=0.2
            )

        self.wait(3)


# ========================== PART 19: SUMMARY (15-20s) ==========================
class Part19(Scene):
    """Recap the core loop with a clean flowchart"""
    def construct(self):
        title = Text("SUMMARY", font_size=56, color=TECH_CYAN, weight=BOLD)
        title.to_edge(UP, buff=0.4)

        # Key takeaways
        takeaways = VGroup(
            Text("1. Sensors are NOISY — we can't trust raw data", font_size=24, color=TEXT_WHITE),
            Text("2. The Kalman Filter combines MODEL + MEASUREMENT", font_size=24, color=TEXT_WHITE),
            Text("3. PREDICT where you'll be, then UPDATE with sensors", font_size=24, color=TEXT_WHITE),
            Text("4. The Kalman GAIN balances trust between the two", font_size=24, color=TEXT_WHITE),
            Text("5. The estimate CONVERGES to the true state", font_size=24, color=TEXT_WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        takeaways.move_to(UP * 0.3)

        # Color highlights
        takeaways[0][0][21:26].set_color(NEON_PINK)   # NOISY
        takeaways[1][0][29:34].set_color(TECH_CYAN)    # MODEL
        takeaways[1][0][37:48].set_color(NEON_PINK)    # MEASUREMENT
        takeaways[2][0][0:7].set_color(TECH_CYAN)      # PREDICT
        takeaways[2][0][31:37].set_color(VIBRANT_ORANGE)  # UPDATE
        takeaways[3][0][11:15].set_color(VIBRANT_ORANGE)  # GAIN
        takeaways[4][0][17:26].set_color(VIBRANT_ORANGE)  # CONVERGES

        # Types summary
        types_box = RoundedRectangle(width=10, height=1.5, corner_radius=0.15,
                                      fill_color=SUBTLE_NAVY, fill_opacity=0.9,
                                      stroke_color=VIBRANT_ORANGE, stroke_width=2)
        types_box.to_edge(DOWN, buff=0.5)

        types_text = VGroup(
            Text("KF", font_size=22, color=TECH_CYAN, weight=BOLD),
            Text(" (Linear)  •  ", font_size=20, color=TEXT_WHITE),
            Text("EKF", font_size=22, color=NEON_PINK, weight=BOLD),
            Text(" (Nonlinear)  •  ", font_size=20, color=TEXT_WHITE),
            Text("UKF", font_size=22, color=VIBRANT_ORANGE, weight=BOLD),
            Text(" (Sigma Points)", font_size=20, color=TEXT_WHITE),
        ).arrange(RIGHT, buff=0.05)
        types_text.move_to(types_box.get_center())

        # Animations
        self.play(Write(title), run_time=1)
        self.wait(0.5)

        for t in takeaways:
            self.play(Write(t), run_time=1.5)
            self.wait(0.5)

        self.play(FadeIn(types_box), Write(types_text), run_time=1.5)
        self.wait(3)


# ========================== PART 20: OUTRO (13-18s) ==========================
class Part20(Scene):
    """Thank-you screen, subscribe CTA, key takeaways"""
    def construct(self):
        # Big thank you
        thanks = Text("THANK YOU!", font_size=72, color=TECH_CYAN, weight=BOLD).shift(UP * 1.5)

        subtitle = Text("for watching", font_size=36, color=TEXT_WHITE)
        subtitle.next_to(thanks, DOWN, buff=0.3)

        # CTA
        like_text = Text("👍 LIKE", font_size=36, color=NEON_PINK, weight=BOLD)
        sub_text = Text("🔔 SUBSCRIBE", font_size=36, color=VIBRANT_ORANGE, weight=BOLD)
        share_text = Text("📤 SHARE", font_size=36, color=TECH_CYAN, weight=BOLD)

        cta = VGroup(like_text, sub_text, share_text).arrange(RIGHT, buff=1.5)
        cta.move_to(DOWN * 0.5)

        # Topic recap
        topic_box = RoundedRectangle(width=10, height=1.8, corner_radius=0.15,
                                      fill_color=SUBTLE_NAVY, fill_opacity=0.9,
                                      stroke_color=TECH_CYAN, stroke_width=2)
        topic_box.to_edge(DOWN, buff=0.5)

        topic_text = VGroup(
            Text("The Kalman Filter:", font_size=24, color=TECH_CYAN, weight=BOLD),
            Text("Optimal estimation from noisy data", font_size=22, color=TEXT_WHITE),
        ).arrange(DOWN, buff=0.1)
        topic_text.move_to(topic_box.get_center())

        # Decorative pulse rings
        rings = VGroup(*[
            Circle(radius=0.5 + i * 0.6, stroke_width=2 - i * 0.3,
                   color=TECH_CYAN, stroke_opacity=0.3 - i * 0.05)
            for i in range(4)
        ]).move_to(ORIGIN)

        # Animations
        self.play(
            FadeIn(thanks, scale=1.3),
            run_time=1
        )
        self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=0.8)
        self.wait(1)

        # CTA appears
        self.play(
            LaggedStart(
                FadeIn(like_text, shift=UP * 0.5),
                FadeIn(sub_text, shift=UP * 0.5),
                FadeIn(share_text, shift=UP * 0.5),
                lag_ratio=0.3
            ),
            run_time=1.5
        )
        self.wait(1)

        # Pulse effect
        for ring in rings:
            self.add(ring)
            self.play(ring.animate.scale(4).set_opacity(0), run_time=0.5)
            self.remove(ring)

        self.play(FadeIn(topic_box), Write(topic_text), run_time=1.5)
        self.wait(1)

        # Final fade
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )
        self.wait(1)
