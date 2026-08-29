"""
YouTube thumbnail for "How Radar Measures Distance AND Speed".

Rendered as a single still frame in the same visual language as the video, so
the thumbnail and the opening shot feel like the same piece of work.

    python -m manim -s -r 1280,720 --media_dir media thumbnail.py Thumbnail

The PNG lands in media/images/thumbnail/Thumbnail.png; build_thumbnail.py
copies it to output/ and reports the file size against YouTube's 2 MB limit.
"""

import numpy as np
from manim import *

from main import (DEEP_NAVY, SUBTLE, RADAR_GREEN, TECH_CYAN, NEON_PINK,
                  AMBER, TEXT_WHITE, DIM_TEXT, dish, plane)

config.background_color = DEEP_NAVY


class Thumbnail(Scene):
    def construct(self):
        # ---------------------------------------------------------- backdrop
        # faint PPI arcs sweeping out of the bottom-right corner
        pivot = np.array([5.2, -4.6, 0.0])
        arcs = VGroup(*[
            Arc(radius=r, start_angle=PI * 0.42, angle=PI * 0.42,
                color=SUBTLE, stroke_width=3, stroke_opacity=0.55)
            .move_arc_center_to(pivot)
            for r in (3.2, 4.4, 5.6, 6.8, 8.0)
        ])
        self.add(arcs)

        # ---------------------------------------------------------- radar art
        radar = dish(scale=1.3, color=TECH_CYAN).move_to(RIGHT * 2.05 + DOWN * 1.35)
        origin = radar[2].get_center()

        out_waves = VGroup(*[
            Arc(radius=0.95 + i * 0.60, start_angle=-PI / 5.2, angle=2 * PI / 5.2,
                color=RADAR_GREEN, stroke_width=9 - i * 1.0,
                stroke_opacity=0.95 - i * 0.13).move_arc_center_to(origin)
            for i in range(5)
        ]).rotate(0.52, about_point=origin)

        target = plane(color=TEXT_WHITE, scale=1.5).rotate(PI - 0.35)
        target.move_to(RIGHT * 5.15 + UP * 2.0)
        halo = Circle(radius=0.95, color=AMBER, stroke_width=5,
                      stroke_opacity=0.85).move_to(target)

        echo = VGroup(*[
            Arc(radius=0.75 + i * 0.42, start_angle=PI * 0.72, angle=PI * 0.46,
                color=NEON_PINK, stroke_width=7 - i * 1.2,
                stroke_opacity=0.9 - i * 0.2).move_arc_center_to(target.get_center())
            for i in range(3)
        ])

        self.add(out_waves, radar, halo, echo, target)

        # ---------------------------------------------------------- the words
        kicker = Text("HOW RADAR MEASURES", font_size=40, color=DIM_TEXT, weight=BOLD)
        w1 = Text("DISTANCE", font_size=112, color=RADAR_GREEN, weight=BOLD)
        w2 = Text("+ SPEED", font_size=112, color=NEON_PINK, weight=BOLD)

        words = VGroup(kicker, w1, w2).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        words.move_to(LEFT * 7.11 + UP * 1.35, aligned_edge=LEFT).shift(RIGHT * 0.55)

        bar = Rectangle(width=0.16, height=words.height + 0.25, stroke_width=0,
                        fill_color=AMBER, fill_opacity=1)
        bar.next_to(words, LEFT, buff=0.34)
        self.add(bar, words)

        # ---------------------------------------------------------- formulas
        def chip(text, color):
            t = Text(text, font_size=40, color=TEXT_WHITE, weight=BOLD)
            box = RoundedRectangle(corner_radius=0.16,
                                   width=t.width + 0.72, height=t.height + 0.62,
                                   stroke_color=color, stroke_width=5,
                                   fill_color=DEEP_NAVY, fill_opacity=0.92).move_to(t)
            return VGroup(box, t)

        chips = VGroup(chip("R = c·Δt / 2", RADAR_GREEN),
                       chip("v = λ·f_d / 2", NEON_PINK))
        chips.arrange(RIGHT, buff=0.45)
        chips.next_to(words, DOWN, aligned_edge=LEFT, buff=0.6)
        self.add(chips)

        tag = Text("ONE ECHO  ·  TWO ANSWERS", font_size=30, color=AMBER, weight=BOLD)
        tag.next_to(chips, DOWN, aligned_edge=LEFT, buff=0.42)
        self.add(tag)
