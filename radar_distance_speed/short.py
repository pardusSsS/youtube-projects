"""
Vertical Short: "How Can Radar Know Your Speed?"

Six scenes, 1080×1920, kept under sixty seconds. Same narration-driven timing as
the long video: each scene ends with `self.fill()`, which pads the picture out to
the length of its MP3 in voiceovers/durations.json.

    python build.py --short

The frame here is 4.5 × 8 Manim units, so everything is built narrow and tall,
and `fit()` guards any text that could run past the edges.
"""

import numpy as np
from manim import *

from main import (DEEP_NAVY, PANEL_NAVY, SUBTLE, RADAR_GREEN, TECH_CYAN,
                  NEON_PINK, AMBER, TEXT_WHITE, DIM_TEXT, NARRATION,
                  panel, plane, live_text)

config.background_color = DEEP_NAVY

# Manim derives pixels-per-unit from frame_width alone and never adjusts it for a
# 9:16 canvas, so a vertical render would letterbox the scene into a middle band.
# Pinning both dimensions makes the 1080x1920 frame exactly 4.5 x 8 units.
config.frame_height = 8.0
config.frame_width = 4.5

TAIL = 0.35          # Shorts breathe less than the long cut
SAFE_W = 4.05        # usable width; the frame is 4.5 units across


def fit(mob, w=SAFE_W):
    """Shrink anything that would run past the vertical frame's narrow edges."""
    if mob.width > w:
        mob.scale_to_fit_width(w)
    return mob


class NarratedShort(Scene):
    def fill(self):
        name = type(self).__name__
        target = NARRATION.get(name)
        played = self.renderer.time
        if target is None:
            print(f"[SYNC] {name}: no narration entry, holding 1.0s")
            self.wait(1.0)
            return
        pad = target + TAIL - played
        flag = "  <-- LONG PAD" if pad > 3 else ("  <-- OVERRUN" if pad < 0 else "")
        print(f"[SYNC] {name}: anim={played:6.2f}s  voice={target:6.2f}s  pad={pad:6.2f}s{flag}")
        self.wait(max(pad, 0.25))


# ------------------------------------------------------------------ props
def speed_gun(scale=1.0, color=TECH_CYAN):
    """Handheld speed gun, pointing right."""
    body = RoundedRectangle(corner_radius=0.06, width=0.95, height=0.5,
                            stroke_color=color, stroke_width=5,
                            fill_color=PANEL_NAVY, fill_opacity=1)
    horn = Polygon([0.47, 0.22, 0], [0.86, 0.34, 0], [0.86, -0.34, 0], [0.47, -0.22, 0],
                   stroke_color=color, stroke_width=5,
                   fill_color=PANEL_NAVY, fill_opacity=1)
    grip = Polygon([-0.28, -0.25, 0], [-0.08, -0.25, 0], [-0.14, -0.78, 0],
                   [-0.36, -0.78, 0], stroke_color=color, stroke_width=5,
                   fill_color=PANEL_NAVY, fill_opacity=1)
    lamp = Dot([0.8, 0, 0], radius=0.07, color=AMBER)
    return VGroup(body, horn, grip, lamp).scale(scale)


def car(scale=1.0, color=TEXT_WHITE):
    """Small side-view car, pointing left."""
    lower = RoundedRectangle(corner_radius=0.09, width=1.5, height=0.42,
                             stroke_color=color, stroke_width=4,
                             fill_color=color, fill_opacity=0.16)
    cabin = Polygon([-0.42, 0.21, 0], [-0.22, 0.58, 0], [0.28, 0.58, 0], [0.5, 0.21, 0],
                    stroke_color=color, stroke_width=4,
                    fill_color=color, fill_opacity=0.16)
    w1 = Circle(radius=0.16, color=color, stroke_width=4,
                fill_color=DEEP_NAVY, fill_opacity=1).move_to([-0.45, -0.24, 0])
    w2 = w1.copy().move_to([0.45, -0.24, 0])
    return VGroup(lower, cabin, w1, w2).scale(scale)


# ============================ 1 : THE HOOK ============================
class Short1(NarratedShort):
    def construct(self):
        t1 = Text("HOW CAN RADAR", font_size=52, color=TEXT_WHITE, weight=BOLD)
        t2 = Text("KNOW YOUR", font_size=52, color=TEXT_WHITE, weight=BOLD)
        t3 = Text("SPEED?", font_size=76, color=TECH_CYAN, weight=BOLD)
        title = VGroup(t1, t2, t3).arrange(DOWN, buff=0.16)
        fit(title)
        title.move_to(UP * 2.55)

        self.play(LaggedStart(FadeIn(t1, shift=DOWN * 0.2),
                              FadeIn(t2, shift=DOWN * 0.2),
                              FadeIn(t3, scale=1.2), lag_ratio=0.35), run_time=1.6)

        gun = speed_gun(scale=1.0).move_to(LEFT * 1.35 + UP * 0.15)
        veh = car(scale=1.0).move_to(RIGHT * 1.35 + UP * 0.1)
        self.play(FadeIn(gun, shift=RIGHT * 0.2), FadeIn(veh, shift=LEFT * 0.2), run_time=0.8)

        beam = VGroup(*[Arc(radius=0.34 + i * 0.24, start_angle=-PI / 5, angle=2 * PI / 5,
                            color=RADAR_GREEN, stroke_width=5 - i * 0.7)
                        .move_arc_center_to(gun[3].get_center()) for i in range(4)])
        self.play(LaggedStart(*[Create(a) for a in beam], lag_ratio=0.18), run_time=0.7)

        read = Text("90", font_size=92, color=AMBER, weight=BOLD)
        unit = Text("km/h", font_size=30, color=AMBER).next_to(read, RIGHT, buff=0.18)
        readout = VGroup(read, unit).arrange(RIGHT, buff=0.2).move_to(DOWN * 1.75)
        box = panel(readout, color=AMBER, buff=0.32)
        self.play(Create(box), FadeIn(read, scale=1.3), FadeIn(unit), run_time=0.9)
        self.play(Flash(readout.get_center(), color=AMBER, flash_radius=1.3,
                        line_length=0.25, num_lines=16), run_time=0.5)

        sub = VGroup(
            Text("it never measured", font_size=30, color=NEON_PINK),
            Text("how far away you were", font_size=30, color=NEON_PINK),
        ).arrange(DOWN, buff=0.12)
        fit(sub).move_to(DOWN * 2.95)
        self.play(FadeIn(sub, shift=UP * 0.2), run_time=1.0)
        self.wait(0.8)
        self.fill()


# ============================ 2 : DOPPLER ============================
class Short2(NarratedShort):
    def construct(self):
        title = Text("THE DOPPLER EFFECT", font_size=42, color=TECH_CYAN, weight=BOLD)
        fit(title).move_to(UP * 3.4)
        self.play(Write(title), run_time=1.2)

        src = Dot(LEFT * 1.7 + UP * 1.5, radius=0.15, color=AMBER)
        vel = Arrow(src.get_center(), src.get_center() + RIGHT * 0.85,
                    color=AMBER, stroke_width=6, buff=0.16,
                    max_tip_length_to_length_ratio=0.3)
        self.play(FadeIn(src, scale=2), GrowArrow(vel), run_time=0.8)

        emitted = VGroup()
        for _ in range(6):
            ring = Circle(radius=0.16, color=TECH_CYAN, stroke_width=3.5)
            ring.move_to(src.get_center())
            emitted.add(ring)
            self.add(ring)
            self.play(src.animate.shift(RIGHT * 0.45), vel.animate.shift(RIGHT * 0.45),
                      *[r.animate.scale(1.5) for r in emitted],
                      run_time=0.8, rate_func=linear)
        self.play(emitted.animate.set_stroke(opacity=0.28), run_time=0.4)

        ahead = VGroup(
            Text("AHEAD", font_size=32, color=NEON_PINK, weight=BOLD),
            Text("squeezed → higher", font_size=27, color=NEON_PINK),
        ).arrange(DOWN, buff=0.1)
        fit(ahead).move_to(DOWN * 1.15)
        behind = VGroup(
            Text("BEHIND", font_size=32, color=TECH_CYAN, weight=BOLD),
            Text("stretched → lower", font_size=27, color=TECH_CYAN),
        ).arrange(DOWN, buff=0.1)
        fit(behind).move_to(DOWN * 2.15)

        self.play(FadeIn(ahead, shift=UP * 0.2), run_time=0.9)
        self.play(FadeIn(behind, shift=UP * 0.2), run_time=0.9)

        kick = Text("a moving source squeezes", font_size=27, color=TEXT_WHITE)
        kick2 = Text("its own wavefronts", font_size=27, color=TEXT_WHITE)
        kg = VGroup(kick, kick2).arrange(DOWN, buff=0.1)
        fit(kg).move_to(DOWN * 3.05)
        self.play(FadeIn(kg), run_time=1.1)
        self.wait(0.7)
        self.fill()


# ============================ 3 : THE ECHO ============================
class Short3(NarratedShort):
    def construct(self):
        title = Text("SAME FOR RADIO WAVES", font_size=40, color=RADAR_GREEN, weight=BOLD)
        fit(title).move_to(UP * 3.4)
        self.play(Write(title), run_time=1.0)

        gun = speed_gun(scale=1.05).move_to(LEFT * 1.4 + UP * 1.4)
        veh = car(scale=1.05).move_to(RIGHT * 1.35 + UP * 1.35)
        self.play(FadeIn(gun), FadeIn(veh), run_time=0.8)

        out = VGroup(*[Arc(radius=0.3 + i * 0.3, start_angle=-PI / 5, angle=2 * PI / 5,
                           color=TECH_CYAN, stroke_width=5)
                       .move_arc_center_to(gun[3].get_center()) for i in range(4)])
        out_l = Text("goes out at  f₀", font_size=27, color=TECH_CYAN)
        fit(out_l).move_to(DOWN * 0.35)
        self.play(LaggedStart(*[Create(a) for a in out], lag_ratio=0.15),
                  FadeIn(out_l), run_time=1.6)
        self.play(Flash(veh.get_center(), color=AMBER, flash_radius=0.8,
                        line_length=0.25, num_lines=14), run_time=0.5)

        back = VGroup(*[Arc(radius=0.28 + i * 0.16, start_angle=PI * 0.8, angle=2 * PI / 5,
                            color=NEON_PINK, stroke_width=5)
                        .move_arc_center_to(veh.get_left() + LEFT * 0.1) for i in range(4)])
        back_l = VGroup(
            Text("comes back at  f₀ + f_d", font_size=27, color=NEON_PINK),
            Text("squeezed by the moving car", font_size=24, color=DIM_TEXT),
        ).arrange(DOWN, buff=0.12)
        fit(back_l).move_to(DOWN * 1.35)
        self.play(LaggedStart(*[Create(a) for a in back], lag_ratio=0.15),
                  FadeIn(back_l), run_time=1.6)

        kick = VGroup(
            Text("measure that difference", font_size=30, color=AMBER, weight=BOLD),
            Text("and you have the speed", font_size=30, color=AMBER, weight=BOLD),
        ).arrange(DOWN, buff=0.12)
        fit(kick).move_to(DOWN * 2.9)
        self.play(FadeIn(kick, shift=UP * 0.2), run_time=1.1)
        self.wait(0.9)
        self.fill()


# ============================ 4 : THE EQUATION ============================
class Short4(NarratedShort):
    def construct(self):
        eq = Text("f_d  =  2v / λ", font_size=76, color=AMBER, weight=BOLD)
        fit(eq, 3.4).move_to(UP * 2.2)
        box = panel(eq, color=AMBER, buff=0.34)
        self.play(Create(box), Write(eq), run_time=1.8)

        why = Text("why the 2 ?", font_size=40, color=NEON_PINK, weight=BOLD)
        fit(why).move_to(UP * 0.75)
        self.play(FadeIn(why, shift=UP * 0.2), run_time=0.7)

        step1 = VGroup(
            Text("1  the wave reaches you", font_size=29, color=TECH_CYAN),
            Text("shift #1", font_size=25, color=DIM_TEXT),
        ).arrange(DOWN, buff=0.1)
        step2 = VGroup(
            Text("2  you reflect it, still moving", font_size=29, color=NEON_PINK),
            Text("shift #2", font_size=25, color=DIM_TEXT),
        ).arrange(DOWN, buff=0.1)
        steps = VGroup(step1, step2).arrange(DOWN, buff=0.55)
        fit(steps).move_to(DOWN * 0.85)

        self.play(FadeIn(step1, shift=RIGHT * 0.2), run_time=0.9)
        self.play(FadeIn(step2, shift=RIGHT * 0.2), run_time=0.9)

        tot = Text("shifted twice  →  ×2", font_size=34, color=RADAR_GREEN, weight=BOLD)
        fit(tot).move_to(DOWN * 2.6)
        self.play(FadeIn(tot, shift=UP * 0.2), run_time=0.9)
        self.play(Indicate(eq, color=AMBER, scale_factor=1.08), run_time=0.9)
        self.wait(0.7)
        self.fill()


# ============================ 5 : THE NUMBERS ============================
class Short5(NarratedShort):
    def construct(self):
        title = Text("HOW BIG IS IT?", font_size=44, color=RADAR_GREEN, weight=BOLD)
        fit(title).move_to(UP * 3.35)
        band = VGroup(
            Text("24 GHz police radar", font_size=30, color=TEXT_WHITE),
            Text("λ  =  1.25 cm", font_size=32, color=TECH_CYAN, weight=BOLD),
        ).arrange(DOWN, buff=0.14)
        fit(band).move_to(UP * 2.1)
        self.play(Write(title), run_time=1.0)
        self.play(FadeIn(band, shift=UP * 0.2), run_time=1.0)

        def row(what, speed, shift, color):
            a = Text(what, font_size=29, color=TEXT_WHITE)
            b = Text(speed, font_size=25, color=DIM_TEXT)
            c = Text(shift, font_size=40, color=color, weight=BOLD)
            g = VGroup(a, b, c).arrange(DOWN, buff=0.12)
            return VGroup(panel(g, color=color, buff=0.26), fit(g, 3.4))

        r1 = row("a car", "30 m/s", "4.8 kHz", AMBER)
        r2 = row("a person walking", "1 m/s", "160 Hz", RADAR_GREEN)
        rows = VGroup(r1, r2).arrange(DOWN, buff=0.45)
        fit(rows).move_to(DOWN * 0.35)

        self.play(FadeIn(r1, shift=UP * 0.2), run_time=0.9)
        self.wait(0.7)
        self.play(FadeIn(r2, shift=UP * 0.2), run_time=0.9)
        self.wait(0.6)
        self.play(Indicate(r1, color=AMBER, scale_factor=1.06), run_time=0.8)

        kick = VGroup(
            Text("kilohertz on a gigahertz carrier", font_size=26, color=TEXT_WHITE),
            Text("tiny — but trivial to measure", font_size=28, color=AMBER, weight=BOLD),
        ).arrange(DOWN, buff=0.14)
        fit(kick).move_to(DOWN * 3.05)
        self.play(FadeIn(kick, shift=UP * 0.2), run_time=1.1)
        self.wait(0.6)
        self.fill()


# ============================ 6 : THE CATCH ============================
class Short6(NarratedShort):
    def construct(self):
        title = Text("ONE CATCH", font_size=52, color=NEON_PINK, weight=BOLD)
        fit(title).move_to(UP * 3.35)
        self.play(FadeIn(title, scale=1.2), run_time=0.9)

        gun = speed_gun(scale=0.9).move_to(LEFT * 1.45 + DOWN * 1.9)
        origin = gun[3].get_center()
        tgt_pos = RIGHT * 0.75 + UP * 0.75
        los = DashedLine(origin, tgt_pos, color=SUBTLE, stroke_width=2.5, dash_length=0.1)
        veh = car(scale=0.85).move_to(tgt_pos)
        self.play(FadeIn(gun), Create(los), FadeIn(veh), run_time=1.1)

        d = tgt_pos - origin
        los_dir = d / np.linalg.norm(d)
        theta = ValueTracker(0.0)

        v_arrow = always_redraw(lambda: Arrow(
            tgt_pos, tgt_pos + rotate_vector(los_dir, theta.get_value()) * 1.25,
            color=AMBER, stroke_width=7, buff=0, max_tip_length_to_length_ratio=0.24))
        self.add(v_arrow)

        eq = Text("v_r  =  v · cos θ", font_size=44, color=AMBER, weight=BOLD)
        fit(eq, 3.6).move_to(UP * 2.65)
        self.play(Write(eq), run_time=1.0)

        readout = live_text(lambda: f"θ = {np.degrees(theta.get_value()):.0f}°   "
                                    f"f_d ∝ {np.cos(theta.get_value()):.2f}",
                            color=TECH_CYAN, font_size=30,
                            anchor=LEFT * 1.9 + UP * 2.1)
        self.add(readout)

        headon = Text("head-on  →  full speed", font_size=28, color=RADAR_GREEN)
        fit(headon).move_to(DOWN * 3.05)
        self.play(FadeIn(headon), run_time=0.8)
        self.wait(0.5)

        self.play(FadeOut(headon), theta.animate.set_value(PI / 2),
                  run_time=2.4, rate_func=smooth)
        readout.clear_updaters()

        gone = VGroup(
            Text("90° across the beam", font_size=30, color=NEON_PINK),
            Text("f_d  =  0", font_size=44, color=NEON_PINK, weight=BOLD),
            Text("INVISIBLE", font_size=40, color=NEON_PINK, weight=BOLD),
        ).arrange(DOWN, buff=0.14)
        fit(gone).move_to(DOWN * 2.85)
        self.play(FadeIn(gone, shift=UP * 0.2),
                  Flash(veh.get_center(), color=NEON_PINK, flash_radius=1.0,
                        line_length=0.25, num_lines=16), run_time=1.2)

        last = Text("which is why they", font_size=28, color=TEXT_WHITE)
        last2 = Text("never aim it sideways", font_size=28, color=TEXT_WHITE)
        lg = VGroup(last, last2).arrange(DOWN, buff=0.1)
        fit(lg).move_to(DOWN * 2.85)
        self.play(FadeOut(gone), FadeIn(lg), run_time=1.0)
        self.wait(0.8)
        self.fill()
