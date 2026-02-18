from manim import *
import numpy as np

# ========================== COLOR PALETTE ==========================
DEEP_NAVY = "#020B1F"
TECH_CYAN = "#00F0FF"
NEON_PINK = "#FF0055"
VIBRANT_ORANGE = "#FF9F00"
TEXT_WHITE = "#FFFFFF"
SUBTLE_NAVY = "#1E2A45"

# YouTube Shorts Configuration (9:16 aspect ratio)
config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 14.0
config.frame_width = 14.0 * (1080 / 1920)  # ~7.875
config.background_color = DEEP_NAVY


class KalmanShort(Scene):
    """Kalman Filter YouTube Short — 1 minute explainer"""
    def construct(self):
        # ==================== HOOK (0-4s) ====================
        hook_title = Text("KALMAN FILTER", font_size=72, color=TECH_CYAN, weight=BOLD)
        hook_sub = Text("in 60 seconds", font_size=36, color=NEON_PINK)
        hook_sub.next_to(hook_title, DOWN, buff=0.3)
        hook = VGroup(hook_title, hook_sub).move_to(UP * 2)

        # Scatter noisy dots for visual
        np.random.seed(42)
        dots = VGroup(*[
            Dot(point=[np.random.normal(0, 1.8), np.random.normal(-3, 1.5), 0],
                radius=0.04, color=NEON_PINK, fill_opacity=0.6)
            for _ in range(40)
        ])

        self.play(FadeIn(hook_title, scale=1.3), run_time=0.6)
        self.play(FadeIn(hook_sub, shift=UP * 0.2),
                  LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.02),
                  run_time=0.8)
        self.wait(0.6)
        self.play(FadeOut(hook), FadeOut(dots), run_time=0.5)

        # ==================== PROBLEM (4-12s) ====================
        prob_title = Text("THE PROBLEM", font_size=52, color=TECH_CYAN, weight=BOLD)
        prob_title.to_edge(UP, buff=0.8)

        prob_desc = Text("Sensors are NOISY", font_size=36, color=NEON_PINK)
        prob_desc.next_to(prob_title, DOWN, buff=0.4)

        # Mini graph — true vs noisy
        axes = Axes(
            x_range=[0, 8, 1], y_range=[-2, 2, 1],
            x_length=6.5, y_length=4,
            axis_config={"color": SUBTLE_NAVY, "stroke_width": 2},
        ).move_to(DOWN * 1.5)

        true_curve = axes.plot(lambda x: 1.5 * np.sin(x), x_range=[0, 8],
                               color=TECH_CYAN, stroke_width=4)
        true_label = Text("True Signal", font_size=22, color=TECH_CYAN)
        true_label.next_to(axes, DOWN, buff=0.3).shift(LEFT * 1.5)

        np.random.seed(7)
        noisy_x = np.linspace(0.3, 7.7, 25)
        noisy_y = [1.5 * np.sin(x) + np.random.normal(0, 0.5) for x in noisy_x]
        noisy_dots = VGroup(*[
            Dot(axes.c2p(x, y), radius=0.06, color=NEON_PINK, fill_opacity=0.8)
            for x, y in zip(noisy_x, noisy_y)
        ])
        noisy_label = Text("Noisy Data", font_size=22, color=NEON_PINK)
        noisy_label.next_to(true_label, RIGHT, buff=1.0)

        self.play(Write(prob_title), run_time=0.6)
        self.play(Write(prob_desc), run_time=0.6)
        self.play(Create(axes), run_time=0.8)
        self.play(Create(true_curve), Write(true_label), run_time=1.2)
        self.play(
            LaggedStart(*[FadeIn(d, scale=0.5) for d in noisy_dots], lag_ratio=0.03),
            Write(noisy_label), run_time=1.2
        )
        self.wait(1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

        # ==================== CORE IDEA (12-22s) ====================
        idea_title = Text("THE SOLUTION", font_size=52, color=VIBRANT_ORANGE, weight=BOLD)
        idea_title.to_edge(UP, buff=0.8)

        # Model box
        model_box = RoundedRectangle(width=6.5, height=3.2, corner_radius=0.15,
                                      fill_color=SUBTLE_NAVY, fill_opacity=0.9,
                                      stroke_color=TECH_CYAN, stroke_width=3)
        model_box.move_to(UP * 0.5)
        model_title = Text("PHYSICAL MODEL", font_size=28, color=TECH_CYAN, weight=BOLD)
        model_title.next_to(model_box.get_top(), DOWN, buff=0.3)
        model_eq = MathTex(r"\hat{x}_{k+1} = F \cdot x_k + B \cdot u_k",
                           font_size=36, color=TECH_CYAN)
        model_eq.next_to(model_title, DOWN, buff=0.3)
        model_note = Text("Predicts the future", font_size=22, color=TEXT_WHITE)
        model_note.next_to(model_eq, DOWN, buff=0.2)

        # Sensor box
        sensor_box = RoundedRectangle(width=6.5, height=3.2, corner_radius=0.15,
                                       fill_color=SUBTLE_NAVY, fill_opacity=0.9,
                                       stroke_color=NEON_PINK, stroke_width=3)
        sensor_box.move_to(DOWN * 3.5)
        sensor_title = Text("SENSOR DATA", font_size=28, color=NEON_PINK, weight=BOLD)
        sensor_title.next_to(sensor_box.get_top(), DOWN, buff=0.3)
        sensor_eq = MathTex(r"z_k = H \cdot x_k + v_k",
                            font_size=36, color=NEON_PINK)
        sensor_eq.next_to(sensor_title, DOWN, buff=0.3)
        sensor_note = Text("Measures reality (noisy)", font_size=22, color=TEXT_WHITE)
        sensor_note.next_to(sensor_eq, DOWN, buff=0.2)

        # Plus sign
        plus = Text("+", font_size=64, color=VIBRANT_ORANGE, weight=BOLD)
        plus.move_to(DOWN * 1.5)

        self.play(Write(idea_title), run_time=0.6)
        self.play(FadeIn(model_box), Write(model_title), run_time=0.8)
        self.play(Write(model_eq), FadeIn(model_note), run_time=1.0)
        self.play(FadeIn(plus, scale=1.5), run_time=0.4)
        self.play(FadeIn(sensor_box), Write(sensor_title), run_time=0.8)
        self.play(Write(sensor_eq), FadeIn(sensor_note), run_time=1.0)
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

        # ==================== PREDICT-UPDATE CYCLE (22-36s) ====================
        cycle_title = Text("THE CYCLE", font_size=52, color=TECH_CYAN, weight=BOLD)
        cycle_title.to_edge(UP, buff=0.8)

        # Flow boxes — vertical arrangement
        box_w, box_h = 5.5, 1.3

        pred_box = RoundedRectangle(width=box_w, height=box_h, corner_radius=0.12,
                                     fill_color=SUBTLE_NAVY, fill_opacity=0.9,
                                     stroke_color=TECH_CYAN, stroke_width=3)
        pred_text = Text("PREDICT", font_size=30, color=TECH_CYAN, weight=BOLD)
        pred_sub = Text("Where will I be next?", font_size=20, color=TEXT_WHITE)
        pred_content = VGroup(pred_text, pred_sub).arrange(DOWN, buff=0.1)
        pred = VGroup(pred_box, pred_content).move_to(UP * 1.5)

        meas_box = RoundedRectangle(width=box_w, height=box_h, corner_radius=0.12,
                                     fill_color=SUBTLE_NAVY, fill_opacity=0.9,
                                     stroke_color=NEON_PINK, stroke_width=3)
        meas_text = Text("MEASURE", font_size=30, color=NEON_PINK, weight=BOLD)
        meas_sub = Text("What does the sensor say?", font_size=20, color=TEXT_WHITE)
        meas_content = VGroup(meas_text, meas_sub).arrange(DOWN, buff=0.1)
        meas = VGroup(meas_box, meas_content).move_to(DOWN * 0.5)

        upd_box = RoundedRectangle(width=box_w, height=box_h, corner_radius=0.12,
                                    fill_color=SUBTLE_NAVY, fill_opacity=0.9,
                                    stroke_color=VIBRANT_ORANGE, stroke_width=3)
        upd_text = Text("UPDATE", font_size=30, color=VIBRANT_ORANGE, weight=BOLD)
        upd_sub = Text("Fuse both → best estimate", font_size=20, color=TEXT_WHITE)
        upd_content = VGroup(upd_text, upd_sub).arrange(DOWN, buff=0.1)
        upd = VGroup(upd_box, upd_content).move_to(DOWN * 2.5)

        a1 = Arrow(pred_box.get_bottom(), meas_box.get_top(),
                    color=TEXT_WHITE, stroke_width=2, buff=0.1)
        a2 = Arrow(meas_box.get_bottom(), upd_box.get_top(),
                    color=TEXT_WHITE, stroke_width=2, buff=0.1)

        loop_arrow = CurvedArrow(
            upd_box.get_right() + RIGHT * 0.1,
            pred_box.get_right() + RIGHT * 0.1,
            color=VIBRANT_ORANGE, stroke_width=3, angle=-TAU / 4
        )
        loop_label = Text("Repeat", font_size=20, color=VIBRANT_ORANGE)
        loop_label.next_to(loop_arrow, RIGHT, buff=0.15)

        self.play(Write(cycle_title), run_time=0.6)
        self.play(FadeIn(pred), run_time=0.6)
        self.play(GrowArrow(a1), run_time=0.4)
        self.play(FadeIn(meas), run_time=0.6)
        self.play(GrowArrow(a2), run_time=0.4)
        self.play(FadeIn(upd), run_time=0.6)
        self.play(Create(loop_arrow), Write(loop_label), run_time=0.8)
        self.wait(0.5)

        # Pulse cycle twice
        for _ in range(2):
            self.play(pred_box.animate.set_stroke(width=6), run_time=0.25)
            self.play(pred_box.animate.set_stroke(width=3), run_time=0.2)
            self.play(meas_box.animate.set_stroke(width=6), run_time=0.25)
            self.play(meas_box.animate.set_stroke(width=3), run_time=0.2)
            self.play(upd_box.animate.set_stroke(width=6), run_time=0.25)
            self.play(upd_box.animate.set_stroke(width=3), run_time=0.2)
        self.wait(0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

        # ==================== KALMAN GAIN (36-44s) ====================
        gain_title = Text("KALMAN GAIN", font_size=52, color=VIBRANT_ORANGE, weight=BOLD)
        gain_title.to_edge(UP, buff=0.8)

        gain_desc = Text("The 'trust balancer'", font_size=32, color=TEXT_WHITE)
        gain_desc.next_to(gain_title, DOWN, buff=0.4)

        # Slider visualization
        slider_bg = RoundedRectangle(width=6, height=0.7, corner_radius=0.18,
                                      fill_color=SUBTLE_NAVY, fill_opacity=0.9,
                                      stroke_color=TEXT_WHITE, stroke_width=2)
        slider_bg.move_to(DOWN * 0.5)

        trust_model = Text("Trust MODEL", font_size=22, color=TECH_CYAN, weight=BOLD)
        trust_model.next_to(slider_bg, LEFT, buff=0.15).shift(UP * 0.6)
        trust_sensor = Text("Trust SENSOR", font_size=22, color=NEON_PINK, weight=BOLD)
        trust_sensor.next_to(slider_bg, RIGHT, buff=0.15).shift(UP * 0.6)

        knob = Circle(radius=0.25, fill_color=VIBRANT_ORANGE, fill_opacity=1,
                      stroke_color=VIBRANT_ORANGE, stroke_width=2)
        knob.move_to(slider_bg.get_center())

        low_k = Text("K ≈ 0 → Trust the model", font_size=24, color=TECH_CYAN)
        high_k = Text("K ≈ 1 → Trust the sensor", font_size=24, color=NEON_PINK)
        k_explains = VGroup(low_k, high_k).arrange(DOWN, buff=0.25)
        k_explains.move_to(DOWN * 2.5)

        self.play(Write(gain_title), Write(gain_desc), run_time=0.8)
        self.play(FadeIn(slider_bg), Write(trust_model), Write(trust_sensor),
                  FadeIn(knob), run_time=0.8)

        # Animate slider
        self.play(knob.animate.move_to(slider_bg.get_left() + RIGHT * 0.5), run_time=1.0)
        self.play(Write(low_k), run_time=0.5)
        self.play(knob.animate.move_to(slider_bg.get_right() + LEFT * 0.5), run_time=1.0)
        self.play(Write(high_k), run_time=0.5)
        self.play(knob.animate.move_to(slider_bg.get_center()), run_time=0.6)
        self.wait(0.6)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

        # ==================== CONVERGENCE (44-52s) ====================
        conv_title = Text("THE RESULT", font_size=52, color=TECH_CYAN, weight=BOLD)
        conv_title.to_edge(UP, buff=0.8)

        conv_axes = Axes(
            x_range=[0, 8, 1], y_range=[-2, 2, 1],
            x_length=6.5, y_length=4,
            axis_config={"color": SUBTLE_NAVY, "stroke_width": 2},
        ).move_to(DOWN * 0.5)

        true_line = conv_axes.plot(lambda x: 1.5 * np.sin(0.8 * x), x_range=[0, 8],
                                   color=TEXT_WHITE, stroke_width=3)

        np.random.seed(42)
        m_x = np.linspace(0.3, 7.7, 25)
        m_y = [1.5 * np.sin(0.8 * x) + np.random.normal(0, 0.5) for x in m_x]
        conv_dots = VGroup(*[
            Dot(conv_axes.c2p(x, y), radius=0.05, color=NEON_PINK, fill_opacity=0.6)
            for x, y in zip(m_x, m_y)
        ])

        # Kalman estimate
        est_y = []
        kf_est = 0
        for i, x in enumerate(m_x):
            true_val = 1.5 * np.sin(0.8 * x)
            k = 0.7 / (1 + i * 0.15)
            kf_est = kf_est + k * (m_y[i] - kf_est)
            kf_est = kf_est * 0.7 + true_val * 0.3
            est_y.append(kf_est)

        est_path = VMobject(color=VIBRANT_ORANGE, stroke_width=4)
        est_pts = [conv_axes.c2p(x, y) for x, y in zip(m_x, est_y)]
        est_path.set_points_smoothly(est_pts)

        # Legend
        legend = VGroup(
            VGroup(Line(LEFT * 0.3, RIGHT * 0.3, color=TEXT_WHITE, stroke_width=3),
                   Text("True", font_size=18, color=TEXT_WHITE)).arrange(RIGHT, buff=0.15),
            VGroup(Dot(radius=0.05, color=NEON_PINK),
                   Text("Noisy", font_size=18, color=NEON_PINK)).arrange(RIGHT, buff=0.15),
            VGroup(Line(LEFT * 0.3, RIGHT * 0.3, color=VIBRANT_ORANGE, stroke_width=4),
                   Text("Kalman", font_size=18, color=VIBRANT_ORANGE)).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        legend.move_to(DOWN * 4)

        conv_result = Text("Estimate converges to truth!", font_size=28, color=VIBRANT_ORANGE)
        conv_result.move_to(DOWN * 5.2)

        self.play(Write(conv_title), run_time=0.6)
        self.play(Create(conv_axes), run_time=0.6)
        self.play(Create(true_line), run_time=0.8)
        self.play(
            LaggedStart(*[FadeIn(d, scale=0.5) for d in conv_dots], lag_ratio=0.03),
            run_time=0.8
        )
        self.play(Create(est_path), run_time=2.0)
        self.play(FadeIn(legend), run_time=0.6)
        self.play(Write(conv_result), run_time=0.8)
        self.wait(1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

        # ==================== OUTRO (52-60s) ====================
        thanks = Text("KALMAN FILTER", font_size=64, color=TECH_CYAN, weight=BOLD)
        thanks.move_to(UP * 3)

        tagline = Text("See Through the Noise", font_size=36, color=NEON_PINK)
        tagline.next_to(thanks, DOWN, buff=0.3)

        # CTA
        like_btn = Text("👍 LIKE", font_size=36, color=NEON_PINK, weight=BOLD)
        sub_btn = Text("🔔 SUBSCRIBE", font_size=36, color=VIBRANT_ORANGE, weight=BOLD)
        share_btn = Text("📤 SHARE", font_size=36, color=TECH_CYAN, weight=BOLD)
        cta = VGroup(like_btn, sub_btn, share_btn).arrange(DOWN, buff=0.5)
        cta.move_to(DOWN * 1)

        # Pulse rings
        rings = VGroup(*[
            Circle(radius=0.5 + i * 0.5, stroke_width=2 - i * 0.3,
                   color=TECH_CYAN, stroke_opacity=0.3 - i * 0.05)
            for i in range(4)
        ]).move_to(UP * 3)

        self.play(FadeIn(thanks, scale=1.2), run_time=0.6)
        self.play(FadeIn(tagline, shift=UP * 0.2), run_time=0.5)
        self.play(
            LaggedStart(
                FadeIn(like_btn, shift=UP * 0.3),
                FadeIn(sub_btn, shift=UP * 0.3),
                FadeIn(share_btn, shift=UP * 0.3),
                lag_ratio=0.2
            ), run_time=1.0
        )

        for ring in rings:
            self.add(ring)
            self.play(ring.animate.scale(4).set_opacity(0), run_time=0.4)
            self.remove(ring)

        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
