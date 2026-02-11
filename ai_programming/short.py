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


class Part5Short(Scene):
    """Tokenization - Breaking Code into Pieces (YouTube Shorts Version)"""
    def construct(self):
        # Title at top
        title = Text("Tokenization", font_size=60, color=ELECTRIC_CYAN)
        title.to_edge(UP, buff=0.8)
        
        # Subtitle
        subtitle = Text("Breaking Code into Pieces", font_size=32, color=WHITE)
        subtitle.next_to(title, DOWN, buff=0.3)
        
        # Original code - smaller font for vertical layout
        code_text = Text('print("Hello, World!")', font_size=32, color=WHITE)
        code_text.next_to(subtitle, DOWN, buff=1.0)
        
        # Tokens - arranged in a grid for vertical layout (3 rows)
        tokens = ["print", "(", '"', "Hello", ",", " World", "!", '"', ")"]
        token_colors = [ELECTRIC_CYAN, SUBTLE_NAVY, NEON_PINK, VIBRANT_ORANGE, 
                       SUBTLE_NAVY, VIBRANT_ORANGE, NEON_PINK, NEON_PINK, SUBTLE_NAVY]
        
        token_boxes = VGroup()
        for i, (token, color) in enumerate(zip(tokens, token_colors)):
            box = RoundedRectangle(
                width=max(len(token)*0.28 + 0.5, 0.7), height=0.65,
                corner_radius=0.1, stroke_color=color, stroke_width=3,
                fill_color=color, fill_opacity=0.2
            )
            label = Text(token, font_size=22, color=WHITE)
            token_box = VGroup(box, label)
            token_boxes.add(token_box)
        
        # Arrange in 3 rows for vertical format
        row1 = VGroup(*token_boxes[0:3]).arrange(RIGHT, buff=0.35)
        row2 = VGroup(*token_boxes[3:6]).arrange(RIGHT, buff=0.35)
        row3 = VGroup(*token_boxes[6:9]).arrange(RIGHT, buff=0.35)
        
        token_grid = VGroup(row1, row2, row3).arrange(DOWN, buff=0.6)
        token_grid.move_to(ORIGIN)
        
        # Token IDs - arranged below each token
        ids = ["1024", "28", "15", "7592", "11", "3468", "0", "15", "29"]
        id_labels = VGroup()
        for i, (id_val, token_box) in enumerate(zip(ids, token_boxes)):
            id_label = Text(f"[{id_val}]", font_size=14, color=SUBTLE_NAVY)
            id_label.next_to(token_box, DOWN, buff=0.25)
            id_labels.add(id_label)
        
        # Explanation at bottom
        explanation = Text("Each token gets a unique ID", font_size=28, color=NEON_PINK)
        explanation.to_edge(DOWN, buff=2.0)
        
        # Animations
        self.play(Write(title), run_time=1.0)
        self.play(FadeIn(subtitle, shift=DOWN), run_time=0.8)
        self.play(Write(code_text), run_time=1.5)
        self.wait(0.5)
        
        # Arrow from code to tokens
        arrow = Arrow(
            code_text.get_bottom() + DOWN*0.2, 
            token_grid.get_top() + UP*0.2, 
            color=ELECTRIC_CYAN,
            stroke_width=4
        )
        self.play(GrowArrow(arrow), run_time=0.8)
        
        # Show tokens row by row
        self.play(
            *[FadeIn(token_box, shift=DOWN) for token_box in row1],
            run_time=0.8
        )
        self.play(
            *[FadeIn(token_box, shift=DOWN) for token_box in row2],
            run_time=0.8
        )
        self.play(
            *[FadeIn(token_box, shift=DOWN) for token_box in row3],
            run_time=0.8
        )
        
        self.play(FadeOut(arrow), run_time=0.4)
        
        # Show IDs
        self.play(
            *[FadeIn(id_label, shift=UP) for id_label in id_labels],
            run_time=1.2
        )
        
        self.play(FadeIn(explanation, shift=UP), run_time=0.8)
        self.wait(2)
        
        # Final highlight effect
        self.play(
            *[token_box[0].animate.set_stroke(WHITE, width=4) for token_box in token_boxes],
            run_time=0.4
        )
        self.play(
            *[token_box[0].animate.set_stroke(token_colors[i], width=3) 
              for i, token_box in enumerate(token_boxes)],
            run_time=0.4
        )
        self.wait(1)
