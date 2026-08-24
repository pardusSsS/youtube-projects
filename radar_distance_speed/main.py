"""
How Radar Measures Distance AND Speed
=====================================

Twenty Manim scenes, one per narration block.  Every scene inherits from
`NarratedScene`, whose `fill()` call pads the scene out to the exact length of
its MP3 in `voiceovers/durations.json`.  Run `voice.py` before rendering, or
build the whole thing with `build.py`.
"""

import json
import os

import numpy as np
from manim import *

# ============================ LOOK & FEEL ============================
DEEP_NAVY = "#050A1A"
PANEL_NAVY = "#0C1730"
SUBTLE = "#22314F"
RADAR_GREEN = "#00FF9C"
TECH_CYAN = "#00E5FF"
NEON_PINK = "#FF2D6F"
AMBER = "#FFB300"
TEXT_WHITE = "#EAF2FF"
DIM_TEXT = "#8FA3C4"

config.background_color = DEEP_NAVY

# ============================ NARRATION SYNC ============================
_HERE = os.path.dirname(os.path.abspath(__file__))
_DUR_FILE = os.path.join(_HERE, "voiceovers", "durations.json")
NARRATION = json.load(open(_DUR_FILE)) if os.path.exists(_DUR_FILE) else {}
TAIL = 0.6          # breathing room after the voice stops


class NarratedScene(Scene):
    """Scene that stretches its own tail so picture length == narration length."""

    def fill(self):
        name = type(self).__name__
        target = NARRATION.get(name)
        played = self.renderer.time
        if target is None:
            print(f"[SYNC] {name}: no narration entry, holding 1.0s")
            self.wait(1.0)
            return
        pad = target + TAIL - played
        flag = "  <-- LONG PAD" if pad > 5 else ("  <-- OVERRUN" if pad < 0 else "")
        print(f"[SYNC] {name}: anim={played:6.2f}s  voice={target:6.2f}s  pad={pad:6.2f}s{flag}")
        self.wait(max(pad, 0.35))


# ============================ SHARED BUILDERS ============================
def head(text, color=TECH_CYAN, size=40):
    t = Text(text, font_size=size, color=color, weight=BOLD).to_edge(UP, buff=0.35)
    rule = Line(LEFT * 6.3, RIGHT * 6.3, stroke_width=2, color=SUBTLE)
    rule.next_to(t, DOWN, buff=0.16)
    return VGroup(t, rule)


def panel(mob, color=TECH_CYAN, buff=0.3, opacity=0.10):
    return RoundedRectangle(
        corner_radius=0.14,
        width=mob.width + 2 * buff,
        height=mob.height + 2 * buff,
        stroke_color=color, stroke_width=2.5,
        fill_color=color, fill_opacity=opacity,
    ).move_to(mob)


def formula(text, color=AMBER, size=46):
    return Text(text, font_size=size, color=color, weight=BOLD)


def dish(scale=1.0, color=TECH_CYAN):
    """A simple parabolic-dish side view pointing right."""
    face = Arc(radius=0.9, start_angle=PI * 0.62, angle=-PI * 1.24,
               color=color, stroke_width=6)
    feed = Line(face.get_center() + LEFT * 0.0, RIGHT * 0.55, color=color, stroke_width=4)
    feed.move_to(face.get_center() + RIGHT * 0.3)
    horn = Dot(feed.get_right(), radius=0.09, color=AMBER)
    mast = Line(ORIGIN, DOWN * 0.9, color=color, stroke_width=5).next_to(face, DOWN, buff=0)
    base = Line(LEFT * 0.4, RIGHT * 0.4, color=color, stroke_width=6).next_to(mast, DOWN, buff=0)
    return VGroup(face, feed, horn, mast, base).scale(scale)


def plane(color=TEXT_WHITE, scale=1.0):
    """Small top-down aircraft silhouette pointing left."""
    body = Polygon([0.7, 0, 0], [-0.5, 0.13, 0], [-0.7, 0, 0], [-0.5, -0.13, 0],
                   color=color, fill_color=color, fill_opacity=1, stroke_width=1)
    wing = Polygon([0.05, 0, 0], [-0.35, 0.55, 0], [-0.45, 0.55, 0], [-0.25, 0, 0],
                   color=color, fill_color=color, fill_opacity=1, stroke_width=1)
    wing2 = wing.copy().flip(RIGHT, about_point=ORIGIN)
    tail = Polygon([-0.5, 0, 0], [-0.68, 0.25, 0], [-0.75, 0.25, 0], [-0.7, 0, 0],
                   color=color, fill_color=color, fill_opacity=1, stroke_width=1)
    tail2 = tail.copy().flip(RIGHT, about_point=ORIGIN)
    return VGroup(body, wing, wing2, tail, tail2).scale(scale)


def live_text(fn, font_size=38, color=TECH_CYAN, anchor=ORIGIN, edge=LEFT):
    """A self-updating readout built from Text (Manim's DecimalNumber needs LaTeX)."""
    return always_redraw(
        lambda: Text(fn(), font_size=font_size, color=color, weight=BOLD)
        .move_to(anchor, aligned_edge=edge))


def bullet(text, color=TEXT_WHITE, size=28, dot_color=RADAR_GREEN):
    d = Text("▸", font_size=size, color=dot_color)
    t = Text(text, font_size=size, color=color)
    return VGroup(d, t).arrange(RIGHT, buff=0.22)


# ============================ PART 1 : HOOK ============================
class Part1(NarratedScene):
    def construct(self):
        rings = VGroup(*[Circle(radius=r, color=SUBTLE, stroke_width=2)
                         for r in (1.15, 2.3, 3.45)])
        cross = VGroup(Line(LEFT * 3.45, RIGHT * 3.45, color=SUBTLE, stroke_width=1.5),
                       Line(DOWN * 3.45, UP * 3.45, color=SUBTLE, stroke_width=1.5))
        scope = VGroup(rings, cross)

        wedge = AnnularSector(inner_radius=0.0, outer_radius=3.45, angle=-0.65,
                              start_angle=PI / 2, color=RADAR_GREEN,
                              fill_opacity=0.20, stroke_width=0)
        sweep = Line(ORIGIN, UP * 3.45, color=RADAR_GREEN, stroke_width=4)
        beam = VGroup(wedge, sweep)

        np.random.seed(11)
        blip_pts = [np.array([2.1, 1.4, 0]), np.array([-1.9, 1.9, 0]),
                    np.array([-2.6, -1.2, 0]), np.array([1.2, -2.4, 0]),
                    np.array([2.9, -0.6, 0]), np.array([-0.7, -1.5, 0])]
        blips = VGroup(*[Dot(p, radius=0.10, color=AMBER) for p in blip_pts])

        self.play(Create(rings, lag_ratio=0.3), Create(cross), run_time=1.8)
        self.add(beam)
        self.play(Rotate(beam, -TAU, about_point=ORIGIN, rate_func=linear),
                  LaggedStart(*[FadeIn(b, scale=3) for b in blips], lag_ratio=0.22),
                  run_time=5.0)
        self.play(Rotate(beam, -TAU, about_point=ORIGIN, rate_func=linear), run_time=5.0)

        backdrop = VGroup(scope, beam, blips)
        self.play(backdrop.animate.set_opacity(0.16), run_time=0.8)
        self.remove(beam)

        t1 = Text("HOW RADAR MEASURES", font_size=50, color=TEXT_WHITE, weight=BOLD)
        t2 = Text("DISTANCE  AND  SPEED", font_size=62, color=TECH_CYAN, weight=BOLD)
        title = VGroup(t1, t2).arrange(DOWN, buff=0.22).shift(UP * 1.55)
        self.play(FadeIn(t1, shift=DOWN * 0.3), run_time=1.0)
        self.play(Write(t2), run_time=1.6)

        def card(label, arrow_txt, eq, color):
            lab = Text(label, font_size=32, color=color, weight=BOLD)
            src = Text(arrow_txt, font_size=23, color=DIM_TEXT)
            f = Text(eq, font_size=34, color=TEXT_WHITE, weight=BOLD)
            g = VGroup(lab, src, f).arrange(DOWN, buff=0.18)
            return VGroup(panel(g, color=color, buff=0.34), g)

        c1 = card("RANGE", "from  TIME OF FLIGHT", "R = c·Δt / 2", RADAR_GREEN)
        c2 = card("VELOCITY", "from  DOPPLER SHIFT", "v = λ·f_d / 2", NEON_PINK)
        cards = VGroup(c1, c2).arrange(RIGHT, buff=0.9).shift(DOWN * 1.35)

        self.play(FadeIn(c1, shift=UP * 0.4), run_time=1.1)
        self.play(FadeIn(c2, shift=UP * 0.4), run_time=1.1)

        tagline = Text("two answers · two different physics · one echo",
                       font_size=26, color=AMBER)
        tagline.to_edge(DOWN, buff=0.4)
        self.play(Write(tagline), run_time=1.8)
        self.wait(1.0)
        self.play(Indicate(c1, color=RADAR_GREEN, scale_factor=1.06), run_time=0.9)
        self.play(Indicate(c2, color=NEON_PINK, scale_factor=1.06), run_time=0.9)
        self.wait(1.0)

        self.play(FadeOut(tagline), run_time=0.5)
        road = VGroup(
            Text("time of flight  ·  range resolution  ·  ambiguous range",
                 font_size=24, color=DIM_TEXT),
            Text("the Doppler shift  ·  radial velocity  ·  phase across pulses",
                 font_size=24, color=DIM_TEXT),
            Text("range-Doppler maps  ·  blind speeds  ·  FMCW chirps",
                 font_size=24, color=DIM_TEXT),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.38)
        for r in road:
            self.play(FadeIn(r, shift=UP * 0.2), run_time=1.0)
            self.wait(0.8)
        self.wait(0.6)
        for _ in range(2):
            ping = Circle(radius=0.25, color=RADAR_GREEN, stroke_width=5).move_to(ORIGIN)
            self.add(ping)
            self.play(ping.animate.scale(16).set_stroke(opacity=0.0),
                      run_time=2.0, rate_func=linear)
            self.remove(ping)
        self.wait(0.8)
        self.fill()


# ============================ PART 2 : THE PULSE ============================
class Part2(NarratedScene):
    def construct(self):
        h = head("IT ALL STARTS WITH A PULSE")
        self.play(FadeIn(h[0]), Create(h[1]), run_time=1.2)

        radar = dish(scale=1.0).move_to(LEFT * 5.2 + DOWN * 0.6)
        ground = Line(LEFT * 6.6, RIGHT * 6.6, color=SUBTLE, stroke_width=3).shift(DOWN * 2.6)
        target = plane(color=TEXT_WHITE, scale=1.15).move_to(RIGHT * 4.6 + UP * 1.1)
        target.rotate(PI)  # nose to the right

        self.play(Create(ground), FadeIn(radar, shift=RIGHT * 0.3), run_time=1.4)
        self.play(FadeIn(target, shift=LEFT * 0.5), run_time=1.0)

        origin = radar[2].get_center()

        def wavefronts(n=5, color=TECH_CYAN):
            return VGroup(*[Arc(radius=0.35 + i * 0.28, start_angle=-PI / 3.4,
                                angle=2 * PI / 3.4, color=color,
                                stroke_width=5 - i * 0.5).move_arc_center_to(origin)
                            for i in range(n)])

        pulse = wavefronts()
        self.play(LaggedStart(*[Create(a) for a in pulse], lag_ratio=0.12), run_time=1.2)
        self.play(pulse.animate.scale(4.6, about_point=origin).set_opacity(0.35),
                  run_time=2.6, rate_func=linear)
        self.play(FadeOut(pulse), run_time=0.4)

        c_exact = Text("c = 299 792 458 m/s", font_size=40, color=RADAR_GREEN, weight=BOLD)
        c_round = Text("c ≈ 3 × 10⁸ m/s", font_size=48, color=RADAR_GREEN, weight=BOLD)
        c_exact.move_to(DOWN * 0.9 + RIGHT * 0.4)
        c_round.move_to(c_exact)
        box = panel(c_round, color=RADAR_GREEN, buff=0.35)

        self.play(Write(c_exact), run_time=1.8)
        self.wait(0.8)
        self.play(Create(box), Transform(c_exact, c_round), run_time=1.2)

        pts = VGroup(
            bullet("fixed in free space", TEXT_WHITE),
            bullet("independent of transmitter, target, weather", TEXT_WHITE),
            bullet("a speed you KNOW turns time into distance", AMBER, dot_color=AMBER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(box, DOWN, buff=0.5)
        pts.set_x(0)

        for b in pts:
            self.play(FadeIn(b, shift=RIGHT * 0.3), run_time=0.9)
            self.wait(0.5)

        self.play(Indicate(pts[2], color=AMBER, scale_factor=1.05), run_time=1.0)
        self.wait(0.6)

        self.play(FadeOut(pts), FadeOut(box), FadeOut(c_exact),
                  FadeOut(radar), FadeOut(target), FadeOut(ground), run_time=0.8)
        scale_line = Line(LEFT * 5.2, RIGHT * 5.2, color=SUBTLE, stroke_width=3).shift(DOWN * 1.5)
        marks = VGroup(*[Line(DOWN * 0.14, UP * 0.14, color=DIM_TEXT, stroke_width=2)
                         .move_to(scale_line.get_left() + RIGHT * i * 1.3) for i in range(9)])
        tick_lbl = VGroup(*[Text(f"{i} μs", font_size=18, color=DIM_TEXT)
                            .next_to(marks[i], DOWN, buff=0.12) for i in range(0, 9, 2)])
        self.play(Create(scale_line), Create(marks), FadeIn(tick_lbl), run_time=1.4)
        cap = Text("300 metres every microsecond", font_size=30, color=AMBER)
        cap.next_to(scale_line, UP, buff=0.6)
        photon = Dot(scale_line.get_left(), radius=0.12, color=AMBER)
        self.play(FadeIn(cap), FadeIn(photon, scale=2), run_time=0.9)
        self.play(photon.animate.move_to(scale_line.get_right()), run_time=5.0, rate_func=linear)
        self.wait(0.7)
        km = Text("so 1 km, out and back, costs 6.67 μs of delay",
                  font_size=30, color=RADAR_GREEN, weight=BOLD).to_edge(DOWN, buff=0.6)
        self.play(Write(km), run_time=2.0)
        self.wait(2.2)
        self.fill()


# ============================ PART 3 : ROUND TRIP TIME ============================
class Part3(NarratedScene):
    def construct(self):
        h = head("RANGE  =  TIME OF FLIGHT")
        self.play(FadeIn(h[0]), Create(h[1]), run_time=1.0)

        radar = dish(scale=0.8).move_to(LEFT * 5.4 + UP * 1.4)
        tgt = plane(scale=1.0).rotate(PI).move_to(RIGHT * 4.8 + UP * 1.4)
        path = DashedLine(radar.get_right() + RIGHT * 0.15, tgt.get_left(),
                          color=SUBTLE, stroke_width=2, dash_length=0.14)
        rlabel = Text("R = ?", font_size=30, color=AMBER).next_to(path, UP, buff=0.18)

        self.play(FadeIn(radar), FadeIn(tgt), Create(path), Write(rlabel), run_time=1.8)

        out = Arrow(radar.get_right() + RIGHT * 0.2, tgt.get_left() + LEFT * 0.1,
                    color=TECH_CYAN, stroke_width=6, buff=0, max_tip_length_to_length_ratio=0.05)
        back = Arrow(tgt.get_left() + LEFT * 0.1, radar.get_right() + RIGHT * 0.2,
                     color=NEON_PINK, stroke_width=6, buff=0,
                     max_tip_length_to_length_ratio=0.05).shift(DOWN * 0.45)
        out_l = Text("transmit", font_size=22, color=TECH_CYAN).next_to(out, UP, buff=0.12)
        back_l = Text("echo", font_size=22, color=NEON_PINK).next_to(back, DOWN, buff=0.12)

        self.play(GrowArrow(out), FadeIn(out_l), run_time=1.4)
        self.play(Flash(tgt.get_center(), color=AMBER, line_length=0.3,
                        num_lines=14, flash_radius=0.7), run_time=0.7)
        self.play(GrowArrow(back), FadeIn(back_l), run_time=1.4)

        # timing strip
        axis = Line(LEFT * 5.6, RIGHT * 5.6, color=DIM_TEXT, stroke_width=3).shift(DOWN * 2.0)
        tick0 = Line(DOWN * 0.22, UP * 0.22, color=TEXT_WHITE, stroke_width=3).move_to(axis.get_left())
        tick1 = Line(DOWN * 0.22, UP * 0.22, color=TEXT_WHITE, stroke_width=3).move_to(axis.get_left() + RIGHT * 7.4)
        tx = Text("TX", font_size=24, color=TECH_CYAN).next_to(tick0, DOWN, buff=0.2)
        rx = Text("RX", font_size=24, color=NEON_PINK).next_to(tick1, DOWN, buff=0.2)
        pulse_tx = Rectangle(width=0.16, height=0.75, fill_color=TECH_CYAN, fill_opacity=1,
                             stroke_width=0).next_to(tick0, UP, buff=0.02)
        pulse_rx = Rectangle(width=0.16, height=0.5, fill_color=NEON_PINK, fill_opacity=1,
                             stroke_width=0).next_to(tick1, UP, buff=0.02)
        brace = BraceBetweenPoints(tick0.get_bottom() + DOWN * 0.65,
                                   tick1.get_bottom() + DOWN * 0.65, direction=DOWN)
        dt = Text("Δt", font_size=32, color=AMBER, weight=BOLD).next_to(brace, DOWN, buff=0.12)

        self.play(Create(axis), Create(tick0), Create(tick1), FadeIn(tx), FadeIn(rx), run_time=1.2)
        self.play(FadeIn(pulse_tx, scale=1.5), run_time=0.5)
        self.play(FadeIn(pulse_rx, scale=1.5), run_time=0.5)
        self.play(GrowFromCenter(brace), Write(dt), run_time=1.0)

        eq = Text("R  =  c · Δt / 2", font_size=52, color=AMBER, weight=BOLD).move_to(DOWN * 0.45)
        self.play(Write(eq), run_time=1.6)
        half = SurroundingRectangle(eq[-2:], color=NEON_PINK, stroke_width=3, buff=0.08)
        note = Text("the wave travels the distance TWICE", font_size=24, color=NEON_PINK)
        note.next_to(eq, DOWN, buff=0.22)
        self.play(Create(half), FadeIn(note), run_time=1.2)
        self.play(Indicate(half, color=NEON_PINK), run_time=0.9)
        self.wait(0.8)

        self.play(FadeOut(VGroup(out, back, out_l, back_l)), run_time=0.6)
        tt = ValueTracker(0.0)
        clk_lbl = Text("elapsed", font_size=22, color=DIM_TEXT).move_to(LEFT * 4.6 + UP * 2.85)
        clk = live_text(lambda: f"{tt.get_value():.1f} μs", color=AMBER, font_size=40,
                        anchor=LEFT * 4.9 + UP * 2.3)
        photon = Dot(radar.get_right() + RIGHT * 0.2, radius=0.13, color=AMBER)
        self.play(FadeIn(clk_lbl), FadeIn(photon, scale=2), run_time=0.8)
        self.add(clk)
        self.play(photon.animate.move_to(tgt.get_left() + LEFT * 0.1),
                  tt.animate.set_value(50), run_time=3.4, rate_func=linear)
        self.play(Flash(tgt.get_center(), color=AMBER, flash_radius=0.7,
                        num_lines=14, line_length=0.3), run_time=0.6)
        self.play(photon.animate.set_color(NEON_PINK).move_to(radar.get_right() + RIGHT * 0.2),
                  tt.animate.set_value(100), run_time=3.4, rate_func=linear)
        clk.clear_updaters()
        self.play(Indicate(clk, color=AMBER, scale_factor=1.15), run_time=0.9)
        self.wait(0.8)
        deriv = VGroup(
            Text("path travelled  =  c · Δt", font_size=27, color=DIM_TEXT),
            Text("but that path  =  2R", font_size=27, color=RADAR_GREEN, weight=BOLD),
        ).arrange(DOWN, buff=0.22).move_to(RIGHT * 4.1 + UP * 2.55)
        self.play(FadeIn(deriv[0]), run_time=1.0)
        self.play(FadeIn(deriv[1], shift=UP * 0.2), run_time=1.4)
        self.wait(1.2)
        self.play(Indicate(eq, color=AMBER, scale_factor=1.06), run_time=1.0)
        self.wait(2.6)
        self.fill()


# ============================ PART 4 : WORKED EXAMPLE ============================
class Part4(NarratedScene):
    def construct(self):
        h = head("A WORKED EXAMPLE", color=AMBER)
        self.play(FadeIn(h[0]), Create(h[1]), run_time=1.0)

        given = Text("echo arrives  Δt = 100 μs  after transmission",
                     font_size=34, color=TEXT_WHITE).shift(UP * 1.9)
        self.play(Write(given), run_time=2.0)

        steps = VGroup(
            Text("total path  =  c × Δt", font_size=36, color=DIM_TEXT),
            Text("=  3×10⁸ m/s  ×  100×10⁻⁶ s", font_size=36, color=TEXT_WHITE),
            Text("=  30 000 m", font_size=40, color=TECH_CYAN, weight=BOLD),
            Text("R  =  30 000 / 2  =  15 000 m", font_size=40, color=RADAR_GREEN, weight=BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36).shift(UP * 0.05)
        steps.set_x(-0.6)

        for s in steps:
            self.play(FadeIn(s, shift=RIGHT * 0.35), run_time=0.95)
            self.wait(0.55)

        answer = Text("15 km", font_size=64, color=AMBER, weight=BOLD)
        answer.next_to(steps, DOWN, buff=0.5).set_x(0)
        abox = panel(answer, color=AMBER, buff=0.32)
        self.play(Create(abox), Write(answer), run_time=1.3)
        self.play(Flash(answer.get_center(), color=AMBER, flash_radius=1.6,
                        line_length=0.35, num_lines=18), run_time=0.8)

        rule = VGroup(
            Text("RULES OF THUMB", font_size=24, color=NEON_PINK, weight=BOLD),
            Text("6.67 μs  per km  of range", font_size=26, color=TEXT_WHITE),
            Text("12.36 μs  per nautical mile", font_size=26, color=TEXT_WHITE),
        ).arrange(DOWN, buff=0.16)
        rule.to_edge(DOWN, buff=0.42)
        rbox = panel(rule, color=NEON_PINK, buff=0.26)
        self.play(FadeIn(rbox), FadeIn(rule), run_time=1.2)
        self.wait(0.9)

        self.play(FadeOut(VGroup(given, steps, answer, abox)), run_time=0.9)
        ex2t = Text("a second one:  Δt = 1 ms", font_size=34, color=TEXT_WHITE).shift(UP * 2.15)
        ex2 = VGroup(
            Text("c × Δt  =  3×10⁸ × 1×10⁻³  =  300 000 m", font_size=32, color=TEXT_WHITE),
            Text("R  =  150 000 m  =  150 km", font_size=40, color=RADAR_GREEN, weight=BOLD),
        ).arrange(DOWN, buff=0.35).shift(UP * 1.0)
        self.play(Write(ex2t), run_time=1.6)
        self.play(FadeIn(ex2[0], shift=RIGHT * 0.3), run_time=1.1)
        self.wait(0.8)
        self.play(FadeIn(ex2[1], shift=RIGHT * 0.3), run_time=1.1)
        self.wait(1.0)
        ladder = VGroup(*[Text(t, font_size=26, color=c) for t, c in [
            ("6.67 μs   →       1 km", TEXT_WHITE),
            ("66.7 μs   →      10 km", TEXT_WHITE),
            ("667 μs    →     100 km", TEXT_WHITE),
            ("2.00 ms   →     300 km", AMBER),
        ]]).arrange(DOWN, aligned_edge=LEFT, buff=0.2).shift(DOWN * 0.75)
        for l in ladder:
            self.play(FadeIn(l, shift=LEFT * 0.25), run_time=0.7)
            self.wait(0.5)
        self.wait(0.8)
        lin = Text("delay and range are simply proportional — nothing else to it",
                   font_size=27, color=TECH_CYAN).shift(DOWN * 2.35)
        self.play(Write(lin), run_time=2.0)
        self.play(Indicate(ex2[1], color=RADAR_GREEN, scale_factor=1.06), run_time=1.0)
        self.wait(2.0)
        self.fill()


# ============================ PART 5 : RANGE RESOLUTION ============================
class Part5(NarratedScene):
    def construct(self):
        h = head("HOW FINELY?  RANGE RESOLUTION")
        self.play(FadeIn(h[0]), Create(h[1]), run_time=1.0)

        # a pulse drawn as a rectangular envelope on a range axis
        axis = Line(LEFT * 5.8, RIGHT * 5.8, color=DIM_TEXT, stroke_width=3).shift(UP * 1.4)
        axlabel = Text("range →", font_size=22, color=DIM_TEXT).next_to(axis, RIGHT, buff=0.12)
        wide = Rectangle(width=2.4, height=0.9, fill_color=TECH_CYAN, fill_opacity=0.45,
                         stroke_color=TECH_CYAN, stroke_width=3)
        wide.next_to(axis.get_left() + RIGHT * 1.6, UP, buff=0.02)
        br = Brace(wide, DOWN, buff=0.06)
        brl = Text("pulse length in space  =  c·τ", font_size=24, color=AMBER)
        brl.next_to(br, DOWN, buff=0.1)

        self.play(Create(axis), FadeIn(axlabel), run_time=0.9)
        self.play(FadeIn(wide, scale=0.6), run_time=0.8)
        self.play(GrowFromCenter(br), Write(brl), run_time=1.3)
        self.wait(0.6)

        # two close targets
        t1 = Dot(LEFT * 1.4 + DOWN * 0.7, radius=0.13, color=TEXT_WHITE)
        t2 = Dot(LEFT * 0.5 + DOWN * 0.7, radius=0.13, color=TEXT_WHITE)
        tl = Text("two targets, close together", font_size=24, color=TEXT_WHITE)
        tl.next_to(VGroup(t1, t2), UP, buff=0.25)
        self.play(FadeIn(t1, scale=2), FadeIn(t2, scale=2), FadeIn(tl), run_time=1.0)

        # merged echo
        merged = FunctionGraph(lambda x: 1.0 * np.exp(-((x + 0.95) ** 2) / 0.55),
                               x_range=[-4.5, 2.5], color=NEON_PINK, stroke_width=5)
        merged.shift(DOWN * 2.7)
        m_lab = Text("echoes overlap → ONE blip", font_size=26, color=NEON_PINK)
        m_lab.next_to(merged, RIGHT, buff=0.4).shift(UP * 0.3)
        self.play(Create(merged), FadeIn(m_lab), run_time=1.6)
        self.wait(0.8)

        # shorten the pulse -> resolved
        narrow = Rectangle(width=0.5, height=0.9, fill_color=RADAR_GREEN, fill_opacity=0.5,
                           stroke_color=RADAR_GREEN, stroke_width=3).move_to(wide).align_to(wide, LEFT)
        split = VGroup(
            FunctionGraph(lambda x: 1.0 * np.exp(-((x + 1.4) ** 2) / 0.05),
                          x_range=[-4.5, 2.5], color=RADAR_GREEN, stroke_width=5),
            FunctionGraph(lambda x: 1.0 * np.exp(-((x + 0.5) ** 2) / 0.05),
                          x_range=[-4.5, 2.5], color=RADAR_GREEN, stroke_width=5),
        ).shift(DOWN * 2.7)
        s_lab = Text("shorter pulse → TWO blips", font_size=26, color=RADAR_GREEN)
        s_lab.move_to(m_lab)
        self.play(Transform(wide, narrow), FadeOut(br), FadeOut(brl),
                  Transform(merged, split), Transform(m_lab, s_lab), run_time=1.8)
        self.wait(0.8)

        eq = Text("ΔR  =  c·τ / 2", font_size=48, color=AMBER, weight=BOLD).shift(UP * 0.15 + RIGHT * 3.1)
        ebox = panel(eq, color=AMBER, buff=0.28)
        self.play(Create(ebox), Write(eq), run_time=1.4)

        tab = VGroup(
            Text("τ = 1 μs      →   ΔR = 150 m", font_size=25, color=TEXT_WHITE),
            Text("τ = 100 ns   →   ΔR = 15 m", font_size=25, color=TEXT_WHITE),
            Text("τ = 10 ns     →   ΔR = 1.5 m", font_size=25, color=RADAR_GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        tab.next_to(ebox, DOWN, buff=0.4).set_x(3.1)
        for row in tab:
            self.play(FadeIn(row, shift=LEFT * 0.25), run_time=0.6)
        self.wait(0.7)

        self.play(FadeOut(VGroup(axis, axlabel, wide, t1, t2, tl, merged, m_lab)), run_time=0.9)
        self.play(VGroup(ebox, eq, tab).animate.move_to(LEFT * 3.4 + UP * 0.75), run_time=1.2)
        bw = VGroup(
            Text("the same statement in frequency:", font_size=25, color=DIM_TEXT),
            Text("ΔR  =  c / (2 · B)", font_size=44, color=TECH_CYAN, weight=BOLD),
            Text("B  =  signal BANDWIDTH", font_size=23, color=DIM_TEXT),
        ).arrange(DOWN, buff=0.22).move_to(RIGHT * 3.4 + UP * 1.5)
        self.play(FadeIn(bw[0]), run_time=0.8)
        self.play(Write(bw[1]), run_time=1.5)
        self.play(FadeIn(bw[2]), run_time=0.8)
        self.wait(1.0)
        bwtab = VGroup(
            Text("B = 1 MHz      →   ΔR = 150 m", font_size=25, color=TEXT_WHITE),
            Text("B = 150 MHz   →   ΔR = 1 m", font_size=25, color=TEXT_WHITE),
            Text("B = 4 GHz       →   ΔR = 3.75 cm", font_size=25, color=TECH_CYAN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        bwtab.next_to(bw, DOWN, buff=0.45).set_x(3.4)
        for r in bwtab:
            self.play(FadeIn(r, shift=LEFT * 0.25), run_time=0.7)
            self.wait(0.4)
        self.wait(0.6)
        pc = VGroup(
            Text("PULSE COMPRESSION", font_size=28, color=AMBER, weight=BOLD),
            Text("send a LONG chirp for energy, squeeze it on receive for resolution",
                 font_size=24, color=TEXT_WHITE),
            Text("so you no longer have to choose", font_size=26, color=RADAR_GREEN, weight=BOLD),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.4)
        for p in pc:
            self.play(FadeIn(p, shift=UP * 0.2), run_time=0.9)
            self.wait(0.5)
        self.play(Indicate(pc[2], color=RADAR_GREEN, scale_factor=1.05), run_time=1.0)
        self.wait(2.5)
        self.fill()


# ============================ PART 6 : PRF & AMBIGUOUS RANGE ============================
class Part6(NarratedScene):
    def construct(self):
        h = head("THE PRICE:  AMBIGUOUS RANGE", color=NEON_PINK)
        self.play(FadeIn(h[0]), Create(h[1]), run_time=1.0)

        base = Line(LEFT * 6.0, RIGHT * 6.0, color=DIM_TEXT, stroke_width=3).shift(UP * 0.6)
        xs = [-5.2, -1.8, 1.6, 5.0]
        txs = VGroup(*[Rectangle(width=0.18, height=1.1, fill_color=TECH_CYAN,
                                 fill_opacity=1, stroke_width=0)
                       .move_to(base.get_left() + RIGHT * (x + 6.0) + UP * 0.55)
                       for x in xs])
        self.play(Create(base), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(p, scale=1.4) for p in txs], lag_ratio=0.25), run_time=1.6)

        pri_brace = BraceBetweenPoints(txs[0].get_bottom(), txs[1].get_bottom(), direction=DOWN)
        pri_lab = VGroup(
            Text("PRI  =  1 / PRF", font_size=28, color=AMBER, weight=BOLD),
            Text("pulse repetition interval", font_size=20, color=DIM_TEXT),
        ).arrange(DOWN, buff=0.1).next_to(pri_brace, DOWN, buff=0.12)
        self.play(GrowFromCenter(pri_brace), FadeIn(pri_lab), run_time=1.3)
        self.wait(0.6)

        # a near echo (fine) and a far echo (arrives after next TX)
        near = Rectangle(width=0.14, height=0.55, fill_color=RADAR_GREEN, fill_opacity=1,
                         stroke_width=0).move_to(txs[0].get_center() + RIGHT * 1.1 + DOWN * 0.28)
        near_l = Text("near echo — safe", font_size=21, color=RADAR_GREEN).next_to(near, UP, buff=0.15)
        self.play(FadeIn(near, shift=DOWN * 0.2), FadeIn(near_l), run_time=1.0)
        self.wait(0.5)

        far = Rectangle(width=0.14, height=0.55, fill_color=NEON_PINK, fill_opacity=1,
                        stroke_width=0).move_to(txs[1].get_center() + RIGHT * 0.9 + DOWN * 0.28)
        far_arc = CurvedArrow(txs[0].get_top() + UP * 0.15, far.get_top() + UP * 0.15,
                              color=NEON_PINK, stroke_width=3, angle=-0.7)
        far_l = Text("echo of pulse 1 — arrives AFTER pulse 2", font_size=21, color=NEON_PINK)
        far_l.next_to(far_arc, UP, buff=0.1)
        self.play(Create(far_arc), FadeIn(far), FadeIn(far_l), run_time=1.6)
        self.wait(0.5)

        wrong = Text("displayed as a CLOSE target — second-time-around echo",
                     font_size=26, color=NEON_PINK, weight=BOLD).shift(DOWN * 2.15)
        self.play(Write(wrong), run_time=1.8)

        eq = Text("R_max  =  c / (2 · PRF)", font_size=46, color=AMBER, weight=BOLD).shift(DOWN * 3.05)
        ex = Text("PRF = 1 kHz  →  R_max = 150 km", font_size=26, color=TEXT_WHITE)
        ex.next_to(eq, DOWN, buff=0.22)
        self.play(Write(eq), run_time=1.4)
        self.play(FadeIn(ex), run_time=0.9)
        self.wait(0.7)

        self.play(FadeOut(VGroup(far_arc, far_l, near_l, wrong, pri_brace, pri_lab)), run_time=0.8)
        self.play(VGroup(eq, ex).animate.move_to(DOWN * 0.85), run_time=1.0)
        tbl = VGroup(
            Text("PRF            R_max", font_size=23, color=DIM_TEXT),
            Text("250 Hz      600 km", font_size=24, color=TEXT_WHITE),
            Text("1 kHz        150 km", font_size=24, color=TEXT_WHITE),
            Text("10 kHz         15 km", font_size=24, color=NEON_PINK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        tbl.move_to(LEFT * 4.4 + DOWN * 2.35)
        for r in tbl:
            self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.65)
            self.wait(0.35)
        self.play(Indicate(tbl[3], color=NEON_PINK, scale_factor=1.08), run_time=1.0)
        self.wait(1.0)
        tradeoff = VGroup(
            Text("raise the PRF  →  more pulses, better Doppler", font_size=23, color=RADAR_GREEN),
            Text("raise the PRF  →  and R_max collapses", font_size=23, color=NEON_PINK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        tradeoff.move_to(RIGHT * 2.6 + DOWN * 2.35)
        self.play(FadeIn(tradeoff[0], shift=LEFT * 0.25), run_time=1.1)
        self.wait(0.9)
        self.play(FadeIn(tradeoff[1], shift=LEFT * 0.25), run_time=1.1)
        self.wait(1.0)
        keep = Text("hold on to that tension — it comes back later",
                    font_size=27, color=AMBER, weight=BOLD).to_edge(DOWN, buff=0.35)
        self.play(Write(keep), run_time=1.9)
        self.play(Indicate(keep, color=AMBER, scale_factor=1.05), run_time=1.0)
        self.wait(2.4)
        self.fill()


# ============================ PART 7 : WHY RANGE-RATE FAILS ============================
class Part7(NarratedScene):
    def construct(self):
        h = head("SO... WHAT ABOUT SPEED?")
        self.play(FadeIn(h[0]), Create(h[1]), run_time=1.0)

        idea = Text("obvious idea:  measure range twice, divide by the time between",
                    font_size=30, color=TEXT_WHITE).shift(UP * 1.95)
        self.play(Write(idea), run_time=2.2)

        ax = Axes(x_range=[0, 6, 1], y_range=[0, 6, 1], x_length=7.2, y_length=3.6,
                  axis_config={"color": SUBTLE, "stroke_width": 2,
                               "include_ticks": False}).shift(LEFT * 2.6 + DOWN * 0.55)
        xl = Text("time", font_size=22, color=DIM_TEXT).next_to(ax, DOWN, buff=0.15)
        yl = Text("range", font_size=22, color=DIM_TEXT).next_to(ax, LEFT, buff=0.15)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=1.2)

        p1 = Dot(ax.c2p(1.4, 4.4), radius=0.11, color=TECH_CYAN)
        p2 = Dot(ax.c2p(4.4, 2.6), radius=0.11, color=TECH_CYAN)
        e1 = Line(ax.c2p(1.4, 3.5), ax.c2p(1.4, 5.3), color=NEON_PINK, stroke_width=5)
        e2 = Line(ax.c2p(4.4, 1.7), ax.c2p(4.4, 3.5), color=NEON_PINK, stroke_width=5)
        conn = DashedLine(p1.get_center(), p2.get_center(), color=AMBER, stroke_width=3)
        l1 = Text("R₁", font_size=24, color=TECH_CYAN).next_to(p1, LEFT, buff=0.2)
        l2 = Text("R₂", font_size=24, color=TECH_CYAN).next_to(p2, RIGHT, buff=0.2)

        self.play(FadeIn(p1, scale=2), Write(l1), run_time=0.8)
        self.play(FadeIn(p2, scale=2), Write(l2), run_time=0.8)
        self.play(Create(conn), run_time=0.8)
        self.play(Create(e1), Create(e2), run_time=1.0)
        err_l = Text("± range error", font_size=21, color=NEON_PINK).next_to(e1, UP, buff=0.12)
        self.play(FadeIn(err_l), run_time=0.7)

        calc = VGroup(
            Text("v  =  (R₂ − R₁) / Δt", font_size=34, color=AMBER, weight=BOLD),
            Text("range error   ±15 m", font_size=26, color=TEXT_WHITE),
            Text("time gap        0.1 s", font_size=26, color=TEXT_WHITE),
            Text("→  velocity error  ±150 m/s", font_size=30, color=NEON_PINK, weight=BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).shift(RIGHT * 3.7 + DOWN * 0.4)
        for c in calc:
            self.play(FadeIn(c, shift=LEFT * 0.25), run_time=0.75)
            self.wait(0.3)

        verdict = Text("far too crude for anything fast", font_size=30,
                       color=NEON_PINK, weight=BOLD).to_edge(DOWN, buff=0.55)
        self.play(Write(verdict), run_time=1.4)
        self.play(Indicate(calc[3], color=NEON_PINK, scale_factor=1.08), run_time=0.9)
        need = Text("we need something far more sensitive — the wave itself",
                    font_size=26, color=RADAR_GREEN)
        need.move_to(verdict)
        self.play(FadeOut(verdict), FadeIn(need), run_time=1.0)
        self.wait(0.6)

        self.play(FadeOut(VGroup(idea, ax, xl, yl, p1, p2, e1, e2, conn,
                                 l1, l2, err_l, calc, need)), run_time=1.0)
        cmp_hdr = Text("two ways to get velocity", font_size=32, color=TEXT_WHITE).shift(UP * 2.2)
        self.play(Write(cmp_hdr), run_time=1.5)

        def _box(title, a, b, c, color):
            t = Text(title, font_size=26, color=color, weight=BOLD)
            x = Text(a, font_size=22, color=TEXT_WHITE)
            y = Text(b, font_size=22, color=TEXT_WHITE)
            z = Text(c, font_size=25, color=color, weight=BOLD)
            g = VGroup(t, x, y, z).arrange(DOWN, buff=0.22)
            return VGroup(panel(g, color=color, buff=0.34), g)

        b_range = _box("RANGE DIFFERENCING", "needs two separate looks",
                       "error  ≈  ±150 m/s", "far too coarse", NEON_PINK)
        b_dopp = _box("DOPPLER SHIFT", "one dwell is enough",
                      "error  ≈  ±0.1 m/s", "1000× better", RADAR_GREEN)
        cmp_g = VGroup(b_range, b_dopp).arrange(RIGHT, buff=0.8).shift(DOWN * 0.15)
        cmp_g.scale_to_fit_width(11.4)
        self.play(FadeIn(b_range, shift=RIGHT * 0.4), run_time=1.3)
        self.wait(1.2)
        self.play(FadeIn(b_dopp, shift=LEFT * 0.4), run_time=1.3)
        self.wait(1.4)
        self.play(Indicate(b_dopp, color=RADAR_GREEN, scale_factor=1.06), run_time=1.0)
        hook = Text("so we stop timing the wave — and start listening to its frequency",
                    font_size=28, color=AMBER, weight=BOLD).to_edge(DOWN, buff=0.55)
        self.play(Write(hook), run_time=2.2)
        self.wait(3.4)
        self.fill()


# ============================ PART 8 : DOPPLER INTUITION ============================
class Part8(NarratedScene):
    def construct(self):
        h = head("THE DOPPLER EFFECT", color=NEON_PINK)
        self.play(FadeIn(h[0]), Create(h[1]), run_time=1.0)

        siren = Text("a siren passing you on the street", font_size=30, color=TEXT_WHITE).shift(UP * 2.05)
        self.play(Write(siren), run_time=1.6)

        source = Dot(ORIGIN, radius=0.16, color=AMBER).shift(DOWN * 0.35)
        vel = Arrow(source.get_center(), source.get_center() + RIGHT * 1.5,
                    color=AMBER, stroke_width=6, buff=0.18)
        vlab = Text("v", font_size=28, color=AMBER, weight=BOLD).next_to(vel, UP, buff=0.1)

        # wavefronts emitted at successive instants from shifted centres
        fronts = VGroup()
        for i in range(6):
            r = 0.6 + i * 0.62
            cx = -i * 0.42            # earlier fronts were emitted further left
            fronts.add(Circle(radius=r, color=TECH_CYAN, stroke_width=3.5,
                              stroke_opacity=0.85 - i * 0.08)
                       .move_to(source.get_center() + RIGHT * cx))

        self.play(FadeIn(source, scale=2), GrowArrow(vel), Write(vlab), run_time=1.2)
        self.play(LaggedStart(*[Create(f) for f in fronts], lag_ratio=0.18), run_time=2.8)
        self.wait(0.6)

        front_lbl = VGroup(
            Text("AHEAD", font_size=26, color=NEON_PINK, weight=BOLD),
            Text("wavefronts squeezed", font_size=22, color=NEON_PINK),
            Text("higher frequency", font_size=24, color=NEON_PINK, weight=BOLD),
        ).arrange(DOWN, buff=0.12).move_to(RIGHT * 4.6 + DOWN * 0.35)
        back_lbl = VGroup(
            Text("BEHIND", font_size=26, color=TECH_CYAN, weight=BOLD),
            Text("wavefronts stretched", font_size=22, color=TECH_CYAN),
            Text("lower frequency", font_size=24, color=TECH_CYAN, weight=BOLD),
        ).arrange(DOWN, buff=0.12).move_to(LEFT * 4.6 + DOWN * 0.35)

        self.play(FadeIn(front_lbl, shift=LEFT * 0.3), run_time=1.1)
        self.play(FadeIn(back_lbl, shift=RIGHT * 0.3), run_time=1.1)
        self.wait(0.8)

        bridge = Text("radio waves off a moving target behave exactly the same way",
                      font_size=28, color=TEXT_WHITE).shift(DOWN * 2.75)
        self.play(FadeOut(siren), Write(bridge), run_time=1.8)

        result = VGroup(
            Text("closing target   →   frequency goes UP", font_size=27, color=NEON_PINK),
            Text("receding target →   frequency goes DOWN", font_size=27, color=TECH_CYAN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).shift(DOWN * 3.35)
        self.play(FadeOut(bridge), FadeIn(result[0], shift=UP * 0.2), run_time=1.0)
        self.play(FadeIn(result[1], shift=UP * 0.2), run_time=1.0)
        self.wait(0.6)

        self.play(FadeOut(VGroup(front_lbl, back_lbl, result)), run_time=0.8)
        self.play(FadeOut(fronts), run_time=0.6)
        emitted = VGroup()
        self.play(source.animate.shift(LEFT * 4.2), vel.animate.shift(LEFT * 4.2),
                  vlab.animate.shift(LEFT * 4.2), run_time=1.0)
        for _ in range(7):
            ring = Circle(radius=0.18, color=TECH_CYAN, stroke_width=3.5)
            ring.move_to(source.get_center())
            emitted.add(ring)
            self.add(ring)
            self.play(source.animate.shift(RIGHT * 1.2), vel.animate.shift(RIGHT * 1.2),
                      vlab.animate.shift(RIGHT * 1.2),
                      *[r.animate.scale(1.75) for r in emitted],
                      run_time=0.85, rate_func=linear)
        self.wait(0.8)
        self.play(FadeOut(emitted), FadeOut(source), FadeOut(vel), FadeOut(vlab), run_time=0.8)
        eqp = VGroup(
            Text("a radar target does exactly this to the ECHO", font_size=30, color=TEXT_WHITE),
            Text("and — as we are about to see — the shift happens TWICE",
                 font_size=30, color=AMBER, weight=BOLD),
        ).arrange(DOWN, buff=0.3).shift(DOWN * 0.3)
        self.play(FadeIn(eqp[0], shift=UP * 0.2), run_time=1.2)
        self.wait(1.3)
        self.play(FadeIn(eqp[1], shift=UP * 0.2), run_time=1.2)
        self.wait(1.8)
        self.fill()


# ============================ PART 9 : THE DOPPLER EQUATION ============================
class Part9(NarratedScene):
    def construct(self):
        h = head("THE DOPPLER EQUATION", color=AMBER)
        self.play(FadeIn(h[0]), Create(h[1]), run_time=1.0)

        eq = Text("f_d  =  2 · v_r / λ", font_size=68, color=AMBER, weight=BOLD).shift(UP * 1.75)
        ebox = panel(eq, color=AMBER, buff=0.38)
        self.play(Create(ebox), Write(eq), run_time=2.0)

        legend = VGroup(
            Text("f_d  Doppler frequency shift  [Hz]", font_size=25, color=TEXT_WHITE),
            Text("v_r  radial velocity  [m/s]", font_size=25, color=TEXT_WHITE),
            Text("λ    wavelength  =  c / f₀  [m]", font_size=25, color=TEXT_WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).shift(LEFT * 3.4 + DOWN * 0.55)
        for l in legend:
            self.play(FadeIn(l, shift=RIGHT * 0.25), run_time=0.6)

        why = Text("why the factor of 2 ?", font_size=32, color=NEON_PINK, weight=BOLD)
        why.shift(RIGHT * 3.3 + UP * 0.2)
        self.play(Write(why), run_time=1.2)

        steps = VGroup(
            Text("1 ▸ target RECEIVES a compressed wave", font_size=23, color=TECH_CYAN),
            Text("2 ▸ target RE-RADIATES while moving", font_size=23, color=TECH_CYAN),
            Text("shift applied twice  →  ×2", font_size=26, color=NEON_PINK, weight=BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).next_to(why, DOWN, buff=0.4)
        steps.set_x(3.3)
        for s in steps:
            self.play(FadeIn(s, shift=LEFT * 0.25), run_time=0.8)
            self.wait(0.35)

        sign = VGroup(
            Text("f_d  >  0    target CLOSING", font_size=27, color=NEON_PINK, weight=BOLD),
            Text("f_d  <  0    target OPENING", font_size=27, color=TECH_CYAN, weight=BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.5).set_x(-3.0)
        self.play(FadeIn(sign[0], shift=UP * 0.2), run_time=0.9)
        self.play(FadeIn(sign[1], shift=UP * 0.2), run_time=0.9)
        self.wait(0.6)

        self.play(FadeOut(VGroup(legend, why, steps, sign)), run_time=0.9)
        self.play(VGroup(ebox, eq).animate.scale(0.78).to_edge(UP, buff=1.15), run_time=1.0)
        lane1 = Text("1 ▸ the wave ARRIVES at a moving target",
                     font_size=26, color=TECH_CYAN).shift(UP * 1.15)
        w_in = FunctionGraph(lambda x: 0.3 * np.sin(5.0 * x), x_range=[-5.4, -0.6],
                             color=TECH_CYAN, stroke_width=4).shift(UP * 0.25)
        w_mid = FunctionGraph(lambda x: 0.3 * np.sin(8.5 * x), x_range=[0.6, 5.4],
                              color=AMBER, stroke_width=4).shift(UP * 0.25)
        tgt_dot = Dot(UP * 0.25, radius=0.14, color=TEXT_WHITE)
        self.play(FadeIn(lane1), run_time=0.9)
        self.play(Create(w_in), FadeIn(tgt_dot), run_time=1.3)
        self.play(Create(w_mid), run_time=1.3)
        s1 = Text("shift #1", font_size=22, color=AMBER).next_to(w_mid, UP, buff=0.12)
        self.play(FadeIn(s1), run_time=0.6)
        self.wait(0.8)
        lane2 = Text("2 ▸ and it RE-RADIATES while still moving",
                     font_size=26, color=NEON_PINK).shift(DOWN * 1.2)
        w_out = FunctionGraph(lambda x: 0.3 * np.sin(12.0 * x), x_range=[-5.4, -0.6],
                              color=NEON_PINK, stroke_width=4).shift(DOWN * 2.0)
        self.play(FadeIn(lane2), run_time=0.9)
        self.play(Create(w_out), run_time=1.3)
        s2 = Text("shift #2", font_size=22, color=NEON_PINK).next_to(w_out, UP, buff=0.12)
        self.play(FadeIn(s2), run_time=0.6)
        self.wait(1.0)
        tot = Text("two shifts on one echo   →   that is the factor of 2",
                   font_size=30, color=AMBER, weight=BOLD).to_edge(DOWN, buff=0.4)
        self.play(Write(tot), run_time=2.0)
        self.play(Indicate(eq, color=AMBER, scale_factor=1.08), run_time=1.0)
        self.wait(1.8)
        self.fill()


# ============================ PART 10 : DOPPLER NUMBERS ============================
class Part10(NarratedScene):
    def construct(self):
        h = head("HOW BIG IS THE SHIFT?", color=RADAR_GREEN)
        self.play(FadeIn(h[0]), Create(h[1]), run_time=1.0)

        def row(icon, band, lam, speed, fd, color):
            g = VGroup(
                Text(icon, font_size=30, color=color, weight=BOLD),
                Text(band, font_size=24, color=TEXT_WHITE),
                Text(lam, font_size=24, color=DIM_TEXT),
                Text(speed, font_size=24, color=TEXT_WHITE),
                Text(fd, font_size=30, color=color, weight=BOLD),
            )
            for i, w in enumerate([2.5, 2.6, 2.4, 3.0, 2.6]):
                g[i].scale_to_fit_height(min(g[i].height, 0.42))
            g.arrange(RIGHT, buff=0.55)
            return g

        hdr = VGroup(
            Text("BAND", font_size=22, color=DIM_TEXT),
            Text("λ", font_size=22, color=DIM_TEXT),
            Text("TARGET SPEED", font_size=22, color=DIM_TEXT),
            Text("DOPPLER SHIFT", font_size=22, color=DIM_TEXT),
        ).arrange(RIGHT, buff=1.55).shift(UP * 2.1)

        r1 = row("■", "X-band  10 GHz", "λ = 3 cm", "aircraft  300 m/s", "20 kHz", TECH_CYAN)
        r2 = row("■", "K-band  24 GHz", "λ = 1.25 cm", "car  30 m/s", "4.8 kHz", AMBER)
        r3 = row("■", "K-band  24 GHz", "λ = 1.25 cm", "person  1 m/s", "160 Hz", RADAR_GREEN)
        rows = VGroup(r1, r2, r3).arrange(DOWN, buff=0.62, aligned_edge=LEFT).shift(UP * 0.35)
        rows.set_x(0)

        self.play(FadeIn(hdr), run_time=0.9)
        for r in rows:
            self.play(FadeIn(r, shift=RIGHT * 0.3), run_time=1.0)
            self.wait(0.9)

        line = Line(LEFT * 5.5, RIGHT * 5.5, color=SUBTLE, stroke_width=2).next_to(rows, DOWN, buff=0.5)
        self.play(Create(line), run_time=0.6)

        pt = VGroup(
            Text("kilohertz shifts on a gigahertz carrier", font_size=30, color=TEXT_WHITE),
            Text("tiny in ratio — but easy to measure directly", font_size=30, color=AMBER, weight=BOLD),
        ).arrange(DOWN, buff=0.22).next_to(line, DOWN, buff=0.4)
        self.play(FadeIn(pt[0]), run_time=1.0)
        self.play(FadeIn(pt[1]), run_time=1.0)
        self.wait(0.8)

        self.play(FadeOut(VGroup(hdr, rows, line, pt)), run_time=0.9)
        calc_t = Text("watch it live:  X-band,  λ = 3 cm",
                      font_size=30, color=TEXT_WHITE).shift(UP * 2.2)
        self.play(Write(calc_t), run_time=1.6)
        vtr = ValueTracker(0.0)
        track = Line(LEFT * 4.6, RIGHT * 4.6, color=SUBTLE, stroke_width=3).shift(UP * 0.6)
        t0 = Text("0", font_size=20, color=DIM_TEXT).next_to(track, DOWN, buff=0.15).set_x(-4.6)
        t1 = Text("400 m/s", font_size=20, color=DIM_TEXT).next_to(track, DOWN, buff=0.15).set_x(4.6)
        self.play(Create(track), FadeIn(t0), FadeIn(t1), run_time=0.9)
        mover = always_redraw(lambda: Dot(
            track.get_left() + RIGHT * (vtr.get_value() / 400.0) * 9.2,
            radius=0.13, color=AMBER))
        v_read = live_text(lambda: f"v_r  =  {vtr.get_value():.0f} m/s", color=TECH_CYAN,
                           font_size=40, anchor=LEFT * 4.4 + DOWN * 0.9)
        f_read = live_text(lambda: f"f_d  =  {2 * vtr.get_value() / 0.03 / 1000:.1f} kHz",
                           color=NEON_PINK, font_size=40, anchor=LEFT * 4.4 + DOWN * 1.8)
        self.add(mover, v_read, f_read)
        self.play(vtr.animate.set_value(340), run_time=5.0, rate_func=smooth)
        self.wait(1.0)
        self.play(vtr.animate.set_value(80), run_time=3.0, rate_func=smooth)
        self.wait(1.0)
        self.play(vtr.animate.set_value(400), run_time=3.0, rate_func=smooth)
        mover.clear_updaters()
        v_read.clear_updaters()
        f_read.clear_updaters()
        self.wait(0.8)
        kick = Text("a straight line — measure f_d and you have the speed",
                    font_size=28, color=AMBER, weight=BOLD).to_edge(DOWN, buff=0.5)
        self.play(Write(kick), run_time=2.2)
        self.wait(3.0)
        self.fill()


# ============================ PART 11 : RADIAL VELOCITY ONLY ============================
class Part11(NarratedScene):
    def construct(self):
        h = head("DOPPLER SEES ONLY RADIAL MOTION", color=NEON_PINK, size=36)
        self.play(FadeIn(h[0]), Create(h[1]), run_time=1.0)

        radar = dish(scale=0.75).move_to(LEFT * 4.9 + DOWN * 1.4)
        origin = radar[2].get_center()
        tgt_pos = RIGHT * 1.2 + UP * 1.1
        los = DashedLine(origin, tgt_pos, color=SUBTLE, stroke_width=2.5, dash_length=0.13)
        _d = tgt_pos - origin
        _ang = float(np.arctan2(_d[1], _d[0]))
        los_lab = Text("line of sight", font_size=20, color=DIM_TEXT)
        los_lab.move_to(origin + _d * 0.45).shift(DOWN * 0.3).rotate(_ang)
        tgt = plane(scale=0.95).move_to(tgt_pos)

        self.play(FadeIn(radar), Create(los), FadeIn(los_lab), FadeIn(tgt), run_time=1.6)

        theta = ValueTracker(0.0)
        los_dir = normalize(tgt_pos - origin)

        def vel_arrow():
            ang = theta.get_value()
            d = rotate_vector(los_dir, ang)
            return Arrow(tgt_pos, tgt_pos + d * 2.1, color=AMBER, stroke_width=7,
                         buff=0, max_tip_length_to_length_ratio=0.16)

        def radial_arrow():
            ang = theta.get_value()
            mag = 2.1 * np.cos(ang)
            return Arrow(tgt_pos, tgt_pos + los_dir * mag, color=NEON_PINK, stroke_width=7,
                         buff=0, max_tip_length_to_length_ratio=0.2) if abs(mag) > 0.06 else \
                Dot(tgt_pos, radius=0.07, color=NEON_PINK)

        v = always_redraw(vel_arrow)
        vr = always_redraw(radial_arrow)
        self.play(GrowArrow(vel_arrow()), run_time=0.8)
        self.add(v, vr)

        vl = Text("v", font_size=28, color=AMBER, weight=BOLD).next_to(tgt, UP * 2.4 + RIGHT * 1.2)
        self.play(FadeIn(vl), run_time=0.5)

        eq = Text("v_r  =  v · cos θ", font_size=46, color=AMBER, weight=BOLD).move_to(RIGHT * 3.8 + UP * 2.6)
        self.play(Write(eq), run_time=1.3)

        th_lbl = Text("θ  =", font_size=32, color=TEXT_WHITE).move_to(RIGHT * 2.9 + UP * 0.35)
        th_val = live_text(lambda: f"{np.degrees(theta.get_value()):.0f}°",
                           color=TECH_CYAN, anchor=RIGHT * 3.6 + UP * 0.35)
        fd_lbl = Text("f_d  ∝", font_size=32, color=TEXT_WHITE).move_to(RIGHT * 2.9 + DOWN * 0.35)
        fd_val = live_text(lambda: f"{np.cos(theta.get_value()):.2f}",
                           color=NEON_PINK, anchor=RIGHT * 3.6 + DOWN * 0.35)
        readout = VGroup(th_lbl, fd_lbl)
        self.play(FadeIn(th_lbl), FadeIn(fd_lbl), run_time=0.8)
        self.add(th_val, fd_val)

        self.play(theta.animate.set_value(PI / 3), run_time=2.4, rate_func=smooth)
        note1 = Text("60° off  →  only half the speed shows up", font_size=24, color=TEXT_WHITE)
        note1.shift(DOWN * 3.15)
        self.play(FadeIn(note1), run_time=0.9)
        self.wait(0.9)

        self.play(theta.animate.set_value(PI / 2), run_time=2.4, rate_func=smooth)
        note2 = Text("90° — crossing the beam  →  f_d = 0   INVISIBLE to Doppler",
                     font_size=27, color=NEON_PINK, weight=BOLD).move_to(note1)
        self.play(FadeOut(note1), FadeIn(note2), run_time=1.0)
        self.play(Flash(tgt.get_center(), color=NEON_PINK, flash_radius=1.0,
                        line_length=0.3, num_lines=16), run_time=0.8)
        self.wait(0.8)

        self.play(theta.animate.set_value(0.0), run_time=1.8, rate_func=smooth)
        note3 = Text("head-on  →  full speed measured", font_size=27,
                     color=RADAR_GREEN, weight=BOLD).move_to(note1)
        self.play(FadeOut(note2), FadeIn(note3), run_time=0.9)
        th_val.clear_updaters()
        fd_val.clear_updaters()
        self.wait(0.6)

        self.play(FadeOut(VGroup(note3, vl)), run_time=0.7)
        self.remove(th_val, fd_val)
        th_live = live_text(lambda: f"{np.degrees(theta.get_value()):.0f}°",
                            color=TECH_CYAN, anchor=RIGHT * 3.6 + UP * 0.35)
        fd_live = live_text(lambda: f"{np.cos(theta.get_value()):.2f}",
                            color=NEON_PINK, anchor=RIGHT * 3.6 + DOWN * 0.35)
        self.add(th_live, fd_live)
        conseq = VGroup(
            bullet("a crossing target hides in the clutter notch", size=23,
                   color=NEON_PINK, dot_color=NEON_PINK),
            bullet("this is why siting a radar off the flight path matters", size=23),
            bullet("two radars, two angles  →  the full velocity vector", size=23,
                   color=RADAR_GREEN, dot_color=RADAR_GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).shift(DOWN * 2.6)
        conseq.set_x(0.8)
        self.play(theta.animate.set_value(PI / 2), FadeIn(conseq[0], shift=RIGHT * 0.25),
                  run_time=2.6, rate_func=smooth)
        self.wait(0.8)
        self.play(theta.animate.set_value(PI / 4), FadeIn(conseq[1], shift=RIGHT * 0.25),
                  run_time=2.4, rate_func=smooth)
        self.wait(0.8)
        self.play(theta.animate.set_value(0.0), FadeIn(conseq[2], shift=RIGHT * 0.25),
                  run_time=2.4, rate_func=smooth)
        th_live.clear_updaters()
        fd_live.clear_updaters()
        self.wait(1.0)
        self.play(Indicate(eq, color=AMBER, scale_factor=1.08), run_time=1.0)
        self.wait(3.4)
        self.fill()


# ============================ PART 12 : PHASE ACROSS PULSES ============================
class Part12(NarratedScene):
    def construct(self):
        h = head("MEASURING IT:  PULSE-TO-PULSE PHASE")
        self.play(FadeIn(h[0]), Create(h[1]), run_time=1.0)

        q = Text("we never measure 10 GHz directly — we measure PHASE",
                 font_size=30, color=TEXT_WHITE).shift(UP * 2.15)
        self.play(Write(q), run_time=2.0)

        # pulse train, sampled at one range bin
        base = Line(LEFT * 5.6, LEFT * 0.2, color=DIM_TEXT, stroke_width=3).shift(UP * 0.3)
        pulses = VGroup(*[Rectangle(width=0.13, height=0.7, fill_color=TECH_CYAN,
                                    fill_opacity=1, stroke_width=0)
                          .move_to(base.get_left() + RIGHT * (0.5 + i * 0.85) + UP * 0.35)
                          for i in range(6)])
        gate = DashedLine(base.get_left() + UP * 1.35, base.get_right() + UP * 1.35,
                          color=AMBER, stroke_width=2.5, dash_length=0.1)
        gate_l = Text("same range bin, every pulse", font_size=21, color=AMBER)
        gate_l.next_to(gate, UP, buff=0.12)

        self.play(Create(base), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(p, scale=1.4) for p in pulses], lag_ratio=0.15), run_time=1.4)
        self.play(Create(gate), FadeIn(gate_l), run_time=1.0)

        # phasor
        circ = Circle(radius=1.5, color=SUBTLE, stroke_width=3).shift(RIGHT * 3.6 + DOWN * 0.15)
        cdot = Dot(circ.get_center(), radius=0.05, color=DIM_TEXT)
        phi = ValueTracker(0.0)
        arm = always_redraw(lambda: Line(
            circ.get_center(),
            circ.get_center() + 1.5 * np.array([np.cos(phi.get_value()), np.sin(phi.get_value()), 0]),
            color=NEON_PINK, stroke_width=6))
        tip = always_redraw(lambda: Dot(
            circ.get_center() + 1.5 * np.array([np.cos(phi.get_value()), np.sin(phi.get_value()), 0]),
            radius=0.1, color=NEON_PINK))
        clab = Text("echo phase", font_size=22, color=NEON_PINK).next_to(circ, UP, buff=0.2)

        self.play(Create(circ), FadeIn(cdot), FadeIn(clab), run_time=1.0)
        self.add(arm, tip)

        expl = VGroup(
            bullet("target moves a fraction of λ between pulses", size=25),
            bullet("that shifts the echo phase by a FIXED step", size=25),
            bullet("phase step per pulse  =  2π · f_d / PRF", size=25, color=AMBER, dot_color=AMBER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).shift(LEFT * 3.0 + DOWN * 1.9)

        turns = 0.0
        for b in expl:
            turns += 0.9
            self.play(FadeIn(b, shift=RIGHT * 0.25),
                      phi.animate.set_value(2 * PI * turns),
                      run_time=1.5, rate_func=linear)
            self.wait(0.35)

        turns += 1.6
        self.play(phi.animate.set_value(2 * PI * turns), run_time=2.6, rate_func=linear)
        kicker = Text("the phase walks around the circle at exactly the Doppler rate",
                      font_size=26, color=RADAR_GREEN).to_edge(DOWN, buff=0.35)
        turns += 1.0
        self.play(Write(kicker), phi.animate.set_value(2 * PI * turns),
                  run_time=1.8, rate_func=linear)
        self.wait(0.5)

        self.play(FadeOut(VGroup(q, kicker)), run_time=0.7)
        num = VGroup(
            Text("X-band, PRF = 2 kHz, target closing at 150 m/s",
                 font_size=25, color=TEXT_WHITE),
            Text("f_d  =  2 × 150 / 0.03  =  10 kHz", font_size=26, color=AMBER),
            Text("→  five full turns of phase between pulses",
                 font_size=26, color=NEON_PINK, weight=BOLD),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.35)
        for n in num:
            turns += 0.7
            self.play(FadeIn(n, shift=UP * 0.2), phi.animate.set_value(2 * PI * turns),
                      run_time=1.2, rate_func=linear)
            self.wait(0.6)
        turns += 1.4
        self.play(phi.animate.set_value(2 * PI * turns), run_time=2.4, rate_func=linear)
        self.wait(2.2)
        self.fill()


# ============================ PART 13 : SLOW TIME & FFT ============================
class Part13(NarratedScene):
    def construct(self):
        h = head("SLOW TIME  →  FFT  →  VELOCITY", color=RADAR_GREEN)
        self.play(FadeIn(h[0]), Create(h[1]), run_time=1.0)

        ax = Axes(x_range=[0, 12, 2], y_range=[-1.4, 1.4, 1], x_length=6.0, y_length=2.6,
                  axis_config={"color": SUBTLE, "stroke_width": 2, "include_ticks": False})
        ax.shift(LEFT * 3.5 + UP * 0.85)
        axl = Text("slow time  (pulse number)", font_size=21, color=DIM_TEXT).next_to(ax, DOWN, buff=0.18)
        self.play(Create(ax), FadeIn(axl), run_time=1.1)

        sig = ax.plot(lambda x: np.cos(2.1 * x), x_range=[0, 12], color=NEON_PINK, stroke_width=4)
        samples = VGroup(*[Dot(ax.c2p(x, np.cos(2.1 * x)), radius=0.07, color=AMBER)
                           for x in np.arange(0.3, 12, 0.62)])
        self.play(LaggedStart(*[FadeIn(d, scale=2) for d in samples], lag_ratio=0.05), run_time=2.0)
        self.play(Create(sig), run_time=1.6)

        fast = Text("fast time = WITHIN one pulse  →  range", font_size=23, color=TECH_CYAN)
        slow = Text("slow time = ACROSS pulses  →  velocity", font_size=23, color=NEON_PINK)
        legend = VGroup(fast, slow).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        legend.next_to(axl, DOWN, buff=0.45).set_x(-3.5)
        self.play(FadeIn(fast, shift=RIGHT * 0.2), run_time=0.9)
        self.play(FadeIn(slow, shift=RIGHT * 0.2), run_time=0.9)

        arrow = Arrow(LEFT * 0.2, RIGHT * 0.9, color=AMBER, stroke_width=8,
                      buff=0, max_tip_length_to_length_ratio=0.3).shift(UP * 0.85)
        fft = Text("FFT", font_size=32, color=AMBER, weight=BOLD).next_to(arrow, UP, buff=0.15)
        self.play(GrowArrow(arrow), Write(fft), run_time=1.0)

        ax2 = Axes(x_range=[-1, 1, 0.5], y_range=[0, 1.2, 1], x_length=4.6, y_length=2.6,
                   axis_config={"color": SUBTLE, "stroke_width": 2, "include_ticks": False})
        ax2.shift(RIGHT * 3.9 + UP * 0.85)
        ax2l = Text("Doppler frequency", font_size=21, color=DIM_TEXT).next_to(ax2, DOWN, buff=0.18)
        peak = ax2.plot(lambda x: np.exp(-((x - 0.42) ** 2) / 0.0022),
                        x_range=[-1, 1, 0.005], color=RADAR_GREEN, stroke_width=4)
        pk_lab = Text("f_d", font_size=26, color=RADAR_GREEN, weight=BOLD)
        pk_lab.next_to(ax2.c2p(0.42, 1.0), UP, buff=0.15)

        self.play(Create(ax2), FadeIn(ax2l), run_time=1.0)
        self.play(Create(peak), FadeIn(pk_lab), run_time=1.4)
        self.play(Flash(ax2.c2p(0.42, 1.0), color=RADAR_GREEN, flash_radius=0.6,
                        line_length=0.22, num_lines=14), run_time=0.7)

        res = VGroup(
            Text("peak POSITION  →  target velocity", font_size=26, color=TEXT_WHITE),
            Text("peak WIDTH  →  set by how long we looked", font_size=26, color=TEXT_WHITE),
            Text("longer coherent processing → finer velocity resolution",
                 font_size=27, color=AMBER, weight=BOLD),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.45)
        for r in res:
            self.play(FadeIn(r, shift=UP * 0.2), run_time=0.85)
        self.wait(0.5)

        self.play(FadeOut(VGroup(res, fast, slow)), run_time=0.8)
        note = Text("look for longer  →  the peak gets sharper",
                    font_size=28, color=TEXT_WHITE).shift(DOWN * 1.45)
        self.play(FadeIn(note), run_time=1.0)
        sharp = ax2.plot(lambda x: np.exp(-((x - 0.42) ** 2) / 0.0004),
                         x_range=[-1, 1, 0.002], color=RADAR_GREEN, stroke_width=4)
        self.play(Transform(peak, sharp), run_time=1.8)
        self.wait(0.8)
        two = ax2.plot(lambda x: np.exp(-((x - 0.42) ** 2) / 0.0004)
                       + 0.75 * np.exp(-((x + 0.35) ** 2) / 0.0004),
                       x_range=[-1, 1, 0.002], color=RADAR_GREEN, stroke_width=4)
        note2 = Text("two targets in the SAME range bin, split by velocity alone",
                     font_size=27, color=AMBER, weight=BOLD).move_to(note)
        self.play(Transform(peak, two), FadeOut(note), FadeIn(note2), run_time=1.8)
        self.wait(1.2)
        eqres = VGroup(
            Text("velocity resolution", font_size=23, color=DIM_TEXT),
            Text("Δv  =  λ / (2 · T_dwell)", font_size=34, color=AMBER, weight=BOLD),
            Text("32 ms dwell at X-band  →  0.47 m/s", font_size=24, color=TEXT_WHITE),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(eqres[0]), run_time=0.7)
        self.play(Write(eqres[1]), run_time=1.6)
        self.play(FadeIn(eqres[2]), run_time=0.9)
        self.play(Indicate(eqres[1], color=AMBER, scale_factor=1.06), run_time=1.0)
        self.wait(3.0)
        self.fill()


# ============================ PART 14 : RANGE-DOPPLER MAP ============================
class Part14(NarratedScene):
    def construct(self):
        h = head("THE RANGE-DOPPLER MAP", color=AMBER)
        self.play(FadeIn(h[0]), Create(h[1]), run_time=1.0)

        nx, ny = 16, 11
        cell = 0.34
        grid = VGroup()
        for i in range(nx):
            for j in range(ny):
                grid.add(Square(side_length=cell, stroke_color=SUBTLE, stroke_width=1,
                                fill_color=PANEL_NAVY, fill_opacity=0.75)
                         .move_to(RIGHT * (i - nx / 2 + 0.5) * cell + UP * (j - ny / 2 + 0.5) * cell))
        grid.move_to(LEFT * 3.4 + DOWN * 0.4)

        self.play(FadeIn(grid, lag_ratio=0.004), run_time=1.8)
        xlab = Text("slow time  (pulse #)", font_size=20, color=NEON_PINK).next_to(grid, DOWN, buff=0.2)
        ylab = Text("fast time (range)", font_size=20, color=TECH_CYAN).next_to(grid, LEFT, buff=0.25).rotate(PI / 2)
        self.play(FadeIn(xlab), FadeIn(ylab), run_time=0.9)

        # highlight a column sweeping = FFT along slow time
        cols = [VGroup(*[grid[i * ny + j] for j in range(ny)]) for i in range(nx)]
        highlight = SurroundingRectangle(cols[0], color=AMBER, stroke_width=3, buff=0.02)
        fftl = Text("FFT along each row", font_size=22, color=AMBER).next_to(grid, UP, buff=0.22)
        self.play(Create(highlight), FadeIn(fftl), run_time=0.8)
        for i in range(1, nx, 2):
            self.play(highlight.animate.move_to(cols[i]), run_time=0.13, rate_func=linear)
        self.play(FadeOut(highlight), run_time=0.3)

        arrow = Arrow(LEFT * 0.55, RIGHT * 0.35, color=AMBER, stroke_width=8, buff=0,
                      max_tip_length_to_length_ratio=0.32).shift(DOWN * 0.4)
        self.play(GrowArrow(arrow), run_time=0.7)

        # the resulting map
        map_rect = Rectangle(width=5.4, height=3.8, stroke_color=TECH_CYAN, stroke_width=3,
                             fill_color=PANEL_NAVY, fill_opacity=0.9).shift(RIGHT * 3.8 + DOWN * 0.4)
        vaxis = Text("velocity  →", font_size=21, color=NEON_PINK).next_to(map_rect, DOWN, buff=0.2)
        raxis = Text("range  →", font_size=21, color=TECH_CYAN).next_to(map_rect, LEFT, buff=0.22).rotate(PI / 2)
        zero = DashedLine(map_rect.get_bottom() + UP * 0.06, map_rect.get_top() + DOWN * 0.06,
                          color=DIM_TEXT, stroke_width=2, dash_length=0.1)
        zero.set_x(map_rect.get_x())
        zl = Text("0", font_size=18, color=DIM_TEXT).next_to(zero, DOWN, buff=0.06).shift(LEFT * 0.42)

        self.play(Create(map_rect), FadeIn(vaxis), FadeIn(raxis), Create(zero), FadeIn(zl), run_time=1.4)

        def blob(dx, dy, color, label):
            g = VGroup()
            for k in range(4):
                g.add(Dot(map_rect.get_center() + RIGHT * dx + UP * dy,
                          radius=0.10 + k * 0.075, color=color,
                          fill_opacity=0.55 - k * 0.12))
            t = Text(label, font_size=19, color=color)
            t.next_to(g, UP, buff=0.12)
            return VGroup(g, t)

        b1 = blob(1.5, 1.0, RADAR_GREEN, "closing, far")
        b2 = blob(-1.7, -1.1, TECH_CYAN, "opening, near")
        b3 = blob(0.0, -0.2, NEON_PINK, "clutter (v = 0)")

        self.play(FadeIn(b1, scale=0.5), run_time=0.9)
        self.play(FadeIn(b2, scale=0.5), run_time=0.9)
        self.play(FadeIn(b3, scale=0.5), run_time=0.9)

        kicker = Text("one image  ·  range from the vertical  ·  speed from the horizontal",
                      font_size=27, color=TEXT_WHITE).to_edge(DOWN, buff=0.42)
        self.play(Write(kicker), run_time=2.0)
        self.play(Indicate(b1, color=RADAR_GREEN, scale_factor=1.15), run_time=0.9)
        self.wait(0.6)

        self.play(FadeOut(VGroup(grid, xlab, ylab, fftl, arrow, kicker)), run_time=0.9)
        map_g = VGroup(map_rect, vaxis, raxis, zero, zl, b1, b2, b3)
        self.play(map_g.animate.scale(1.2).move_to(LEFT * 3.1 + DOWN * 0.15), run_time=1.4)
        readout = VGroup(
            Text("READING A BLIP", font_size=27, color=AMBER, weight=BOLD),
            Text("vertical      →  range  =  32 km", font_size=23, color=TECH_CYAN),
            Text("horizontal  →  v_r  =  +180 m/s", font_size=23, color=NEON_PINK),
            Text("brightness  →  echo strength / RCS", font_size=23, color=TEXT_WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).move_to(RIGHT * 3.7 + UP * 0.9)
        for r in readout:
            self.play(FadeIn(r, shift=LEFT * 0.25), run_time=0.85)
            self.wait(0.55)
        self.wait(0.6)
        self.play(b1.animate.shift(RIGHT * 0.45), run_time=2.0)
        acc = Text("a blip drifting sideways = a target accelerating",
                   font_size=21, color=DIM_TEXT)
        acc.next_to(readout, DOWN, buff=0.5).set_x(3.7)
        self.play(FadeIn(acc), run_time=0.9)
        self.wait(0.8)
        why = VGroup(
            Text("every dwell produces a whole map like this", font_size=26, color=TEXT_WHITE),
            Text("detection, tracking and clutter rejection all live here",
                 font_size=26, color=AMBER, weight=BOLD),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(why[0], shift=UP * 0.2), run_time=1.1)
        self.wait(0.8)
        self.play(FadeIn(why[1], shift=UP * 0.2), run_time=1.1)
        self.wait(2.6)
        self.fill()


# ============================ PART 15 : CLUTTER REJECTION / MTI ============================
class Part15(NarratedScene):
    def construct(self):
        h = head("BONUS:  KILLING THE CLUTTER", color=RADAR_GREEN)
        self.play(FadeIn(h[0]), Create(h[1]), run_time=1.0)

        ax = Axes(x_range=[-1, 1, 0.5], y_range=[0, 1.15, 1], x_length=9.5, y_length=3.6,
                  axis_config={"color": SUBTLE, "stroke_width": 2, "include_ticks": False})
        ax.shift(DOWN * 0.35)
        xl = Text("Doppler frequency", font_size=22, color=DIM_TEXT).next_to(ax, DOWN, buff=0.2)
        yl = Text("echo power", font_size=22, color=DIM_TEXT).next_to(ax, LEFT, buff=0.2).rotate(PI / 2)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=1.2)

        clutter = ax.plot(lambda x: np.exp(-(x ** 2) / 0.0035),
                          x_range=[-1, 1, 0.004], color=NEON_PINK, stroke_width=5)
        cl = Text("ground clutter — hills, buildings, sea", font_size=24, color=NEON_PINK)
        cl.next_to(ax.c2p(0, 1.05), UP, buff=0.15).shift(RIGHT * 1.4)
        target = ax.plot(lambda x: 0.16 * np.exp(-((x - 0.52) ** 2) / 0.0022),
                         x_range=[-1, 1, 0.004], color=RADAR_GREEN, stroke_width=5)
        tl = Text("aircraft", font_size=24, color=RADAR_GREEN)
        tl.next_to(ax.c2p(0.52, 0.16), UP, buff=0.2)

        self.play(Create(clutter), FadeIn(cl), run_time=1.6)
        self.wait(0.5)
        self.play(Create(target), FadeIn(tl), run_time=1.2)
        ratio = Text("clutter can be 10 000× stronger than the target",
                     font_size=26, color=NEON_PINK).shift(UP * 2.05)
        self.play(Write(ratio), run_time=1.8)
        self.wait(0.6)

        notch = Rectangle(width=1.05, height=3.6, fill_color=AMBER, fill_opacity=0.22,
                          stroke_color=AMBER, stroke_width=3).move_to(ax.c2p(0, 0.575))
        nl = Text("MTI notch filter", font_size=24, color=AMBER, weight=BOLD)
        nl.next_to(notch, UP, buff=0.15).shift(LEFT * 1.6)
        self.play(FadeIn(notch), FadeIn(nl), run_time=1.2)
        self.play(FadeOut(clutter), FadeOut(cl), run_time=1.2)
        self.play(Flash(ax.c2p(0.52, 0.16), color=RADAR_GREEN, flash_radius=0.8,
                        line_length=0.25, num_lines=14), run_time=0.7)

        res = VGroup(
            Text("stationary things sit at zero Doppler — one narrow column",
                 font_size=27, color=TEXT_WHITE),
            Text("notch it out, and the moving target survives",
                 font_size=29, color=RADAR_GREEN, weight=BOLD),
        ).arrange(DOWN, buff=0.24).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(res[0], shift=UP * 0.2), run_time=1.1)
        self.play(FadeIn(res[1], shift=UP * 0.2), run_time=1.1)
        self.wait(0.6)

        self.play(FadeOut(VGroup(ratio, res)), run_time=0.8)
        moving = VGroup(
            Text("MTI  —  moving target indication", font_size=28, color=AMBER, weight=BOLD),
            Text("simplest form: subtract successive pulses", font_size=24, color=TEXT_WHITE),
            Text("anything that did not move cancels to zero", font_size=24, color=TEXT_WHITE),
        ).arrange(DOWN, buff=0.2).shift(UP * 2.15)
        for m in moving:
            self.play(FadeIn(m, shift=UP * 0.2), run_time=0.9)
            self.wait(0.5)
        self.wait(0.6)
        cost = VGroup(
            Text("the cost: slow targets sitting inside the notch are lost too",
                 font_size=26, color=NEON_PINK),
            Text("a hovering helicopter, a drifting boat, a person walking",
                 font_size=24, color=DIM_TEXT),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(cost[0], shift=UP * 0.2), run_time=1.2)
        self.wait(0.9)
        self.play(FadeIn(cost[1], shift=UP * 0.2), run_time=1.0)
        self.wait(1.0)
        self.play(Indicate(notch, color=AMBER, scale_factor=1.04), run_time=1.0)
        self.wait(3.4)
        self.fill()


# ============================ PART 16 : DOPPLER AMBIGUITY ============================
class Part16(NarratedScene):
    def construct(self):
        h = head("DOPPLER HAS LIMITS TOO", color=NEON_PINK)
        self.play(FadeIn(h[0]), Create(h[1]), run_time=1.0)

        idea = Text("we sample the phase once per pulse — so PRF is our sampling rate",
                    font_size=28, color=TEXT_WHITE).shift(UP * 2.15)
        self.play(Write(idea), run_time=2.2)

        ax = Axes(x_range=[0, 10, 1], y_range=[-1.5, 1.5, 1], x_length=7.4, y_length=2.4,
                  axis_config={"color": SUBTLE, "stroke_width": 2, "include_ticks": False})
        ax.shift(LEFT * 2.6 + UP * 0.55)
        true_w = ax.plot(lambda x: np.cos(6.4 * x), x_range=[0, 10, 0.01],
                         color=DIM_TEXT, stroke_width=2.5)
        sample_x = np.arange(0.25, 10, 0.98)
        dots = VGroup(*[Dot(ax.c2p(x, np.cos(6.4 * x)), radius=0.075, color=AMBER)
                        for x in sample_x])
        alias = ax.plot(lambda x: np.cos(6.4 * 0.25 + (6.4 - 2 * PI / 0.98) * (x - 0.25)),
                        x_range=[0, 10, 0.01], color=NEON_PINK, stroke_width=4)

        self.play(Create(ax), Create(true_w), run_time=1.4)
        tw = Text("true fast target", font_size=20, color=DIM_TEXT).next_to(ax, UP, buff=0.12).shift(LEFT * 2.2)
        self.play(FadeIn(tw), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(d, scale=2) for d in dots], lag_ratio=0.08), run_time=1.6)
        self.play(Create(alias), run_time=1.4)
        al = Text("looks SLOW — aliased", font_size=22, color=NEON_PINK).next_to(ax, DOWN, buff=0.2)
        self.play(FadeIn(al), run_time=0.8)
        self.wait(0.7)

        eq = Text("v_unamb  =  ± λ · PRF / 4", font_size=40, color=AMBER, weight=BOLD)
        eq.shift(RIGHT * 3.9 + UP * 0.8)
        ebox = panel(eq, color=AMBER, buff=0.26)
        self.play(Create(ebox), Write(eq), run_time=1.5)

        pts = VGroup(
            bullet("Nyquist applies to velocity", size=24),
            bullet("beyond it, fast targets fold back", size=24, color=NEON_PINK, dot_color=NEON_PINK),
            bullet("f_d = n · PRF  →  falls in the clutter notch", size=24,
                   color=NEON_PINK, dot_color=NEON_PINK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).shift(DOWN * 2.1)
        pts.set_x(-0.3)
        for p in pts:
            self.play(FadeIn(p, shift=RIGHT * 0.25), run_time=0.85)
            self.wait(0.3)

        blind = Text("BLIND SPEED — the target simply disappears",
                     font_size=30, color=NEON_PINK, weight=BOLD).to_edge(DOWN, buff=0.4)
        self.play(Write(blind), run_time=1.6)
        self.play(Indicate(blind, color=NEON_PINK, scale_factor=1.06), run_time=0.9)
        self.wait(0.5)

        self.play(FadeOut(VGroup(idea, blind, pts)), run_time=0.8)
        self.play(Indicate(alias, color=NEON_PINK, scale_factor=1.02), run_time=1.0)
        self.wait(0.8)
        nums = VGroup(
            Text("X-band, λ = 3 cm, PRF = 2 kHz", font_size=25, color=TEXT_WHITE),
            Text("v_unamb  =  0.03 × 2000 / 4  =  ± 15 m/s",
                 font_size=28, color=AMBER, weight=BOLD),
            Text("only 54 km/h — an aircraft folds over many times",
                 font_size=25, color=NEON_PINK),
        ).arrange(DOWN, buff=0.2).shift(DOWN * 1.95)
        for n in nums:
            self.play(FadeIn(n, shift=UP * 0.2), run_time=1.0)
            self.wait(0.7)
        self.wait(0.8)
        fix = VGroup(
            Text("the fixes", font_size=23, color=DIM_TEXT),
            Text("stagger the PRF  ·  raise the PRF  ·  unfold with a second dwell",
                 font_size=25, color=RADAR_GREEN, weight=BOLD),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(fix[0]), run_time=0.7)
        self.play(Write(fix[1]), run_time=2.2)
        self.wait(1.0)
        self.play(Indicate(eq, color=AMBER, scale_factor=1.06), run_time=1.0)
        self.wait(2.6)
        self.fill()


# ============================ PART 17 : THE PRF DILEMMA ============================
class Part17(NarratedScene):
    def construct(self):
        h = head("THE PRF DILEMMA", color=AMBER)
        self.play(FadeIn(h[0]), Create(h[1]), run_time=1.0)

        def col(title, r, v, use, color):
            t = Text(title, font_size=30, color=color, weight=BOLD)
            r_ = Text(r, font_size=24, color=TEXT_WHITE)
            v_ = Text(v, font_size=24, color=TEXT_WHITE)
            u_ = Text(use, font_size=21, color=DIM_TEXT)
            g = VGroup(t, Line(LEFT * 1.5, RIGHT * 1.5, color=color, stroke_width=2),
                       r_, v_, u_).arrange(DOWN, buff=0.28)
            return VGroup(panel(g, color=color, buff=0.35), g)

        c1 = col("LOW PRF", "range  UNAMBIGUOUS", "velocity  ambiguous",
                 "air-traffic surveillance", RADAR_GREEN)
        c2 = col("HIGH PRF", "range  ambiguous", "velocity  UNAMBIGUOUS",
                 "fighter look-down / missile", NEON_PINK)
        cols = VGroup(c1, c2).arrange(RIGHT, buff=0.7).shift(UP * 0.85)
        cols.scale_to_fit_width(11.6)

        self.play(FadeIn(c1, shift=RIGHT * 0.4), run_time=1.3)
        self.wait(0.8)
        self.play(FadeIn(c2, shift=LEFT * 0.4), run_time=1.3)
        self.wait(0.9)

        law = Text("R_max  ×  v_unamb  =  c · λ / 8   =   CONSTANT",
                   font_size=36, color=AMBER, weight=BOLD).shift(DOWN * 1.55)
        lbox = panel(law, color=AMBER, buff=0.3)
        self.play(Create(lbox), Write(law), run_time=2.0)
        self.play(Indicate(law, color=AMBER, scale_factor=1.05), run_time=1.0)

        note = Text("you cannot buy one without selling the other",
                    font_size=27, color=TEXT_WHITE).next_to(lbox, DOWN, buff=0.35)
        self.play(FadeIn(note), run_time=1.1)

        fix = VGroup(
            Text("THE ESCAPE:  PRF STAGGERING", font_size=27, color=RADAR_GREEN, weight=BOLD),
            Text("transmit several PRFs and cross-solve the ambiguities",
                 font_size=24, color=TEXT_WHITE),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.38)
        self.play(FadeIn(fix, shift=UP * 0.25), run_time=1.4)
        self.wait(0.6)

        self.play(FadeOut(VGroup(cols, note, fix)), run_time=0.9)
        self.play(VGroup(lbox, law).animate.scale(0.85).to_edge(UP, buff=1.15), run_time=1.0)
        data = [
            ("PRF", "R_max", "v_unamb", "typical user", DIM_TEXT, 24),
            ("300 Hz", "500 km", "± 2 m/s", "ATC surveillance", RADAR_GREEN, 24),
            ("3 kHz", "50 km", "± 22 m/s", "weather / marine", TECH_CYAN, 24),
            ("30 kHz", "5 km", "± 225 m/s", "fighter, missile seeker", NEON_PINK, 24),
        ]
        table = VGroup()
        for k, (a, b, c, d, colr, fs) in enumerate(data):
            y = 0.55 - k * 0.78
            row = VGroup()
            for txt, x in [(a, -5.4), (b, -3.0), (c, -0.4), (d, 2.4)]:
                t = Text(txt, font_size=fs if txt != d else fs - 2, color=colr)
                t.move_to(np.array([x, y, 0.0]), aligned_edge=LEFT)
                row.add(t)
            table.add(row)
        self.play(FadeIn(table[0]), run_time=0.8)
        for row in table[1:]:
            self.play(FadeIn(row, shift=RIGHT * 0.25), run_time=1.0)
            self.wait(0.8)
        self.wait(0.8)
        self.play(Indicate(table[3], color=NEON_PINK, scale_factor=1.05), run_time=1.0)
        self.wait(1.0)
        stag = VGroup(
            Text("PRF STAGGERING", font_size=28, color=RADAR_GREEN, weight=BOLD),
            Text("transmit three different PRFs; only the TRUE range and speed",
                 font_size=24, color=TEXT_WHITE),
            Text("agree across all three — the ambiguities cancel each other",
                 font_size=24, color=TEXT_WHITE),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.35)
        for s in stag:
            self.play(FadeIn(s, shift=UP * 0.2), run_time=0.9)
            self.wait(0.5)
        self.wait(3.0)
        self.fill()


# ============================ PART 18 : FMCW ============================
class Part18(NarratedScene):
    def construct(self):
        h = head("ANOTHER ROUTE:  FMCW  CHIRP RADAR", color=TECH_CYAN, size=36)
        self.play(FadeIn(h[0]), Create(h[1]), run_time=1.0)

        ax = Axes(x_range=[0, 10, 1], y_range=[0, 4, 1], x_length=8.6, y_length=3.3,
                  axis_config={"color": SUBTLE, "stroke_width": 2, "include_ticks": False})
        ax.shift(LEFT * 1.6 + UP * 0.5)
        xl = Text("time", font_size=21, color=DIM_TEXT).next_to(ax, DOWN, buff=0.15)
        yl = Text("frequency", font_size=21, color=DIM_TEXT).next_to(ax, LEFT, buff=0.18).rotate(PI / 2)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=1.2)

        def ramp(x, shift=0.0):
            xx = (x - shift) % 3.3
            return 0.35 + xx * 1.05

        tx = VGroup(*[ax.plot(lambda x: ramp(x), x_range=[k * 3.3 + 0.02, min((k + 1) * 3.3 - 0.02, 10), 0.01],
                              color=TECH_CYAN, stroke_width=4) for k in range(3)])
        rx = VGroup(*[ax.plot(lambda x: ramp(x, 0.55),
                              x_range=[k * 3.3 + 0.6, min((k + 1) * 3.3 + 0.55, 10), 0.01],
                              color=NEON_PINK, stroke_width=4) for k in range(3)])

        self.play(Create(tx), run_time=2.0)
        txl = Text("transmitted chirp", font_size=21, color=TECH_CYAN).next_to(ax, UP, buff=0.12).shift(LEFT * 2.6)
        self.play(FadeIn(txl), run_time=0.6)
        self.play(Create(rx), run_time=1.8)
        rxl = Text("echo — delayed by 2R/c", font_size=21, color=NEON_PINK).next_to(ax, UP, buff=0.12).shift(RIGHT * 2.0)
        self.play(FadeIn(rxl), run_time=0.7)

        # the beat gap
        gx = 2.4
        gap = Line(ax.c2p(gx, ramp(gx, 0.55)), ax.c2p(gx, ramp(gx)), color=AMBER, stroke_width=6)
        gb = Brace(gap, RIGHT, buff=0.08)
        gl = Text("f_beat", font_size=26, color=AMBER, weight=BOLD).next_to(gb, RIGHT, buff=0.1)
        self.play(Create(gap), GrowFromCenter(gb), Write(gl), run_time=1.4)

        eq = Text("f_beat  =  (2R/c) · (B/T)", font_size=32, color=AMBER, weight=BOLD)
        eq.shift(DOWN * 1.85).set_x(-1.6)
        self.play(Write(eq), run_time=1.5)
        self.wait(0.6)

        updown = VGroup(
            Text("SWEEP UP  then  SWEEP DOWN", font_size=27, color=TEXT_WHITE, weight=BOLD),
            Text("range shifts both beats the SAME way", font_size=24, color=TECH_CYAN),
            Text("Doppler shifts them in OPPOSITE ways", font_size=24, color=NEON_PINK),
            Text("R  =  (f_up + f_dn)/2       v  ∝  (f_up − f_dn)/2",
                 font_size=26, color=RADAR_GREEN, weight=BOLD),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.35)
        for u in updown:
            self.play(FadeIn(u, shift=UP * 0.2), run_time=0.9)
            self.wait(0.25)
        self.play(Indicate(updown[3], color=RADAR_GREEN, scale_factor=1.05), run_time=1.0)
        self.wait(0.5)

        self.play(FadeOut(VGroup(updown, eq)), run_time=0.8)
        dotx = ValueTracker(0.05)
        runner = always_redraw(lambda: Dot(ax.c2p(dotx.get_value(), ramp(dotx.get_value())),
                                           radius=0.1, color=AMBER))
        self.add(runner)
        self.play(dotx.animate.set_value(3.2), run_time=3.0, rate_func=linear)
        runner.clear_updaters()
        self.play(FadeOut(VGroup(ax, xl, yl, tx, txl, rx, rxl, gap, gb, gl, runner)), run_time=0.8)
        adv = VGroup(
            Text("WHY FMCW WON THE CAR", font_size=30, color=TECH_CYAN, weight=BOLD),
            bullet("no high-power pulse — cheap solid-state transmitters", size=24),
            bullet("huge bandwidth (4 GHz at 77 GHz) → centimetre resolution", size=24),
            bullet("range AND velocity from a 2-D FFT of the beat signal", size=24),
            bullet("no blind range — it transmits and receives at the same time", size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(UP * 0.35)
        adv.set_x(-0.3)
        self.play(FadeIn(adv[0], shift=RIGHT * 0.2), run_time=1.0)
        for b in adv[1:]:
            self.play(FadeIn(b, shift=RIGHT * 0.25), run_time=0.9)
            self.wait(0.6)
        self.wait(1.0)
        close = Text("the same two answers — reached by frequency instead of timing",
                     font_size=28, color=AMBER, weight=BOLD).to_edge(DOWN, buff=0.4)
        self.play(Write(close), run_time=2.2)
        self.wait(2.5)
        self.fill()


# ============================ PART 19 : APPLICATIONS ============================
class Part19(NarratedScene):
    def construct(self):
        h = head("WHERE THIS SHOWS UP", color=RADAR_GREEN)
        self.play(FadeIn(h[0]), Create(h[1]), run_time=1.0)

        def card(title, line, color):
            t = Text(title, font_size=27, color=color, weight=BOLD)
            s = Text(line, font_size=20, color=TEXT_WHITE)
            s.scale_to_fit_width(min(s.width, 3.5))
            g = VGroup(t, s).arrange(DOWN, buff=0.18)
            box = RoundedRectangle(corner_radius=0.14, width=3.9, height=1.65,
                                   stroke_color=color, stroke_width=2.5,
                                   fill_color=color, fill_opacity=0.09).move_to(g)
            return VGroup(box, g)

        c1 = card("SPEED GUN", "pure Doppler — no ranging at all", AMBER)
        c2 = card("WEATHER RADAR", "rainfall from power, wind from Doppler", TECH_CYAN)
        c3 = card("ADAPTIVE CRUISE", "FMCW — range + closing rate, 100s/sec", RADAR_GREEN)
        c4 = card("AIR TRAFFIC CONTROL", "long-range surveillance, low PRF", NEON_PINK)
        c5 = card("AIR DEFENCE", "pulse-Doppler tracking through clutter", AMBER)

        top = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.35).shift(UP * 1.15)
        bot = VGroup(c4, c5).arrange(RIGHT, buff=0.35).shift(DOWN * 0.85)

        for c in [c1, c2, c3, c4, c5]:
            self.play(FadeIn(c, scale=0.85), run_time=0.85)
            self.wait(0.55)

        line = Line(LEFT * 5.6, RIGHT * 5.6, color=SUBTLE, stroke_width=2).shift(DOWN * 2.35)
        self.play(Create(line), run_time=0.6)
        kick = VGroup(
            Text("tornado warnings, collision braking, air safety", font_size=27, color=TEXT_WHITE),
            Text("all resting on the same two equations", font_size=30, color=AMBER, weight=BOLD),
        ).arrange(DOWN, buff=0.22).next_to(line, DOWN, buff=0.35)
        self.play(FadeIn(kick[0]), run_time=1.0)
        self.play(FadeIn(kick[1]), run_time=1.0)
        self.wait(0.6)

        self.play(FadeOut(VGroup(top, bot, line, kick)), run_time=0.9)
        story = Text("ONE EXAMPLE:  TORNADO DETECTION",
                     font_size=30, color=NEON_PINK, weight=BOLD).shift(UP * 2.35)
        self.play(Write(story), run_time=1.8)
        steps = VGroup(
            bullet("echo POWER tells you where the rain is", size=25),
            bullet("Doppler tells you how fast each parcel moves", size=25),
            bullet("side by side: one half closing, the other receding", size=25,
                   color=AMBER, dot_color=AMBER),
            bullet("that couplet is rotation — a mesocyclone signature", size=25,
                   color=NEON_PINK, dot_color=NEON_PINK),
            bullet("the warning goes out ~13 minutes before touchdown", size=25,
                   color=RADAR_GREEN, dot_color=RADAR_GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(DOWN * 0.35)
        steps.set_x(-0.2)
        for s in steps:
            self.play(FadeIn(s, shift=RIGHT * 0.25), run_time=1.0)
            self.wait(0.8)
        self.play(Indicate(steps[3], color=NEON_PINK, scale_factor=1.05), run_time=1.0)
        self.wait(0.8)
        close = Text("distance and speed — out of a single reflected wave",
                     font_size=30, color=TEXT_WHITE, weight=BOLD).to_edge(DOWN, buff=0.45)
        self.play(Write(close), run_time=2.2)
        self.wait(3.2)
        self.fill()


# ============================ PART 20 : RECAP & OUTRO ============================
class Part20(NarratedScene):
    def construct(self):
        h = head("TWO MEASUREMENTS · TWO MECHANISMS")
        self.play(FadeIn(h[0]), Create(h[1]), run_time=1.1)

        def side(title, mech, eq, items, color):
            t = Text(title, font_size=34, color=color, weight=BOLD)
            m = Text(mech, font_size=22, color=DIM_TEXT)
            e = Text(eq, font_size=44, color=TEXT_WHITE, weight=BOLD)
            its = VGroup(*[Text(i, font_size=20, color=DIM_TEXT) for i in items])
            its.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
            g = VGroup(t, m, e, its).arrange(DOWN, buff=0.26)
            return VGroup(panel(g, color=color, buff=0.36), g)

        left = side("RANGE", "TIME OF FLIGHT", "R = c·Δt / 2",
                    ["resolution:  ΔR = c·τ/2", "limit:  R_max = c / 2·PRF"], RADAR_GREEN)
        right = side("VELOCITY", "DOPPLER SHIFT", "v = λ·f_d / 2",
                     ["needs radial motion:  v·cosθ", "limit:  ±λ·PRF/4"], NEON_PINK)
        cols = VGroup(left, right).arrange(RIGHT, buff=0.7).shift(UP * 0.75)
        cols.scale_to_fit_width(11.8)

        self.play(FadeIn(left, shift=RIGHT * 0.4), run_time=1.3)
        self.play(FadeIn(right, shift=LEFT * 0.4), run_time=1.3)
        self.wait(1.0)

        join = Text("a range-Doppler map delivers BOTH from the same received data",
                    font_size=28, color=AMBER, weight=BOLD).shift(DOWN * 1.55)
        self.play(Write(join), run_time=2.2)
        self.wait(0.8)

        wave = Text("every limit we met — resolution, ambiguity, blind speeds —",
                    font_size=26, color=TEXT_WHITE).shift(DOWN * 2.35)
        wave2 = Text("traces back to one choice:  THE WAVEFORM",
                     font_size=30, color=TECH_CYAN, weight=BOLD).shift(DOWN * 2.9)
        self.play(FadeIn(wave), run_time=1.1)
        self.play(Write(wave2), run_time=1.5)
        self.wait(1.0)

        self.play(FadeOut(VGroup(cols, join, wave, wave2)), run_time=1.0)
        end = Text("Thanks for watching", font_size=54, color=TEXT_WHITE, weight=BOLD)
        end2 = Text("like  ·  subscribe  ·  more radar engineering", font_size=28, color=AMBER)
        grp = VGroup(end, end2).arrange(DOWN, buff=0.35).shift(DOWN * 0.2)
        self.play(FadeIn(end, scale=1.15), run_time=1.2)
        self.play(Write(end2), run_time=1.4)
        rings = VGroup(*[Circle(radius=1.2 + i * 0.9, color=RADAR_GREEN,
                                stroke_width=3, stroke_opacity=0.5 - i * 0.12)
                         for i in range(4)]).move_to(grp)
        self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.2), run_time=1.6)
        self.wait(0.6)

        self.play(FadeOut(rings), run_time=0.8)
        recap = VGroup(
            Text("R  =  c·Δt / 2", font_size=34, color=RADAR_GREEN, weight=BOLD),
            Text("v  =  λ·f_d / 2", font_size=34, color=NEON_PINK, weight=BOLD),
        ).arrange(RIGHT, buff=1.2).next_to(grp, DOWN, buff=0.8)
        self.play(FadeIn(recap[0], shift=UP * 0.2), run_time=1.0)
        self.play(FadeIn(recap[1], shift=UP * 0.2), run_time=1.0)
        self.wait(1.2)
        for _ in range(4):
            ping = Circle(radius=0.3, color=RADAR_GREEN, stroke_width=5).move_to(grp.get_center())
            self.add(ping)
            self.play(ping.animate.scale(14).set_stroke(opacity=0.0),
                      run_time=2.2, rate_func=linear)
            self.remove(ping)
        self.wait(1.5)
        self.play(FadeOut(VGroup(end, end2, recap)), run_time=1.5)
        self.wait(1.0)
        self.fill()
