from manim import *
import numpy as np

# Global style
config.background_color = "#020B1F"

# ========================================
# PART 1: THE HOOK (3-6 seconds)
# ========================================
class Part1(Scene):
    def construct(self):
        
        # Explosive title entrance
        title = Text("HOW COMPUTERS", font_size=72, weight=BOLD, color="#00F0FF")
        title2 = Text("UNDERSTAND CODE", font_size=72, weight=BOLD, color="#FF0055")
        title2.next_to(title, DOWN, buff=0.2)
        
        # Flash effect
        flash = Circle(radius=8, color="#FF9F00", fill_opacity=0.3, stroke_width=0)
        
        self.play(
            FadeIn(flash, scale=0.1, run_time=0.3),
            FadeOut(flash, run_time=0.5)
        )
        self.play(
            Write(title, run_time=0.8),
            Write(title2, run_time=0.8)
        )
        self.wait(0.4)
        self.play(FadeOut(title), FadeOut(title2), run_time=0.5)


# ========================================
# PART 2: THE HUMAN WORLD (13-25s)
# ========================================
class Part2(Scene):
    def construct(self):
        
        title = Text("The Human Side", font_size=48, color="#00F0FF")
        title.to_edge(UP, buff=0.5)
        
        # Code snippet in a beautiful frame
        code_text = Code(
            code_string="""def hello():
    print("Hello, World!")
    return True""",
            language="python",
            background="rectangle",
            background_config={"stroke_color": "#00F0FF", "stroke_width": 3},
            add_line_numbers=False,
            formatter_style="monokai"
        ).scale(0.8)
        code_text.shift(UP * 0.5)
        
        human_label = Text("Human-Readable", font_size=32, color="#FF9F00")
        human_label.next_to(code_text, DOWN, buff=0.8)
        
        # Glow effect
        glow = Rectangle(
            width=code_text.width + 0.4,
            height=code_text.height + 0.4,
            color="#00F0FF",
            fill_opacity=0.1,
            stroke_width=0
        ).move_to(code_text)
        
        self.play(Write(title, run_time=2))
        self.wait(1)
        self.play(
            FadeIn(glow, scale=0.95, run_time=1.5),
            FadeIn(code_text, run_time=2)
        )
        self.wait(2)
        self.play(Write(human_label, run_time=2))
        self.wait(3)
        
        # Pulse the glow
        self.play(
            glow.animate.set_fill(opacity=0.2),
            run_time=1.5,
            rate_func=there_and_back
        )
        self.wait(3)


# ========================================
# PART 3: THE MACHINE WORLD (13-25s)
# ========================================
class Part3(Scene):
    def construct(self):
        
        title = Text("The Machine Side", font_size=48, color="#FF0055")
        title.to_edge(UP, buff=0.5)
        
        # Binary representation
        binary_lines = VGroup()
        binary_strings = [
            "01001000 01100101 01101100",
            "01101100 01101111 00100000",
            "01010111 01101111 01110010",
            "01101100 01100100 00100001"
        ]
        
        for i, bin_str in enumerate(binary_strings):
            line = Text(bin_str, font="Monospace", font_size=24, color="#00F0FF")
            line.shift(UP * (1 - i * 0.6))
            binary_lines.add(line)
        
        machine_label = Text("Machine Code", font_size=32, color="#FF9F00")
        machine_label.next_to(binary_lines, DOWN, buff=0.8)
        
        # Digital rain effect
        particles = VGroup(*[
            Text(str(np.random.choice(["0", "1"])), font_size=20, color="#00F0FF", opacity=0.3)
            .shift(RIGHT * np.random.uniform(-6, 6) + UP * np.random.uniform(-3, 4))
            for _ in range(30)
        ])
        
        self.play(Write(title, run_time=2))
        self.wait(1)
        self.play(LaggedStart(*[FadeIn(p, shift=DOWN*0.5) for p in particles], lag_ratio=0.05, run_time=2))
        self.wait(1.5)
        self.play(LaggedStart(*[Write(line) for line in binary_lines], lag_ratio=0.3, run_time=3))
        self.wait(2)
        self.play(Write(machine_label, run_time=2))
        self.wait(4)


# ========================================
# PART 4: THE GAP (13-25s)
# ========================================
class Part4(Scene):
    def construct(self):
        
        title = Text("The Translation Problem", font_size=42, color="#FF9F00")
        title.to_edge(UP, buff=0.5)
        
        # Two worlds separated
        human_side = Rectangle(width=3, height=4, color="#00F0FF", stroke_width=4)
        human_side.shift(LEFT * 3.5)
        human_text = Text("Human\nCode", font_size=28, color="#FFFFFF")
        human_text.move_to(human_side)
        
        machine_side = Rectangle(width=3, height=4, color="#FF0055", stroke_width=4)
        machine_side.shift(RIGHT * 3.5)
        machine_text = Text("Machine\nCode", font_size=28, color="#FFFFFF")
        machine_text.move_to(machine_side)
        
        # The gap
        gap = DoubleArrow(
            start=human_side.get_right(),
            end=machine_side.get_left(),
            color="#FF9F00",
            stroke_width=5,
            buff=0
        )
        question = Text("???", font_size=56, color="#FF9F00", weight=BOLD)
        question.next_to(gap, UP, buff=0.3)
        
        self.play(Write(title, run_time=2))
        self.wait(1.5)
        self.play(
            Create(human_side, run_time=1.5),
            Write(human_text, run_time=1.5)
        )
        self.wait(1)
        self.play(
            Create(machine_side, run_time=1.5),
            Write(machine_text, run_time=1.5)
        )
        self.wait(1.5)
        self.play(GrowArrow(gap, run_time=2))
        self.wait(1)
        self.play(Write(question, run_time=1.5, rate_func=there_and_back_with_pause))
        self.wait(3)
        
        # Pulse question
        self.play(
            question.animate.scale(1.2),
            run_time=1,
            rate_func=there_and_back
        )
        self.wait(2)


# ========================================
# PART 5: THE PIPELINE OVERVIEW (13-25s)
# ========================================
class Part5(Scene):
    def construct(self):
        
        title = Text("The Translation Pipeline", font_size=44, color="#00F0FF")
        title.to_edge(UP, buff=0.4)
        
        # Pipeline stages
        stages = VGroup()
        stage_names = ["Source\nCode", "Lexer", "Parser", "Compiler/\nInterpreter", "Machine\nCode"]
        colors = ["#FFFFFF", "#00F0FF", "#FF0055", "#FF9F00", "#00F0FF"]
        
        for i, (name, color) in enumerate(zip(stage_names, colors)):
            box = Rectangle(width=1.8, height=1.2, color=color, stroke_width=3)
            text = Text(name, font_size=18, color=color)
            text.move_to(box)
            group = VGroup(box, text)
            group.shift(LEFT * 5 + RIGHT * i * 2.5)
            stages.add(group)
        
        # Arrows between stages
        arrows = VGroup()
        for i in range(len(stages) - 1):
            arrow = Arrow(
                start=stages[i].get_right(),
                end=stages[i+1].get_left(),
                color="#FF9F00",
                stroke_width=3,
                buff=0.1
            )
            arrows.add(arrow)
        
        pipeline = VGroup(stages, arrows)
        pipeline.shift(DOWN * 0.5)
        
        self.play(Write(title, run_time=2.5))
        self.wait(2)
        
        # Animate pipeline construction
        for stage in stages:
            self.play(FadeIn(stage, shift=DOWN*0.3, run_time=1.2))
            self.wait(0.5)
        
        self.wait(2)
        
        for arrow in arrows:
            self.play(GrowArrow(arrow, run_time=1))
            self.wait(0.3)
        
        self.wait(3)
        
        # Flow animation
        dot = Dot(color="#FF9F00", radius=0.15)
        dot.move_to(stages[0].get_center())
        self.add(dot)
        
        for i in range(len(stages) - 1):
            self.play(
                dot.animate.move_to(stages[i+1].get_center()),
                run_time=1.5,
                rate_func=smooth
            )
            self.wait(0.5)
        
        self.wait(2)


# ========================================
# PART 6: LEXICAL ANALYSIS - TOKENIZATION (13-25s)
# ========================================
class Part6(Scene):
    def construct(self):
        
        title = Text("Step 1: Lexical Analysis (Tokenization)", font_size=38, color="#00F0FF")
        title.to_edge(UP, buff=0.4)
        
        # Source code
        source = Text('x = 10 + 5', font="Monospace", font_size=36, color="#FFFFFF")
        source.shift(UP * 1.5)
        
        # Tokens
        tokens = VGroup()
        token_data = [
            ("x", "#00F0FF", "IDENTIFIER"),
            ("=", "#FF0055", "OPERATOR"),
            ("10", "#FF9F00", "NUMBER"),
            ("+", "#FF0055", "OPERATOR"),
            ("5", "#FF9F00", "NUMBER")
        ]
        
        for i, (text, color, label) in enumerate(token_data):
            box = Rectangle(width=1, height=0.8, color=color, stroke_width=3)
            token_text = Text(text, font_size=28, color=color, font="Monospace")
            token_text.move_to(box)
            label_text = Text(label, font_size=12, color=color)
            label_text.next_to(box, DOWN, buff=0.1)
            
            token_group = VGroup(box, token_text, label_text)
            token_group.shift(LEFT * 4 + RIGHT * i * 2 + DOWN * 1)
            tokens.add(token_group)
        
        self.play(Write(title, run_time=2.5))
        self.wait(1.5)
        self.play(Write(source, run_time=2))
        self.wait(2)
        
        # Break down into tokens with scanning effect
        for i, char_group in enumerate(tokens):
            # Highlight corresponding part in source
            highlight = Rectangle(
                width=0.5,
                height=0.6,
                color=token_data[i][1],
                fill_opacity=0.2,
                stroke_width=2
            )
            highlight.move_to(source).shift(LEFT * 1.5 + RIGHT * i * 0.6)
            
            self.play(Create(highlight, run_time=0.5))
            self.play(
                TransformFromCopy(highlight, char_group, run_time=1.5),
                FadeOut(highlight, run_time=1)
            )
            self.wait(0.8)
        
        self.wait(4)


# ========================================
# PART 7: TOKEN STREAM VISUALIZATION (13-25s)
# ========================================
class Part7(Scene):
    def construct(self):
        
        title = Text("Token Stream", font_size=44, color="#00F0FF")
        title.to_edge(UP, buff=0.5)
        
        # Create flowing tokens
        tokens_text = ["IDENT", "OP", "NUM", "OP", "NUM"]
        colors = ["#00F0FF", "#FF0055", "#FF9F00", "#FF0055", "#FF9F00"]
        
        stream = VGroup()
        for i, (tok, col) in enumerate(zip(tokens_text, colors)):
            circle = Circle(radius=0.5, color=col, fill_opacity=0.3, stroke_width=4)
            text = Text(tok, font_size=18, color=col, weight=BOLD)
            text.move_to(circle)
            token = VGroup(circle, text)
            token.shift(LEFT * 6 + RIGHT * i * 2.5)
            stream.add(token)
        
        # Arrow path
        path_arrow = Arrow(
            start=LEFT * 6,
            end=RIGHT * 6,
            color="#FF9F00",
            stroke_width=3,
            buff=0
        )
        path_arrow.shift(DOWN * 1)
        
        self.play(Write(title, run_time=2))
        self.wait(1.5)
        self.play(Create(path_arrow, run_time=2))
        self.wait(1)
        
        # Tokens flow in
        for token in stream:
            token.shift(DOWN * 1)
            self.play(
                FadeIn(token, shift=RIGHT*0.5, run_time=1),
                token.animate.set_opacity(1)
            )
            self.wait(0.5)
        
        self.wait(2)
        
        # Flow animation
        self.play(
            stream.animate.shift(RIGHT * 3),
            run_time=3,
            rate_func=smooth
        )
        self.wait(3)


# ========================================
# PART 8: SYNTAX ANALYSIS - PARSING (13-25s)
# ========================================
class Part8(Scene):
    def construct(self):
        
        title = Text("Step 2: Syntax Analysis (Parsing)", font_size=38, color="#FF0055")
        title.to_edge(UP, buff=0.4)
        
        subtitle = Text("Building the Parse Tree", font_size=28, color="#FFFFFF")
        subtitle.next_to(title, DOWN, buff=0.3)
        
        # Parse tree structure
        # Root: Assignment
        root = Circle(radius=0.5, color="#FF0055", stroke_width=4)
        root_text = Text("=", font_size=28, color="#FF0055", weight=BOLD)
        root_text.move_to(root)
        root_node = VGroup(root, root_text)
        root_node.shift(UP * 0.5)
        
        # Left child: Variable
        left_child = Circle(radius=0.4, color="#00F0FF", stroke_width=3)
        left_text = Text("x", font_size=24, color="#00F0FF")
        left_text.move_to(left_child)
        left_node = VGroup(left_child, left_text)
        left_node.shift(LEFT * 2.5 + DOWN * 1.5)
        
        # Right child: Addition
        right_child = Circle(radius=0.4, color="#FF9F00", stroke_width=3)
        right_text = Text("+", font_size=24, color="#FF9F00")
        right_text.move_to(right_child)
        right_node = VGroup(right_child, right_text)
        right_node.shift(RIGHT * 1 + DOWN * 1.5)
        
        # Right-right children: Numbers
        num1 = Circle(radius=0.35, color="#00F0FF", stroke_width=3)
        num1_text = Text("10", font_size=20, color="#00F0FF")
        num1_text.move_to(num1)
        num1_node = VGroup(num1, num1_text)
        num1_node.shift(LEFT * 0 + DOWN * 3)
        
        num2 = Circle(radius=0.35, color="#00F0FF", stroke_width=3)
        num2_text = Text("5", font_size=20, color="#00F0FF")
        num2_text.move_to(num2)
        num2_node = VGroup(num2, num2_text)
        num2_node.shift(RIGHT * 2 + DOWN * 3)
        
        # Edges
        edge1 = Line(root.get_bottom(), left_child.get_top(), color="#FFFFFF", stroke_width=2)
        edge2 = Line(root.get_bottom(), right_child.get_top(), color="#FFFFFF", stroke_width=2)
        edge3 = Line(right_child.get_bottom(), num1.get_top(), color="#FFFFFF", stroke_width=2)
        edge4 = Line(right_child.get_bottom(), num2.get_top(), color="#FFFFFF", stroke_width=2)
        
        self.play(Write(title, run_time=2))
        self.play(Write(subtitle, run_time=1.5))
        self.wait(2)
        
        # Build tree top-down
        self.play(FadeIn(root_node, scale=0.5, run_time=1.5))
        self.wait(1)
        
        self.play(
            Create(edge1, run_time=1.2),
            Create(edge2, run_time=1.2)
        )
        self.play(
            FadeIn(left_node, shift=DOWN*0.3, run_time=1.2),
            FadeIn(right_node, shift=DOWN*0.3, run_time=1.2)
        )
        self.wait(1.5)
        
        self.play(
            Create(edge3, run_time=1),
            Create(edge4, run_time=1)
        )
        self.play(
            FadeIn(num1_node, shift=DOWN*0.3, run_time=1),
            FadeIn(num2_node, shift=DOWN*0.3, run_time=1)
        )
        self.wait(3)
        
        # Highlight the tree structure
        tree = VGroup(edge1, edge2, edge3, edge4, root_node, left_node, right_node, num1_node, num2_node)
        self.play(
            tree.animate.set_stroke(width=5),
            run_time=1.5,
            rate_func=there_and_back
        )
        self.wait(3)


# ========================================
# PART 9: ABSTRACT SYNTAX TREE (13-25s)
# ========================================
class Part9(ThreeDScene):
    def construct(self):
        
        title = Text("Abstract Syntax Tree (AST)", font_size=42, color="#00F0FF")
        title.to_edge(UP, buff=0.5)
        self.add_fixed_in_frame_mobjects(title)
        
        # 3D tree structure
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)
        
        # Create nodes with depth
        root_sphere = Sphere(radius=0.3, resolution=(20, 20))
        root_sphere.set_color("#FF0055")
        root_sphere.shift(UP * 1)
        
        left_sphere = Sphere(radius=0.25, resolution=(20, 20))
        left_sphere.set_color("#00F0FF")
        left_sphere.shift(LEFT * 1.5 + DOWN * 0.5)
        
        right_sphere = Sphere(radius=0.25, resolution=(20, 20))
        right_sphere.set_color("#FF9F00")
        right_sphere.shift(RIGHT * 1.5 + DOWN * 0.5)
        
        child1 = Sphere(radius=0.2, resolution=(20, 20))
        child1.set_color("#00F0FF")
        child1.shift(RIGHT * 0.8 + DOWN * 2)
        
        child2 = Sphere(radius=0.2, resolution=(20, 20))
        child2.set_color("#00F0FF")
        child2.shift(RIGHT * 2.2 + DOWN * 2)
        
        # Connecting lines in 3D
        line1 = Line3D(start=root_sphere.get_center(), end=left_sphere.get_center(), color="#FFFFFF", thickness=0.02)
        line2 = Line3D(start=root_sphere.get_center(), end=right_sphere.get_center(), color="#FFFFFF", thickness=0.02)
        line3 = Line3D(start=right_sphere.get_center(), end=child1.get_center(), color="#FFFFFF", thickness=0.02)
        line4 = Line3D(start=right_sphere.get_center(), end=child2.get_center(), color="#FFFFFF", thickness=0.02)
        
        tree_3d = VGroup(line1, line2, line3, line4, root_sphere, left_sphere, right_sphere, child1, child2)
        
        self.wait(1)
        self.play(FadeIn(root_sphere, scale=0.5, run_time=2))
        self.wait(1)
        
        self.play(
            Create(line1, run_time=1.5),
            Create(line2, run_time=1.5)
        )
        self.play(
            FadeIn(left_sphere, shift=DOWN*0.2, run_time=1.5),
            FadeIn(right_sphere, shift=DOWN*0.2, run_time=1.5)
        )
        self.wait(1.5)
        
        self.play(
            Create(line3, run_time=1.2),
            Create(line4, run_time=1.2)
        )
        self.play(
            FadeIn(child1, shift=DOWN*0.2, run_time=1.2),
            FadeIn(child2, shift=DOWN*0.2, run_time=1.2)
        )
        self.wait(2)
        
        # Rotate the tree
        self.play(
            Rotate(tree_3d, angle=2*PI, axis=UP, run_time=5, rate_func=smooth)
        )
        self.wait(3)


# ========================================
# PART 10: SEMANTIC ANALYSIS (13-25s)
# ========================================
class Part10(Scene):
    def construct(self):
        
        title = Text("Step 3: Semantic Analysis", font_size=42, color="#FF9F00")
        title.to_edge(UP, buff=0.5)
        
        subtitle = Text("Checking Meaning & Types", font_size=30, color="#FFFFFF")
        subtitle.next_to(title, DOWN, buff=0.3)
        
        # Example checks
        checks = VGroup()
        check_items = [
            ("✓ Variable declared?", "#00F0FF"),
            ("✓ Type compatible?", "#00F0FF"),
            ("✓ Scope valid?", "#00F0FF"),
            ("✗ Division by zero?", "#FF0055")
        ]
        
        for i, (text, color) in enumerate(check_items):
            check = Text(text, font_size=32, color=color, weight=BOLD)
            check.shift(UP * (1 - i * 0.8))
            checks.add(check)
        
        # Visualization of type checking
        var_box = Rectangle(width=2, height=1, color="#00F0FF", stroke_width=3)
        var_box.shift(LEFT * 3 + DOWN * 1.5)
        var_text = Text("x: int", font_size=24, color="#FFFFFF")
        var_text.move_to(var_box)
        
        value_box = Rectangle(width=2, height=1, color="#00F0FF", stroke_width=3)
        value_box.shift(RIGHT * 3 + DOWN * 1.5)
        value_text = Text("15: int", font_size=24, color="#FFFFFF")
        value_text.move_to(value_box)
        
        check_arrow = DoubleArrow(
            start=var_box.get_right(),
            end=value_box.get_left(),
            color="#FF9F00",
            stroke_width=4,
            buff=0.2
        )
        check_label = Text("Type Match!", font_size=28, color="#FF9F00", weight=BOLD)
        check_label.next_to(check_arrow, UP, buff=0.2)
        
        self.play(Write(title, run_time=2))
        self.play(Write(subtitle, run_time=1.5))
        self.wait(2)
        
        for check in checks:
            self.play(Write(check, run_time=1.5))
            self.wait(0.8)
        
        self.wait(2)
        
        self.play(
            FadeOut(checks),
            run_time=1.5
        )
        
        self.play(
            FadeIn(var_box, shift=RIGHT*0.3, run_time=1.5),
            Write(var_text, run_time=1.5)
        )
        self.wait(1)
        
        self.play(
            FadeIn(value_box, shift=LEFT*0.3, run_time=1.5),
            Write(value_text, run_time=1.5)
        )
        self.wait(1.5)
        
        self.play(GrowArrow(check_arrow, run_time=2))
        self.play(Write(check_label, run_time=1.5))
        self.wait(3)


# ========================================
# PART 11: INTERMEDIATE REPRESENTATION (13-25s)
# ========================================
class Part11(Scene):
    def construct(self):
        
        title = Text("Intermediate Representation (IR)", font_size=40, color="#00F0FF")
        title.to_edge(UP, buff=0.4)
        
        # Three-column comparison
        high_level = VGroup()
        high_title = Text("High-Level", font_size=24, color="#FFFFFF", weight=BOLD)
        high_title.shift(UP * 2.2 + LEFT * 4)
        high_code = Code(
            code_string="x = 10 + 5",
            language="python",
            background="rectangle",
            background_config={"stroke_color": "#00F0FF", "stroke_width": 2},
            add_line_numbers=False
        ).scale(0.6)
        high_code.next_to(high_title, DOWN, buff=0.3)
        high_level.add(high_title, high_code)
        
        ir_rep = VGroup()
        ir_title = Text("IR (3-Address)", font_size=24, color="#FF9F00", weight=BOLD)
        ir_title.shift(UP * 2.2)
        ir_lines = VGroup(
            Text("t1 = 10", font="Monospace", font_size=18, color="#FF9F00"),
            Text("t2 = 5", font="Monospace", font_size=18, color="#FF9F00"),
            Text("t3 = t1 + t2", font="Monospace", font_size=18, color="#FF9F00"),
            Text("x = t3", font="Monospace", font_size=18, color="#FF9F00")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        ir_lines.next_to(ir_title, DOWN, buff=0.3)
        ir_rep.add(ir_title, ir_lines)
        
        low_level = VGroup()
        low_title = Text("Assembly", font_size=24, color="#FF0055", weight=BOLD)
        low_title.shift(UP * 2.2 + RIGHT * 4)
        low_code = VGroup(
            Text("MOV R1, 10", font="Monospace", font_size=16, color="#FF0055"),
            Text("MOV R2, 5", font="Monospace", font_size=16, color="#FF0055"),
            Text("ADD R3, R1, R2", font="Monospace", font_size=16, color="#FF0055"),
            Text("MOV [x], R3", font="Monospace", font_size=16, color="#FF0055")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        low_code.next_to(low_title, DOWN, buff=0.3)
        low_level.add(low_title, low_code)
        
        # Arrows
        arrow1 = Arrow(
            start=high_code.get_right() + RIGHT * 0.2,
            end=ir_lines.get_left() + LEFT * 0.2,
            color="#FF9F00",
            stroke_width=3,
            buff=0.1
        )
        arrow2 = Arrow(
            start=ir_lines.get_right() + RIGHT * 0.2,
            end=low_code.get_left() + LEFT * 0.2,
            color="#FF9F00",
            stroke_width=3,
            buff=0.1
        )
        
        self.play(Write(title, run_time=2.5))
        self.wait(2)
        
        self.play(
            Write(high_title, run_time=1.5),
            FadeIn(high_code, run_time=2)
        )
        self.wait(2)
        
        self.play(GrowArrow(arrow1, run_time=1.5))
        self.play(
            Write(ir_title, run_time=1.5),
            LaggedStart(*[Write(line) for line in ir_lines], lag_ratio=0.3, run_time=2.5)
        )
        self.wait(2)
        
        self.play(GrowArrow(arrow2, run_time=1.5))
        self.play(
            Write(low_title, run_time=1.5),
            LaggedStart(*[Write(line) for line in low_code], lag_ratio=0.3, run_time=2.5)
        )
        self.wait(4)


# ========================================
# PART 12: OPTIMIZATION STAGE (13-25s)
# ========================================
class Part12(Scene):
    def construct(self):
        
        title = Text("Code Optimization", font_size=44, color="#FF9F00")
        title.to_edge(UP, buff=0.5)
        
        # Before optimization
        before_label = Text("Before", font_size=32, color="#FF0055", weight=BOLD)
        before_label.shift(UP * 1.8 + LEFT * 3.5)
        
        before_code = VGroup(
            Text("t1 = 10", font="Monospace", font_size=24, color="#FFFFFF"),
            Text("t2 = 5", font="Monospace", font_size=24, color="#FFFFFF"),
            Text("t3 = t1 + t2", font="Monospace", font_size=24, color="#FFFFFF"),
            Text("x = t3", font="Monospace", font_size=24, color="#FFFFFF")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        before_code.next_to(before_label, DOWN, buff=0.5)
        
        # After optimization
        after_label = Text("After", font_size=32, color="#00F0FF", weight=BOLD)
        after_label.shift(UP * 1.8 + RIGHT * 3.5)
        
        after_code = VGroup(
            Text("x = 15", font="Monospace", font_size=28, color="#00F0FF", weight=BOLD)
        )
        after_code.next_to(after_label, DOWN, buff=0.5)
        
        # Transformation arrow
        transform_arrow = Arrow(
            start=before_code.get_right() + RIGHT * 0.3,
            end=after_code.get_left() + LEFT * 0.3,
            color="#FF9F00",
            stroke_width=5,
            buff=0.2
        )
        
        optimize_label = Text("Constant Folding", font_size=20, color="#FF9F00")
        optimize_label.next_to(transform_arrow, UP, buff=0.2)
        
        # Speedometer visualization
        speedometer = Arc(
            radius=1.2,
            start_angle=PI,
            angle=PI,
            color="#1E2A45",
            stroke_width=8
        )
        speedometer.shift(DOWN * 1.8)
        
        needle = Line(ORIGIN, UP * 1, color="#FF0055", stroke_width=4)
        needle.shift(DOWN * 1.8)
        
        speed_text = Text("Efficiency", font_size=24, color="#FFFFFF")
        speed_text.next_to(speedometer, DOWN, buff=0.3)
        
        self.play(Write(title, run_time=2))
        self.wait(1.5)
        
        self.play(
            Write(before_label, run_time=1.5),
            LaggedStart(*[Write(line) for line in before_code], lag_ratio=0.2, run_time=2.5)
        )
        self.wait(2)
        
        self.play(
            GrowArrow(transform_arrow, run_time=2),
            Write(optimize_label, run_time=2)
        )
        self.wait(1.5)
        
        self.play(
            Write(after_label, run_time=1.5),
            Write(after_code, run_time=2)
        )
        self.wait(2)
        
        # Show efficiency gain
        self.play(
            Create(speedometer, run_time=1.5),
            Write(speed_text, run_time=1.5)
        )
        self.play(Create(needle, run_time=1))
        self.play(
            Rotate(needle, angle=PI*0.7, about_point=needle.get_start(), run_time=2.5, rate_func=smooth)
        )
        self.wait(3)


# ========================================
# PART 13: CODE GENERATION (13-25s)
# ========================================
class Part13(Scene):
    def construct(self):
        
        title = Text("Code Generation", font_size=44, color="#00F0FF")
        title.to_edge(UP, buff=0.5)
        
        subtitle = Text("Converting to Assembly", font_size=28, color="#FFFFFF")
        subtitle.next_to(title, DOWN, buff=0.3)
        
        # IR to Assembly
        ir_box = Rectangle(width=3, height=3, color="#FF9F00", stroke_width=4)
        ir_box.shift(LEFT * 4 + DOWN * 0.5)
        ir_label = Text("IR", font_size=32, color="#FF9F00", weight=BOLD)
        ir_label.move_to(ir_box)
        
        asm_box = Rectangle(width=3, height=3, color="#FF0055", stroke_width=4)
        asm_box.shift(RIGHT * 4 + DOWN * 0.5)
        asm_label = Text("Assembly", font_size=28, color="#FF0055", weight=BOLD)
        asm_label.move_to(asm_box)
        
        # Generator machine in the middle
        generator = VGroup()
        gear1 = Circle(radius=0.6, color="#00F0FF", stroke_width=4)
        gear2 = Circle(radius=0.4, color="#00F0FF", stroke_width=4)
        gear2.shift(RIGHT * 0.7 + UP * 0.5)
        
        # Gear teeth (simplified)
        teeth1 = VGroup(*[
            Line(ORIGIN, ORIGIN + UP * 0.2, color="#00F0FF", stroke_width=3)
            .rotate(i * PI / 4, about_point=ORIGIN)
            for i in range(8)
        ])
        teeth1.move_to(gear1)
        
        gen_label = Text("Code\nGenerator", font_size=18, color="#FFFFFF")
        gen_label.next_to(gear1, DOWN, buff=0.5)
        
        generator.add(gear1, gear2, teeth1, gen_label)
        generator.shift(DOWN * 0.5)
        
        # Arrows
        input_arrow = Arrow(
            start=ir_box.get_right(),
            end=gear1.get_left(),
            color="#FF9F00",
            stroke_width=4,
            buff=0.1
        )
        
        output_arrow = Arrow(
            start=gear1.get_right(),
            end=asm_box.get_left(),
            color="#FF0055",
            stroke_width=4,
            buff=0.1
        )
        
        self.play(Write(title, run_time=2))
        self.play(Write(subtitle, run_time=1.5))
        self.wait(2)
        
        self.play(
            Create(ir_box, run_time=1.5),
            Write(ir_label, run_time=1.5)
        )
        self.wait(1)
        
        self.play(GrowArrow(input_arrow, run_time=1.5))
        self.play(
            FadeIn(generator, scale=0.8, run_time=2)
        )
        self.wait(1)
        
        # Animate gears turning
        self.play(
            Rotate(gear1, angle=2*PI, run_time=3, rate_func=linear),
            Rotate(teeth1, angle=2*PI, run_time=3, rate_func=linear),
            Rotate(gear2, angle=-3*PI, run_time=3, rate_func=linear)
        )
        self.wait(1)
        
        self.play(GrowArrow(output_arrow, run_time=1.5))
        self.play(
            Create(asm_box, run_time=1.5),
            Write(asm_label, run_time=1.5)
        )
        self.wait(3)


# ========================================
# PART 14: ASSEMBLY LANGUAGE (13-25s)
# ========================================
class Part14(Scene):
    def construct(self):
        
        title = Text("Assembly Language", font_size=44, color="#FF0055")
        title.to_edge(UP, buff=0.5)
        
        # Assembly instructions with explanations
        instructions = VGroup()
        
        inst_data = [
            ("MOV R1, 10", "Load 10 into register R1", "#00F0FF"),
            ("MOV R2, 5", "Load 5 into register R2", "#00F0FF"),
            ("ADD R3, R1, R2", "Add R1 and R2, store in R3", "#FF9F00"),
            ("MOV [x], R3", "Store R3 value at memory address x", "#FF0055")
        ]
        
        for i, (inst, desc, color) in enumerate(inst_data):
            inst_text = Text(inst, font="Monospace", font_size=26, color=color, weight=BOLD)
            desc_text = Text(desc, font_size=18, color="#FFFFFF")
            
            inst_text.shift(UP * (1.5 - i * 1) + LEFT * 2)
            desc_text.next_to(inst_text, RIGHT, buff=0.5)
            
            group = VGroup(inst_text, desc_text)
            instructions.add(group)
        
        # Register visualization
        register_label = Text("Registers", font_size=28, color="#00F0FF", weight=BOLD)
        register_label.shift(DOWN * 2.5 + LEFT * 4)
        
        registers = VGroup()
        reg_names = ["R1", "R2", "R3"]
        reg_values = ["10", "5", "15"]
        
        for i, (name, val) in enumerate(zip(reg_names, reg_values)):
            reg_box = Rectangle(width=1.5, height=0.6, color="#00F0FF", stroke_width=3)
            reg_name = Text(name, font_size=20, color="#00F0FF")
            reg_val = Text(val, font_size=20, color="#FF9F00", weight=BOLD)
            
            reg_box.shift(DOWN * 2.5 + LEFT * 4 + RIGHT * i * 1.8 + DOWN * 0.7)
            reg_name.move_to(reg_box).shift(LEFT * 0.4)
            reg_val.move_to(reg_box).shift(RIGHT * 0.3)
            
            registers.add(VGroup(reg_box, reg_name, reg_val))
        
        self.play(Write(title, run_time=2))
        self.wait(2)
        
        for i, instruction in enumerate(instructions):
            self.play(Write(instruction, run_time=2))
            self.wait(1.5)
            
            # Show register update when relevant
            if i == 0:
                self.play(
                    Write(register_label, run_time=1),
                    FadeIn(registers[0], shift=UP*0.2, run_time=1.5)
                )
            elif i == 1:
                self.play(FadeIn(registers[1], shift=UP*0.2, run_time=1.5))
            elif i == 2:
                self.play(FadeIn(registers[2], shift=UP*0.2, run_time=1.5))
                # Highlight the operation
                self.play(
                    registers[2][2].animate.scale(1.3),
                    run_time=0.8,
                    rate_func=there_and_back
                )
            
            self.wait(1)
        
        self.wait(3)


# ========================================
# PART 15: MACHINE CODE TRANSLATION (13-25s)
# ========================================
class Part15(Scene):
    def construct(self):
        
        title = Text("Assembly → Machine Code", font_size=40, color="#00F0FF")
        title.to_edge(UP, buff=0.4)
        
        # Assembly on left
        asm_label = Text("Assembly", font_size=28, color="#FF0055", weight=BOLD)
        asm_label.shift(UP * 2 + LEFT * 4)
        
        asm_code = VGroup(
            Text("MOV R1, 10", font="Monospace", font_size=22, color="#FF0055"),
            Text("ADD R3, R1, R2", font="Monospace", font_size=22, color="#FF0055")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        asm_code.next_to(asm_label, DOWN, buff=0.5)
        
        # Machine code on right
        machine_label = Text("Machine Code", font_size=28, color="#00F0FF", weight=BOLD)
        machine_label.shift(UP * 2 + RIGHT * 3.5)
        
        machine_code = VGroup(
            Text("10110001 00001010", font="Monospace", font_size=20, color="#00F0FF"),
            Text("00000011 11000010", font="Monospace", font_size=20, color="#00F0FF")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        machine_code.next_to(machine_label, DOWN, buff=0.5)
        
        # Binary conversion visualization
        conversion_arrows = VGroup()
        for i in range(2):
            arrow = Arrow(
                start=asm_code[i].get_right() + RIGHT * 0.2,
                end=machine_code[i].get_left() + LEFT * 0.2,
                color="#FF9F00",
                stroke_width=3,
                buff=0.1
            )
            conversion_arrows.add(arrow)
        
        # CPU chip
        cpu = VGroup()
        chip_rect = RoundedRectangle(
            width=2.5,
            height=2,
            corner_radius=0.2,
            color="#00F0FF",
            stroke_width=4,
            fill_opacity=0.1
        )
        chip_rect.shift(DOWN * 1.8)
        
        chip_label = Text("CPU", font_size=36, color="#00F0FF", weight=BOLD)
        chip_label.move_to(chip_rect)
        
        # Pins
        pins = VGroup()
        for i in range(6):
            pin = Line(ORIGIN, LEFT * 0.3, color="#1E2A45", stroke_width=3)
            pin.next_to(chip_rect, LEFT, buff=0).shift(UP * (1 - i * 0.4))
            pins.add(pin)
        
        for i in range(6):
            pin = Line(ORIGIN, RIGHT * 0.3, color="#1E2A45", stroke_width=3)
            pin.next_to(chip_rect, RIGHT, buff=0).shift(UP * (1 - i * 0.4))
            pins.add(pin)
        
        cpu.add(chip_rect, chip_label, pins)
        
        self.play(Write(title, run_time=2.5))
        self.wait(2)
        
        self.play(
            Write(asm_label, run_time=1.5),
            LaggedStart(*[Write(line) for line in asm_code], lag_ratio=0.4, run_time=2)
        )
        self.wait(2)
        
        for i, arrow in enumerate(conversion_arrows):
            self.play(GrowArrow(arrow, run_time=1.5))
            self.wait(0.5)
        
        self.play(
            Write(machine_label, run_time=1.5),
            LaggedStart(*[Write(line) for line in machine_code], lag_ratio=0.4, run_time=2)
        )
        self.wait(2)
        
        self.play(FadeIn(cpu, shift=UP*0.3, run_time=2))
        self.wait(1)
        
        # Binary flows into CPU
        flow_particle = Circle(radius=0.1, color="#FF9F00", fill_opacity=0.8)
        flow_particle.move_to(machine_code[0].get_bottom())
        
        self.play(
            flow_particle.animate.move_to(chip_rect.get_top()),
            run_time=2,
            rate_func=smooth
        )
        self.play(FadeOut(flow_particle, scale=0.5, run_time=0.5))
        
        self.wait(3)


# ========================================
# PART 16: EXECUTION IN CPU (13-25s)
# ========================================
class Part16(ThreeDScene):
    def construct(self):
        
        title = Text("Execution Inside the CPU", font_size=40, color="#FF9F00")
        title.to_edge(UP, buff=0.5)
        self.add_fixed_in_frame_mobjects(title)
        
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)
        
        # 3D CPU components
        # ALU (Arithmetic Logic Unit)
        alu = Cube(side_length=1.5, fill_opacity=0.3, stroke_width=2)
        alu.set_color("#00F0FF")
        alu.shift(LEFT * 2)
        
        alu_label = Text("ALU", font_size=24, color="#00F0FF", weight=BOLD)
        alu_label.move_to(alu)
        self.add_fixed_in_frame_mobjects(alu_label)
        
        # Control Unit
        control = Cube(side_length=1.2, fill_opacity=0.3, stroke_width=2)
        control.set_color("#FF0055")
        control.shift(RIGHT * 2 + UP * 0.5)
        
        control_label = Text("Control\nUnit", font_size=20, color="#FF0055", weight=BOLD)
        control_label.move_to(control)
        self.add_fixed_in_frame_mobjects(control_label)
        
        # Registers
        reg1 = Cube(side_length=0.7, fill_opacity=0.4, stroke_width=2)
        reg1.set_color("#FF9F00")
        reg1.shift(DOWN * 1.5 + LEFT * 1)
        
        reg2 = Cube(side_length=0.7, fill_opacity=0.4, stroke_width=2)
        reg2.set_color("#FF9F00")
        reg2.shift(DOWN * 1.5 + RIGHT * 1)
        
        # Data flow lines
        flow1 = Line3D(
            start=reg1.get_center() + UP * 0.35,
            end=alu.get_center() + DOWN * 0.75,
            color="#00F0FF",
            thickness=0.02
        )
        
        flow2 = Line3D(
            start=reg2.get_center() + UP * 0.35,
            end=alu.get_center() + DOWN * 0.75,
            color="#00F0FF",
            thickness=0.02
        )
        
        control_flow = Line3D(
            start=control.get_center() + DOWN * 0.6,
            end=alu.get_center() + UP * 0.75,
            color="#FF0055",
            thickness=0.02
        )
        
        cpu_3d = VGroup(alu, control, reg1, reg2)
        
        self.wait(1.5)
        
        self.play(FadeIn(alu, scale=0.8, run_time=2))
        self.wait(1)
        
        self.play(FadeIn(control, scale=0.8, run_time=2))
        self.wait(1)
        
        self.play(
            FadeIn(reg1, shift=UP*0.3, run_time=1.5),
            FadeIn(reg2, shift=UP*0.3, run_time=1.5)
        )
        self.wait(1.5)
        
        # Show data flow
        self.play(
            Create(flow1, run_time=2),
            Create(flow2, run_time=2)
        )
        self.wait(1)
        
        self.play(Create(control_flow, run_time=2))
        self.wait(2)
        
        # Rotate to show 3D structure
        self.play(
            Rotate(cpu_3d, angle=PI, axis=UP, run_time=4, rate_func=smooth)
        )
        self.wait(3)


# ========================================
# PART 17: FETCH-DECODE-EXECUTE CYCLE (13-25s)
# ========================================
class Part17(Scene):
    def construct(self):
        
        title = Text("The CPU Cycle", font_size=44, color="#00F0FF")
        title.to_edge(UP, buff=0.5)
        
        # Circular cycle diagram
        radius = 2
        center = ORIGIN
        
        # Three stages
        fetch = Circle(radius=0.8, color="#00F0FF", fill_opacity=0.2, stroke_width=4)
        fetch.shift(UP * radius)
        fetch_text = Text("FETCH", font_size=24, color="#00F0FF", weight=BOLD)
        fetch_text.move_to(fetch)
        
        decode = Circle(radius=0.8, color="#FF0055", fill_opacity=0.2, stroke_width=4)
        decode.shift(DOWN * radius * 0.5 + LEFT * radius * 0.866)
        decode_text = Text("DECODE", font_size=22, color="#FF0055", weight=BOLD)
        decode_text.move_to(decode)
        
        execute = Circle(radius=0.8, color="#FF9F00", fill_opacity=0.2, stroke_width=4)
        execute.shift(DOWN * radius * 0.5 + RIGHT * radius * 0.866)
        execute_text = Text("EXECUTE", font_size=22, color="#FF9F00", weight=BOLD)
        execute_text.move_to(execute)
        
        # Cycle arrows
        arrow1 = CurvedArrow(
            start_point=fetch.get_bottom() + LEFT * 0.3,
            end_point=decode.get_top() + RIGHT * 0.2,
            color="#FFFFFF",
            stroke_width=4
        )
        
        arrow2 = CurvedArrow(
            start_point=decode.get_right() + UP * 0.2,
            end_point=execute.get_left() + UP * 0.2,
            color="#FFFFFF",
            stroke_width=4
        )
        
        arrow3 = CurvedArrow(
            start_point=execute.get_top() + LEFT * 0.2,
            end_point=fetch.get_bottom() + RIGHT * 0.3,
            color="#FFFFFF",
            stroke_width=4
        )
        
        cycle = VGroup(fetch, fetch_text, decode, decode_text, execute, execute_text, arrow1, arrow2, arrow3)
        
        # Descriptions
        descriptions = VGroup(
            Text("1. Get instruction from memory", font_size=20, color="#00F0FF"),
            Text("2. Interpret the instruction", font_size=20, color="#FF0055"),
            Text("3. Perform the operation", font_size=20, color="#FF9F00")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        descriptions.shift(DOWN * 2.8)
        
        self.play(Write(title, run_time=2))
        self.wait(2)
        
        # Build cycle
        self.play(
            FadeIn(fetch, scale=0.7, run_time=1.5),
            Write(fetch_text, run_time=1.5)
        )
        self.wait(0.5)
        
        self.play(Create(arrow1, run_time=1.5))
        self.play(
            FadeIn(decode, scale=0.7, run_time=1.5),
            Write(decode_text, run_time=1.5)
        )
        self.wait(0.5)
        
        self.play(Create(arrow2, run_time=1.5))
        self.play(
            FadeIn(execute, scale=0.7, run_time=1.5),
            Write(execute_text, run_time=1.5)
        )
        self.wait(0.5)
        
        self.play(Create(arrow3, run_time=1.5))
        self.wait(2)
        
        # Show descriptions
        for desc in descriptions:
            self.play(Write(desc, run_time=1.5))
            self.wait(0.8)
        
        self.wait(2)
        
        # Animate cycle running
        indicator = Dot(radius=0.15, color="#FF9F00")
        indicator.move_to(fetch)
        self.add(indicator)
        
        for _ in range(2):
            self.play(indicator.animate.move_to(decode), run_time=1.5, rate_func=smooth)
            self.wait(0.3)
            self.play(indicator.animate.move_to(execute), run_time=1.5, rate_func=smooth)
            self.wait(0.3)
            self.play(indicator.animate.move_to(fetch), run_time=1.5, rate_func=smooth)
            self.wait(0.3)
        
        self.wait(2)


# ========================================
# PART 18: COMPILED VS INTERPRETED (13-25s)
# ========================================
class Part18(Scene):
    def construct(self):
        
        title = Text("Two Paths: Compiled vs Interpreted", font_size=36, color="#00F0FF")
        title.to_edge(UP, buff=0.4)
        
        # Compiled path (top)
        compiled_label = Text("COMPILED (C, C++)", font_size=28, color="#00F0FF", weight=BOLD)
        compiled_label.shift(UP * 2 + LEFT * 3)
        
        compiled_boxes = VGroup()
        comp_stages = ["Source", "Compiler", "Machine\nCode", "Execute"]
        for i, stage in enumerate(comp_stages):
            box = Rectangle(width=1.5, height=0.8, color="#00F0FF", stroke_width=3)
            text = Text(stage, font_size=16, color="#00F0FF")
            text.move_to(box)
            group = VGroup(box, text)
            group.shift(UP * 0.8 + LEFT * 3.5 + RIGHT * i * 2)
            compiled_boxes.add(group)
        
        comp_arrows = VGroup()
        for i in range(len(compiled_boxes) - 1):
            arrow = Arrow(
                start=compiled_boxes[i].get_right(),
                end=compiled_boxes[i+1].get_left(),
                color="#00F0FF",
                stroke_width=2,
                buff=0.05
            )
            comp_arrows.add(arrow)
        
        # Interpreted path (bottom)
        interpreted_label = Text("INTERPRETED (Python, JS)", font_size=28, color="#FF0055", weight=BOLD)
        interpreted_label.shift(DOWN * 0.5 + LEFT * 3)
        
        interpreted_boxes = VGroup()
        interp_stages = ["Source", "Interpreter", "Execute\nLine-by-Line"]
        for i, stage in enumerate(interp_stages):
            box = Rectangle(width=1.8, height=0.8, color="#FF0055", stroke_width=3)
            text = Text(stage, font_size=16, color="#FF0055")
            text.move_to(box)
            group = VGroup(box, text)
            group.shift(DOWN * 1.7 + LEFT * 3 + RIGHT * i * 2.5)
            interpreted_boxes.add(group)
        
        interp_arrows = VGroup()
        for i in range(len(interpreted_boxes) - 1):
            arrow = Arrow(
                start=interpreted_boxes[i].get_right(),
                end=interpreted_boxes[i+1].get_left(),
                color="#FF0055",
                stroke_width=2,
                buff=0.05
            )
            interp_arrows.add(arrow)
        
        # Loop back arrow for interpreter
        loop_arrow = CurvedArrow(
            start_point=interpreted_boxes[2].get_bottom() + DOWN * 0.3,
            end_point=interpreted_boxes[1].get_bottom() + DOWN * 0.3,
            color="#FF9F00",
            stroke_width=3,
            angle=-TAU/4
        )
        loop_label = Text("Repeat", font_size=14, color="#FF9F00")
        loop_label.next_to(loop_arrow, DOWN, buff=0.1)
        
        self.play(Write(title, run_time=2.5))
        self.wait(2)
        
        # Build compiled path
        self.play(Write(compiled_label, run_time=1.5))
        self.wait(1)
        
        for i, box in enumerate(compiled_boxes):
            self.play(FadeIn(box, shift=DOWN*0.2, run_time=1))
            if i < len(comp_arrows):
                self.play(GrowArrow(comp_arrows[i], run_time=0.8))
            self.wait(0.5)
        
        self.wait(2)
        
        # Build interpreted path
        self.play(Write(interpreted_label, run_time=1.5))
        self.wait(1)
        
        for i, box in enumerate(interpreted_boxes):
            self.play(FadeIn(box, shift=DOWN*0.2, run_time=1))
            if i < len(interp_arrows):
                self.play(GrowArrow(interp_arrows[i], run_time=0.8))
            self.wait(0.5)
        
        self.wait(1.5)
        
        self.play(
            Create(loop_arrow, run_time=2),
            Write(loop_label, run_time=1.5)
        )
        self.wait(3)


# ========================================
# PART 19: THE COMPLETE JOURNEY (13-25s)
# ========================================
class Part19(Scene):
    def construct(self):
        
        title = Text("The Complete Journey", font_size=44, color="#FF9F00")
        title.to_edge(UP, buff=0.2)
        
        # Vertical flowchart
        stages = VGroup()
        stage_data = [
            ("Source Code", "#FFFFFF", "print('Hello')"),
            ("↓ Lexer", "#00F0FF", "Tokens"),
            ("↓ Parser", "#FF0055", "AST"),
            ("↓ Semantic", "#FF9F00", "Type Check"),
            ("↓ IR Gen", "#00F0FF", "Intermediate"),
            ("↓ Optimize", "#FF0055", "Faster Code"),
            ("↓ Code Gen", "#FF9F00", "Assembly"),
            ("↓ Assemble", "#00F0FF", "Machine Code"),
            ("CPU Execute", "#FF0055", "01010101...")
        ]
        
        for i, (stage_name, color, detail) in enumerate(stage_data):
            # Clean stage name (remove arrow if present)
            clean_name = stage_name.replace("↓ ", "")
            
            box = RoundedRectangle(width=6.0, height=0.65, corner_radius=0.1, color=color, stroke_width=3)
            stage_text = Text(clean_name, font_size=24, color=color, weight=BOLD)
            detail_text = Text(detail, font_size=18, color="#FFFFFF", font="Monospace")
            
            # Align text inside box
            stage_text.next_to(box.get_left(), RIGHT, buff=0.4)
            detail_text.next_to(box.get_right(), LEFT, buff=0.4)
            
            group = VGroup(box, stage_text, detail_text)
            stages.add(group)
            
        stages.arrange(DOWN, buff=0.15)
        stages.next_to(title, DOWN, buff=0.5)
        
        self.play(Write(title, run_time=2.5))
        self.wait(2)
        
        # Animate journey
        for i, stage in enumerate(stages):
            if i % 2 == 0:  # Boxes
                self.play(FadeIn(stage, shift=DOWN*0.3, run_time=1.2))
            else:  # Arrows
                self.play(Write(stage, run_time=0.8))
            self.wait(0.6)
        
        self.wait(2)
        
        # Flow indicator
        flow_dot = Dot(radius=0.12, color="#FF9F00")
        flow_dot.move_to(stages[0])
        self.add(flow_dot)
        
        for stage in stages[1:]:
            self.play(
                flow_dot.animate.move_to(stage),
                run_time=0.8,
                rate_func=smooth
            )
            self.wait(0.3)
        
        # Final pulse
        self.play(
            flow_dot.animate.scale(2).set_opacity(0),
            run_time=1.5
        )
        
        self.wait(3)


# ========================================
# PART 20: OUTRO & SUMMARY (13-25s)
# ========================================
class Part20(Scene):
    def construct(self):
        
        # Main title
        title = Text("From Human to Machine", font_size=52, color="#00F0FF", weight=BOLD)
        title.shift(UP * 2.5)
        
        # Key takeaways
        takeaways = VGroup(
            Text("✓ Computers don't understand code directly", font_size=24, color="#FFFFFF"),
            Text("✓ Multiple translation layers bridge the gap", font_size=24, color="#FFFFFF"),
            Text("✓ Lexer → Parser → Compiler → Assembly → CPU", font_size=24, color="#FFFFFF"),
            Text("✓ Each step transforms closer to machine language", font_size=24, color="#FFFFFF")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        takeaways.shift(DOWN * 0.2)
        
        # Closing visual
        code_icon = Text("{ }", font_size=80, color="#00F0FF", weight=BOLD)
        code_icon.shift(DOWN * 2.8 + LEFT * 3)
        

        
        binary_icon = Text("010101", font_size=60, color="#FF0055", weight=BOLD, font="Monospace")
        binary_icon.shift(DOWN * 2.8 + RIGHT * 3)
        
        footer = Text("Understanding empowers creation", font_size=28, color="#FF9F00", slant=ITALIC)
        footer.to_edge(DOWN, buff=0.5)
        
        # Animations
        self.play(Write(title, run_time=2.5))
        self.wait(2)
        
        for takeaway in takeaways:
            self.play(FadeIn(takeaway, shift=RIGHT*0.3, run_time=1.5))
            self.wait(1)
        
        self.wait(2)
        
        self.play(
            FadeIn(code_icon, scale=0.7, run_time=1.5)
        )
        self.wait(1)
        

        
        self.play(
            FadeIn(binary_icon, scale=0.7, run_time=1.5)
        )
        self.wait(2)
        
        self.play(Write(footer, run_time=2))
        self.wait(3)
        
        # Final fade
        everything = VGroup(title, takeaways, code_icon, binary_icon, footer)
        self.play(FadeOut(everything, run_time=2))
        self.wait(1)