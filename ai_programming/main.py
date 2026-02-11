from manim import *
import numpy as np

# Vibrant Space Tech Color Palette
DEEP_NAVY = "#020B1F"
ELECTRIC_CYAN = "#00F0FF"
NEON_PINK = "#FF0055"
VIBRANT_ORANGE = "#FF9F00"
SUBTLE_NAVY = "#1E2A45"

config.background_color = DEEP_NAVY


class Part1(Scene):
    """The Hook - Can Machines Think in Code? (3-6 seconds)"""
    def construct(self):
        # Main title with glitch effect
        title = Text("Can Machines", font_size=72, color=WHITE, weight=BOLD)
        title2 = Text("Think in Code?", font_size=80, color=ELECTRIC_CYAN, weight=BOLD)
        title_group = VGroup(title, title2).arrange(DOWN, buff=0.3)
        
        # Glitch copies
        glitch1 = title_group.copy().set_color(NEON_PINK).shift(LEFT*0.05 + UP*0.02)
        glitch2 = title_group.copy().set_color(VIBRANT_ORANGE).shift(RIGHT*0.05 + DOWN*0.02)
        
        # Code symbols flying in background
        symbols = VGroup(*[
            Text(s, font_size=30, color=SUBTLE_NAVY).move_to([
                np.random.uniform(-6, 6), np.random.uniform(-3.5, 3.5), 0
            ]) for s in ["def", "if", "for", "class", "{}", "[]", "()", "=>", "==", "//"]
        ])
        
        # Fast animation sequence
        self.add(symbols)
        self.play(
            *[FadeIn(s, shift=UP*0.5) for s in symbols],
            run_time=0.3
        )
        self.play(
            FadeIn(glitch1, scale=1.5),
            FadeIn(glitch2, scale=1.5),
            FadeIn(title_group, scale=1.2),
            run_time=0.5
        )
        self.play(
            glitch1.animate.set_opacity(0),
            glitch2.animate.set_opacity(0),
            run_time=0.3
        )
        
        # Zoom effect
        self.play(
            title_group.animate.scale(0.1).set_opacity(0),
            *[s.animate.scale(3).set_opacity(0) for s in symbols],
            run_time=0.5
        )
        self.wait(0.2)


class Part2(Scene):
    """The LLM Brain - Billions of Parameters (13-20 seconds)"""
    def construct(self):
        title = Text("The AI Brain", font_size=56, color=ELECTRIC_CYAN)
        title.to_edge(UP, buff=0.5)
        
        # Create neural network visualization
        layers = []
        layer_sizes = [4, 6, 8, 6, 4]
        x_positions = [-4, -2, 0, 2, 4]
        
        all_nodes = VGroup()
        all_edges = VGroup()
        
        for i, (size, x) in enumerate(zip(layer_sizes, x_positions)):
            layer = VGroup()
            for j in range(size):
                y = (j - (size-1)/2) * 0.6
                node = Circle(radius=0.15, color=ELECTRIC_CYAN, fill_opacity=0.8)
                node.move_to([x, y, 0])
                node.set_stroke(ELECTRIC_CYAN, width=2)
                layer.add(node)
            layers.append(layer)
            all_nodes.add(layer)
        
        # Create edges between layers
        for i in range(len(layers)-1):
            for node1 in layers[i]:
                for node2 in layers[i+1]:
                    edge = Line(
                        node1.get_center(), node2.get_center(),
                        stroke_width=0.5, color=SUBTLE_NAVY
                    )
                    all_edges.add(edge)
        
        network = VGroup(all_edges, all_nodes).shift(UP*0.5)
        
        subtitle = Text("Billions of Parameters, One Goal", font_size=32, color=WHITE)
        subtitle2 = Text("Understanding Language", font_size=36, color=VIBRANT_ORANGE)
        subtitles = VGroup(subtitle, subtitle2).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        
        # Animations
        self.play(Write(title), run_time=1.5)
        self.play(Create(all_edges), run_time=2)
        self.play(
            *[GrowFromCenter(node) for layer in layers for node in layer],
            run_time=2
        )
        self.wait(1)
        
        # Pulse animation
        for _ in range(2):
            self.play(
                *[node.animate.set_fill(NEON_PINK, opacity=1) for node in layers[0]],
                run_time=0.3
            )
            for i in range(1, len(layers)):
                self.play(
                    *[node.animate.set_fill(ELECTRIC_CYAN, opacity=0.8) for node in layers[i-1]],
                    *[node.animate.set_fill(NEON_PINK, opacity=1) for node in layers[i]],
                    run_time=0.4
                )
            self.play(
                *[node.animate.set_fill(ELECTRIC_CYAN, opacity=0.8) for node in layers[-1]],
                run_time=0.3
            )
        
        self.play(FadeIn(subtitles, shift=UP), run_time=1.5)
        self.wait(3)


class Part3(Scene):
    """The Transformer Architecture (15-20 seconds)"""
    def construct(self):
        title = Text("The Transformer", font_size=52, color=ELECTRIC_CYAN)
        title.to_edge(UP, buff=0.4)
        
        # Architecture blocks
        def create_block(text, color, width=2.5, height=0.7):
            rect = RoundedRectangle(
                corner_radius=0.1, width=width, height=height,
                stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.2
            )
            label = Text(text, font_size=20, color=WHITE)
            return VGroup(rect, label)
        
        # Encoder side
        enc_label = Text("Encoder", font_size=28, color=ELECTRIC_CYAN)
        enc_embed = create_block("Input Embedding", ELECTRIC_CYAN)
        enc_attn = create_block("Self-Attention", NEON_PINK)
        enc_ffn = create_block("Feed Forward", VIBRANT_ORANGE)
        enc_stack = VGroup(enc_embed, enc_attn, enc_ffn).arrange(UP, buff=0.3)
        enc_box = SurroundingRectangle(enc_stack, color=ELECTRIC_CYAN, buff=0.2, stroke_width=2)
        enc_label.next_to(enc_box, UP, buff=0.2)
        encoder = VGroup(enc_label, enc_box, enc_stack).shift(LEFT*2.5)
        
        # Decoder side
        dec_label = Text("Decoder", font_size=28, color=VIBRANT_ORANGE)
        dec_embed = create_block("Output Embedding", ELECTRIC_CYAN)
        dec_attn1 = create_block("Masked Self-Attention", NEON_PINK)
        dec_attn2 = create_block("Cross-Attention", NEON_PINK)
        dec_ffn = create_block("Feed Forward", VIBRANT_ORANGE)
        dec_stack = VGroup(dec_embed, dec_attn1, dec_attn2, dec_ffn).arrange(UP, buff=0.25)
        dec_box = SurroundingRectangle(dec_stack, color=VIBRANT_ORANGE, buff=0.2, stroke_width=2)
        dec_label.next_to(dec_box, UP, buff=0.2)
        decoder = VGroup(dec_label, dec_box, dec_stack).shift(RIGHT*2.5)
        
        # Cross connection arrow
        cross_arrow = Arrow(
            enc_attn.get_right() + RIGHT*0.5, dec_attn2.get_left() + LEFT*0.3,
            color=NEON_PINK, stroke_width=3
        )
        
        architecture = VGroup(encoder, decoder, cross_arrow).shift(DOWN*0.3)
        
        # Animations
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(enc_label), Create(enc_box), run_time=1)
        self.play(
            *[FadeIn(block, shift=UP) for block in enc_stack],
            run_time=2
        )
        self.wait(0.5)
        self.play(FadeIn(dec_label), Create(dec_box), run_time=1)
        self.play(
            *[FadeIn(block, shift=UP) for block in dec_stack],
            run_time=2
        )
        self.play(GrowArrow(cross_arrow), run_time=1.5)
        
        # Highlight flow
        self.play(
            enc_embed[0].animate.set_fill(ELECTRIC_CYAN, opacity=0.8),
            run_time=0.5
        )
        self.play(
            enc_embed[0].animate.set_fill(ELECTRIC_CYAN, opacity=0.2),
            enc_attn[0].animate.set_fill(NEON_PINK, opacity=0.8),
            run_time=0.5
        )
        self.play(
            enc_attn[0].animate.set_fill(NEON_PINK, opacity=0.2),
            cross_arrow.animate.set_color(WHITE),
            dec_attn2[0].animate.set_fill(NEON_PINK, opacity=0.8),
            run_time=0.8
        )
        self.play(
            dec_attn2[0].animate.set_fill(NEON_PINK, opacity=0.2),
            cross_arrow.animate.set_color(NEON_PINK),
            run_time=0.5
        )
        self.wait(3)


class Part4(Scene):
    """The Training Data (15-20 seconds)"""
    def construct(self):
        title = Text("Learning from Code", font_size=52, color=ELECTRIC_CYAN)
        title.to_edge(UP, buff=0.4)
        
        # Data source icons
        def create_source(name, icon_text):
            icon = RoundedRectangle(
                width=1.8, height=1.8, corner_radius=0.2,
                stroke_color=ELECTRIC_CYAN, stroke_width=3,
                fill_color=SUBTLE_NAVY, fill_opacity=0.5
            )
            symbol = Text(icon_text, font_size=36)
            label = Text(name, font_size=18, color=WHITE)
            label.next_to(icon, DOWN, buff=0.2)
            return VGroup(icon, symbol, label)
        
        github = create_source("GitHub", "</>")
        stackoverflow = create_source("StackOverflow", "?!")
        docs = create_source("Documentation", "📄")
        
        sources = VGroup(github, stackoverflow, docs).arrange(RIGHT, buff=1)
        sources.shift(UP*1)
        
        # AI model representation
        model = Circle(radius=1, color=VIBRANT_ORANGE, fill_opacity=0.3, stroke_width=4)
        model_label = Text("AI", font_size=48, color=VIBRANT_ORANGE)
        model_group = VGroup(model, model_label).shift(DOWN*2)
        
        # Code snippets flowing
        code_snippets = [
            "def hello():",
            "for i in range:",
            "class Model:",
            "import numpy",
            "return result"
        ]
        
        flowing_code = VGroup(*[
            Text(code, font_size=16, color=ELECTRIC_CYAN).move_to(
                sources[i % 3].get_center()
            ) for i, code in enumerate(code_snippets)
        ])
        
        stat_text = Text("Billions of Lines of Code", font_size=28, color=NEON_PINK)
        stat_text.to_edge(DOWN, buff=0.5)
        
        # Animations
        self.play(Write(title), run_time=1.5)
        self.play(
            *[FadeIn(source, shift=DOWN) for source in sources],
            run_time=2
        )
        self.play(GrowFromCenter(model_group), run_time=1.5)
        
        # Flow animation
        for i, code in enumerate(flowing_code):
            source_idx = i % 3
            code.move_to(sources[source_idx].get_center())
            self.play(
                code.animate.move_to(model.get_center()).set_opacity(0),
                model.animate.set_fill(opacity=0.3 + (i+1)*0.1),
                run_time=0.8
            )
        
        self.play(
            model.animate.set_stroke(color=WHITE, width=6),
            Flash(model, color=VIBRANT_ORANGE, line_length=0.5),
            run_time=1
        )
        self.play(
            model.animate.set_stroke(color=VIBRANT_ORANGE, width=4),
            FadeIn(stat_text, shift=UP),
            run_time=1.5
        )
        self.wait(3)


class Part5(Scene):
    """Tokenization - Breaking Code into Pieces (15-20 seconds)"""
    def construct(self):
        title = Text("Tokenization", font_size=52, color=ELECTRIC_CYAN)
        title.to_edge(UP, buff=0.4)
        
        # Original code
        code_text = Text('print("Hello, World!")', font_size=36, color=WHITE)
        code_text.shift(UP*1.5)
        
        # Tokens
        tokens = ["print", "(", '"', "Hello", ",", " World", "!", '"', ")"]
        token_colors = [ELECTRIC_CYAN, SUBTLE_NAVY, NEON_PINK, VIBRANT_ORANGE, 
                       SUBTLE_NAVY, VIBRANT_ORANGE, NEON_PINK, NEON_PINK, SUBTLE_NAVY]
        
        token_boxes = VGroup()
        for i, (token, color) in enumerate(zip(tokens, token_colors)):
            box = RoundedRectangle(
                width=max(len(token)*0.25 + 0.4, 0.6), height=0.7,
                corner_radius=0.1, stroke_color=color, stroke_width=3,
                fill_color=color, fill_opacity=0.2
            )
            label = Text(token, font_size=20, color=WHITE)
            token_box = VGroup(box, label)
            token_boxes.add(token_box)
        
        token_boxes.arrange(RIGHT, buff=0.15)
        token_boxes.shift(DOWN*0.5)
        
        # Token IDs
        ids = ["1024", "28", "15", "7592", "11", "3468", "0", "15", "29"]
        id_labels = VGroup(*[
            Text(f"[{id}]", font_size=16, color=SUBTLE_NAVY)
            for id in ids
        ])
        for id_label, token_box in zip(id_labels, token_boxes):
            id_label.next_to(token_box, DOWN, buff=0.2)
        
        explanation = Text("Each token gets a unique ID", font_size=28, color=NEON_PINK)
        explanation.to_edge(DOWN, buff=0.7)
        
        # Animations
        self.play(Write(title), run_time=1.5)
        self.play(Write(code_text), run_time=2)
        self.wait(1)
        
        # Break into tokens
        arrow = Arrow(code_text.get_bottom(), token_boxes.get_top(), color=ELECTRIC_CYAN)
        self.play(GrowArrow(arrow), run_time=1)
        
        self.play(
            *[FadeIn(token_box, shift=DOWN, lag_ratio=0.1) 
              for token_box in token_boxes],
            run_time=2.5
        )
        self.play(FadeOut(arrow), run_time=0.5)
        
        self.play(
            *[FadeIn(id_label, shift=UP) for id_label in id_labels],
            run_time=1.5
        )
        self.play(FadeIn(explanation, shift=UP), run_time=1)
        self.wait(3)


class Part6(ThreeDScene):
    """Embedding - Words to Vectors (15-20 seconds)"""
    def construct(self):
        self.set_camera_orientation(phi=70*DEGREES, theta=-45*DEGREES)
        
        # 3D axes
        axes = ThreeDAxes(
            x_range=[-3, 3], y_range=[-3, 3], z_range=[-3, 3],
            x_length=6, y_length=6, z_length=6,
            axis_config={"color": SUBTLE_NAVY, "stroke_width": 2}
        )
        
        # Title (2D overlay)
        title = Text("Embedding Space", font_size=48, color=ELECTRIC_CYAN)
        title.to_corner(UL, buff=0.5)
        self.add_fixed_in_frame_mobjects(title)
        
        # Token points in 3D space
        token_data = [
            ("def", [1, 1, 2], ELECTRIC_CYAN),
            ("function", [1.2, 0.8, 2.1], ELECTRIC_CYAN),
            ("print", [-1, 1, 0], NEON_PINK),
            ("return", [-0.8, 1.2, -0.2], NEON_PINK),
            ("for", [0, -1, 1], VIBRANT_ORANGE),
            ("while", [0.2, -0.8, 1.1], VIBRANT_ORANGE),
        ]
        
        points = VGroup()
        labels = VGroup()
        for token, pos, color in token_data:
            sphere = Sphere(radius=0.15, resolution=(16, 16))
            sphere.set_color(color)
            sphere.move_to(pos)
            points.add(sphere)
            
            label = Text(token, font_size=18, color=color)
            label.move_to(pos)
            label.shift(UP*0.3 + RIGHT*0.3)
            self.add_fixed_orientation_mobjects(label)
            labels.add(label)
        
        explanation = Text("Similar tokens cluster together", font_size=28, color=WHITE)
        explanation.to_edge(DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(explanation)
        
        # Animations
        self.play(Write(title), run_time=1)
        self.play(Create(axes), run_time=2)
        
        for point, label in zip(points, labels):
            self.play(
                GrowFromCenter(point),
                FadeIn(label),
                run_time=0.6
            )
        
        # Rotate camera
        self.play(FadeIn(explanation), run_time=1)
        self.move_camera(phi=60*DEGREES, theta=45*DEGREES, run_time=4)
        self.wait(2)
        self.move_camera(phi=75*DEGREES, theta=-30*DEGREES, run_time=3)
        self.wait(2)


class Part7(Scene):
    """The Attention Mechanism (18-25 seconds)"""
    def construct(self):
        title = Text("Attention Mechanism", font_size=48, color=ELECTRIC_CYAN)
        title.to_edge(UP, buff=0.3)
        
        # Query, Key, Value matrices
        def create_matrix(name, color):
            rect = Rectangle(width=1.2, height=1.8, stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.2)
            label = Text(name, font_size=24, color=color)
            label.next_to(rect, UP, buff=0.2)
            # Matrix elements
            elements = VGroup(*[
                Text("·", font_size=20, color=WHITE).move_to(rect.get_center() + 
                    [0.3*(j-0.5), 0.5*(1-i), 0])
                for i in range(3) for j in range(2)
            ])
            return VGroup(label, rect, elements)
        
        query = create_matrix("Query", ELECTRIC_CYAN)
        key = create_matrix("Key", NEON_PINK)
        value = create_matrix("Value", VIBRANT_ORANGE)
        
        matrices = VGroup(query, key, value).arrange(RIGHT, buff=1.5)
        matrices.shift(UP*0.5)
        
        # Attention formula
        formula = MathTex(
            r"\text{Attention} = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V",
            font_size=36, color=WHITE
        )
        formula.to_edge(DOWN, buff=1)
        
        # Question text
        question = Text("Which tokens should I focus on?", font_size=28, color=NEON_PINK)
        question.next_to(matrices, DOWN, buff=0.8)
        
        # Animations
        self.play(Write(title), run_time=1.5)
        
        self.play(FadeIn(query, shift=UP), run_time=1)
        self.play(FadeIn(key, shift=UP), run_time=1)
        self.play(FadeIn(value, shift=UP), run_time=1)
        
        self.play(Write(question), run_time=1.5)
        self.wait(1)
        
        # Show interaction
        qk_arrow = Arrow(query[1].get_right(), key[1].get_left(), color=WHITE, stroke_width=2)
        kv_arrow = Arrow(key[1].get_right(), value[1].get_left(), color=WHITE, stroke_width=2)
        
        self.play(GrowArrow(qk_arrow), run_time=1)
        self.play(GrowArrow(kv_arrow), run_time=1)
        
        self.play(Write(formula), run_time=2)
        
        # Highlight formula parts
        self.play(
            formula[0][0:9].animate.set_color(VIBRANT_ORANGE),
            run_time=0.5
        )
        self.play(
            formula[0][0:9].animate.set_color(WHITE),
            run_time=0.5
        )
        self.wait(4)


class Part8(Scene):
    """Self-Attention in Action (18-25 seconds)"""
    def construct(self):
        title = Text("Self-Attention in Action", font_size=48, color=ELECTRIC_CYAN)
        title.to_edge(UP, buff=0.3)
        
        # Code tokens
        tokens = ["def", "calculate", "(", "x", ",", "y", ")", ":"]
        token_boxes = VGroup()
        
        for token in tokens:
            box = RoundedRectangle(
                width=max(len(token)*0.2 + 0.5, 0.6), height=0.6,
                corner_radius=0.1, stroke_color=ELECTRIC_CYAN, stroke_width=2,
                fill_color=SUBTLE_NAVY, fill_opacity=0.5
            )
            label = Text(token, font_size=20, color=WHITE)
            token_boxes.add(VGroup(box, label))
        
        token_boxes.arrange(RIGHT, buff=0.15)
        token_boxes.shift(UP*1)
        
        # Attention lines from "def"
        attention_weights = [1.0, 0.8, 0.1, 0.3, 0.05, 0.25, 0.1, 0.6]
        attention_lines = VGroup()
        
        source = token_boxes[0]  # "def"
        for i, (target, weight) in enumerate(zip(token_boxes, attention_weights)):
            if i == 0:
                continue
            line = Line(
                source.get_bottom(), target.get_top(),
                stroke_width=weight * 6,
                color=NEON_PINK
            )
            line.set_opacity(weight)
            attention_lines.add(line)
        
        # Weight labels
        weight_text = Text("Attention weights show relevance", font_size=24, color=WHITE)
        weight_text.shift(DOWN*1)
        
        # Softmax visualization
        softmax_label = Text("softmax →", font_size=20, color=VIBRANT_ORANGE)
        bars = VGroup()
        for i, weight in enumerate(attention_weights[1:]):
            bar = Rectangle(
                width=0.3, height=weight * 2,
                fill_color=NEON_PINK, fill_opacity=0.8,
                stroke_color=NEON_PINK, stroke_width=1
            )
            bars.add(bar)
        bars.arrange(RIGHT, buff=0.1, aligned_edge=DOWN)
        softmax_group = VGroup(softmax_label, bars).arrange(RIGHT, buff=0.5)
        softmax_group.shift(DOWN*2.5)
        
        # Animations
        self.play(Write(title), run_time=1.5)
        self.play(
            *[FadeIn(box, shift=DOWN) for box in token_boxes],
            run_time=2
        )
        self.wait(1)
        
        # Highlight source token
        self.play(
            token_boxes[0][0].animate.set_stroke(VIBRANT_ORANGE, width=4),
            run_time=0.5
        )
        
        # Show attention lines one by one
        for line in attention_lines:
            self.play(Create(line), run_time=0.4)
        
        self.play(FadeIn(weight_text), run_time=1)
        self.wait(1)
        
        self.play(
            FadeIn(softmax_label),
            *[GrowFromEdge(bar, DOWN) for bar in bars],
            run_time=2
        )
        self.wait(4)


class Part9(Scene):
    """Multi-Head Attention (15-20 seconds)"""
    def construct(self):
        title = Text("Multi-Head Attention", font_size=48, color=ELECTRIC_CYAN)
        title.to_edge(UP, buff=0.3)
        
        # Multiple attention heads
        head_colors = [ELECTRIC_CYAN, NEON_PINK, VIBRANT_ORANGE, "#00FF88"]
        heads = VGroup()
        
        for i, color in enumerate(head_colors):
            head = VGroup()
            rect = RoundedRectangle(
                width=1.5, height=2,
                corner_radius=0.1, stroke_color=color, stroke_width=3,
                fill_color=color, fill_opacity=0.15
            )
            label = Text(f"Head {i+1}", font_size=18, color=color)
            label.move_to(rect.get_top() + DOWN*0.3)
            
            # Mini attention pattern
            dots = VGroup(*[
                Dot(radius=0.05, color=color).move_to(
                    rect.get_center() + [0.3*(j-1), 0.3*(1-k), 0]
                ) for j in range(3) for k in range(3)
            ])
            head.add(rect, label, dots)
            heads.add(head)
        
        heads.arrange(RIGHT, buff=0.5)
        heads.shift(UP*0.5)
        
        # Merge operation
        merge_arrow = Arrow(heads.get_bottom(), DOWN*2, color=WHITE, stroke_width=3)
        
        concat_box = RoundedRectangle(
            width=5, height=0.8,
            corner_radius=0.1, stroke_color=WHITE, stroke_width=3,
            fill_color=SUBTLE_NAVY, fill_opacity=0.5
        )
        concat_label = Text("Concatenate & Project", font_size=20, color=WHITE)
        concat_group = VGroup(concat_box, concat_label).shift(DOWN*2.5)
        
        explanation = Text("Different heads learn different patterns", font_size=24, color=NEON_PINK)
        explanation.to_edge(DOWN, buff=0.5)
        
        # Animations
        self.play(Write(title), run_time=1.5)
        
        for head in heads:
            self.play(FadeIn(head, shift=UP), run_time=0.8)
        
        self.wait(1)
        
        # Animate patterns in each head
        for head in heads:
            self.play(
                *[Flash(dot, color=head[0].get_stroke_color(), line_length=0.1) 
                  for dot in head[2]],
                run_time=0.5
            )
        
        self.play(GrowArrow(merge_arrow), run_time=1)
        self.play(FadeIn(concat_group), run_time=1)
        self.play(FadeIn(explanation), run_time=1)
        self.wait(4)


class Part10(Scene):
    """Feed-Forward Networks (13-18 seconds)"""
    def construct(self):
        title = Text("Feed-Forward Network", font_size=48, color=ELECTRIC_CYAN)
        title.to_edge(UP, buff=0.3)
        
        # Input layer
        input_nodes = VGroup(*[
            Circle(radius=0.2, color=ELECTRIC_CYAN, fill_opacity=0.8)
            for _ in range(4)
        ]).arrange(DOWN, buff=0.4)
        input_nodes.shift(LEFT*4)
        input_label = Text("Input", font_size=20, color=ELECTRIC_CYAN)
        input_label.next_to(input_nodes, UP, buff=0.3)
        
        # Hidden layer (expanded)
        hidden_nodes = VGroup(*[
            Circle(radius=0.2, color=NEON_PINK, fill_opacity=0.8)
            for _ in range(8)
        ]).arrange(DOWN, buff=0.2)
        hidden_label = Text("Hidden\n(4x larger)", font_size=18, color=NEON_PINK)
        hidden_label.next_to(hidden_nodes, UP, buff=0.3)
        
        # Output layer
        output_nodes = VGroup(*[
            Circle(radius=0.2, color=VIBRANT_ORANGE, fill_opacity=0.8)
            for _ in range(4)
        ]).arrange(DOWN, buff=0.4)
        output_nodes.shift(RIGHT*4)
        output_label = Text("Output", font_size=20, color=VIBRANT_ORANGE)
        output_label.next_to(output_nodes, UP, buff=0.3)
        
        # Connections
        edges1 = VGroup(*[
            Line(i.get_right(), h.get_left(), stroke_width=0.5, color=SUBTLE_NAVY)
            for i in input_nodes for h in hidden_nodes
        ])
        edges2 = VGroup(*[
            Line(h.get_right(), o.get_left(), stroke_width=0.5, color=SUBTLE_NAVY)
            for h in hidden_nodes for o in output_nodes
        ])
        
        # Activation function
        activation = MathTex(r"\text{GELU}(x) = x \cdot \Phi(x)", font_size=28, color=WHITE)
        activation.to_edge(DOWN, buff=0.8)
        
        # Animations
        self.play(Write(title), run_time=1.5)
        self.play(
            FadeIn(input_label),
            *[GrowFromCenter(node) for node in input_nodes],
            run_time=1.5
        )
        self.play(Create(edges1), run_time=1.5)
        self.play(
            FadeIn(hidden_label),
            *[GrowFromCenter(node) for node in hidden_nodes],
            run_time=1.5
        )
        self.play(Create(edges2), run_time=1.5)
        self.play(
            FadeIn(output_label),
            *[GrowFromCenter(node) for node in output_nodes],
            run_time=1.5
        )
        
        # Show activation
        self.play(Write(activation), run_time=1.5)
        
        # Signal flow
        for _ in range(2):
            self.play(
                *[node.animate.set_fill(WHITE) for node in input_nodes],
                run_time=0.3
            )
            self.play(
                *[node.animate.set_fill(ELECTRIC_CYAN) for node in input_nodes],
                *[node.animate.set_fill(WHITE) for node in hidden_nodes],
                run_time=0.4
            )
            self.play(
                *[node.animate.set_fill(NEON_PINK) for node in hidden_nodes],
                *[node.animate.set_fill(WHITE) for node in output_nodes],
                run_time=0.4
            )
            self.play(
                *[node.animate.set_fill(VIBRANT_ORANGE) for node in output_nodes],
                run_time=0.3
            )
        self.wait(2)


class Part11(ThreeDScene):
    """Layer Stacking (15-20 seconds)"""
    def construct(self):
        self.set_camera_orientation(phi=70*DEGREES, theta=-30*DEGREES)
        
        title = Text("Stacked Transformer Layers", font_size=44, color=ELECTRIC_CYAN)
        title.to_corner(UL, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        
        # Create stacked layers
        layers = VGroup()
        layer_colors = [ELECTRIC_CYAN, NEON_PINK, VIBRANT_ORANGE, "#00FF88", 
                       ELECTRIC_CYAN, NEON_PINK]
        
        for i, color in enumerate(layer_colors):
            layer = Prism(dimensions=[4, 2, 0.4])
            layer.set_color(color)
            layer.set_opacity(0.6)
            layer.shift(UP * i * 0.6)
            layers.add(layer)
        
        layers.move_to(ORIGIN)
        
        # Layer labels
        depth_text = Text("Deeper = More Understanding", font_size=28, color=WHITE)
        depth_text.to_edge(DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(depth_text)
        
        # Animations
        self.play(Write(title), run_time=1)
        
        for layer in layers:
            self.play(FadeIn(layer, shift=UP*0.5), run_time=0.7)
        
        self.wait(1)
        
        # Data flow animation
        data_sphere = Sphere(radius=0.2)
        data_sphere.set_color(WHITE)
        data_sphere.move_to(layers[0].get_center() + DOWN*1)
        
        self.play(GrowFromCenter(data_sphere), run_time=0.5)
        
        for layer in layers:
            self.play(
                data_sphere.animate.move_to(layer.get_center()),
                layer.animate.set_opacity(0.9),
                run_time=0.5
            )
            self.play(layer.animate.set_opacity(0.6), run_time=0.2)
        
        self.play(FadeOut(data_sphere), run_time=0.3)
        self.play(FadeIn(depth_text), run_time=1)
        
        # Rotate view
        self.move_camera(phi=60*DEGREES, theta=30*DEGREES, run_time=3)
        self.wait(3)


class Part12(Scene):
    """Context Window (15-20 seconds)"""
    def construct(self):
        title = Text("Context Window", font_size=48, color=ELECTRIC_CYAN)
        title.to_edge(UP, buff=0.3)
        
        # Long code sequence
        code_tokens = ["import", "numpy", "def", "process", "(", "data", ")", ":", 
                      "result", "=", "[]", "for", "item", "in", "data", ":", "..."]
        
        all_tokens = VGroup()
        for token in code_tokens:
            box = RoundedRectangle(
                width=max(len(token)*0.15 + 0.3, 0.5), height=0.5,
                corner_radius=0.08, stroke_color=SUBTLE_NAVY, stroke_width=2,
                fill_color=SUBTLE_NAVY, fill_opacity=0.3
            )
            label = Text(token, font_size=14, color=WHITE)
            all_tokens.add(VGroup(box, label))
        
        all_tokens.arrange(RIGHT, buff=0.1)
        all_tokens.scale(0.9)
        all_tokens.shift(UP*0.5)
        
        # Context window highlight
        window_size = 8
        window_rect = Rectangle(
            width=5, height=0.9,
            stroke_color=NEON_PINK, stroke_width=4,
            fill_opacity=0
        )
        window_rect.move_to(all_tokens[4:12].get_center())
        
        window_label = Text("Context Window (8K-128K tokens)", font_size=24, color=NEON_PINK)
        window_label.next_to(window_rect, DOWN, buff=0.5)
        
        explanation = Text("The model can only 'see' tokens within its window", 
                          font_size=22, color=WHITE)
        explanation.to_edge(DOWN, buff=0.8)
        
        # Animations
        self.play(Write(title), run_time=1.5)
        self.play(
            *[FadeIn(token, shift=DOWN) for token in all_tokens],
            run_time=2
        )
        self.wait(1)
        
        self.play(Create(window_rect), run_time=1)
        
        # Highlight tokens in window
        for i in range(4, 12):
            self.play(
                all_tokens[i][0].animate.set_stroke(ELECTRIC_CYAN, width=3),
                all_tokens[i][0].animate.set_fill(ELECTRIC_CYAN, opacity=0.3),
                run_time=0.2
            )
        
        self.play(FadeIn(window_label), run_time=1)
        
        # Slide window
        self.play(
            window_rect.animate.shift(RIGHT*1.5),
            run_time=2
        )
        self.play(
            window_rect.animate.shift(LEFT*3),
            run_time=2
        )
        self.play(
            window_rect.animate.move_to(all_tokens[4:12].get_center()),
            run_time=1
        )
        
        self.play(FadeIn(explanation), run_time=1)
        self.wait(3)


class Part13(Scene):
    """Probability Distribution (18-25 seconds)"""
    def construct(self):
        title = Text("Predicting the Next Token", font_size=48, color=ELECTRIC_CYAN)
        title.to_edge(UP, buff=0.3)
        
        # Input prompt
        prompt = Text('def add(a, b): return a', font_size=28, color=WHITE)
        prompt.shift(UP*2)
        cursor = Text("▌", font_size=28, color=NEON_PINK)
        cursor.next_to(prompt, RIGHT, buff=0.05)
        
        # Probability bars
        predictions = [
            ("+", 0.75, ELECTRIC_CYAN),
            ("*", 0.08, NEON_PINK),
            ("-", 0.06, VIBRANT_ORANGE),
            ("/", 0.04, SUBTLE_NAVY),
            ("b", 0.03, SUBTLE_NAVY),
            ("(", 0.02, SUBTLE_NAVY),
        ]
        
        bars = VGroup()
        labels = VGroup()
        percentages = VGroup()
        
        for i, (token, prob, color) in enumerate(predictions):
            bar = Rectangle(
                width=prob * 6, height=0.5,
                fill_color=color, fill_opacity=0.8,
                stroke_color=color, stroke_width=2
            )
            bar.align_to(LEFT*2, LEFT)
            bar.shift(DOWN*(i*0.7 - 0.5))
            
            label = Text(f'"{token}"', font_size=20, color=WHITE)
            label.next_to(bar, LEFT, buff=0.3)
            
            pct = Text(f"{prob*100:.0f}%", font_size=18, color=color)
            pct.next_to(bar, RIGHT, buff=0.2)
            
            bars.add(bar)
            labels.add(label)
            percentages.add(pct)
        
        bar_group = VGroup(bars, labels, percentages).shift(DOWN*0.5)
        
        winner_box = SurroundingRectangle(
            VGroup(bars[0], labels[0], percentages[0]),
            color=ELECTRIC_CYAN, stroke_width=3, buff=0.1
        )
        
        # Animations
        self.play(Write(title), run_time=1.5)
        self.play(Write(prompt), FadeIn(cursor), run_time=1.5)
        
        # Blinking cursor
        self.play(cursor.animate.set_opacity(0), run_time=0.3)
        self.play(cursor.animate.set_opacity(1), run_time=0.3)
        
        # Show predictions
        for bar, label, pct in zip(bars, labels, percentages):
            self.play(
                FadeIn(label),
                GrowFromEdge(bar, LEFT),
                FadeIn(pct),
                run_time=0.6
            )
        
        self.wait(1)
        self.play(Create(winner_box), run_time=1)
        
        # Token selected
        selected = Text("+", font_size=28, color=ELECTRIC_CYAN)
        selected.next_to(cursor, RIGHT, buff=0)
        self.play(
            FadeIn(selected, shift=UP),
            Flash(selected, color=ELECTRIC_CYAN),
            run_time=1
        )
        self.wait(4)


class Part14(Scene):
    """Temperature & Sampling (15-20 seconds)"""
    def construct(self):
        title = Text("Temperature Controls Creativity", font_size=44, color=ELECTRIC_CYAN)
        title.to_edge(UP, buff=0.3)
        
        # Low temperature distribution
        low_temp_title = Text("Low Temp (0.2)", font_size=22, color=ELECTRIC_CYAN)
        low_bars = VGroup(*[
            Rectangle(width=0.4, height=h, fill_color=ELECTRIC_CYAN, fill_opacity=0.8,
                     stroke_color=ELECTRIC_CYAN)
            for h in [2.5, 0.3, 0.1, 0.05, 0.03]
        ]).arrange(RIGHT, buff=0.1, aligned_edge=DOWN)
        low_label = Text("Focused", font_size=18, color=WHITE)
        low_temp_group = VGroup(low_temp_title, low_bars, low_label).arrange(DOWN, buff=0.3)
        low_temp_group.shift(LEFT*4)
        
        # Medium temperature
        med_temp_title = Text("Med Temp (0.7)", font_size=22, color=VIBRANT_ORANGE)
        med_bars = VGroup(*[
            Rectangle(width=0.4, height=h, fill_color=VIBRANT_ORANGE, fill_opacity=0.8,
                     stroke_color=VIBRANT_ORANGE)
            for h in [1.5, 0.9, 0.5, 0.3, 0.2]
        ]).arrange(RIGHT, buff=0.1, aligned_edge=DOWN)
        med_label = Text("Balanced", font_size=18, color=WHITE)
        med_temp_group = VGroup(med_temp_title, med_bars, med_label).arrange(DOWN, buff=0.3)
        
        # High temperature
        high_temp_title = Text("High Temp (1.5)", font_size=22, color=NEON_PINK)
        high_bars = VGroup(*[
            Rectangle(width=0.4, height=h, fill_color=NEON_PINK, fill_opacity=0.8,
                     stroke_color=NEON_PINK)
            for h in [0.8, 0.7, 0.65, 0.6, 0.55]
        ]).arrange(RIGHT, buff=0.1, aligned_edge=DOWN)
        high_label = Text("Creative", font_size=18, color=WHITE)
        high_temp_group = VGroup(high_temp_title, high_bars, high_label).arrange(DOWN, buff=0.3)
        high_temp_group.shift(RIGHT*4)
        
        all_temps = VGroup(low_temp_group, med_temp_group, high_temp_group)
        
        # Formula
        formula = MathTex(
            r"p_i = \frac{e^{z_i/T}}{\sum_j e^{z_j/T}}",
            font_size=32, color=WHITE
        )
        formula.to_edge(DOWN, buff=0.6)
        
        # Animations
        self.play(Write(title), run_time=1.5)
        
        self.play(
            FadeIn(low_temp_title),
            *[GrowFromEdge(bar, DOWN) for bar in low_bars],
            run_time=1.5
        )
        self.play(FadeIn(low_label), run_time=0.5)
        
        self.play(
            FadeIn(med_temp_title),
            *[GrowFromEdge(bar, DOWN) for bar in med_bars],
            run_time=1.5
        )
        self.play(FadeIn(med_label), run_time=0.5)
        
        self.play(
            FadeIn(high_temp_title),
            *[GrowFromEdge(bar, DOWN) for bar in high_bars],
            run_time=1.5
        )
        self.play(FadeIn(high_label), run_time=0.5)
        
        self.play(Write(formula), run_time=2)
        self.wait(4)


class Part15(Scene):
    """Token-by-Token Generation (18-25 seconds)"""
    def construct(self):
        title = Text("Autoregressive Generation", font_size=44, color=ELECTRIC_CYAN)
        title.to_edge(UP, buff=0.3)
        
        # Code being generated
        code_prefix = "def fibonacci(n):"
        generated_tokens = [" ", "if", " n", " <=", " 1", ":", " return", " n"]
        
        code_display = Text(code_prefix, font_size=28, color=WHITE)
        code_display.shift(UP*1.5 + LEFT*2)
        
        cursor = Text("▌", font_size=28, color=NEON_PINK)
        cursor.next_to(code_display, RIGHT, buff=0)
        
        # Cycle visualization
        cycle_center = DOWN*1.5
        cycle_radius = 1.5
        
        steps = ["Encode", "Attend", "Predict", "Sample"]
        step_colors = [ELECTRIC_CYAN, NEON_PINK, VIBRANT_ORANGE, "#00FF88"]
        step_mobjects = VGroup()
        
        for i, (step, color) in enumerate(zip(steps, step_colors)):
            angle = i * PI/2 + PI/4
            pos = cycle_center + cycle_radius * np.array([np.cos(angle), np.sin(angle), 0])
            
            circle = Circle(radius=0.4, color=color, fill_opacity=0.3, stroke_width=3)
            circle.move_to(pos)
            label = Text(step, font_size=16, color=color)
            label.move_to(pos)
            step_mobjects.add(VGroup(circle, label))
        
        # Arrows between steps
        arrows = VGroup()
        for i in range(4):
            start = step_mobjects[i][0].get_center()
            end = step_mobjects[(i+1)%4][0].get_center()
            direction = end - start
            direction = direction / np.linalg.norm(direction)
            arrow = Arrow(
                start + direction * 0.5,
                end - direction * 0.5,
                color=WHITE, stroke_width=2
            )
            arrows.add(arrow)
        
        # Animations
        self.play(Write(title), run_time=1.5)
        self.play(Write(code_display), FadeIn(cursor), run_time=1.5)
        
        self.play(
            *[FadeIn(step) for step in step_mobjects],
            *[GrowArrow(arrow) for arrow in arrows],
            run_time=2
        )
        
        # Generate tokens one by one
        current_text = code_prefix
        for token in generated_tokens:
            # Animate cycle
            for i, step in enumerate(step_mobjects):
                self.play(
                    step[0].animate.set_fill(step_colors[i], opacity=0.8),
                    run_time=0.15
                )
                self.play(
                    step[0].animate.set_fill(step_colors[i], opacity=0.3),
                    run_time=0.1
                )
            
            # Add token
            current_text += token
            new_display = Text(current_text, font_size=28, color=WHITE)
            new_display.move_to(code_display.get_left(), aligned_edge=LEFT)
            
            self.play(
                Transform(code_display, new_display),
                cursor.animate.next_to(new_display, RIGHT, buff=0),
                run_time=0.3
            )
        
        self.wait(3)


class Part16(Scene):
    """Syntax Awareness (15-20 seconds)"""
    def construct(self):
        title = Text("Syntax Awareness", font_size=48, color=ELECTRIC_CYAN)
        title.to_edge(UP, buff=0.3)
        
        # Code with syntax highlighting
        code_lines = [
            ("def", ELECTRIC_CYAN),
            (" calculate", WHITE),
            ("(", SUBTLE_NAVY),
            ("x", VIBRANT_ORANGE),
            (", ", WHITE),
            ("y", VIBRANT_ORANGE),
            (")", SUBTLE_NAVY),
            (":", NEON_PINK),
        ]
        
        line1 = VGroup(*[Text(t, font_size=28, color=c) for t, c in code_lines])
        line1.arrange(RIGHT, buff=0)
        line1.shift(UP*1)
        
        line2_parts = [
            ("    ", WHITE),
            ("return", ELECTRIC_CYAN),
            (" x ", WHITE),
            ("+", NEON_PINK),
            (" y", WHITE),
        ]
        line2 = VGroup(*[Text(t, font_size=28, color=c) for t, c in line2_parts])
        line2.arrange(RIGHT, buff=0)
        line2.next_to(line1, DOWN, buff=0.3, aligned_edge=LEFT)
        
        code = VGroup(line1, line2)
        code.shift(UP*0.5)
        
        # Bracket matching visualization
        open_bracket = line1[2]
        close_bracket = line1[6]
        
        bracket_line = ArcBetweenPoints(
            open_bracket.get_bottom(),
            close_bracket.get_bottom(),
            angle=-PI/3,
            color=NEON_PINK,
            stroke_width=3
        )
        
        # Indentation visualization
        indent_arrow = Arrow(
            line1.get_left() + DOWN*0.5,
            line2.get_left() + UP*0.1,
            color=VIBRANT_ORANGE, stroke_width=3
        )
        indent_label = Text("4 spaces", font_size=18, color=VIBRANT_ORANGE)
        indent_label.next_to(indent_arrow, LEFT, buff=0.2)
        
        # Rules learned
        rules = VGroup(
            Text("✓ Bracket Matching", font_size=24, color=NEON_PINK),
            Text("✓ Proper Indentation", font_size=24, color=VIBRANT_ORANGE),
            Text("✓ Keyword Recognition", font_size=24, color=ELECTRIC_CYAN),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        rules.to_edge(DOWN, buff=0.8)
        
        # Animations
        self.play(Write(title), run_time=1.5)
        self.play(
            *[Write(part) for part in line1],
            run_time=2
        )
        self.play(
            *[Write(part) for part in line2],
            run_time=1.5
        )
        
        self.wait(0.5)
        
        # Show bracket matching
        self.play(
            open_bracket.animate.set_color(WHITE).scale(1.3),
            close_bracket.animate.set_color(WHITE).scale(1.3),
            run_time=0.5
        )
        self.play(Create(bracket_line), run_time=1)
        self.play(
            open_bracket.animate.set_color(SUBTLE_NAVY).scale(1/1.3),
            close_bracket.animate.set_color(SUBTLE_NAVY).scale(1/1.3),
            run_time=0.5
        )
        
        # Show indentation
        self.play(
            GrowArrow(indent_arrow),
            FadeIn(indent_label),
            run_time=1
        )
        
        # Show rules
        for rule in rules:
            self.play(FadeIn(rule, shift=RIGHT), run_time=0.8)
        
        self.wait(3)


class Part17(Scene):
    """Semantic Understanding (18-25 seconds)"""
    def construct(self):
        title = Text("Semantic Understanding", font_size=48, color=ELECTRIC_CYAN)
        title.to_edge(UP, buff=0.3)
        
        # Code with variable tracking
        code_text = """def greet(name):
    message = "Hello, " + name
    return message"""
        
        code = Code(
            code_string=code_text,
            language="python",
            paragraph_config={"font_size": 20},
            background="rectangle",
            background_config={
                "stroke_color": ELECTRIC_CYAN,
                "stroke_width": 2,
            },
        )
        code.shift(UP*0.5 + LEFT*2)
        
        # Variable tracking arrows
        annotations = VGroup()
        
        name_box1 = RoundedRectangle(
            width=1, height=0.4, corner_radius=0.1,
            stroke_color=VIBRANT_ORANGE, stroke_width=2
        ).shift(UP*0.5 + LEFT*0.1)
        
        name_box2 = RoundedRectangle(
            width=1, height=0.4, corner_radius=0.1,
            stroke_color=VIBRANT_ORANGE, stroke_width=2
        ).shift(UP*0.3 + RIGHT*1.4)
        
        tracking_arrow = Arrow(
            name_box1.get_right(),
            name_box2.get_left(),
            color=VIBRANT_ORANGE, stroke_width=2
        )
        
        # Understanding panel
        understanding = VGroup(
            Text("The AI understands:", font_size=24, color=WHITE),
            Text("• 'name' is a string parameter", font_size=20, color=ELECTRIC_CYAN),
            Text("• 'message' stores concatenated text", font_size=20, color=NEON_PINK),
            Text("• Return type matches 'message'", font_size=20, color=VIBRANT_ORANGE),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        understanding.shift(RIGHT*3)
        
        # Animations
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(code), run_time=2)
        self.wait(1)
        
        # Show variable tracking
        self.play(Create(name_box1), run_time=0.8)
        self.play(GrowArrow(tracking_arrow), run_time=1)
        self.play(Create(name_box2), run_time=0.8)
        
        # Show understanding
        for item in understanding:
            self.play(FadeIn(item, shift=LEFT), run_time=0.8)
        
        self.wait(4)


class Part18(Scene):
    """The Math Behind It (15-20 seconds)"""
    def construct(self):
        title = Text("The Mathematics", font_size=48, color=ELECTRIC_CYAN)
        title.to_edge(UP, buff=0.3)
        
        # Loss function
        loss_title = Text("Cross-Entropy Loss", font_size=28, color=NEON_PINK)
        loss_formula = MathTex(
            r"\mathcal{L} = -\sum_{i} y_i \log(\hat{y}_i)",
            font_size=36, color=WHITE
        )
        loss_group = VGroup(loss_title, loss_formula).arrange(DOWN, buff=0.3)
        loss_group.shift(UP*1 + LEFT*3)
        
        # Gradient descent
        grad_title = Text("Gradient Descent", font_size=28, color=VIBRANT_ORANGE)
        grad_formula = MathTex(
            r"\theta_{t+1} = \theta_t - \eta \nabla \mathcal{L}",
            font_size=36, color=WHITE
        )
        grad_group = VGroup(grad_title, grad_formula).arrange(DOWN, buff=0.3)
        grad_group.shift(UP*1 + RIGHT*3)
        
        # Loss landscape visualization
        axes = Axes(
            x_range=[-3, 3], y_range=[0, 5],
            x_length=5, y_length=2.5,
            axis_config={"color": SUBTLE_NAVY}
        ).shift(DOWN*1.5)
        
        curve = axes.plot(
            lambda x: 0.5 * x**2 + 0.3 * np.sin(3*x) + 2,
            color=ELECTRIC_CYAN, stroke_width=3
        )
        
        # Gradient descent ball
        ball = Dot(color=VIBRANT_ORANGE, radius=0.15)
        ball.move_to(axes.c2p(-2, 0.5*4 + 0.3*np.sin(-6) + 2))
        
        # Path
        path_points = [
            axes.c2p(x, 0.5*x**2 + 0.3*np.sin(3*x) + 2)
            for x in np.linspace(-2, 0, 20)
        ]
        
        min_label = Text("Minimum Loss", font_size=18, color=NEON_PINK)
        min_label.next_to(axes.c2p(0, 2), DOWN, buff=0.3)
        
        # Animations
        self.play(Write(title), run_time=1.5)
        
        self.play(
            FadeIn(loss_group, shift=DOWN),
            FadeIn(grad_group, shift=DOWN),
            run_time=2
        )
        
        self.play(Create(axes), Create(curve), run_time=2)
        self.play(GrowFromCenter(ball), run_time=0.5)
        
        # Animate descent
        for i in range(len(path_points) - 1):
            self.play(
                ball.animate.move_to(path_points[i+1]),
                run_time=0.15
            )
        
        self.play(
            Flash(ball, color=VIBRANT_ORANGE),
            FadeIn(min_label),
            run_time=1
        )
        self.wait(3)


class Part19(Scene):
    """Putting It All Together (18-25 seconds)"""
    def construct(self):
        title = Text("The Complete Pipeline", font_size=48, color=ELECTRIC_CYAN)
        title.to_edge(UP, buff=0.3)
        
        # Pipeline stages
        stages = [
            ("Prompt", ELECTRIC_CYAN),
            ("Tokenize", NEON_PINK),
            ("Embed", VIBRANT_ORANGE),
            ("Attend", "#00FF88"),
            ("Predict", ELECTRIC_CYAN),
            ("Output", NEON_PINK),
        ]
        
        stage_mobjects = VGroup()
        arrows = VGroup()
        
        for i, (name, color) in enumerate(stages):
            rect = RoundedRectangle(
                width=1.4, height=0.8,
                corner_radius=0.1, stroke_color=color, stroke_width=3,
                fill_color=color, fill_opacity=0.2
            )
            label = Text(name, font_size=18, color=color)
            stage = VGroup(rect, label)
            stage_mobjects.add(stage)
        
        stage_mobjects.arrange(RIGHT, buff=0.5)
        stage_mobjects.shift(UP*0.5)
        
        for i in range(len(stages) - 1):
            arrow = Arrow(
                stage_mobjects[i].get_right(),
                stage_mobjects[i+1].get_left(),
                color=WHITE, stroke_width=2
            )
            arrows.add(arrow)
        
        # Example flow
        input_text = Text('"Write hello world"', font_size=22, color=WHITE)
        input_text.next_to(stage_mobjects, UP, buff=0.8)
        
        output_text = Text('print("Hello, World!")', font_size=22, color=ELECTRIC_CYAN)
        output_text.next_to(stage_mobjects, DOWN, buff=0.8)
        
        # Data flow dot
        flow_dot = Dot(color=WHITE, radius=0.2)
        flow_dot.move_to(input_text.get_center())
        
        # Animations
        self.play(Write(title), run_time=1.5)
        self.play(Write(input_text), run_time=1)
        
        for stage, arrow in zip(stage_mobjects[:-1], arrows):
            self.play(FadeIn(stage), run_time=0.5)
            self.play(GrowArrow(arrow), run_time=0.3)
        self.play(FadeIn(stage_mobjects[-1]), run_time=0.5)
        
        # Animate flow
        self.play(GrowFromCenter(flow_dot), run_time=0.5)
        
        for i, stage in enumerate(stage_mobjects):
            self.play(
                flow_dot.animate.move_to(stage.get_center()),
                stage[0].animate.set_fill(opacity=0.6),
                run_time=0.5
            )
            self.play(
                stage[0].animate.set_fill(opacity=0.2),
                run_time=0.2
            )
        
        self.play(
            flow_dot.animate.move_to(output_text.get_center()),
            run_time=0.5
        )
        self.play(
            FadeOut(flow_dot),
            Write(output_text),
            run_time=1.5
        )
        
        # Final highlight
        self.play(
            *[stage[0].animate.set_stroke(WHITE, width=4) for stage in stage_mobjects],
            run_time=0.5
        )
        self.play(
            *[stage[0].animate.set_stroke(stage[0].get_stroke_color(), width=3) 
              for stage in stage_mobjects],
            run_time=0.5
        )
        self.wait(4)


class Part20(Scene):
    """The Future (13-18 seconds)"""
    def construct(self):
        title = Text("The Future of AI Coding", font_size=52, color=ELECTRIC_CYAN)
        title.to_edge(UP, buff=0.5)
        
        # Evolving capabilities
        capabilities = [
            ("Today", "Single-file code generation", ELECTRIC_CYAN),
            ("Soon", "Full project understanding", NEON_PINK),
            ("Future", "Autonomous software development", VIBRANT_ORANGE),
        ]
        
        cap_mobjects = VGroup()
        for era, desc, color in capabilities:
            era_text = Text(era, font_size=32, color=color, weight=BOLD)
            desc_text = Text(desc, font_size=22, color=WHITE)
            group = VGroup(era_text, desc_text).arrange(DOWN, buff=0.2)
            cap_mobjects.add(group)
        
        cap_mobjects.arrange(RIGHT, buff=1.5)
        cap_mobjects.shift(UP*0.3)
        
        # Progress arrows
        progress_arrows = VGroup()
        for i in range(2):
            arrow = Arrow(
                cap_mobjects[i].get_right() + RIGHT*0.2,
                cap_mobjects[i+1].get_left() + LEFT*0.2,
                color=WHITE, stroke_width=3
            )
            progress_arrows.add(arrow)
        
        # Closing message
        closing = Text("The code you imagine, AI can create", 
                      font_size=32, color=WHITE)
        closing.to_edge(DOWN, buff=1.5)
        
        # Subscribe CTA
        cta = Text("Subscribe for more!", font_size=28, color=NEON_PINK)
        cta.next_to(closing, DOWN, buff=0.5)
        
        # Animations
        self.play(Write(title), run_time=1.5)
        
        for cap in cap_mobjects:
            self.play(FadeIn(cap, shift=UP), run_time=1)
        
        for arrow in progress_arrows:
            self.play(GrowArrow(arrow), run_time=0.5)
        
        self.wait(1)
        
        self.play(Write(closing), run_time=2)
        self.play(
            FadeIn(cta, shift=UP),
            cta.animate.set_color(WHITE),
            run_time=1
        )
        self.play(
            cta.animate.set_color(NEON_PINK),
            run_time=0.5
        )
        
        # Final flash
        self.play(
            *[Flash(cap[0], color=cap[0].get_color(), line_length=0.3) 
              for cap in cap_mobjects],
            run_time=1
        )
        self.wait(3)

