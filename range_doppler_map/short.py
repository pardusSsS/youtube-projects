"""
Vertical Short: "What Is a Range-Doppler Map?"

Six scenes, 1080x1920, kept under sixty seconds.  Every scene ends with
`self.fill()`, which pads the picture out to the length of that scene's MP3 in
voiceovers/durations.json -- timing is derived, never hand-tuned.

    python build.py

Two things matter when rendering 9:16 in Manim.  It derives pixels-per-unit from
`frame_width` alone and never adjusts it for a tall canvas, so a vertical render
silently letterboxes the scene into a middle band; pinning both dimensions makes
the 1080x1920 frame exactly 4.5 x 8 units.  And the frame is then only 4.5 units
across, so every text block goes through `fit()`.  Content is kept above
y = -3.0, clear of the Shorts title overlay.

No LaTeX: MathTex/DecimalNumber shell out to `latex`, so all formulas are Pango
`Text` with Unicode glyphs and live readouts go through `live_text()`.
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
config.frame_height = 8.0
config.frame_width = 4.5

# ============================ NARRATION SYNC ============================
_HERE = os.path.dirname(os.path.abspath(__file__))
_DUR_FILE = os.path.join(_HERE, "voiceovers", "durations.json")
NARRATION = json.load(open(_DUR_FILE)) if os.path.exists(_DUR_FILE) else {}

TAIL = 0.35          # Shorts breathe less than a long cut
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


# ============================ SHARED BUILDERS ============================
def panel(mob, color=TECH_CYAN, buff=0.3, opacity=0.10):
    return RoundedRectangle(
        corner_radius=0.14,
        width=mob.width + 2 * buff,
        height=mob.height + 2 * buff,
        stroke_color=color, stroke_width=2.5,
        fill_color=color, fill_opacity=opacity,
    ).move_to(mob)


def live_text(fn, font_size=30, color=TECH_CYAN, anchor=ORIGIN, edge=LEFT):
    """A self-updating readout built from Text (DecimalNumber needs LaTeX)."""
    return always_redraw(
        lambda: Text(fn(), font_size=font_size, color=color, weight=BOLD)
        .move_to(anchor, aligned_edge=edge))


def dish(scale=1.0, color=TECH_CYAN):
    """A simple parabolic-dish side view pointing right."""
    face = Arc(radius=0.9, start_angle=PI * 0.62, angle=-PI * 1.24,
               color=color, stroke_width=6)
    feed = Line(ORIGIN, RIGHT * 0.55, color=color, stroke_width=4)
    feed.move_to(face.get_center() + RIGHT * 0.3)
    horn = Dot(feed.get_right(), radius=0.09, color=AMBER)
    mast = Line(ORIGIN, DOWN * 0.9, color=color, stroke_width=5).next_to(face, DOWN, buff=0)
    base = Line(LEFT * 0.4, RIGHT * 0.4, color=color, stroke_width=6).next_to(mast, DOWN, buff=0)
    return VGroup(face, feed, horn, mast, base).scale(scale)


def data_grid(nx=8, ny=10, cell=0.32):
    """The raw dwell: rows are range bins (fast time), columns are pulses (slow time)."""
    cells = {}
    grid = VGroup()
    for i in range(nx):
        for j in range(ny):
            sq = Square(side_length=cell, stroke_color=SUBTLE, stroke_width=1,
                        fill_color=PANEL_NAVY, fill_opacity=0.9)
            sq.move_to(RIGHT * (i - nx / 2 + 0.5) * cell + UP * (j - ny / 2 + 0.5) * cell)
            cells[(i, j)] = sq
            grid.add(sq)
    return grid, cells


def rd_map(width=3.5, height=3.0):
    """The finished map: range up the side, velocity across, zero-Doppler marked."""
    rect = Rectangle(width=width, height=height, stroke_color=TECH_CYAN,
                     stroke_width=3, fill_color=PANEL_NAVY, fill_opacity=0.92)
    vax = Text("velocity  →", font_size=24, color=NEON_PINK).next_to(rect, DOWN, buff=0.16)
    rax = Text("range  →", font_size=24, color=TECH_CYAN)
    rax.rotate(PI / 2).next_to(rect, LEFT, buff=0.16)
    zero = DashedLine(rect.get_bottom() + UP * 0.05, rect.get_top() + DOWN * 0.05,
                      color=DIM_TEXT, stroke_width=2, dash_length=0.09)
    zero.set_x(rect.get_x())
    return VGroup(rect, vax, rax, zero)


def blob(center, dx, dy, color, radius=0.10):
    """A detection: concentric dots faking a point spread on the map."""
    g = VGroup()
    for k in range(4):
        g.add(Dot(center + RIGHT * dx + UP * dy, radius=radius + k * 0.065,
                  color=color, fill_opacity=0.55 - k * 0.12))
    return g


# ============================ 1 : THE HOOK ============================
class Short1(NarratedShort):
    def construct(self):
        t1 = Text("WHAT IS A", font_size=48, color=TEXT_WHITE, weight=BOLD)
        t2 = Text("RANGE-DOPPLER", font_size=48, color=TECH_CYAN, weight=BOLD)
        t3 = Text("MAP?", font_size=72, color=TECH_CYAN, weight=BOLD)
        title = VGroup(t1, t2, t3).arrange(DOWN, buff=0.14)
        fit(title).move_to(UP * 2.9)

        self.play(LaggedStart(FadeIn(t1, shift=DOWN * 0.2),
                              FadeIn(t2, shift=DOWN * 0.2),
                              FadeIn(t3, scale=1.2), lag_ratio=0.35), run_time=1.6)

        ant = dish(scale=0.42, color=TECH_CYAN).move_to(LEFT * 1.5 + UP * 1.5)
        self.play(FadeIn(ant, shift=RIGHT * 0.2), run_time=0.6)
        beam = VGroup(*[Arc(radius=0.3 + i * 0.26, start_angle=-PI / 5, angle=2 * PI / 5,
                            color=RADAR_GREEN, stroke_width=5 - i * 0.8)
                        .move_arc_center_to(ant[2].get_center()) for i in range(4)])
        self.play(LaggedStart(*[Create(a) for a in beam], lag_ratio=0.18), run_time=0.9)

        m = rd_map(width=3.3, height=2.3).move_to(DOWN * 0.6)
        self.play(FadeOut(beam), Create(m[0]), run_time=0.8)
        self.play(FadeIn(m[1]), FadeIn(m[2]), Create(m[3]), run_time=0.7)

        c = m[0].get_center()
        b1 = blob(c, 0.95, 0.62, RADAR_GREEN)
        b2 = blob(c, -1.0, -0.5, TECH_CYAN)
        b3 = blob(c, 0.0, -0.15, NEON_PINK)
        self.play(LaggedStart(FadeIn(b1, scale=0.5), FadeIn(b2, scale=0.5),
                              FadeIn(b3, scale=0.5), lag_ratio=0.45), run_time=1.4)
        self.play(Flash(b1.get_center(), color=RADAR_GREEN, flash_radius=0.6,
                        line_length=0.18, num_lines=14), run_time=0.5)

        kick = VGroup(
            Text("not a blip", font_size=30, color=DIM_TEXT),
            Text("a whole picture", font_size=32, color=AMBER, weight=BOLD),
        ).arrange(DOWN, buff=0.12)
        fit(kick).move_to(DOWN * 2.6)
        self.play(FadeIn(kick, shift=UP * 0.2), run_time=1.0)
        self.wait(0.5)
        self.fill()


# ============================ 2 : THE RAW TABLE ============================
class Short2(NarratedShort):
    def construct(self):
        title = Text("IT STARTS AS A TABLE", font_size=38, color=RADAR_GREEN, weight=BOLD)
        fit(title).move_to(UP * 3.45)
        self.play(Write(title), run_time=1.0)

        nx, ny = 8, 10
        grid, cells = data_grid(nx, ny)
        grid.move_to(UP * 0.45)
        self.play(FadeIn(grid, lag_ratio=0.01), run_time=1.2)

        rax = Text("range\n(fast time)", font_size=23, color=TECH_CYAN, line_spacing=0.6)
        rax.rotate(PI / 2).next_to(grid, LEFT, buff=0.14)
        cax = Text("pulse #   (slow time)  →", font_size=23, color=NEON_PINK)
        fit(cax, 3.6).next_to(grid, DOWN, buff=0.18)
        self.play(FadeIn(rax), FadeIn(cax), run_time=0.9)

        # Two targets and the clutter ridge sit in fixed range bins; everything
        # else is thermal noise, which is what makes the bright rows readable.
        rng = np.random.default_rng(7)
        targets = {8: RADAR_GREEN, 3: TECH_CYAN, 5: NEON_PINK}

        for i in range(nx):
            anims = []
            for j in range(ny):
                if j in targets:
                    anims.append(cells[(i, j)].animate.set_fill(
                        targets[j], opacity=0.55 + 0.3 * rng.random()))
                else:
                    anims.append(cells[(i, j)].animate.set_fill(
                        SUBTLE, opacity=0.25 + 0.45 * rng.random()))
            self.play(*anims, run_time=0.42, rate_func=linear)

        note = VGroup(
            Text("one row  =  one range bin", font_size=27, color=TECH_CYAN),
            Text("one column  =  one pulse", font_size=27, color=NEON_PINK),
            Text("hundreds of pulses, one look", font_size=26, color=TEXT_WHITE),
        ).arrange(DOWN, buff=0.16)
        fit(note).move_to(DOWN * 2.45)
        self.play(FadeIn(note[0], shift=UP * 0.15), run_time=0.7)
        self.play(FadeIn(note[1], shift=UP * 0.15), run_time=0.7)
        self.play(FadeIn(note[2], shift=UP * 0.15), run_time=0.8)
        self.wait(0.4)
        self.fill()


# ============================ 3 : FFT ALONG SLOW TIME ============================
class Short3(NarratedShort):
    def construct(self):
        title = Text("PICK ONE ROW", font_size=42, color=AMBER, weight=BOLD)
        fit(title).move_to(UP * 3.45)
        self.play(FadeIn(title, scale=1.15), run_time=0.8)

        # the row itself, pulled out of the table
        n = 9
        cell = 0.4
        strip = VGroup(*[Square(side_length=cell, stroke_color=SUBTLE, stroke_width=1.5,
                               fill_color=RADAR_GREEN, fill_opacity=0.55)
                        .move_to(RIGHT * (i - n / 2 + 0.5) * cell) for i in range(n)])
        fit(strip).move_to(UP * 2.6)
        lbl = Text("same target, every pulse", font_size=25, color=DIM_TEXT)
        fit(lbl).next_to(strip, DOWN, buff=0.18)
        self.play(LaggedStart(*[FadeIn(s, scale=0.6) for s in strip], lag_ratio=0.08),
                  run_time=1.0)
        self.play(FadeIn(lbl), run_time=0.5)

        # ...but the phase creeps from pulse to pulse
        ph = Text("the PHASE creeps", font_size=30, color=NEON_PINK, weight=BOLD)
        fit(ph).move_to(UP * 1.65)
        self.play(FadeIn(ph, shift=UP * 0.15), run_time=0.6)

        axis = Line(LEFT * 1.75, RIGHT * 1.75, color=SUBTLE, stroke_width=2).move_to(UP * 0.9)
        self.play(Create(axis), run_time=0.4)

        xs = np.linspace(-1.7, 1.7, n)
        pf = lambda x: 0.5 * np.sin(2.3 * x + 0.5)
        dots = VGroup(*[Dot([x, 0.9 + pf(x), 0], radius=0.06, color=AMBER) for x in xs])
        stems = VGroup(*[Line([x, 0.9, 0], [x, 0.9 + pf(x), 0],
                              color=AMBER, stroke_width=2, stroke_opacity=0.55) for x in xs])
        self.play(LaggedStart(*[AnimationGroup(Create(s), FadeIn(d, scale=0.5))
                                for s, d in zip(stems, dots)], lag_ratio=0.12),
                  run_time=1.6)

        curve = VMobject(stroke_color=AMBER, stroke_width=3.5, stroke_opacity=0.65)
        curve.set_points_smoothly([np.array([x, 0.9 + pf(x), 0])
                                   for x in np.linspace(-1.7, 1.7, 48)])
        self.play(Create(curve), run_time=1.0)

        that = Text("a creep is a frequency", font_size=27, color=TEXT_WHITE)
        fit(that).move_to(DOWN * 0.1)
        self.play(FadeIn(that), run_time=0.6)

        arrow = Arrow(UP * 0.1, DOWN * 0.55, color=AMBER, stroke_width=7, buff=0,
                      max_tip_length_to_length_ratio=0.35).move_to(DOWN * 0.72)
        fftl = Text("FFT", font_size=32, color=AMBER, weight=BOLD).next_to(arrow, RIGHT, buff=0.18)
        self.play(GrowArrow(arrow), FadeIn(fftl), run_time=0.7)

        # the spectrum: one clean peak whose position is the velocity
        sax = Line(LEFT * 1.7, RIGHT * 1.7, color=SUBTLE, stroke_width=2).move_to(DOWN * 2.3)
        peak_x = 0.85
        spec = VMobject(stroke_color=RADAR_GREEN, stroke_width=4)
        spec.set_points_smoothly([np.array([x, -2.3 + 0.85 * np.exp(-((x - peak_x) / 0.19) ** 2), 0])
                                  for x in np.linspace(-1.7, 1.7, 90)])
        sl = Text("f_d", font_size=26, color=RADAR_GREEN, weight=BOLD)
        sl.move_to([peak_x, -1.25, 0])
        self.play(Create(sax), run_time=0.4)
        self.play(Create(spec), FadeIn(sl), run_time=1.2)

        out = Text("→  v  =  λ f_d / 2", font_size=32, color=AMBER, weight=BOLD)
        fit(out).move_to(DOWN * 2.75)
        self.play(FadeIn(out, shift=UP * 0.15), run_time=0.9)
        self.wait(0.4)
        self.fill()


# ============================ 4 : THE MAP APPEARS ============================
class Short4(NarratedShort):
    def construct(self):
        title = Text("EVERY ROW, ONE FFT", font_size=38, color=TECH_CYAN, weight=BOLD)
        fit(title).move_to(UP * 3.5)
        self.play(Write(title), run_time=0.9)

        grid, cells = data_grid(nx=8, ny=8, cell=0.2)
        grid.move_to(UP * 2.5)
        rng = np.random.default_rng(3)
        for (i, j), sq in cells.items():
            sq.set_fill(SUBTLE if j not in (2, 5) else RADAR_GREEN,
                        opacity=0.3 + 0.4 * rng.random())
        gl = Text("raw table", font_size=22, color=DIM_TEXT).next_to(grid, LEFT, buff=0.22)
        self.play(FadeIn(grid, lag_ratio=0.02), FadeIn(gl), run_time=0.9)

        arrow = Arrow(UP * 0.2, DOWN * 0.2, color=AMBER, stroke_width=7, buff=0,
                      max_tip_length_to_length_ratio=0.4).move_to(UP * 1.4)
        self.play(GrowArrow(arrow), run_time=0.5)

        m = rd_map(width=3.4, height=2.6).move_to(DOWN * 0.25)
        self.play(Create(m[0]), run_time=0.9)
        self.play(FadeIn(m[2], shift=RIGHT * 0.15), run_time=0.6)
        self.play(FadeIn(m[1], shift=UP * 0.15), Create(m[3]), run_time=0.7)

        c = m[0].get_center()
        b1 = blob(c, 1.0, 0.75, RADAR_GREEN)
        b2 = blob(c, -1.05, -0.62, TECH_CYAN)
        b3 = blob(c, 0.0, -0.1, NEON_PINK)
        self.play(LaggedStart(FadeIn(b1, scale=0.5), FadeIn(b2, scale=0.5),
                              FadeIn(b3, scale=0.5), lag_ratio=0.4), run_time=1.3)

        key = VGroup(
            Text("vertical      →  range", font_size=27, color=TECH_CYAN),
            Text("horizontal  →  velocity", font_size=27, color=NEON_PINK),
            Text("brightness  →  echo strength", font_size=26, color=AMBER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        fit(key).move_to(DOWN * 2.45)
        for r in key:
            self.play(FadeIn(r, shift=RIGHT * 0.18), run_time=0.55)
        self.wait(0.3)
        self.fill()


# ============================ 5 : READING IT ============================
class Short5(NarratedShort):
    def construct(self):
        title = Text("NOW IT READS LIKE A CHART", font_size=33, color=RADAR_GREEN, weight=BOLD)
        fit(title).move_to(UP * 3.5)

        m = rd_map(width=3.5, height=3.1).move_to(UP * 1.15)
        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(m), run_time=0.8)

        c = m[0].get_center()

        def tag(b, text, color, direction):
            t = Text(text, font_size=23, color=color)
            fit(t, 1.7).next_to(b, direction, buff=0.1)
            return t

        b1 = blob(c, 1.05, 0.95, RADAR_GREEN)
        t1 = tag(b1, "far, closing fast", RADAR_GREEN, LEFT)
        b2 = blob(c, -1.1, -0.85, TECH_CYAN)
        t2 = tag(b2, "near, opening", TECH_CYAN, RIGHT)
        b3 = blob(c, 0.0, -0.15, NEON_PINK, radius=0.12)
        t3 = tag(b3, "clutter", NEON_PINK, RIGHT)

        self.play(FadeIn(b1, scale=0.5), FadeIn(t1), run_time=0.8)
        self.play(FadeIn(b2, scale=0.5), FadeIn(t2), run_time=0.8)
        self.play(FadeIn(b3, scale=0.5), FadeIn(t3), run_time=0.8)

        # everything that is not moving piles up in one column
        col = Rectangle(width=0.42, height=m[0].height - 0.1,
                        stroke_color=NEON_PINK, stroke_width=3,
                        fill_color=NEON_PINK, fill_opacity=0.14)
        col.move_to([m[0].get_x(), m[0].get_y(), 0])
        zv = Text("v = 0", font_size=24, color=NEON_PINK, weight=BOLD)
        zv.next_to(col, UP, buff=0.1)
        self.play(Create(col), FadeIn(zv), run_time=0.8)
        self.play(Indicate(col, color=NEON_PINK, scale_factor=1.04), run_time=0.6)

        cut = Text("cut that column", font_size=30, color=AMBER, weight=BOLD)
        fit(cut).move_to(DOWN * 1.75)
        self.play(FadeIn(cut, shift=UP * 0.15), run_time=0.6)
        self.play(FadeOut(b3), FadeOut(t3), FadeOut(zv),
                  col.animate.set_fill(opacity=0).set_stroke(opacity=0.25), run_time=1.0)

        gone = VGroup(
            Text("clutter gone", font_size=32, color=RADAR_GREEN, weight=BOLD),
            Text("targets untouched", font_size=28, color=TEXT_WHITE),
        ).arrange(DOWN, buff=0.14)
        fit(gone).move_to(DOWN * 2.15)
        self.play(FadeOut(cut), FadeIn(gone, shift=UP * 0.2), run_time=0.9)
        self.play(Indicate(b1, color=RADAR_GREEN, scale_factor=1.15), run_time=0.7)
        self.wait(0.4)
        self.fill()


# ============================ 6 : THE AXIS WRAPS ============================
class Short6(NarratedShort):
    def construct(self):
        title = Text("ONE CATCH", font_size=48, color=NEON_PINK, weight=BOLD)
        fit(title).move_to(UP * 3.45)
        self.play(FadeIn(title, scale=1.2), run_time=0.7)

        m = rd_map(width=3.5, height=2.6).move_to(UP * 1.0)
        self.play(FadeIn(m), run_time=0.7)
        rect = m[0]
        c = rect.get_center()
        half = rect.width / 2 - 0.12

        eq = Text("|v|  <  λ · PRF / 4", font_size=36, color=AMBER, weight=BOLD)
        fit(eq, 3.4).move_to(DOWN * 1.05)
        box = panel(eq, color=AMBER, buff=0.26)
        self.play(Create(box), Write(eq), run_time=1.2)

        clutter = blob(c, 0.0, -0.55, NEON_PINK, radius=0.11)
        self.add(clutter)

        x = ValueTracker(0.35)
        fast = always_redraw(lambda: blob(
            np.array([c[0] + ((x.get_value() + half) % (2 * half)) - half, c[1] + 0.6, 0]),
            0, 0, RADAR_GREEN))
        self.add(fast)

        readout = live_text(lambda: f"v = {x.get_value() * 210:.0f} m/s",
                            color=RADAR_GREEN, font_size=24,
                            anchor=np.array([-1.75, 2.9, 0]))
        self.add(readout)

        self.play(x.animate.set_value(half - 0.05), run_time=1.3, rate_func=linear)
        self.play(x.animate.set_value(half + 0.75), run_time=1.1, rate_func=linear)

        wrap = Text("it wrapped around", font_size=30, color=NEON_PINK, weight=BOLD)
        fit(wrap).move_to(DOWN * 1.85)
        self.play(FadeIn(wrap, shift=UP * 0.15), run_time=0.6)

        self.play(x.animate.set_value(2 * half), run_time=1.2, rate_func=linear)
        readout.clear_updaters()
        self.remove(readout)

        self.play(Flash(clutter.get_center(), color=NEON_PINK, flash_radius=0.55,
                        line_length=0.18, num_lines=14), run_time=0.5)
        folded = VGroup(
            Text("folded into the clutter", font_size=28, color=NEON_PINK),
            Text("and it vanishes", font_size=30, color=NEON_PINK, weight=BOLD),
        ).arrange(DOWN, buff=0.12)
        fit(folded).move_to(DOWN * 1.8)
        self.play(FadeOut(wrap), FadeIn(folded), run_time=0.8)

        outro = VGroup(
            Text("every dwell", font_size=28, color=DIM_TEXT),
            Text("every modern radar", font_size=28, color=TEXT_WHITE),
            Text("builds this map", font_size=34, color=TECH_CYAN, weight=BOLD),
        ).arrange(DOWN, buff=0.13)
        fit(outro).move_to(DOWN * 2.5)
        self.play(FadeOut(folded), FadeIn(outro, shift=UP * 0.2), run_time=1.1)
        self.wait(0.5)
        self.fill()
