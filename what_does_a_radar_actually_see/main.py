"""
What Does a Radar Actually See? | From Chirp to Detection
=========================================================

Sixteen Manim scenes, one per narration block.  Every scene inherits from
`NarratedScene`, whose `fill()` call pads the scene out to the exact length of
its MP3 in `voiceovers/durations.json`.  Run `voice.py` before rendering, or
build the whole thing with `build.py`.

Layout discipline
-----------------
Nothing is positioned by eye.  The frame is carved into named `Zone`s (header,
body, the two half-columns, the footer strip) and every text block is placed by
`Zone.fit()`, which shrinks it until it fits inside that zone with padding.
Zones do not intersect, so two blocks in different zones cannot collide.

On top of that, `NarratedScene` audits itself after every `play()` and
`wait()`: it walks the visible `Text` mobjects, tests every pair of bounding
boxes, and prints a `[LAYOUT]` line for any overlap or anything drifting off
the frame.  `build.py` greps the render log for those lines and refuses to
report success quietly.  Set RADAR_LAYOUT_CHECK=0 to skip the audit.

No LaTeX is used anywhere: MathTex/DecimalNumber shell out to `latex`, so every
formula here is a Pango `Text` built from Unicode glyphs.
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
VIOLET = "#A472FF"
TEXT_WHITE = "#EAF2FF"
DIM_TEXT = "#8FA3C4"

config.background_color = DEEP_NAVY

# ============================ NARRATION SYNC ============================
_HERE = os.path.dirname(os.path.abspath(__file__))
_DUR_FILE = os.path.join(_HERE, "voiceovers", "durations.json")
NARRATION = json.load(open(_DUR_FILE)) if os.path.exists(_DUR_FILE) else {}
TAIL = 0.6          # breathing room after the voice stops

# ============================ LAYOUT ZONES ============================
# The 16:9 frame is 14.222 x 8.0 Manim units.  Everything lives inside these.
LAYOUT_CHECK = os.environ.get("RADAR_LAYOUT_CHECK", "1") != "0"
SAFE_X, SAFE_Y = 7.00, 3.92      # anything beyond this is falling off the frame
TOUCH = 0.05                     # boxes may come this close before it is a clash

# Pacing.  Scenes are choreographed at a natural rhythm and then stretched by
# these three knobs until the picture runs as long as the narration; BEAT is the
# short hold after every substantial reveal, which is what stops an explainer
# from feeling rushed.  build.py prints the per-scene residual.
PACE = float(os.environ.get("RADAR_PACE", "1.40"))
BEAT = float(os.environ.get("RADAR_BEAT", "0.40"))
WAIT_SCALE = float(os.environ.get("RADAR_WAIT", "1.15"))

# Every scene is choreographed once at a natural rhythm, then stretched or
# tightened by a single per-scene multiplier so the picture lands on its own
# narration.  All three knobs above scale together, so the whole scene is
# linear in this number: run the build, read the pad in the sync report, and
# multiply.  Anything missing here plays at 1.0.
TEMPO = {
    "Part1": 0.70, "Part2": 0.84, "Part3": 0.76, "Part4": 0.78,
    "Part5": 0.98, "Part6": 0.91, "Part7": 0.90, "Part8": 0.92,
    "Part9": 1.01, "Part10": 1.06, "Part11": 1.03, "Part12": 1.35,
    "Part13": 1.07, "Part14": 0.96, "Part15": 1.17, "Part16": 1.30,
}


class Zone:
    """A rectangle of the frame.  `fit` scales a mobject down until it lives here."""

    def __init__(self, x0, y0, x1, y1):
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1

    @property
    def center(self):
        return np.array([(self.x0 + self.x1) / 2, (self.y0 + self.y1) / 2, 0.0])

    @property
    def width(self):
        return self.x1 - self.x0

    @property
    def height(self):
        return self.y1 - self.y0

    def fit(self, mob, pad=0.18, max_scale=1.0):
        w, h = self.width - 2 * pad, self.height - 2 * pad
        s = min(w / max(mob.width, 1e-6), h / max(mob.height, 1e-6), max_scale)
        if s < 1.0:
            mob.scale(s)
        mob.move_to(self.center)
        return mob

    def top(self, mob, pad=0.18):
        """Fit, then push to the top of the zone instead of centring."""
        self.fit(mob, pad)
        mob.shift(UP * (self.y1 - pad - mob.get_top()[1]))
        return mob

    def sub(self, x0=0.0, y0=0.0, x1=1.0, y1=1.0):
        """A sub-zone in normalised coordinates."""
        return Zone(self.x0 + x0 * self.width, self.y0 + y0 * self.height,
                    self.x0 + x1 * self.width, self.y0 + y1 * self.height)


HEADER = Zone(-6.95, 2.95, 6.95, 3.88)      # head() lives here
BODY = Zone(-6.95, -3.05, 6.95, 2.82)       # everything under a header
FULL = Zone(-6.95, -3.05, 6.95, 3.80)       # everything when there is no header
LCOL = Zone(-6.95, -3.05, -0.20, 2.82)
RCOL = Zone(0.20, -3.05, 6.95, 2.82)
TOPBAND = Zone(-6.95, 0.05, 6.95, 2.82)
MIDBAND = Zone(-6.95, -1.35, 6.95, 1.35)
BOTBAND = Zone(-6.95, -3.05, 6.95, -0.15)
FOOT = Zone(-6.90, -3.86, 6.90, -3.18)      # caption strip, never anything else


def fit_width(mob, w):
    if mob.width > w:
        mob.scale(w / mob.width)
    return mob


# ============================ SELF-AUDITING SCENE ============================
def _box(mob):
    lo, hi = mob.get_corner(DL), mob.get_corner(UR)
    return lo[0], lo[1], hi[0], hi[1]


def _visible(t):
    parts = t.family_members_with_points()
    if not parts:
        return 0.0
    return max(float(p.get_fill_opacity()) for p in parts)


class NarratedScene(Scene):
    """Scene that stretches its own tail so picture length == narration length,
    and that complains loudly if two pieces of text ever share the same pixels."""

    _seen = set()

    # ---------------------------------------------------------- layout audit
    def _texts(self):
        found = []

        def walk(m):
            if isinstance(m, Text):
                found.append(m)
                return
            for s in m.submobjects:
                walk(s)

        for m in self.mobjects:
            walk(m)
        return [t for t in found
                if t.text.strip() and _visible(t) > 0.15 and t.width > 0.02]

    def _flag(self, kind, msg):
        key = (type(self).__name__, kind, msg)
        if key in self._seen:
            return
        self._seen.add(key)
        print(f"[LAYOUT] {type(self).__name__} {kind}: {msg}")

    def audit(self):
        if not LAYOUT_CHECK:
            return
        ts = self._texts()
        boxes = [_box(t) for t in ts]
        for t, b in zip(ts, boxes):
            if b[0] < -SAFE_X or b[2] > SAFE_X or b[1] < -SAFE_Y or b[3] > SAFE_Y:
                self._flag("OFFSCREEN",
                           f'"{t.text[:34]}" x[{b[0]:.2f},{b[2]:.2f}] y[{b[1]:.2f},{b[3]:.2f}]')
        for i in range(len(ts)):
            for j in range(i + 1, len(ts)):
                a, b = boxes[i], boxes[j]
                dx = min(a[2], b[2]) - max(a[0], b[0]) - TOUCH
                dy = min(a[3], b[3]) - max(a[1], b[1]) - TOUCH
                if dx > 0 and dy > 0:
                    self._flag("OVERLAP",
                               f'"{ts[i].text[:26]}" x "{ts[j].text[:26]}" '
                               f'(dx={dx:.2f} dy={dy:.2f})')

    def play(self, *args, **kwargs):
        # Scene.wait() funnels back through play() with a Wait animation, so
        # those come through already timed and must not be stretched twice.
        if len(args) == 1 and isinstance(args[0], Wait):
            super().play(*args, **kwargs)
            self.audit()
            return
        m = TEMPO.get(type(self).__name__, 1.0)
        rt = kwargs.pop("run_time", 1.0)
        super().play(*args, run_time=rt * PACE * m, **kwargs)
        if rt >= 0.7:                      # a hold after every substantial reveal
            super().wait(BEAT * m)
        self.audit()

    def wait(self, duration=1.0, *args, **kwargs):
        m = TEMPO.get(type(self).__name__, 1.0)
        super().wait(duration * WAIT_SCALE * m, *args, **kwargs)

    # ---------------------------------------------------------- closing card
    def recap(self, title, lines, color=AMBER, clear=None, hold=1.0, zone=None):
        """Clear the body and hold a short summary card. Fills the tail of a
        scene with something worth reading instead of a frozen diagram."""
        if clear is not None:
            self.play(FadeOut(clear), run_time=0.8)
        t = Text(title, font_size=30, color=color, weight=BOLD)
        bs = bullets(lines, size=26, dot_color=color)
        g = VGroup(t, bs).arrange(DOWN, buff=0.40, aligned_edge=LEFT)
        card = carded(g, color=color, buff=0.45, opacity=0.08)
        (zone or BODY).fit(card, pad=0.55)
        self.play(FadeIn(card[0]), FadeIn(t), run_time=1.0)
        for b in bs:
            self.play(FadeIn(b, shift=RIGHT * 0.25), run_time=0.8)
            self.wait(hold)
        self.wait(0.8)
        return card

    # ---------------------------------------------------------- narration pad
    def fill(self):
        name = type(self).__name__
        target = NARRATION.get(name)
        played = self.renderer.time
        if target is None:
            print(f"[SYNC] {name}: no narration entry, holding 1.0s")
            super().wait(1.0)
            return
        pad = target + TAIL - played
        flag = "  <-- LONG PAD" if pad > 5 else ("  <-- OVERRUN" if pad < 0 else "")
        print(f"[SYNC] {name}: anim={played:6.2f}s  voice={target:6.2f}s  pad={pad:6.2f}s{flag}")
        self.audit()
        super().wait(max(pad, 0.35))


# ============================ SHARED BUILDERS ============================
def head(text, color=TECH_CYAN, size=40):
    t = Text(text, font_size=size, color=color, weight=BOLD)
    fit_width(t, 12.4)
    t.move_to([0, 3.55, 0])
    rule = Line(LEFT * 6.3, RIGHT * 6.3, stroke_width=2, color=SUBTLE)
    rule.move_to([0, 3.06, 0])
    return VGroup(t, rule)


def caption(text, color=AMBER, size=27):
    t = Text(text, font_size=size, color=color)
    fit_width(t, 12.8)
    t.move_to(FOOT.center)
    return t


def panel(mob, color=TECH_CYAN, buff=0.3, opacity=0.10):
    return RoundedRectangle(
        corner_radius=0.14,
        width=mob.width + 2 * buff,
        height=mob.height + 2 * buff,
        stroke_color=color, stroke_width=2.5,
        fill_color=color, fill_opacity=opacity,
    ).move_to(mob)


def carded(mob, color=TECH_CYAN, buff=0.3, opacity=0.10):
    return VGroup(panel(mob, color, buff, opacity), mob)


def formula(text, color=AMBER, size=42):
    return Text(text, font_size=size, color=color, weight=BOLD)


def bullet(text, color=TEXT_WHITE, size=26, dot_color=RADAR_GREEN, dot="▸"):
    d = Text(dot, font_size=size, color=dot_color)
    t = Text(text, font_size=size, color=color)
    return VGroup(d, t).arrange(RIGHT, buff=0.22)


def bullets(lines, size=26, color=TEXT_WHITE, dot_color=RADAR_GREEN, buff=0.30):
    return VGroup(*[bullet(l, color, size, dot_color) for l in lines]) \
        .arrange(DOWN, aligned_edge=LEFT, buff=buff)


def chip(label, color=TECH_CYAN, size=21, w=None):
    t = Text(label, font_size=size, color=color, weight=BOLD)
    box = RoundedRectangle(corner_radius=0.1, width=(w or t.width + 0.4),
                           height=0.62, stroke_color=color, stroke_width=2.5,
                           fill_color=color, fill_opacity=0.12).move_to(t)
    return VGroup(box, t)


def chain(labels, colors, size=19, buff=0.26, arrow_color=SUBTLE):
    """The processing chain as a strip of chips joined by arrows."""
    g = VGroup()
    chips = []
    for lab, col in zip(labels, colors):
        c = chip(lab, col, size)
        chips.append(c)
        g.add(c)
    g.arrange(RIGHT, buff=buff + 0.26)
    arrows = VGroup()
    for a, b in zip(chips[:-1], chips[1:]):
        arrows.add(Line(a.get_right() + RIGHT * 0.06, b.get_left() + LEFT * 0.06,
                        stroke_color=arrow_color, stroke_width=3))
    out = VGroup(g, arrows)
    out.chips = chips
    return out


def dish(scale=1.0, color=TECH_CYAN):
    """A compact radar sensor: a box with a beam horn, pointing right."""
    body = RoundedRectangle(corner_radius=0.08, width=0.5, height=0.85,
                            stroke_color=color, stroke_width=4,
                            fill_color=PANEL_NAVY, fill_opacity=1)
    horn = Polygon([0.25, 0.28, 0], [0.72, 0.5, 0], [0.72, -0.5, 0], [0.25, -0.28, 0],
                   stroke_color=color, stroke_width=3,
                   fill_color=color, fill_opacity=0.18)
    dot = Dot([0.72, 0, 0], radius=0.07, color=AMBER)
    return VGroup(body, horn, dot).scale(scale)


def car(color=TEXT_WHITE, scale=1.0, flip=False):
    """A small side-view car silhouette facing right."""
    body = RoundedRectangle(corner_radius=0.08, width=1.5, height=0.42,
                            stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.16)
    roof = Polygon([-0.42, 0.21, 0], [-0.26, 0.56, 0], [0.30, 0.56, 0], [0.48, 0.21, 0],
                   stroke_color=color, stroke_width=3,
                   fill_color=color, fill_opacity=0.16)
    w1 = Circle(radius=0.15, stroke_color=color, stroke_width=3,
                fill_color=DEEP_NAVY, fill_opacity=1).move_to([-0.45, -0.24, 0])
    w2 = w1.copy().move_to([0.48, -0.24, 0])
    g = VGroup(body, roof, w1, w2).scale(scale)
    if flip:
        g.flip(UP)
    return g


def noise(n, amp, seed):
    rng = np.random.default_rng(seed)
    return rng.normal(0, amp, n)


class Chart(VGroup):
    """A framed plot box.  `pt(u, v)` maps the unit square onto it, so curves
    are written in normalised coordinates and never wander outside the frame."""

    def __init__(self, width=6.0, height=3.0, x_label="", y_label="",
                 x_color=DIM_TEXT, y_color=DIM_TEXT, label_size=20,
                 frame_color=SUBTLE, fill_opacity=0.55):
        super().__init__()
        self.w, self.h = width, height
        self.box = Rectangle(width=width, height=height, stroke_color=frame_color,
                             stroke_width=2, fill_color=PANEL_NAVY,
                             fill_opacity=fill_opacity)
        self.add(self.box)
        self.xlab = self.ylab = None
        if x_label:
            self.xlab = Text(x_label, font_size=label_size, color=x_color)
            self.xlab.next_to(self.box, DOWN, buff=0.15)
            self.add(self.xlab)
        if y_label:
            self.ylab = Text(y_label, font_size=label_size, color=y_color)
            self.ylab.rotate(PI / 2).next_to(self.box, LEFT, buff=0.15)
            self.add(self.ylab)

    def pt(self, u, v):
        c = self.box.get_center()
        return c + RIGHT * (u - 0.5) * self.w + UP * (v - 0.5) * self.h

    def poly(self, fn, color=TECH_CYAN, stroke=3, n=400, u0=0.0, u1=1.0):
        pts = [self.pt(u, float(np.clip(fn(u), 0.0, 1.0)))
               for u in np.linspace(u0, u1, n)]
        return VMobject(stroke_color=color, stroke_width=stroke).set_points_as_corners(pts)

    def hline(self, v, color=DIM_TEXT, stroke=2, dashed=False):
        a, b = self.pt(0, v), self.pt(1, v)
        return DashedLine(a, b, color=color, stroke_width=stroke, dash_length=0.12) \
            if dashed else Line(a, b, color=color, stroke_width=stroke)

    def vline(self, u, color=DIM_TEXT, stroke=2, dashed=False):
        a, b = self.pt(u, 0), self.pt(u, 1)
        return DashedLine(a, b, color=color, stroke_width=stroke, dash_length=0.12) \
            if dashed else Line(a, b, color=color, stroke_width=stroke)

    def tick_labels(self, us, labels, size=17, color=DIM_TEXT, buff=0.12):
        g = VGroup()
        for u, lab in zip(us, labels):
            t = Text(lab, font_size=size, color=color)
            t.next_to(self.pt(u, 0), DOWN, buff=buff)
            g.add(t)
        return g


def wave_fn(freqs, amps, noise_amp=0.0, seed=3, base=0.5, gain=1.0):
    """A deterministic sum-of-tones (+ smooth pseudo-noise) in unit coordinates."""
    rng = np.random.default_rng(seed)
    ph = rng.uniform(0, TAU, len(freqs))
    nf = rng.uniform(28.0, 60.0, 7)
    npz = rng.uniform(0, TAU, 7)
    na = rng.uniform(0.5, 1.0, 7)
    na = na / na.sum()

    def f(u):
        v = sum(a * np.sin(TAU * fr * u + p) for fr, a, p in zip(freqs, amps, ph))
        if noise_amp:
            v += noise_amp * sum(a * np.sin(TAU * fr * u + p)
                                 for fr, a, p in zip(nf, na, npz))
        return base + gain * v
    return f


def peak_fn(peaks, floor=0.06, width=0.016, noise_amp=0.03, seed=5):
    """A spectrum: gaussian peaks on a noisy floor, in unit coordinates."""
    rng = np.random.default_rng(seed)
    nf = rng.uniform(40.0, 95.0, 9)
    npz = rng.uniform(0, TAU, 9)
    na = rng.uniform(0.4, 1.0, 9)
    na = na / na.sum()

    def f(u):
        v = floor + noise_amp * sum(a * np.sin(TAU * fr * u + p)
                                    for fr, a, p in zip(nf, na, npz))
        for pu, ph_, pw in peaks:
            v += ph_ * np.exp(-((u - pu) ** 2) / (2 * (pw or width) ** 2))
        return v
    return f


def road(x0=-6.6, x1=-0.5, y=-0.6, color=SUBTLE):
    line = Line([x0, y, 0], [x1, y, 0], stroke_color=color, stroke_width=4)
    dashes = VGroup(*[Line([x, y + 0.45, 0], [x + 0.34, y + 0.45, 0],
                           stroke_color=color, stroke_width=3)
                      for x in np.arange(x0 + 0.3, x1 - 0.3, 0.95)])
    return VGroup(line, dashes)


def beam_cone(apex, length=4.2, half_angle=0.16, color=TECH_CYAN, opacity=0.13):
    tip = np.array(apex, dtype=float)
    up = tip + np.array([length, length * np.tan(half_angle), 0])
    dn = tip + np.array([length, -length * np.tan(half_angle), 0])
    return Polygon(tip, up, dn, stroke_width=0, fill_color=color, fill_opacity=opacity)


# ============================ PART 1 : THE QUESTION ============================
class Part1(NarratedScene):
    def construct(self):
        lab_a = Text("WHAT YOU SEE", font_size=27, color=DIM_TEXT, weight=BOLD)
        lab_a.move_to([-3.55, 2.75, 0])
        lab_b = Text("WHAT THE RADAR SEES", font_size=27, color=AMBER, weight=BOLD)
        lab_b.move_to([3.55, 2.75, 0])

        rd = road(-6.75, -0.45, -0.75)
        ego = car(TECH_CYAN, 0.95).move_to([-6.0, -0.2, 0])
        sensor = dish(0.5, AMBER).move_to([-5.1, -0.3, 0])
        ahead = car(TEXT_WHITE, 0.95).move_to([-1.7, -0.2, 0])
        cone = beam_cone([-4.85, -0.3, 0], 3.0, 0.20, TECH_CYAN, 0.12)
        scene_a = VGroup(rd, ego, sensor, cone, ahead)
        tag_a = Text("a car, thirty metres ahead", font_size=22, color=DIM_TEXT)
        tag_a.move_to([-3.55, -1.85, 0])

        self.play(Create(rd), FadeIn(lab_a), run_time=1.2)
        self.play(FadeIn(ego, shift=RIGHT * 0.4), FadeIn(sensor), run_time=1.0)
        self.play(FadeIn(ahead, shift=LEFT * 0.4), run_time=0.9)
        self.play(FadeIn(cone), run_time=0.7)
        for _ in range(2):
            ping = Arc(radius=0.3, start_angle=-0.5, angle=1.0, color=AMBER,
                       stroke_width=5).move_arc_center_to([-4.9, -0.3, 0])
            self.add(ping)
            self.play(ping.animate.scale(7, about_point=np.array([-4.9, -0.3, 0]))
                      .set_stroke(opacity=0), run_time=1.1, rate_func=linear)
            self.remove(ping)
        self.play(FadeIn(tag_a), run_time=0.8)
        self.wait(1.0)

        ch = Chart(6.1, 2.35, fill_opacity=0.5)
        ch.move_to([3.55, -0.35, 0])
        raw = ch.poly(wave_fn([7, 13, 21], [0.16, 0.11, 0.08], 0.55, 4, 0.5, 1.0),
                      color=RADAR_GREEN, stroke=2.6)
        tag_b = Text("one voltage  ·  512 samples  ·  that is all",
                     font_size=22, color=DIM_TEXT)
        tag_b.move_to([3.55, -1.85, 0])

        self.play(FadeIn(lab_b), Create(ch.box), run_time=1.0)
        self.play(Create(raw), run_time=2.6)
        self.play(FadeIn(tag_b), run_time=0.8)
        self.wait(1.2)
        self.play(Indicate(ch.box, color=RADAR_GREEN, scale_factor=1.03), run_time=1.1)

        everything = VGroup(scene_a, lab_a, lab_b, tag_a, tag_b, ch, raw)
        self.play(FadeOut(everything), run_time=0.9)

        t1 = Text("WHAT DOES A RADAR", font_size=54, color=TEXT_WHITE, weight=BOLD)
        t2 = Text("ACTUALLY SEE?", font_size=72, color=TECH_CYAN, weight=BOLD)
        t1.move_to([0, 1.85, 0])
        t2.move_to([0, 0.85, 0])
        sub = Text("From Chirp to Detection", font_size=34, color=AMBER)
        sub.move_to([0, -0.15, 0])

        self.play(FadeIn(t1, shift=DOWN * 0.3), run_time=1.1)
        self.play(Write(t2), run_time=1.7)
        self.play(FadeIn(sub, shift=UP * 0.25), run_time=1.1)

        strip = chain(
            ["CHIRP", "ECHO", "MIXER", "RANGE FFT", "DOPPLER FFT", "ANGLE FFT",
             "CFAR", "TRACKS"],
            [TECH_CYAN, TECH_CYAN, AMBER, RADAR_GREEN, NEON_PINK, VIOLET,
             AMBER, RADAR_GREEN], size=18)
        fit_width(strip, 13.2)
        strip.move_to([0, -1.75, 0])
        for c in strip.chips:
            self.play(FadeIn(c, scale=0.85), run_time=0.30)
        self.play(Create(strip[1]), run_time=0.9)

        cap = caption("every one of those stages is coming up")
        self.play(FadeIn(cap), run_time=1.0)
        for c in strip.chips:
            self.play(Indicate(c, color=c[1].get_color(), scale_factor=1.14),
                      run_time=0.45)
        cap2 = caption("sixteen steps  ·  one wiggling voltage  ·  one detection")
        self.play(FadeOut(cap), FadeIn(cap2), run_time=1.0)
        self.play(Indicate(sub, color=AMBER, scale_factor=1.10), run_time=1.1)
        self.wait(0.8)
        self.fill()


# ============================ PART 2 : THE CHIRP ============================
class Part2(NarratedScene):
    def construct(self):
        h = head("THE CHIRP — A RULER MADE OF FREQUENCY")
        self.play(FadeIn(h[0]), Create(h[1]), run_time=1.1)

        ch = Chart(6.5, 2.6, "time  →", "frequency  →", label_size=19)
        ch.move_to([-3.25, 1.15, 0])
        self.play(Create(ch.box), FadeIn(ch.xlab), FadeIn(ch.ylab), run_time=1.2)

        ramp = Line(ch.pt(0.06, 0.12), ch.pt(0.94, 0.88),
                    stroke_color=TECH_CYAN, stroke_width=5)
        self.play(Create(ramp), run_time=2.2)

        marker = Dot(ch.pt(0.06, 0.12), radius=0.09, color=AMBER)
        self.add(marker)
        self.play(marker.animate.move_to(ch.pt(0.94, 0.88)), run_time=1.6,
                  rate_func=linear)
        self.play(FadeOut(marker), run_time=0.3)

        b_arrow = DoubleArrow(ch.pt(0.10, 0.12), ch.pt(0.10, 0.88), buff=0,
                              color=NEON_PINK, stroke_width=4,
                              max_tip_length_to_length_ratio=0.11)
        b_lab = Text("B = 1 GHz", font_size=22, color=NEON_PINK)
        b_lab.move_to(ch.pt(0.27, 0.76))
        t_arrow = DoubleArrow(ch.pt(0.06, 0.05), ch.pt(0.94, 0.05), buff=0,
                              color=RADAR_GREEN, stroke_width=4,
                              max_tip_length_to_length_ratio=0.035)
        t_lab = Text("T = 40 μs", font_size=22, color=RADAR_GREEN)
        t_lab.next_to(t_arrow, UP, buff=0.10).shift(RIGHT * 1.5)

        self.play(GrowFromCenter(b_arrow), FadeIn(b_lab), run_time=0.9)
        self.play(GrowFromCenter(t_arrow), FadeIn(t_lab), run_time=0.9)

        rows = VGroup(
            Text("start        f₀ = 77 GHz", font_size=25, color=TEXT_WHITE),
            Text("bandwidth  B = 1 GHz", font_size=25, color=NEON_PINK),
            Text("sweep         T = 40 μs", font_size=25, color=RADAR_GREEN),
            Text("slope     S = B/T = 25 MHz/μs", font_size=25, color=AMBER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.30)
        card = carded(rows, color=SUBTLE, buff=0.34, opacity=0.35)
        RCOL.sub(0.02, 0.60, 1.0, 1.0).fit(card, pad=0.10)

        for r in rows:
            self.play(FadeIn(r, shift=LEFT * 0.25), run_time=0.55)
        self.play(Create(card[0]), run_time=0.7)

        wch = Chart(12.4, 1.35, "the transmitted waveform  ·  frequency climbing the whole time",
                    label_size=20, fill_opacity=0.4)
        wch.move_to([0, -1.75, 0])
        sig = wch.poly(lambda u: 0.5 + 0.42 * np.sin(TAU * (5 + 34 * u) * u),
                       color=TECH_CYAN, stroke=2.4, n=900)
        self.play(Create(wch.box), FadeIn(wch.xlab), run_time=0.9)
        self.play(Create(sig), run_time=2.6)

        cap = caption("different frequency at every instant  →  a timestamp written onto the air")
        self.play(FadeIn(cap), run_time=1.2)
        self.play(Indicate(rows[3], color=AMBER, scale_factor=1.06), run_time=1.1)
        self.play(Flash(ch.pt(0.5, 0.5), color=TECH_CYAN, line_length=0.25,
                        num_lines=14, flash_radius=0.7), run_time=1.0)
        body = VGroup(ch, ramp, b_arrow, b_lab, t_arrow, t_lab, card, wch, sig)
        self.recap("WHY A RAMP?",
                   ["every instant carries its own frequency",
                    "so the echo comes back carrying a timestamp",
                    "and the transmitter never has to stop"],
                   color=TECH_CYAN, clear=body)
        self.fill()


# ============================ PART 3 : THE DELAYED ECHO ============================
class Part3(NarratedScene):
    def construct(self):
        h = head("THE ECHO IS THE SAME RAMP, DELAYED")
        self.play(FadeIn(h[0]), Create(h[1]), run_time=1.0)

        ch = Chart(7.0, 2.9, "time  →", "frequency  →", label_size=19)
        ch.move_to([-3.05, 0.95, 0])
        self.play(Create(ch.box), FadeIn(ch.xlab), FadeIn(ch.ylab), run_time=1.1)

        tx = Line(ch.pt(0.05, 0.10), ch.pt(0.80, 0.90),
                  stroke_color=TECH_CYAN, stroke_width=5)
        tx_lab = Text("TX  (transmitted)", font_size=22, color=TECH_CYAN)
        tx_lab.move_to(ch.pt(0.34, 0.72))
        self.play(Create(tx), FadeIn(tx_lab), run_time=1.4)

        rx = Line(ch.pt(0.20, 0.10), ch.pt(0.95, 0.90),
                  stroke_color=NEON_PINK, stroke_width=5, stroke_opacity=0.95)
        rx_lab = Text("RX  (the echo)", font_size=22, color=NEON_PINK)
        rx_lab.move_to(ch.pt(0.68, 0.24))
        ghost = tx.copy().set_stroke(NEON_PINK, opacity=0.5)
        self.add(ghost)
        self.play(Transform(ghost, rx), FadeIn(rx_lab), run_time=1.6)

        dt = DoubleArrow(ch.pt(0.05, 0.045), ch.pt(0.20, 0.045), buff=0,
                         color=AMBER, stroke_width=4,
                         max_tip_length_to_length_ratio=0.22)
        dt_lab = Text("Δt", font_size=24, color=AMBER)
        dt_lab.next_to(dt, UP, buff=0.06)
        self.play(GrowFromCenter(dt), FadeIn(dt_lab), run_time=0.9)

        mini_rd = Line([0.6, 1.55, 0], [6.6, 1.55, 0], stroke_color=SUBTLE, stroke_width=3)
        sens = dish(0.55, TECH_CYAN).move_to([1.15, 1.95, 0])
        tgt = car(TEXT_WHITE, 0.8).move_to([5.8, 2.0, 0])
        arrow_out = Arrow([1.75, 2.15, 0], [5.1, 2.15, 0], color=TECH_CYAN,
                          stroke_width=4, buff=0, max_tip_length_to_length_ratio=0.05)
        arrow_back = Arrow([5.1, 1.80, 0], [1.75, 1.80, 0], color=NEON_PINK,
                           stroke_width=4, buff=0, max_tip_length_to_length_ratio=0.05)
        r_lab = Text("R = 30 m", font_size=21, color=DIM_TEXT)
        r_lab.move_to([3.5, 1.25, 0])
        mini = VGroup(mini_rd, sens, tgt, arrow_out, arrow_back, r_lab)
        self.play(FadeIn(mini), run_time=1.2)

        f1 = Text("Δt = 2R / c", font_size=34, color=AMBER, weight=BOLD)
        f2 = Text("= 200 nanoseconds", font_size=27, color=TEXT_WHITE)
        fg = VGroup(f1, f2).arrange(DOWN, buff=0.20)
        fcard = carded(fg, color=AMBER, buff=0.30, opacity=0.10)
        fcard.move_to([3.5, -0.25, 0])
        self.play(FadeIn(fcard, shift=UP * 0.25), run_time=1.1)

        warn = VGroup(
            Text("timestamping that directly", font_size=24, color=DIM_TEXT),
            Text("would cost absurd hardware", font_size=24, color=DIM_TEXT),
            Text("so the radar never tries", font_size=25, color=NEON_PINK, weight=BOLD),
        ).arrange(DOWN, buff=0.18)
        warn.move_to([3.5, -1.95, 0])
        for w in warn:
            self.play(FadeIn(w, shift=UP * 0.15), run_time=0.75)

        self.play(Indicate(dt_lab, color=AMBER, scale_factor=1.4), run_time=1.0)

        photon = Dot([1.75, 2.15, 0], radius=0.10, color=AMBER)
        self.play(FadeIn(photon), run_time=0.4)
        self.play(photon.animate.move_to([5.1, 2.15, 0]), run_time=1.4, rate_func=linear)
        self.play(photon.animate.move_to([5.1, 1.80, 0]), run_time=0.3)
        self.play(photon.animate.move_to([1.75, 1.80, 0]), run_time=1.4, rate_func=linear)
        self.play(FadeOut(photon), Flash(np.array([1.75, 1.80, 0]), color=AMBER,
                                         line_length=0.2, num_lines=12), run_time=0.9)

        cap = caption("it measures a difference in frequency instead — same information")
        self.play(FadeIn(cap), run_time=1.2)
        body = VGroup(ch, tx, tx_lab, ghost, rx_lab, dt, dt_lab, mini, fcard, warn)
        self.recap("THE ECHO, SO FAR",
                   ["the same ramp, shifted right by Δt",
                    "Δt = 2R/c  —  200 ns for a car at 30 m",
                    "far too fast to stopwatch directly"],
                   color=NEON_PINK, clear=body)
        self.fill()


# ============================ PART 4 : THE MIXER ============================
class Part4(NarratedScene):
    def construct(self):
        h = head("THE MIXER TURNS DELAY INTO A TONE", color=AMBER)
        self.play(FadeIn(h[0]), Create(h[1]), run_time=1.0)

        ch = Chart(6.4, 2.7, "time  →", "frequency  →", label_size=19)
        ch.move_to([-3.35, 1.05, 0])
        tx = Line(ch.pt(0.05, 0.10), ch.pt(0.80, 0.90),
                  stroke_color=TECH_CYAN, stroke_width=5)
        rx = Line(ch.pt(0.20, 0.10), ch.pt(0.95, 0.90),
                  stroke_color=NEON_PINK, stroke_width=5)
        self.play(Create(ch.box), FadeIn(ch.xlab), FadeIn(ch.ylab), run_time=1.0)
        self.play(Create(tx), Create(rx), run_time=1.3)

        gaps = VGroup()
        for u in (0.34, 0.52, 0.70):
            v_hi = 0.10 + (u - 0.05) * (0.80 / 0.75)
            v_lo = 0.10 + (u - 0.20) * (0.80 / 0.75)
            gaps.add(DoubleArrow(ch.pt(u, v_lo), ch.pt(u, v_hi), buff=0,
                                 color=AMBER, stroke_width=3.5,
                                 max_tip_length_to_length_ratio=0.22))
        for g in gaps:
            self.play(GrowFromCenter(g), run_time=0.5)
        gap_lab = Text("the gap never changes", font_size=22, color=AMBER)
        gap_lab.next_to(ch.box, UP, buff=0.12)
        self.play(FadeIn(gap_lab), run_time=0.8)

        rxa = VGroup(Text("TX", font_size=20, color=TECH_CYAN).move_to(ch.pt(0.10, 0.34)),
                     Text("RX", font_size=20, color=NEON_PINK).move_to(ch.pt(0.26, 0.08)))
        mixer = Circle(radius=0.34, stroke_color=AMBER, stroke_width=4,
                       fill_color=PANEL_NAVY, fill_opacity=1).move_to([2.2, 1.85, 0])
        mx = Text("×", font_size=34, color=AMBER, weight=BOLD).move_to(mixer)
        lpf = chip("LOW-PASS", TECH_CYAN, 18).move_to([4.2, 1.85, 0])
        adc = chip("ADC", RADAR_GREEN, 18).move_to([6.05, 1.85, 0])
        in1 = Text("echo", font_size=19, color=NEON_PINK).move_to([0.75, 2.35, 0])
        in2 = Text("live chirp", font_size=19, color=TECH_CYAN).move_to([0.95, 1.35, 0])
        a1 = Arrow([1.35, 2.25, 0], [1.95, 2.00, 0], color=NEON_PINK, buff=0,
                   stroke_width=3.5, max_tip_length_to_length_ratio=0.22)
        a2 = Arrow([1.45, 1.45, 0], [1.95, 1.70, 0], color=TECH_CYAN, buff=0,
                   stroke_width=3.5, max_tip_length_to_length_ratio=0.22)
        a3 = Arrow(mixer.get_right(), lpf.get_left(), color=AMBER, buff=0.06,
                   stroke_width=3.5, max_tip_length_to_length_ratio=0.22)
        a4 = Arrow(lpf.get_right(), adc.get_left(), color=AMBER, buff=0.06,
                   stroke_width=3.5, max_tip_length_to_length_ratio=0.22)
        block = VGroup(mixer, mx, lpf, adc, in1, in2, a1, a2, a3, a4)
        self.play(FadeIn(block), run_time=1.3)

        f1 = Text("f_b  =  S · Δt  =  2 S R / c", font_size=33, color=AMBER, weight=BOLD)
        f2 = Text("R = 30 m   →   f_b = 5 MHz", font_size=27, color=TEXT_WHITE)
        fg = VGroup(f1, f2).arrange(DOWN, buff=0.22)
        fcard = carded(fg, color=AMBER, buff=0.30, opacity=0.10)
        fcard.move_to([3.4, -0.35, 0])
        self.play(FadeIn(fcard, shift=UP * 0.25), run_time=1.2)

        tone = Chart(6.2, 1.15, "the beat: one clean tone per target", label_size=20,
                     fill_opacity=0.4)
        tone.move_to([3.4, -2.05, 0])
        tsig = tone.poly(lambda u: 0.5 + 0.36 * np.sin(TAU * 9 * u),
                         color=RADAR_GREEN, stroke=2.6, n=500)
        self.play(Create(tone.box), FadeIn(tone.xlab), run_time=0.8)
        self.play(Create(tsig), run_time=1.6)

        cap = caption("range has become a frequency — and frequencies are easy")
        self.play(FadeIn(cap), FadeIn(rxa), run_time=1.1)
        self.play(Indicate(fcard, color=AMBER, scale_factor=1.05), run_time=1.1)
        self.play(Indicate(gaps, color=AMBER, scale_factor=1.1), run_time=1.0)

        rx2 = Line(ch.pt(0.34, 0.10), ch.pt(1.00, 0.80),
                   stroke_color=VIOLET, stroke_width=4)
        far = Text("a second target, further away", font_size=21, color=VIOLET)
        far.move_to(ch.pt(0.66, 0.13))
        self.play(Create(rx2), FadeIn(far), run_time=1.3)
        tsig2 = tone.poly(lambda u: 0.5 + 0.28 * np.sin(TAU * 17 * u),
                          color=VIOLET, stroke=2.4, n=700)
        self.play(Transform(tsig, tsig2), run_time=1.4)
        higher = Text("further  →  bigger gap  →  higher tone", font_size=22, color=VIOLET)
        higher.move_to([3.4, -1.05, 0])
        self.play(FadeIn(higher), run_time=1.0)

        body = VGroup(ch, tx, rx, rx2, gaps, gap_lab, rxa, far, block, fcard,
                      tone, tsig, higher)
        self.recap("THE MIXER",
                   ["multiply the echo by the chirp going out right now",
                    "two delayed ramps differ by a constant frequency",
                    "f_b = 2 S R / c  —  5 MHz for a car at 30 m"],
                   color=AMBER, clear=body)
        self.fill()


# ============================ PART 5 : THE RAW SAMPLES ============================
class Part5(NarratedScene):
    def construct(self):
        h = head("WHAT ACTUALLY LANDS IN MEMORY", color=RADAR_GREEN)
        self.play(FadeIn(h[0]), Create(h[1]), run_time=1.0)

        specs = [("guardrail  ·  8 m", 5, TECH_CYAN),
                 ("car  ·  30 m", 11, RADAR_GREEN),
                 ("sign  ·  45 m", 17, AMBER),
                 ("truck  ·  60 m", 23, NEON_PINK)]
        charts, labels, curves = VGroup(), VGroup(), VGroup()
        for i, (name, freq, col) in enumerate(specs):
            c = Chart(2.85, 0.95, fill_opacity=0.45)
            c.move_to([-5.05 + i * 3.37, 1.72, 0])
            lab = Text(name, font_size=19, color=col)
            lab.next_to(c.box, UP, buff=0.13)
            cur = c.poly(lambda u, f=freq: 0.5 + 0.34 * np.sin(TAU * f * u),
                         color=col, stroke=2.2, n=420)
            charts.add(c)
            labels.add(lab)
            curves.add(cur)

        for c, lab, cur in zip(charts, labels, curves):
            self.play(Create(c.box), FadeIn(lab), run_time=0.45)
            self.play(Create(cur), run_time=0.55)

        plus = Text("all of it arrives at once, summed, on a floor of thermal noise",
                    font_size=25, color=DIM_TEXT)
        plus.move_to([0, 0.62, 0])
        arrows = VGroup(*[Arrow([-5.05 + i * 3.37, 1.15, 0], [-5.05 + i * 3.37, 0.92, 0],
                                color=SUBTLE, buff=0, stroke_width=3,
                                max_tip_length_to_length_ratio=0.5) for i in range(4)])
        self.play(FadeIn(plus), *[GrowArrow(a) for a in arrows], run_time=1.1)

        big = Chart(12.4, 1.95, "one chirp  ·  512 samples  ·  this is the raw truth",
                    label_size=21, fill_opacity=0.5)
        big.move_to([0, -1.55, 0])
        raw = big.poly(wave_fn([5, 11, 17, 23], [0.10, 0.09, 0.07, 0.06], 0.42, 8,
                               0.5, 1.0), color=RADAR_GREEN, stroke=2.4, n=1100)
        self.play(Create(big.box), FadeIn(big.xlab), run_time=0.9)
        self.play(Create(raw), run_time=3.0)

        dots = VGroup(*[Dot(big.pt(u, 0.5 + 0.5 * 0.0), radius=0.032, color=TEXT_WHITE)
                        for u in np.linspace(0.02, 0.98, 60)])
        for d, u in zip(dots, np.linspace(0.02, 0.98, 60)):
            f = wave_fn([5, 11, 17, 23], [0.10, 0.09, 0.07, 0.06], 0.42, 8, 0.5, 1.0)
            d.move_to(big.pt(u, float(np.clip(f(u), 0.02, 0.98))))
        self.play(LaggedStart(*[FadeIn(d, scale=2) for d in dots], lag_ratio=0.02),
                  run_time=1.8)
        self.wait(0.6)
        self.play(FadeOut(dots), run_time=0.5)

        cap = caption("nowhere in that line can a human eye find a target")
        self.play(FadeIn(cap), run_time=1.2)
        self.play(Indicate(big.box, color=RADAR_GREEN, scale_factor=1.02), run_time=1.1)
        body = VGroup(charts, labels, curves, plus, arrows, big, raw)
        self.recap("ONE CHIRP, IN MEMORY",
                   ["a few hundred samples of a single voltage",
                    "every reflector in the beam, summed together",
                    "all of it sitting on thermal noise"],
                   color=RADAR_GREEN, clear=body)
        self.fill()


# ============================ PART 6 : THE RANGE FFT ============================
class Part6(NarratedScene):
    def construct(self):
        h = head("THE RANGE FFT", color=RADAR_GREEN)
        self.play(FadeIn(h[0]), Create(h[1]), run_time=1.0)

        tch = Chart(5.3, 2.1, "one chirp  ·  time", label_size=19)
        tch.move_to([-4.05, 1.45, 0])
        raw = tch.poly(wave_fn([5, 11, 23], [0.11, 0.10, 0.07], 0.40, 8, 0.5, 1.0),
                       color=RADAR_GREEN, stroke=2.3, n=800)
        self.play(Create(tch.box), FadeIn(tch.xlab), run_time=0.8)
        self.play(Create(raw), run_time=2.0)

        fft_box = chip("F F T", AMBER, 24).move_to([-0.35, 1.45, 0])
        a_in = Arrow([-1.32, 1.45, 0], [-0.95, 1.45, 0], color=AMBER, buff=0,
                     stroke_width=4, max_tip_length_to_length_ratio=0.4)
        a_out = Arrow([0.28, 1.45, 0], [0.72, 1.45, 0], color=AMBER, buff=0,
                      stroke_width=4, max_tip_length_to_length_ratio=0.4)
        self.play(FadeIn(fft_box, scale=0.8), GrowArrow(a_in), GrowArrow(a_out),
                  run_time=1.0)

        sch = Chart(5.3, 2.1, "range  →", label_size=19)
        sch.move_to([4.05, 1.45, 0])
        peaks = [(0.16, 0.62, 0.017), (0.44, 0.76, 0.017), (0.78, 0.40, 0.017)]
        spec = sch.poly(peak_fn(peaks), color=TECH_CYAN, stroke=2.8, n=900)
        self.play(Create(sch.box), FadeIn(sch.xlab), run_time=0.8)
        self.play(Create(spec), run_time=1.8)

        names = [("guardrail", 0.15, 0.62, TECH_CYAN, 0.24),
                 ("car", 0.44, 0.76, RADAR_GREEN, 0.18),
                 ("truck", 0.87, 0.40, NEON_PINK, 0.30)]
        tags = VGroup()
        for name, u, v, col, dv in names:
            t = Text(name, font_size=18, color=col)
            t.move_to(sch.pt(u, min(v + dv, 0.94)))
            tags.add(t)
            self.play(FadeIn(t, shift=DOWN * 0.12), run_time=0.55)

        bins = VGroup(*[Rectangle(width=0.42, height=0.34, stroke_color=SUBTLE,
                                  stroke_width=1.5, fill_color=PANEL_NAVY,
                                  fill_opacity=0.8).move_to([-6.3 + i * 0.44, -0.55, 0])
                        for i in range(29)])
        bin_lab = Text("range bins  —  one number per bin, every chirp",
                       font_size=21, color=DIM_TEXT)
        bin_lab.move_to([0, -1.15, 0])
        self.play(LaggedStart(*[FadeIn(b, scale=0.6) for b in bins], lag_ratio=0.02),
                  run_time=1.6)
        self.play(FadeIn(bin_lab), run_time=0.7)
        for idx, col in ((4, TECH_CYAN), (12, RADAR_GREEN), (22, NEON_PINK)):
            self.play(bins[idx].animate.set_fill(col, opacity=0.85), run_time=0.35)

        f1 = Text("ΔR  =  c / 2B  =  15 cm", font_size=34, color=AMBER, weight=BOLD)
        note = Text("bandwidth alone sets it — not power, not the antenna",
                    font_size=23, color=DIM_TEXT)
        fg = VGroup(f1, note).arrange(DOWN, buff=0.22)
        fcard = carded(fg, color=AMBER, buff=0.28, opacity=0.10)
        fcard.move_to([0, -2.25, 0])
        self.play(FadeIn(fcard, shift=UP * 0.2), run_time=1.1)
        self.wait(0.8)

        self.play(FadeOut(VGroup(tch, raw, fft_box, a_in, a_out, bins, bin_lab)),
                  run_time=0.8)
        demo = VGroup(sch, spec, tags)
        self.play(demo.animate.move_to([0, 1.35, 0]).scale(1.25), run_time=1.2)
        self.play(FadeOut(tags), run_time=0.4)

        narrow = sch.poly(peak_fn([(0.46, 0.74, 0.030)]), color=TECH_CYAN, stroke=2.8, n=900)
        wide = sch.poly(peak_fn([(0.435, 0.70, 0.012), (0.485, 0.66, 0.012)]),
                        color=RADAR_GREEN, stroke=2.8, n=900)
        cmp1 = Text("two cars, 10 cm apart  ·  B = 1 GHz  →  one blob",
                    font_size=24, color=TECH_CYAN)
        cmp1.move_to([0, -0.75, 0])
        cmp2 = Text("sweep B = 4 GHz  →  ΔR = 3.75 cm  →  two targets",
                    font_size=24, color=RADAR_GREEN)
        cmp2.move_to([0, -0.75, 0])
        self.play(Transform(spec, narrow), FadeIn(cmp1), run_time=1.3)
        self.wait(1.0)
        self.play(Transform(spec, wide), FadeOut(cmp1), FadeIn(cmp2), run_time=1.4)
        self.wait(0.9)

        punch = VGroup(
            Text("a brutally hard timing problem", font_size=28, color=TEXT_WHITE),
            Text("became an easy frequency problem", font_size=28, color=AMBER, weight=BOLD),
        ).arrange(DOWN, buff=0.20)
        punch.move_to([0, -2.25, 0])
        self.play(FadeOut(fcard), run_time=0.5)
        self.play(FadeIn(punch[0], shift=UP * 0.2), run_time=1.0)
        self.play(FadeIn(punch[1], shift=UP * 0.2), run_time=1.0)
        self.wait(0.8)
        self.play(Indicate(punch[1], color=AMBER, scale_factor=1.06), run_time=1.1)
        self.wait(0.9)
        self.play(FadeOut(VGroup(demo, punch, cmp2)), run_time=0.8)
        self.recap("THE FIRST FFT",
                   ["beat frequency axis  =  range axis",
                    "ΔR = c / 2B  —  bandwidth alone decides"],
                   color=RADAR_GREEN)
        self.fill()


# ============================ PART 7 : A PEAK IS NOT A SIZE ============================
class Part7(NarratedScene):
    def construct(self):
        h = head("A TALL PEAK IS NOT A BIG OBJECT", color=NEON_PINK)
        self.play(FadeIn(h[0]), Create(h[1]), run_time=1.0)

        ch = Chart(5.6, 2.5, "range  →", "received power", label_size=19)
        ch.move_to([-3.55, 1.15, 0])
        curve = ch.poly(lambda u: 0.06 + 0.92 / (1 + 26 * (u + 0.06) ** 4),
                        color=NEON_PINK, stroke=4, n=500)
        self.play(Create(ch.box), FadeIn(ch.xlab), FadeIn(ch.ylab), run_time=1.0)
        self.play(Create(curve), run_time=1.8)

        law = Text("P  ∝  1 / R⁴", font_size=30, color=NEON_PINK, weight=BOLD)
        law.move_to(ch.pt(0.68, 0.72))
        self.play(FadeIn(law), run_time=0.8)

        m1 = Dot(ch.pt(0.24, 0.06 + 0.92 / (1 + 26 * 0.30 ** 4)), radius=0.09, color=AMBER)
        m2 = Dot(ch.pt(0.54, 0.06 + 0.92 / (1 + 26 * 0.60 ** 4)), radius=0.09, color=AMBER)
        d1 = Text("R", font_size=20, color=AMBER).next_to(m1, DOWN, buff=0.16)
        d2 = Text("2R", font_size=20, color=AMBER).next_to(m2, UP, buff=0.16)
        self.play(FadeIn(m1), FadeIn(d1), run_time=0.6)
        self.play(FadeIn(m2), FadeIn(d2), run_time=0.6)
        ratio = Text("double the range  →  1/16 of the echo", font_size=22, color=AMBER)
        ratio.next_to(ch.box, DOWN, buff=0.55)
        self.play(FadeIn(ratio), run_time=0.9)

        title_r = Text("RADAR CROSS SECTION", font_size=24, color=VIOLET, weight=BOLD)
        title_r.move_to([3.5, 2.55, 0])
        rows = [("truck tailgate, square on", 0.98, NEON_PINK),
                ("car", 0.52, RADAR_GREEN),
                ("motorcycle", 0.30, TECH_CYAN),
                ("pedestrian", 0.12, AMBER)]
        bars = VGroup()
        for i, (name, frac, col) in enumerate(rows):
            y = 1.85 - i * 0.78
            lab = Text(name, font_size=20, color=col)
            lab.move_to([0.55, y + 0.30, 0], aligned_edge=LEFT)
            bar = Rectangle(width=max(frac * 5.9, 0.12), height=0.30,
                            stroke_width=0, fill_color=col, fill_opacity=0.85)
            bar.move_to([0.55, y - 0.06, 0], aligned_edge=LEFT)
            bars.add(VGroup(lab, bar))
        self.play(FadeIn(title_r), run_time=0.7)
        for b in bars:
            self.play(FadeIn(b[0]), GrowFromEdge(b[1], LEFT), run_time=0.75)

        note = Text("geometry and material — not how big it looks",
                    font_size=21, color=DIM_TEXT)
        note.move_to([3.5, -1.55, 0])
        self.play(FadeIn(note), run_time=0.9)

        cap = caption("a tall peak means a strong reflector, somewhere — nothing more")
        self.play(FadeIn(cap), run_time=1.2)
        self.wait(0.8)
        self.play(Indicate(bars[0][1], color=NEON_PINK, scale_factor=1.05),
                  Indicate(bars[3][1], color=AMBER, scale_factor=1.35), run_time=1.2)
        self.wait(0.6)
        self.play(Indicate(law, color=NEON_PINK, scale_factor=1.12), run_time=1.1)
        body = VGroup(ch, curve, law, m1, m2, d1, d2, ratio, title_r, bars, note)
        self.recap("READING A PEAK",
                   ["received power falls as 1 / R⁴",
                    "cross section is geometry, not size",
                    "amplitude tells you almost nothing on its own"],
                   color=NEON_PINK, clear=body)
        self.fill()


# ============================ PART 8 : THE FRAME & SLOW TIME ============================
class Part8(NarratedScene):
    def construct(self):
        h = head("ONE CHIRP IS NOT ENOUGH", color=TECH_CYAN)
        self.play(FadeIn(h[0]), Create(h[1]), run_time=1.0)

        ch = Chart(12.4, 1.7, "128 chirps, back to back  ·  40 μs apart  ·  one frame = 5.12 ms",
                   label_size=21, fill_opacity=0.45)
        ch.move_to([0, 1.75, 0])
        self.play(Create(ch.box), FadeIn(ch.xlab), run_time=0.9)

        ramps = VGroup()
        n = 11
        for k in range(n):
            u0 = 0.02 + k * (0.96 / n)
            u1 = u0 + (0.96 / n) * 0.82
            ramps.add(Line(ch.pt(u0, 0.14), ch.pt(u1, 0.86),
                           stroke_color=TECH_CYAN, stroke_width=3.5))
        self.play(LaggedStart(*[Create(r) for r in ramps], lag_ratio=0.35), run_time=2.6)
        brace = DoubleArrow(ch.pt(0.02, 0.04), ch.pt(0.98, 0.04), buff=0,
                            color=RADAR_GREEN, stroke_width=3.5,
                            max_tip_length_to_length_ratio=0.03)
        self.play(GrowFromCenter(brace), run_time=0.9)

        zoom = Chart(5.9, 2.0, "the target barely moves between chirps", label_size=19)
        zoom.move_to([-3.5, -0.85, 0])
        self.play(Create(zoom.box), FadeIn(zoom.xlab), run_time=0.8)
        tgt = car(TEXT_WHITE, 0.7).move_to(zoom.pt(0.30, 0.62))
        self.play(FadeIn(tgt), run_time=0.6)
        ghost1 = tgt.copy().set_opacity(0.35).shift(RIGHT * 0.5)
        ghost2 = tgt.copy().set_opacity(0.2).shift(RIGHT * 1.0)
        self.play(FadeIn(ghost1), FadeIn(ghost2), run_time=0.8)
        nums = VGroup(
            Text("v = 20 m/s ,  T = 40 μs", font_size=22, color=TEXT_WHITE),
            Text("Δd = v·T = 0.8 mm", font_size=24, color=AMBER, weight=BOLD),
        ).arrange(DOWN, buff=0.18)
        nums.move_to(zoom.pt(0.52, 0.20))
        self.play(FadeIn(nums), run_time=0.9)

        lam = Text("λ = 3.9 mm at 77 GHz", font_size=26, color=NEON_PINK, weight=BOLD)
        lam.move_to([3.5, 0.35, 0])
        self.play(FadeIn(lam, shift=UP * 0.2), run_time=0.9)

        phasors = VGroup()
        for i in range(5):
            c = Circle(radius=0.42, stroke_color=SUBTLE, stroke_width=2)
            ang = -i * 0.86
            arr = Line(ORIGIN, 0.42 * np.array([np.cos(ang), np.sin(ang), 0]),
                       stroke_color=TECH_CYAN, stroke_width=4)
            g = VGroup(c, arr).move_to([1.35 + i * 1.12, -1.25, 0])
            phasors.add(g)
        ph_lab = Text("phase of the peak, chirp by chirp", font_size=21, color=DIM_TEXT)
        ph_lab.move_to([3.5, -0.45, 0])
        self.play(FadeIn(ph_lab), run_time=0.7)
        for p in phasors:
            self.play(FadeIn(p, scale=0.7), run_time=0.35)

        dphi = Text("Δφ = 4π Δd / λ ≈ 2.6 rad", font_size=25, color=AMBER, weight=BOLD)
        dphi.move_to([3.5, -2.25, 0])
        self.play(FadeIn(dphi, shift=UP * 0.2), run_time=1.0)

        cap = caption("far too small to change range bins — enormous in phase")
        self.play(FadeIn(cap), run_time=1.2)
        self.play(Indicate(dphi, color=AMBER, scale_factor=1.08), run_time=1.1)
        body = VGroup(ch, ramps, brace, zoom, tgt, ghost1, ghost2, nums, lam,
                      ph_lab, phasors, dphi)
        self.recap("ONE FRAME",
                   ["128 chirps, 40 μs apart, 5.12 ms in total",
                    "the target moves 0.8 mm between chirps",
                    "invisible in range — obvious in phase"],
                   color=TECH_CYAN, clear=body)
        self.fill()


# ============================ PART 9 : THE DOPPLER FFT ============================
class Part9(NarratedScene):
    def construct(self):
        h = head("THE SECOND FFT — ACROSS CHIRPS", color=NEON_PINK)
        self.play(FadeIn(h[0]), Create(h[1]), run_time=1.0)

        pch = Chart(5.3, 2.3, "chirp number  (slow time)", label_size=19)
        pch.move_to([-4.05, 1.35, 0])
        self.play(Create(pch.box), FadeIn(pch.xlab), run_time=0.9)
        dots = VGroup(*[Dot(pch.pt(u, 0.5 + 0.38 * np.sin(TAU * 3.2 * u + 0.4)),
                            radius=0.045, color=NEON_PINK)
                        for u in np.linspace(0.04, 0.96, 34)])
        self.play(LaggedStart(*[FadeIn(d, scale=2) for d in dots], lag_ratio=0.05),
                  run_time=2.0)
        sine = pch.poly(lambda u: 0.5 + 0.38 * np.sin(TAU * 3.2 * u + 0.4),
                        color=NEON_PINK, stroke=2.4, n=600)
        self.play(Create(sine), run_time=1.4)
        phase_lab = Text("the phase of one range bin", font_size=20, color=DIM_TEXT)
        phase_lab.next_to(pch.box, UP, buff=0.14)
        self.play(FadeIn(phase_lab), run_time=0.8)

        fft_box = chip("F F T", AMBER, 24).move_to([-0.35, 1.35, 0])
        a_in = Arrow([-1.32, 1.35, 0], [-0.95, 1.35, 0], color=AMBER, buff=0,
                     stroke_width=4, max_tip_length_to_length_ratio=0.4)
        a_out = Arrow([0.28, 1.35, 0], [0.72, 1.35, 0], color=AMBER, buff=0,
                      stroke_width=4, max_tip_length_to_length_ratio=0.4)
        self.play(FadeIn(fft_box, scale=0.8), GrowArrow(a_in), GrowArrow(a_out),
                  run_time=1.0)

        dch = Chart(5.3, 2.3, "velocity  →", label_size=19)
        dch.move_to([4.05, 1.35, 0])
        spec = dch.poly(peak_fn([(0.72, 0.72, 0.018)]), color=RADAR_GREEN,
                        stroke=2.8, n=800)
        ticks = dch.tick_labels([0.06, 0.5, 0.94], ["−24 m/s", "0", "+24 m/s"], size=16)
        dch.xlab.next_to(ticks, DOWN, buff=0.10)
        self.play(Create(dch.box), FadeIn(dch.xlab), run_time=0.8)
        self.play(Create(spec), FadeIn(ticks), run_time=1.6)
        tag = Text("+20 m/s", font_size=19, color=RADAR_GREEN)
        tag.move_to(dch.pt(0.72, 0.90))
        self.play(FadeIn(tag), run_time=0.7)

        f1 = Text("v  =  λ · f_d / 2", font_size=32, color=AMBER, weight=BOLD)
        f2 = Text("Δv  =  λ / 2·T_frame  ≈  0.4 m/s", font_size=25, color=TEXT_WHITE)
        f3 = Text("stare longer  →  finer velocity resolution", font_size=22, color=DIM_TEXT)
        fg = VGroup(f1, f2, f3).arrange(DOWN, buff=0.22)
        fcard = carded(fg, color=AMBER, buff=0.32, opacity=0.10)
        fcard.move_to([0, -1.55, 0])
        self.play(FadeIn(fcard, shift=UP * 0.2), run_time=1.2)

        cap = caption("a steady rotation is a frequency — and a frequency is a speed")
        self.play(FadeIn(cap), run_time=1.2)
        self.play(Indicate(fcard, color=AMBER, scale_factor=1.04), run_time=1.1)
        body = VGroup(pch, dots, sine, phase_lab, fft_box, a_in, a_out,
                      dch, spec, ticks, tag, fcard)
        self.recap("THE SECOND FFT",
                   ["fast time → range, slow time → velocity",
                    "the frame length fixes the velocity resolution",
                    "the axis wraps beyond λ · PRF / 4"],
                   color=NEON_PINK, clear=body)
        self.fill()


# ============================ PART 10 : THE RANGE-DOPPLER MAP ============================
class Part10(NarratedScene):
    def construct(self):
        h = head("THE RANGE-DOPPLER MAP", color=AMBER)
        self.play(FadeIn(h[0]), Create(h[1]), run_time=1.0)

        nx, ny = 22, 13
        cw = 0.30
        ox, oy = -3.00, -0.15
        blobs = [(0.72, 0.74, RADAR_GREEN), (0.24, 0.36, TECH_CYAN)]
        cells = VGroup()
        rng = np.random.default_rng(7)
        for i in range(nx):
            for j in range(ny):
                u, v = (i + 0.5) / nx, (j + 0.5) / ny
                val = 0.05 + 0.10 * rng.random()
                col = PANEL_NAVY
                for bu, bv, bc in blobs:
                    g = np.exp(-(((u - bu) / 0.05) ** 2 + ((v - bv) / 0.09) ** 2))
                    if g > val:
                        val, col = g, bc
                if abs(u - 0.5) < 0.03:
                    val, col = max(val, 0.55 + 0.35 * rng.random()), NEON_PINK
                cells.add(Square(side_length=cw, stroke_width=0.6,
                                 stroke_color=SUBTLE,
                                 fill_color=col if val > 0.16 else PANEL_NAVY,
                                 fill_opacity=float(np.clip(val, 0.10, 0.95)))
                          .move_to([ox + (i - nx / 2 + 0.5) * cw,
                                    oy + (j - ny / 2 + 0.5) * cw, 0]))
        frame_box = Rectangle(width=nx * cw, height=ny * cw, stroke_color=SUBTLE,
                              stroke_width=2).move_to([ox, oy, 0])
        xlab = Text("velocity  →", font_size=20, color=NEON_PINK)
        xlab.next_to(frame_box, DOWN, buff=0.16)
        ylab = Text("range  →", font_size=20, color=TECH_CYAN)
        ylab.rotate(PI / 2).next_to(frame_box, LEFT, buff=0.16)

        self.play(FadeIn(cells, lag_ratio=0.004), Create(frame_box), run_time=2.4)
        self.play(FadeIn(xlab), FadeIn(ylab), run_time=0.9)

        tags = VGroup(
            Text("closing, far", font_size=18, color=RADAR_GREEN),
            Text("opening, near", font_size=18, color=TECH_CYAN),
            Text("everything stationary", font_size=18, color=NEON_PINK),
        )
        tags[0].move_to([ox + (0.72 - 0.5) * nx * cw, oy + (0.74 - 0.5) * ny * cw + 0.72, 0])
        tags[1].move_to([ox + (0.24 - 0.5) * nx * cw, oy + (0.36 - 0.5) * ny * cw - 0.70, 0])
        tags[2].move_to([ox, oy + ny * cw / 2 + 0.30, 0])
        for t in tags:
            self.play(FadeIn(t, shift=UP * 0.1), run_time=0.7)

        readout = VGroup(
            Text("HOW TO READ IT", font_size=26, color=AMBER, weight=BOLD),
            Text("down       →  range", font_size=23, color=TECH_CYAN),
            Text("across     →  velocity", font_size=23, color=NEON_PINK),
            Text("brightness →  echo strength", font_size=23, color=TEXT_WHITE),
            Text("middle column  →  clutter", font_size=23, color=DIM_TEXT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        rcard = carded(readout, color=SUBTLE, buff=0.34, opacity=0.35)
        rcard.move_to([4.05, 0.05, 0])
        self.play(FadeIn(rcard[0]), FadeIn(readout[0]), run_time=0.9)
        for r in readout[1:]:
            self.play(FadeIn(r, shift=LEFT * 0.2), run_time=0.7)

        cap = caption("one picture — and the scene is already half interpreted")
        self.play(FadeIn(cap), run_time=1.2)
        self.play(Indicate(tags[2], color=NEON_PINK, scale_factor=1.15), run_time=1.1)
        self.play(Indicate(tags[0], color=RADAR_GREEN, scale_factor=1.15), run_time=1.1)
        body = VGroup(cells, frame_box, xlab, ylab, tags, rcard)
        self.recap("READING THE MAP",
                   ["range down the side, velocity across",
                    "brightness is echo strength, not size",
                    "the middle column is the world standing still"],
                   color=AMBER, clear=body)
        self.fill()


# ============================ PART 11 : THE ANGLE FFT ============================
class Part11(NarratedScene):
    def construct(self):
        h = head("WHICH DIRECTION DID IT COME FROM?", color=VIOLET)
        self.play(FadeIn(h[0]), Create(h[1]), run_time=1.0)

        base_y = -0.35
        ants = VGroup(*[VGroup(
            Line([x, base_y, 0], [x, base_y + 0.42, 0], stroke_color=TECH_CYAN,
                 stroke_width=4),
            Dot([x, base_y + 0.42, 0], radius=0.08, color=TECH_CYAN))
            for x in (-5.6, -4.6, -3.6, -2.6)])
        board = Line([-6.1, base_y, 0], [-2.1, base_y, 0], stroke_color=SUBTLE,
                     stroke_width=5)
        rx_lab = Text("four receiving antennas", font_size=20, color=TECH_CYAN)
        rx_lab.move_to([-4.1, base_y - 0.42, 0])
        self.play(Create(board), FadeIn(ants), FadeIn(rx_lab), run_time=1.4)

        fronts = VGroup(*[Line([-6.4 + k * 0.62, base_y + 2.55, 0],
                               [-4.5 + k * 0.62, base_y + 0.55, 0],
                               stroke_color=VIOLET, stroke_width=3, stroke_opacity=0.8)
                          for k in range(6)])
        self.play(LaggedStart(*[Create(f) for f in fronts], lag_ratio=0.18),
                  run_time=1.8)
        theta = Text("θ", font_size=26, color=AMBER)
        theta.move_to([-3.15, base_y + 1.05, 0])
        self.play(FadeIn(theta), run_time=0.7)

        extra = Line([-4.6, base_y + 0.42, 0], [-4.14, base_y + 0.06, 0],
                     stroke_color=AMBER, stroke_width=5)
        d_lab = Text("d", font_size=20, color=DIM_TEXT)
        d_lab.move_to([-5.1, base_y + 0.68, 0])
        extra_lab = Text("extra path  =  d · sin θ", font_size=21, color=AMBER)
        extra_lab.move_to([-4.0, base_y - 0.95, 0])
        self.play(Create(extra), FadeIn(d_lab), FadeIn(extra_lab), run_time=1.2)

        f1 = Text("ψ  =  2π · d · sin θ / λ", font_size=30, color=AMBER, weight=BOLD)
        f2 = Text("a constant phase step, element to element", font_size=21,
                  color=DIM_TEXT)
        fg = VGroup(f1, f2).arrange(DOWN, buff=0.20)
        fcard = carded(fg, color=AMBER, buff=0.30, opacity=0.10)
        fcard.move_to([2.95, 2.05, 0])
        self.play(FadeIn(fcard, shift=DOWN * 0.2), run_time=1.1)

        steps = VGroup(*[Text(t, font_size=22, color=VIOLET)
                         for t in ("0", "ψ", "2ψ", "3ψ")])
        for st, x in zip(steps, (-5.6, -4.6, -3.6, -2.6)):
            st.move_to([x, base_y + 0.78, 0])
        self.play(LaggedStart(*[FadeIn(s, scale=0.6) for s in steps], lag_ratio=0.25),
                  run_time=1.2)

        ach = Chart(5.4, 1.9, "angle  →", label_size=19)
        ach.move_to([3.05, -0.15, 0])
        aspec = ach.poly(peak_fn([(0.63, 0.70, 0.030)]), color=VIOLET, stroke=2.8, n=700)
        aticks = ach.tick_labels([0.08, 0.5, 0.92], ["−60°", "0°", "+60°"], size=16)
        ach.xlab.next_to(aticks, DOWN, buff=0.10)
        fft_lab = Text("a third FFT — this time across antennas", font_size=21,
                       color=DIM_TEXT)
        fft_lab.next_to(ach.box, UP, buff=0.14)
        self.play(Create(ach.box), FadeIn(ach.xlab), FadeIn(fft_lab), run_time=0.9)
        self.play(Create(aspec), FadeIn(aticks), run_time=1.4)

        mimo = VGroup(
            Text("MIMO:  2 TX × 4 RX", font_size=24, color=RADAR_GREEN, weight=BOLD),
            Text("= 8 virtual elements from 6 real ones", font_size=21, color=DIM_TEXT),
        ).arrange(DOWN, buff=0.16)
        mimo.move_to([3.05, -2.15, 0])
        self.play(FadeIn(mimo, shift=UP * 0.2), run_time=1.1)

        cap = caption("phase across space  →  angle, exactly as phase across time gave speed")
        self.play(FadeIn(cap), run_time=1.3)
        self.play(Indicate(fcard, color=AMBER, scale_factor=1.04), run_time=1.1)
        body = VGroup(board, ants, rx_lab, fronts, theta, extra, d_lab, extra_lab,
                      fcard, steps, ach, aspec, aticks, fft_lab, mimo)
        self.recap("THE THIRD FFT",
                   ["phase across antennas becomes direction",
                    "more elements → a sharper angle",
                    "MIMO synthesises elements that are not there"],
                   color=VIOLET, clear=body)
        self.fill()


# ============================ PART 12 : THE CUBE ============================
class Part12(NarratedScene):
    def construct(self):
        h = head("WHAT THE RADAR ACTUALLY HOLDS", color=TECH_CYAN)
        self.play(FadeIn(h[0]), Create(h[1]), run_time=1.0)

        # an isometric stack of slices: range x velocity, repeated along angle
        skew = np.array([0.42, 0.30, 0])
        slices = VGroup()
        rng = np.random.default_rng(21)
        for k in range(4):
            off = skew * k + np.array([-3.9, -0.35, 0])
            face = Rectangle(width=4.0, height=2.6, stroke_color=TECH_CYAN,
                             stroke_width=2.5, fill_color=PANEL_NAVY,
                             fill_opacity=0.85 if k == 0 else 0.7).move_to(off)
            grid = VGroup()
            for i in range(10):
                for j in range(7):
                    val = 0.05 + 0.12 * rng.random()
                    bright = rng.random() > 0.94
                    grid.add(Square(side_length=0.32, stroke_width=0.4,
                                    stroke_color=SUBTLE,
                                    fill_color=AMBER if bright else TECH_CYAN,
                                    fill_opacity=0.85 if bright else val)
                             .move_to(off + RIGHT * (i - 4.5) * 0.38
                                      + UP * (j - 3) * 0.36))
            slices.add(VGroup(face, grid))
        self.play(LaggedStart(*[FadeIn(s, shift=LEFT * 0.3) for s in slices],
                              lag_ratio=0.3), run_time=2.6)

        ax1 = Text("range", font_size=20, color=TECH_CYAN)
        ax1.rotate(PI / 2).move_to([-6.25, -0.35, 0])
        ax2 = Text("velocity", font_size=20, color=NEON_PINK)
        ax2.move_to([-3.9, -1.95, 0])
        ax3 = Text("angle", font_size=20, color=VIOLET)
        ax3.move_to([-1.35, 1.65, 0])
        self.play(FadeIn(ax1), FadeIn(ax2), FadeIn(ax3), run_time=1.0)

        nums = VGroup(
            Text("256 range bins", font_size=24, color=TECH_CYAN),
            Text("×  128 Doppler bins", font_size=24, color=NEON_PINK),
            Text("×  8 angle bins", font_size=24, color=VIOLET),
            Text("≈  262 000 complex numbers", font_size=26, color=AMBER, weight=BOLD),
            Text("rebuilt 20 times a second", font_size=22, color=DIM_TEXT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        ncard = carded(nums, color=SUBTLE, buff=0.34, opacity=0.35)
        ncard.move_to([3.75, 0.55, 0])
        self.play(FadeIn(ncard[0]), run_time=0.7)
        for n in nums:
            self.play(FadeIn(n, shift=LEFT * 0.2), run_time=0.65)

        cap = caption("a radar does not see objects — it sees a cube of energy")
        self.play(FadeIn(cap), run_time=1.3)
        self.play(Indicate(nums[3], color=AMBER, scale_factor=1.06), run_time=1.1)

        body = VGroup(slices, ax1, ax2, ax3, ncard)
        self.recap("NOTHING IN IT IS LABELLED",
                   ["no edges, no objects, no meaning",
                    "most cells hold nothing but noise",
                    "a few hold the sum of everything at one range,",
                    "one speed and one direction"],
                   color=TECH_CYAN, clear=body, hold=0.8)
        self.fill()


def floor_fn(extra=(), boost=0.0):
    """Clutter-plus-noise floor falling away with range, plus optional peaks."""
    base = peak_fn(list(extra), floor=0.10, noise_amp=0.05, seed=13)

    def f(u):
        return base(u) + 0.62 * np.exp(-5.2 * u) + boost
    return f


# ============================ PART 13 : NOISE AND CLUTTER ============================
class Part13(NarratedScene):
    def construct(self):
        h = head("NOISE — AND THE REAL ENEMY, CLUTTER", color=NEON_PINK)
        self.play(FadeIn(h[0]), Create(h[1]), run_time=1.0)

        ch = Chart(7.8, 3.0, "range  →", "power", label_size=19)
        ch.move_to([-2.65, 0.75, 0])
        self.play(Create(ch.box), FadeIn(ch.xlab), FadeIn(ch.ylab), run_time=1.0)

        targets = [(0.12, 0.26, 0.011), (0.20, 0.22, 0.010),
                   (0.47, 0.34, 0.012), (0.83, 0.13, 0.012)]
        curve = ch.poly(floor_fn(targets), color=TECH_CYAN, stroke=2.6, n=900)
        self.play(Create(curve), run_time=2.2)
        floor_lab = Text("clutter + thermal noise", font_size=20, color=TECH_CYAN)
        floor_lab.move_to(ch.pt(0.30, 0.86))
        self.play(FadeIn(floor_lab), run_time=0.8)

        thr = ch.hline(0.42, color=AMBER, stroke=3, dashed=True)
        thr_lab = Text("one fixed threshold", font_size=20, color=AMBER)
        thr_lab.move_to(ch.pt(0.78, 0.52))
        self.play(Create(thr), FadeIn(thr_lab), run_time=1.1)

        fa = VGroup(*[Circle(radius=0.20, stroke_color=NEON_PINK, stroke_width=3)
                      .move_to(ch.pt(u, 0.62)) for u in (0.10, 0.19)])
        fa_lab = Text("false alarms", font_size=20, color=NEON_PINK)
        fa_lab.move_to(ch.pt(0.15, 0.20))
        self.play(Create(fa), FadeIn(fa_lab), run_time=1.1)

        miss = Circle(radius=0.22, stroke_color=RADAR_GREEN, stroke_width=3)
        miss.move_to(ch.pt(0.83, 0.16))
        miss_lab = Text("the target you needed", font_size=20, color=RADAR_GREEN)
        miss_lab.move_to(ch.pt(0.74, 0.30))
        self.play(Create(miss), FadeIn(miss_lab), run_time=1.1)

        side = VGroup(
            Text("THE FLOOR", font_size=25, color=AMBER, weight=BOLD),
            bullet("thermal noise:  k T B · F", TEXT_WHITE, 22, AMBER),
            bullet("the road surface", TEXT_WHITE, 22, AMBER),
            bullet("guardrails and signs", TEXT_WHITE, 22, AMBER),
            bullet("rain, spray, manhole covers", TEXT_WHITE, 22, AMBER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.30)
        card = carded(side, color=SUBTLE, buff=0.32, opacity=0.35)
        Zone(1.55, -0.35, 6.95, 2.82).fit(card, pad=0.12)
        self.play(FadeIn(card[0]), FadeIn(side[0]), run_time=0.8)
        for b in side[1:]:
            self.play(FadeIn(b, shift=LEFT * 0.2), run_time=0.7)

        snr = VGroup(
            Text("what matters is never raw power", font_size=24, color=TEXT_WHITE),
            Text("SNR  —  height above the local floor", font_size=26, color=RADAR_GREEN,
                 weight=BOLD),
        ).arrange(DOWN, buff=0.20)
        scard = carded(snr, color=RADAR_GREEN, buff=0.30, opacity=0.10)
        Zone(1.55, -3.02, 6.95, -0.60).fit(scard, pad=0.12)
        self.play(FadeIn(scard, shift=UP * 0.2), run_time=1.2)

        cap = caption("one number cannot be right at 10 metres and at 200")
        self.play(FadeIn(cap), run_time=1.3)
        self.play(Indicate(fa, color=NEON_PINK, scale_factor=1.2),
                  Indicate(miss, color=RADAR_GREEN, scale_factor=1.2), run_time=1.2)
        body = VGroup(ch, curve, floor_lab, thr, thr_lab, fa, fa_lab, miss,
                      miss_lab, card, scard)
        self.recap("WHY ONE THRESHOLD FAILS",
                   ["the floor itself falls away with range",
                    "close in: false alarms  ·  far out: missed targets",
                    "so the threshold has to move"],
                   color=NEON_PINK, clear=body)
        self.fill()


# ============================ PART 14 : CFAR ============================
class Part14(NarratedScene):
    def construct(self):
        h = head("CFAR — A THRESHOLD THAT BREATHES", color=RADAR_GREEN)
        self.play(FadeIn(h[0]), Create(h[1]), run_time=1.0)

        n = 15
        cw = 0.40
        cells = VGroup()
        for i in range(n):
            k = i - n // 2
            if k == 0:
                col = AMBER
            elif abs(k) <= 2:
                col = NEON_PINK
            else:
                col = TECH_CYAN
            cells.add(Square(side_length=cw, stroke_color=col, stroke_width=2,
                             fill_color=col, fill_opacity=0.22)
                      .move_to([-3.6 + k * (cw + 0.04), 1.85, 0]))
        self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in cells], lag_ratio=0.05),
                  run_time=1.6)

        legend = VGroup(
            bullet("cell under test", AMBER, 22, AMBER, dot="■"),
            bullet("guard cells — keep the target out of its own average",
                   NEON_PINK, 22, NEON_PINK, dot="■"),
            bullet("training cells — estimate the local floor",
                   TECH_CYAN, 22, TECH_CYAN, dot="■"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.30)
        Zone(-6.95, -0.35, -0.30, 1.35).fit(legend, pad=0.12)
        for l in legend:
            self.play(FadeIn(l, shift=RIGHT * 0.2), run_time=0.7)

        ch = Chart(6.1, 2.4, "range  →", label_size=19)
        ch.move_to([3.55, 1.35, 0])
        targets = [(0.12, 0.26, 0.011), (0.47, 0.34, 0.012), (0.83, 0.13, 0.012)]
        curve = ch.poly(floor_fn(targets), color=TECH_CYAN, stroke=2.4, n=800)
        self.play(Create(ch.box), FadeIn(ch.xlab), run_time=0.8)
        self.play(Create(curve), run_time=1.6)

        fixed = ch.hline(0.42, color=DIM_TEXT, stroke=2.5, dashed=True)
        self.play(Create(fixed), run_time=0.8)
        adaptive = ch.poly(lambda u: 0.20 + 0.62 * np.exp(-5.2 * u) + 0.10,
                           color=AMBER, stroke=3.2, n=500)
        self.play(Transform(fixed, adaptive), run_time=1.6)
        ad_lab = Text("the threshold follows the floor", font_size=20, color=AMBER)
        ad_lab.next_to(ch.box, UP, buff=0.14)
        self.play(FadeIn(ad_lab), run_time=0.8)

        hits = VGroup(*[Circle(radius=0.17, stroke_color=RADAR_GREEN, stroke_width=3)
                        .move_to(ch.pt(u, v)) for u, v in
                        ((0.47, 0.50), (0.83, 0.26))])
        hit_lab = Text("both detected", font_size=20, color=RADAR_GREEN)
        hit_lab.move_to(ch.pt(0.62, 0.80))
        self.play(Create(hits), FadeIn(hit_lab), run_time=1.1)

        f1 = Text("threshold  =  α  ×  mean of the training cells", font_size=27,
                  color=AMBER, weight=BOLD)
        f2 = Text("α is set by the false alarm rate you are willing to accept",
                  font_size=22, color=DIM_TEXT)
        fg = VGroup(f1, f2).arrange(DOWN, buff=0.20)
        fcard = carded(fg, color=AMBER, buff=0.30, opacity=0.10)
        fcard.move_to([0, -1.95, 0])
        self.play(FadeIn(fcard, shift=UP * 0.2), run_time=1.2)

        cap = caption("a cell is a detection only if it beats its own neighbourhood")
        self.play(FadeIn(cap), run_time=1.3)
        self.play(Indicate(cells[n // 2], color=AMBER, scale_factor=1.3), run_time=1.1)
        self.play(Indicate(fcard, color=AMBER, scale_factor=1.04), run_time=1.1)
        body = VGroup(cells, legend, ch, curve, fixed, ad_lab, hits, hit_lab, fcard)
        self.recap("CFAR IN ONE LINE",
                   ["every cell is judged against its own neighbourhood",
                    "guard cells keep a target out of its own average",
                    "α buys the false alarm rate you asked for"],
                   color=RADAR_GREEN, clear=body)
        self.fill()


# ============================ PART 15 : DETECTIONS TO TRACKS ============================
class Part15(NarratedScene):
    def construct(self):
        h = head("FROM PEAKS TO A PICTURE", color=RADAR_GREEN)
        self.play(FadeIn(h[0]), Create(h[1]), run_time=1.0)

        centres = [-4.55, 0.0, 4.55]
        panels = VGroup(*[Rectangle(width=4.2, height=2.9, stroke_color=SUBTLE,
                                    stroke_width=2, fill_color=PANEL_NAVY,
                                    fill_opacity=0.5).move_to([x, 0.95, 0])
                          for x in centres])
        titles = VGroup(*[Text(t, font_size=22, color=c, weight=BOLD)
                          for t, c in (("DETECTIONS", TECH_CYAN),
                                       ("CLUSTERS", AMBER),
                                       ("TRACKS", RADAR_GREEN))])
        for t, x in zip(titles, centres):
            t.move_to([x, 2.72, 0])
        self.play(FadeIn(panels), FadeIn(titles), run_time=1.2)

        rng = np.random.default_rng(31)
        groups = [np.array([-1.0, 0.55]), np.array([0.75, 1.15]), np.array([0.15, -0.55])]
        clouds = []
        for g in groups:
            clouds.append([g + rng.normal(0, 0.22, 2) for _ in range(7)])

        pts = VGroup()
        for cl in clouds:
            for p in cl:
                pts.add(Dot([centres[0] + p[0], 0.95 + p[1] - 0.35, 0],
                            radius=0.055, color=TECH_CYAN))
        self.play(LaggedStart(*[FadeIn(d, scale=2) for d in pts], lag_ratio=0.03),
                  run_time=1.8)
        pts_lab = Text("range · velocity · angle · SNR", font_size=19, color=DIM_TEXT)
        pts_lab.move_to([centres[0], -0.85, 0])
        self.play(FadeIn(pts_lab), run_time=0.8)

        pts2 = VGroup()
        boxes = VGroup()
        for cl, col in zip(clouds, (AMBER, AMBER, AMBER)):
            grp = VGroup()
            for p in cl:
                grp.add(Dot([centres[1] + p[0], 0.95 + p[1] - 0.35, 0],
                            radius=0.055, color=col))
            pts2.add(grp)
            boxes.add(SurroundingRectangle(grp, color=col, stroke_width=2.5, buff=0.13))
        self.play(FadeIn(pts2), run_time=0.9)
        self.play(LaggedStart(*[Create(b) for b in boxes], lag_ratio=0.3), run_time=1.4)
        cl_lab = Text("points that belong together", font_size=19, color=DIM_TEXT)
        cl_lab.move_to([centres[1], -0.85, 0])
        self.play(FadeIn(cl_lab), run_time=0.8)

        tracks = VGroup()
        for i, cl in enumerate(clouds):
            c = np.mean(cl, axis=0)
            box = RoundedRectangle(corner_radius=0.08, width=0.95, height=0.7,
                                   stroke_color=RADAR_GREEN, stroke_width=2.5,
                                   fill_opacity=0).move_to(
                [centres[2] + c[0], 0.95 + c[1] - 0.35, 0])
            arr = Arrow(box.get_center(), box.get_center() + RIGHT * 0.75 + UP * 0.12,
                        color=RADAR_GREEN, buff=0, stroke_width=3,
                        max_tip_length_to_length_ratio=0.28)
            idt = Text(f"T{i+1}", font_size=17, color=RADAR_GREEN)
            idt.next_to(box, UP, buff=0.06)
            tracks.add(VGroup(box, arr, idt))
        for t in tracks:
            self.play(FadeIn(t, scale=0.85), run_time=0.6)
        tr_lab = Text("objects with a history", font_size=19, color=DIM_TEXT)
        tr_lab.move_to([centres[2], -0.85, 0])
        self.play(FadeIn(tr_lab), run_time=0.8)

        arrows = VGroup(
            Arrow([-2.35, 0.95, 0], [-2.05, 0.95, 0], color=SUBTLE, buff=0,
                  stroke_width=4, max_tip_length_to_length_ratio=0.5),
            Arrow([2.15, 0.95, 0], [2.45, 0.95, 0], color=SUBTLE, buff=0,
                  stroke_width=4, max_tip_length_to_length_ratio=0.5))
        self.play(*[GrowArrow(a) for a in arrows], run_time=0.8)

        cap = caption("at last, something a human would recognise")
        self.play(FadeIn(cap), run_time=1.2)
        self.wait(0.7)

        body = VGroup(panels, titles, pts, pts2, boxes, tracks, arrows,
                      pts_lab, cl_lab, tr_lab)
        self.recap("BUT NOTICE WHAT WAS NEVER THERE",
                   ["no colour, no texture, no outline",
                    "multipath can hang a ghost under a bridge",
                    "1° of beam is still 1.7 m wide at 100 m",
                    "the radar infers the world — it never sees it"],
                   color=NEON_PINK, clear=body, hold=0.9)
        self.fill()


# ============================ PART 16 : THE WHOLE CHAIN ============================
class Part16(NarratedScene):
    def construct(self):
        strip = chain(
            ["CHIRP", "ECHO", "MIXER", "RANGE FFT", "DOPPLER FFT", "ANGLE FFT",
             "CFAR", "TRACKS"],
            [TECH_CYAN, TECH_CYAN, AMBER, RADAR_GREEN, NEON_PINK, VIOLET,
             AMBER, RADAR_GREEN], size=18)
        fit_width(strip, 13.2)
        strip.move_to([0, 2.55, 0])
        title = Text("FROM CHIRP TO DETECTION", font_size=34, color=TEXT_WHITE,
                     weight=BOLD)
        title.move_to([0, 3.45, 0])
        self.play(FadeIn(title), run_time=1.0)
        self.play(FadeIn(strip, lag_ratio=0.1), run_time=1.4)

        steps = [
            ("a straight-line frequency sweep goes out", TECH_CYAN),
            ("a delayed copy comes back, Δt = 2R/c", TECH_CYAN),
            ("multiply them: delay becomes a beat tone", AMBER),
            ("FFT along the chirp: tone becomes range", RADAR_GREEN),
            ("FFT across chirps: phase drift becomes speed", NEON_PINK),
            ("FFT across antennas: phase becomes direction", VIOLET),
            ("an adaptive threshold decides what is real", AMBER),
            ("clusters become objects, objects gain a history", RADAR_GREEN),
        ]
        slot = None
        for c, (txt, col) in zip(strip.chips, steps):
            new = Text(txt, font_size=28, color=col)
            fit_width(new, 12.0)
            new.move_to([0, 1.30, 0])
            if slot is None:
                self.play(Indicate(c, color=col, scale_factor=1.15),
                          FadeIn(new), run_time=0.8)
            else:
                self.play(Indicate(c, color=col, scale_factor=1.15),
                          FadeOut(slot), FadeIn(new), run_time=0.8)
            slot = new

        self.play(FadeOut(slot), run_time=0.6)
        idea = VGroup(
            Text("one idea to take away", font_size=25, color=DIM_TEXT),
            Text("almost every stage is a Fourier transform,", font_size=30,
                 color=AMBER, weight=BOLD),
            Text("trading one axis for another", font_size=30, color=AMBER, weight=BOLD),
        ).arrange(DOWN, buff=0.22)
        icard = carded(idea, color=AMBER, buff=0.36, opacity=0.10)
        icard.move_to([0, 0.75, 0])
        self.play(FadeIn(icard[0]), FadeIn(idea[0]), run_time=0.9)
        self.play(FadeIn(idea[1], shift=UP * 0.15), run_time=0.9)
        self.play(FadeIn(idea[2], shift=UP * 0.15), run_time=0.9)
        self.wait(1.0)

        closing = VGroup(
            Text("everything a radar knows about the world,", font_size=30,
                 color=TEXT_WHITE),
            Text("built out of a wiggling voltage", font_size=34, color=TECH_CYAN,
                 weight=BOLD),
        ).arrange(DOWN, buff=0.24)
        closing.move_to([0, -1.75, 0])
        self.play(FadeIn(closing[0], shift=UP * 0.2), run_time=1.1)
        self.play(Write(closing[1]), run_time=1.6)
        self.wait(0.8)

        thanks = caption("thanks for watching", color=DIM_TEXT, size=26)
        self.play(FadeIn(thanks), run_time=1.0)
        for c in strip.chips:
            self.play(Indicate(c, color=c[1].get_color(), scale_factor=1.10),
                      run_time=0.28)
        self.wait(1.0)
        self.fill()
