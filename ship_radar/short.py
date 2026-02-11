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

class Part19Short(Scene):
    """Complete Detection Sequence - Vertical Short Version (9:16)"""
    def construct(self):
        # Title
        title = Text("COMPLETE DETECTION\nSEQUENCE", font_size=48, color=TECH_CYAN, line_spacing=1.2)
        title.to_edge(UP, buff=1.0)
        
        # 1. Action Area (Top Half)
        # Ship on bottom-left of this section, Jet on top-right
        action_center = UP * 2.5
        
        ship = self.create_mini_ship().scale(0.8)
        ship.move_to(action_center + LEFT*2 + DOWN*0.2)
        
        jet = self.create_mini_jet().scale(0.6)
        jet.move_to(action_center + RIGHT*2 + UP*1)
        
        # 2. Equation Data Bank (Middle Section)
        # Stacked vertically in the middle
        data_bank_bg = RoundedRectangle(width=8, height=5.5, corner_radius=0.2, 
                                       fill_color=DEEP_NAVY, fill_opacity=0.8, stroke_color=TECH_CYAN, stroke_width=2)
        data_bank_bg.move_to(DOWN * 1.5)
        
        data_bank_title = Text("SYSTEM PARAMETERS", font_size=24, color=TECH_CYAN, weight=BOLD)
        data_bank_title.next_to(data_bank_bg, UP, buff=0.2)
        
        # Prepare equation groups
        eq1 = VGroup(Text("PROPAGATION SPEED:", font_size=20, color=TEAL, font="Monospace"),
                     MathTex(r"c = 3 \times 10^8 \text{ m/s}", font_size=28, color=TEXT_WHITE))
        eq2 = VGroup(Text("RANGE CALCULATION:", font_size=20, color=TEAL, font="Monospace"),
                     MathTex(r"R = \frac{c \cdot t}{2}", font_size=28, color=TECH_CYAN))
        eq3 = VGroup(Text("DOPPLER SHIFT:", font_size=20, color=TEAL, font="Monospace"),
                     MathTex(r"f_d = \frac{2v_r f_0}{c}", font_size=28, color=NEON_PINK))
        eq4 = VGroup(Text("RECEIVED POWER:", font_size=20, color=TEAL, font="Monospace"),
                     MathTex(r"P_r \propto \frac{1}{R^4}", font_size=28, color=VIBRANT_ORANGE))

        # Arrange internals
        for eq in [eq1, eq2, eq3, eq4]:
            eq.arrange(DOWN, aligned_edge=ORIGIN, buff=0.1)

        # Group and arrange main container
        equations_group = VGroup(eq1, eq2, eq3, eq4).arrange(DOWN, buff=0.4, aligned_edge=ORIGIN)
        equations_group.move_to(data_bank_bg.get_center())
        
        # 3. Progress Steps (Bottom Section)
        # 2 Rows of 3 Items
        progress_steps = ["TRANSMIT", "PROPAGATION", "REFLECTION", "ECHO", "PROCESSING", "TRACKING"]
        progress_bar = VGroup()
        
        for i, step in enumerate(progress_steps):
            box = RoundedRectangle(width=2.5, height=0.8, corner_radius=0.15, 
                                  fill_color=SUBTLE_NAVY, fill_opacity=0.5, stroke_color=SUBTLE_NAVY, stroke_width=2)
            txt = Text(step, font_size=18, color=TEXT_WHITE, weight=BOLD)
            txt.move_to(box)
            item = VGroup(box, txt)
            progress_bar.add(item)
            
        progress_bar.arrange_in_grid(rows=2, cols=3, buff=0.2)
        progress_bar.to_edge(DOWN, buff=1.0)
        
        # Tactical Frame (Vertical)
        frame = Rectangle(width=8.5, height=15.5, stroke_color=SUBTLE_NAVY, stroke_width=2)
        
        # Animations
        self.play(
            FadeIn(frame), Write(title),
            FadeIn(ship), FadeIn(jet),
            FadeIn(data_bank_bg), Write(data_bank_title),
            FadeIn(equations_group),
            FadeIn(progress_bar),
            run_time=1.5
        )
        
        # Highlight Helper
        def highlight_step(index, color=TECH_CYAN):
            anims = []
            # Reset all
            for item in progress_bar:
                anims.append(item[0].animate.set_stroke(SUBTLE_NAVY, width=2).set_fill(SUBTLE_NAVY, 0.5))
                anims.append(item[1].animate.set_color(TEXT_WHITE))
            
            # Highlight current
            if index < len(progress_bar):
                anims.append(progress_bar[index][0].animate.set_stroke(color, width=4).set_fill(color, 0.3))
                anims.append(progress_bar[index][1].animate.set_color(color))
            return anims

        def highlight_eq(index):
            anims = []
            for i, eq in enumerate(equations_group):
                if i == index:
                    anims.append(eq.animate.scale(1.1).set_opacity(1))
                    anims.append(eq[0].animate.set_color(VIBRANT_ORANGE))
                else:
                    anims.append(eq.animate.scale(1/1.1 if eq.height > 1.5 else 1).set_opacity(0.3))
                    anims.append(eq[0].animate.set_color(TEAL))
            return anims

        # Sequence
        
        # Step 1: Transmit
        self.play(*highlight_step(0), run_time=0.5)
        pulse = self.create_pulse().move_to(ship.get_right())
        self.play(FadeIn(pulse, scale=0.5), run_time=0.3)
        
        # Step 2: Propagation
        self.play(*highlight_step(1, VIBRANT_ORANGE), *highlight_eq(0), run_time=0.5)
        self.play(
            pulse.animate.move_to(jet.get_center()).scale(2).set_opacity(0.5),
            run_time=1.5
        )
        self.play(*highlight_eq(1), run_time=0.5)
        
        # Step 3: Reflection
        self.play(*highlight_step(2, NEON_PINK), run_time=0.5)
        flash = Circle(radius=0.4, fill_color=NEON_PINK, fill_opacity=0.8, stroke_width=0)
        flash.move_to(jet.get_center())
        self.play(FadeIn(flash), FadeOut(pulse), run_time=0.3)
        
        # Step 4: Echo
        self.play(*highlight_step(3, NEON_PINK), *highlight_eq(3), run_time=0.5)
        echo = self.create_pulse(color=NEON_PINK).move_to(jet.get_center())
        self.play(FadeOut(flash), FadeIn(echo), run_time=0.3)
        self.play(
            echo.animate.move_to(ship.get_right()).set_opacity(0.3),
            run_time=1.5
        )
        self.play(FadeOut(echo), run_time=0.2)
        
        # Step 5: Processing
        self.play(*highlight_step(4, TECH_CYAN), *highlight_eq(2), run_time=0.5)
        process_flash = Circle(radius=0.8, stroke_color=TECH_CYAN, stroke_width=5)
        process_flash.move_to(ship.get_center())
        self.play(Create(process_flash), run_time=0.5)
        self.play(process_flash.animate.scale(0.3).set_opacity(0), run_time=0.5)
        
        # Step 6: Tracking
        self.play(*highlight_step(5, TECH_CYAN), run_time=0.5)
        
        track_line = DashedLine(ship.get_right(), jet.get_center(), 
                               stroke_color=VIBRANT_ORANGE, stroke_width=3)
        track_box = SurroundingRectangle(jet, color=VIBRANT_ORANGE, buff=0.3, stroke_width=4)
        
        self.play(Create(track_line), Create(track_box), run_time=1)
        
        # Final emphasis
        success = Text("TARGET ACQUIRED", font_size=50, color=TECH_CYAN, weight=BOLD)
        success.move_to(action_center)
        success_bg = SurroundingRectangle(success, color=DEEP_NAVY, fill_color=DEEP_NAVY, fill_opacity=0.8)
        success_box = SurroundingRectangle(success, color=TECH_CYAN, buff=0.3, stroke_width=4)
        
        # Make sure text is readable over potential lines
        self.play(
            FadeIn(success_bg),
            Write(success),
            Create(success_box),
            run_time=1
        )
        
        # Reset equations highlight
        self.play(
            *[eq.animate.set_opacity(1).scale(1) for eq in equations_group],
            *[eq[0].animate.set_color(TEAL) for eq in equations_group],
            run_time=1
        )
        
        self.wait(3)

    def create_mini_ship(self):
        hull = Polygon(
            [-1.5, 0, 0], [-1, -0.2, 0], [1, -0.2, 0], [1.5, 0, 0],
            fill_color=SUBTLE_NAVY, fill_opacity=1, stroke_color=TECH_CYAN, stroke_width=2
        )
        tower = Rectangle(width=0.5, height=0.6, fill_color=SUBTLE_NAVY,
                         fill_opacity=1, stroke_color=TECH_CYAN, stroke_width=2)
        tower.move_to([0, 0.3, 0])
        return VGroup(hull, tower)
    
    def create_mini_jet(self):
        body = Polygon(
            [0, 0, 0], [1, 0.1, 0], [1.3, 0, 0], [1, -0.1, 0],
            fill_color=SUBTLE_NAVY, fill_opacity=1, stroke_color=NEON_PINK, stroke_width=2
        )
        return body
    
    def create_pulse(self, color=TECH_CYAN):
        return VGroup(*[
            Arc(radius=0.2+i*0.1, angle=PI/3, stroke_width=3-i*0.5,
                color=color, stroke_opacity=1-i*0.2).rotate(-PI/6)
            for i in range(4)
        ])
