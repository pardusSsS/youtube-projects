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
config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 16.0
config.frame_width = 9.0

# ============================================================================
# PART 5 SHORT: TARGET DETECTION (Vertical)
# ============================================================================
class Part5Short(ThreeDScene):
    def construct(self):
        
        # Title - Adapted for vertical but same text
        title = Text("AI Stage 2:\nTarget Detection", font_size=54, color=NEON_PINK, weight=BOLD)
        self.add_fixed_in_frame_mobjects(title)
        title.to_edge(UP, buff=0.5)
        
        self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES, zoom=0.65)
        
        # 3D Convolutional Neural Network - Vertical Stack
        
        # Layer 1 - Input (Range-Doppler map)
        # Original: range(5), range(5), range(3)
        layer1 = VGroup(*[
            Cube(side_length=0.15, color=TECH_CYAN, fill_opacity=0.6, stroke_width=1)
            .shift(LEFT*1.0 + RIGHT*i*0.18 + UP*j*0.18 + OUT*k*0.18)
            for i in range(5) for j in range(5) for k in range(3)
        ])
        
        # Layer 2 - Feature extraction
        # Original: range(4), range(4), range(4)
        layer2 = VGroup(*[
            Cube(side_length=0.2, color=NEON_PINK, fill_opacity=0.7, stroke_width=1)
            .shift(LEFT*0.8 + RIGHT*i*0.25 + UP*j*0.25 + OUT*k*0.25)
            for i in range(4) for j in range(4) for k in range(4)
        ])
        
        # Layer 3 - Deep features
        # Original: range(3), range(3), range(3)
        layer3 = VGroup(*[
            Cube(side_length=0.25, color=VIBRANT_ORANGE, fill_opacity=0.7, stroke_width=1)
            .shift(LEFT*0.6 + RIGHT*i*0.3 + UP*j*0.3 + OUT*k*0.3)
            for i in range(3) for j in range(3) for k in range(3)
        ])
        
        # Output - Detection decision
        # Original: range(3) spheres
        output = VGroup(*[
            Sphere(radius=0.25, color=TECH_CYAN, fill_opacity=0.9, resolution=(10, 10))
            .shift(UP*(0.5-i*0.8)) # Vertical arrangement
            for i in range(3)
        ])
        
        # Vertical Layout Positioning
        layer1.move_to(UP*4.5)
        layer2.move_to(UP*1.0)
        layer3.move_to(DOWN*2.5)
        output.move_to(DOWN*5.5)
        

        # Using fixed frame positioning for labels is safer in 3D scene
        input_label = Text("Range-Doppler\nMap", font_size=32, color=TECH_CYAN, weight=BOLD)
        input_label.to_edge(LEFT, buff=0.5).shift(UP*4)
        self.add_fixed_in_frame_mobjects(input_label)

        output_label = Text("Detection:\nAircraft\nDrone\nBird", font_size=32, color=TECH_CYAN, weight=BOLD)
        output_label.to_edge(RIGHT, buff=0.5).shift(DOWN*5.5)
        self.add_fixed_in_frame_mobjects(output_label)

        # Animation
        self.play(Write(title), run_time=2.0)
        
        self.play(
            LaggedStart(
                FadeIn(layer1, shift=DOWN, run_time=1.5),
                FadeIn(layer2, shift=DOWN, run_time=1.5),
                FadeIn(layer3, shift=DOWN, run_time=1.5),
                FadeIn(output, shift=DOWN, run_time=1.5),
                lag_ratio=0.4
            )
        )
        
        self.play(Write(input_label), Write(output_label), run_time=2.0)
        self.wait(1)
        
        # Rotate for better view
        self.move_camera(theta=-15*DEGREES, run_time=4)
        self.wait(1)
        
        # AI task description (Original text)
        task = Text("Classify: Target vs Clutter vs Noise", font_size=32, color=VIBRANT_ORANGE, weight=BOLD)
        self.add_fixed_in_frame_mobjects(task)
        task.to_edge(DOWN, buff=0.5)
        
        self.play(Write(task), run_time=2.0)
        self.wait(3)
