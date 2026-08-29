"""
The 1280x720 YouTube thumbnail, rendered as a single Manim still.

    python -m manim -s -r 1280,720 --media_dir media thumbnail.py Thumbnail
    cp media/images/thumbnail/Thumbnail*.png output/thumbnail.png

It imports the palette and the builders from main.py so the thumbnail and the
video share one visual language.  The bottom-right corner is kept clear, since
YouTube stamps the duration badge there.
"""

import numpy as np
from manim import *

from main import (AMBER, DEEP_NAVY, DIM_TEXT, NEON_PINK, PANEL_NAVY, RADAR_GREEN,
                  SUBTLE, TECH_CYAN, TEXT_WHITE, VIOLET, Chart, chip, dish,
                  fit_width, peak_fn)

config.background_color = DEEP_NAVY


class Thumbnail(Scene):
    def construct(self):
        glow = VGroup(*[Circle(radius=r, stroke_color=SUBTLE, stroke_width=2,
                               stroke_opacity=0.5).move_to([-5.0, 1.4, 0])
                        for r in (1.0, 1.9, 2.8, 3.7)])
        self.add(glow)

        sensor = dish(1.15, TECH_CYAN).move_to([-5.5, 1.4, 0])
        self.add(sensor)

        ramp_ch = Chart(3.5, 1.6, fill_opacity=0.65)
        ramp_ch.move_to([-3.4, -1.85, 0])
        ramp = Line(ramp_ch.pt(0.06, 0.12), ramp_ch.pt(0.94, 0.88),
                    stroke_color=TECH_CYAN, stroke_width=6)
        ramp_lab = Text("CHIRP", font_size=22, color=TECH_CYAN, weight=BOLD)
        ramp_lab.next_to(ramp_ch.box, DOWN, buff=0.16)
        self.add(ramp_ch, ramp, ramp_lab)

        spec_ch = Chart(3.5, 1.6, fill_opacity=0.65)
        spec_ch.move_to([0.6, -1.85, 0])
        spec = spec_ch.poly(peak_fn([(0.32, 0.60, 0.020), (0.68, 0.78, 0.020)]),
                            color=RADAR_GREEN, stroke=4, n=600)
        spec_lab = Text("DETECTION", font_size=22, color=RADAR_GREEN, weight=BOLD)
        spec_lab.next_to(spec_ch.box, DOWN, buff=0.16)
        self.add(spec_ch, spec, spec_lab)

        arrow = Arrow([-1.5, -1.85, 0], [-1.05, -1.85, 0], color=AMBER, buff=0,
                      stroke_width=7, max_tip_length_to_length_ratio=0.5)
        self.add(arrow)

        rng = np.random.default_rng(4)
        cube = VGroup()
        for i in range(9):
            for j in range(7):
                bright = (i, j) in ((6, 5), (2, 2))
                cube.add(Square(side_length=0.36, stroke_width=0.6,
                                stroke_color=SUBTLE,
                                fill_color=AMBER if bright else TECH_CYAN,
                                fill_opacity=0.9 if bright else 0.06 + 0.14 * rng.random())
                         .move_to([4.55 + (i - 4) * 0.38, -1.35 + (j - 3) * 0.38, 0]))
        self.add(cube)

        t1 = Text("WHAT DOES A RADAR", font_size=58, color=TEXT_WHITE, weight=BOLD)
        t2 = Text("ACTUALLY SEE?", font_size=86, color=TECH_CYAN, weight=BOLD)
        t1.move_to([0.35, 2.75, 0])
        t2.move_to([0.35, 1.65, 0])
        fit_width(t1, 11.5)
        fit_width(t2, 11.5)
        self.add(t1, t2)

        sub = Text("from chirp to detection", font_size=34, color=AMBER)
        sub.move_to([0.35, 0.62, 0])
        self.add(sub)
