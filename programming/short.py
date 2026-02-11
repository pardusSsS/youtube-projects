from manim import *

# Global style
config.background_color = "#020B1F"
config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 16.0
config.frame_width = 9.0

class Part11(Scene):
    def construct(self):
        title = Text("Intermediate Representation", font_size=55, color="#00F0FF")
        title.to_edge(UP, buff=1.0)
        
        # High-Level Code
        high_title = Text("High-Level", font_size=40, color="#FFFFFF", weight=BOLD)
        high_code = Code(
            code_string="x = 10 + 5",
            language="python",
            background="rectangle",
            background_config={"stroke_color": "#00F0FF", "stroke_width": 3},
            add_line_numbers=False,
            paragraph_config={"font_size": 40}
        ).scale(1.2)
        
        high_group = VGroup(high_title, high_code).arrange(DOWN, buff=0.3)
        
        # IR Code
        ir_title = Text("IR (3-Address)", font_size=40, color="#FF9F00", weight=BOLD)
        ir_lines = VGroup(
            Text("t1 = 10", font="Monospace", font_size=32, color="#FF9F00"),
            Text("t2 = 5", font="Monospace", font_size=32, color="#FF9F00"),
            Text("t3 = t1 + t2", font="Monospace", font_size=32, color="#FF9F00"),
            Text("x = t3", font="Monospace", font_size=32, color="#FF9F00")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        ir_group = VGroup(ir_title, ir_lines).arrange(DOWN, buff=0.3)
        
        # Assembly Code
        low_title = Text("Assembly", font_size=40, color="#FF0055", weight=BOLD)
        low_code = VGroup(
            Text("MOV R1, 10", font="Monospace", font_size=30, color="#FF0055"),
            Text("MOV R2, 5", font="Monospace", font_size=30, color="#FF0055"),
            Text("ADD R3, R1, R2", font="Monospace", font_size=30, color="#FF0055"),
            Text("MOV [x], R3", font="Monospace", font_size=30, color="#FF0055")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        low_group = VGroup(low_title, low_code).arrange(DOWN, buff=0.3)
        
        # Arrange Main Groups
        main_content = VGroup(high_group, ir_group, low_group).arrange(DOWN, buff=1.5)
        main_content.next_to(title, DOWN, buff=1.0)
        
        # Connecting Arrows
        arrow1 = Arrow(
            start=high_code.get_bottom(),
            end=ir_title.get_top(),
            color="#FF9F00",
            stroke_width=6,
            buff=0.2
        )
        
        arrow2 = Arrow(
            start=ir_lines.get_bottom(),
            end=low_title.get_top(),
            color="#FF9F00",
            stroke_width=6,
            buff=0.2
        )
        
        # Animations
        self.play(Write(title, run_time=2))
        self.wait(1)
        
        self.play(FadeIn(high_group, shift=DOWN*0.5, run_time=1.5))
        self.wait(1.5)
        
        self.play(GrowArrow(arrow1, run_time=1.2))
        self.play(FadeIn(ir_group, shift=DOWN*0.5, run_time=1.5))
        self.wait(1.5)
        
        self.play(GrowArrow(arrow2, run_time=1.2))
        self.play(FadeIn(low_group, shift=DOWN*0.5, run_time=1.5))
        
        self.wait(3)
