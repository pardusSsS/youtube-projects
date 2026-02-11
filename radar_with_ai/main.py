from manim import *
import numpy as np

# Monkeypatch for Manim compatibility
# Fixes TypeError: VMobject.scale() got an unexpected keyword argument 'scale_tips'
# caused by GrowArrow usage on CurvedArrow objects
try:
    from manim import CurvedArrow
    original_ca_scale = CurvedArrow.scale

    def patched_ca_scale(self, *args, **kwargs):
        kwargs.pop("scale_tips", None)
        return original_ca_scale(self, *args, **kwargs)

    CurvedArrow.scale = patched_ca_scale
except ImportError:
    pass

# ========================== COLOR PALETTE ==========================
DEEP_NAVY = "#020B1F"
TECH_CYAN = "#00F0FF"
NEON_PINK = "#FF0055"
VIBRANT_ORANGE = "#FF9F00"
TEXT_WHITE = "#FFFFFF"
SUBTLE_NAVY = "#1E2A45"

config.background_color = DEEP_NAVY
# ============================================================================
# PART 1: THE HOOK (3-6 seconds) - EXPLOSIVE OPENING
# ============================================================================
class Part1(ThreeDScene):
    def construct(self):
        
        # 3D Radar tower with AI brain fusion
        self.set_camera_orientation(phi=70*DEGREES, theta=-45*DEGREES)
        
        # Radar dish
        radar_dish = Sphere(radius=0.8, color=TECH_CYAN, fill_opacity=0.3, 
                           resolution=(20, 20), stroke_width=2)
        radar_dish.shift(UP*0.5)
        
        # AI brain (neural network sphere)
        brain = Sphere(radius=0.5, color=NEON_PINK, fill_opacity=0.6, 
                      resolution=(15, 15), stroke_width=2)
        brain.shift(DOWN*0.5)
        
        # Energy connection
        energy_line = Line3D(radar_dish.get_center(), brain.get_center(),
                            color=VIBRANT_ORANGE, stroke_width=8)
        
        # Explosive title
        title = Text("AI × RADAR", font_size=84, color=TEXT_WHITE, weight=BOLD)
        subtitle = Text("The Perfect Fusion", font_size=40, color=TECH_CYAN)
        
        self.add_fixed_in_frame_mobjects(title, subtitle)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.3)
        title_group.to_edge(UP, buff=0.5)
        
        # ANIMATION
        self.play(
            FadeIn(radar_dish, scale=0.5),
            FadeIn(brain, scale=0.5),
            run_time=1
        )
        
        self.play(
            Create(energy_line),
            Flash(radar_dish, color=TECH_CYAN, flash_radius=1.5, num_lines=16),
            Flash(brain, color=NEON_PINK, flash_radius=1.5, num_lines=16),
            run_time=1.5
        )
        
        self.play(
            Write(title, run_time=1),
            FadeIn(subtitle, shift=UP*0.2),
            Rotate(radar_dish, angle=180*DEGREES, axis=UP),
            run_time=1.8
        )
        
        self.wait(0.7)
        self.play(FadeOut(title_group, radar_dish, brain, energy_line), run_time=0.5)


# ============================================================================
# PART 2: RADAR SYSTEM ARCHITECTURE (13-25s)
# ============================================================================
class Part2(Scene):
    def construct(self):
        
        title = Text("Radar System Architecture", font_size=54, color=TECH_CYAN, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        
        self.play(Write(title), run_time=2.5)
        self.wait(2)
        
        # Main components of radar system
        components = [
            ("Transmitter\n(TX)", LEFT*4.5 + UP*1.5, TECH_CYAN),
            ("Antenna\nArray", LEFT*1.5 + UP*1.5, NEON_PINK),
            ("Receiver\n(RX)", RIGHT*1.5 + UP*1.5, VIBRANT_ORANGE),
            ("Signal\nProcessor", RIGHT*4.5 + UP*1.5, TECH_CYAN),
            ("Data\nStorage", LEFT*3 + DOWN*1.5, NEON_PINK),
            ("Detection\nAlgorithm", ORIGIN + DOWN*1.5, VIBRANT_ORANGE),
            ("Tracking\nSystem", RIGHT*3 + DOWN*1.5, TECH_CYAN),
        ]
        
        boxes = VGroup()
        labels = VGroup()
        
        for comp_name, pos, color in components:
            box = RoundedRectangle(width=1.8, height=1.2, corner_radius=0.2,
                                   color=color, stroke_width=4, fill_opacity=0.25)
            box.move_to(pos)
            
            label = Text(comp_name, font_size=22, color=TEXT_WHITE, weight=BOLD)
            label.move_to(box.get_center())
            
            boxes.add(box)
            labels.add(label)
        
        # Connection arrows
        connections = VGroup(
            Arrow(boxes[0].get_right(), boxes[1].get_left(), color=TEXT_WHITE, stroke_width=3, buff=0.1),
            Arrow(boxes[1].get_right(), boxes[2].get_left(), color=TEXT_WHITE, stroke_width=3, buff=0.1),
            Arrow(boxes[2].get_right(), boxes[3].get_left(), color=TEXT_WHITE, stroke_width=3, buff=0.1),
            Arrow(boxes[3].get_bottom(), boxes[5].get_top(), color=TEXT_WHITE, stroke_width=3, buff=0.1),
            Arrow(boxes[5].get_left(), boxes[4].get_right(), color=TEXT_WHITE, stroke_width=3, buff=0.1),
            Arrow(boxes[5].get_right(), boxes[6].get_left(), color=TEXT_WHITE, stroke_width=3, buff=0.1),
        )
        
        self.play(
            LaggedStart(*[FadeIn(box, shift=DOWN*0.3) for box in boxes], lag_ratio=0.2),
            LaggedStart(*[Write(label) for label in labels], lag_ratio=0.2),
            run_time=5
        )
        self.wait(2)
        
        self.play(
            LaggedStart(*[GrowArrow(arrow) for arrow in connections], lag_ratio=0.25),
            run_time=3.5
        )
        self.wait(2)
        
        # Highlight where AI fits
        ai_note = Text("AI can enhance EVERY stage!", font_size=36, color=VIBRANT_ORANGE, weight=BOLD)
        ai_note.to_edge(DOWN, buff=0.8)
        
        self.play(Write(ai_note), run_time=2.5)
        self.wait(4)


# ============================================================================
# PART 3: WHERE AI FITS - SIGNAL PROCESSING (13-25s)
# ============================================================================
class Part3(ThreeDScene):
    def construct(self):
        
        title = Text("AI Stage 1: Signal Processing", font_size=52, color=NEON_PINK, weight=BOLD)
        self.add_fixed_in_frame_mobjects(title)
        title.to_edge(UP, buff=0.5)
        
        self.play(Write(title), run_time=2.5)
        self.wait(2)
        
        self.set_camera_orientation(phi=65*DEGREES, theta=-50*DEGREES)
        
        # 3D Neural Network for signal processing
        # Input layer (raw signal)
        input_layer = VGroup(*[
            Sphere(radius=0.12, color=TECH_CYAN, fill_opacity=0.8, resolution=(8, 8))
            .shift(LEFT*3 + UP*(1-i*0.5) + OUT*j*0.3)
            for i in range(5) for j in range(-1, 2)
        ])
        
        # Hidden layers
        hidden1 = VGroup(*[
            Sphere(radius=0.12, color=NEON_PINK, fill_opacity=0.8, resolution=(8, 8))
            .shift(LEFT*1 + UP*(1.5-i*0.4) + OUT*j*0.3)
            for i in range(7) for j in range(-1, 2)
        ])
        
        hidden2 = VGroup(*[
            Sphere(radius=0.12, color=VIBRANT_ORANGE, fill_opacity=0.8, resolution=(8, 8))
            .shift(RIGHT*1 + UP*(1.5-i*0.4) + OUT*j*0.3)
            for i in range(7) for j in range(-1, 2)
        ])
        
        # Output layer (clean signal)
        output_layer = VGroup(*[
            Sphere(radius=0.12, color=TECH_CYAN, fill_opacity=0.8, resolution=(8, 8))
            .shift(RIGHT*3 + UP*(1-i*0.5) + OUT*j*0.3)
            for i in range(5) for j in range(-1, 2)
        ])
        
        # Labels
        input_label = Text("Noisy\nSignal", font_size=24, color=TECH_CYAN)
        output_label = Text("Clean\nSignal", font_size=24, color=TECH_CYAN)
        
        self.add_fixed_in_frame_mobjects(input_label, output_label)
        input_label.to_edge(LEFT, buff=0.5).shift(UP*0.5)
        output_label.to_edge(RIGHT, buff=0.5).shift(UP*0.5)
        
        # Create network
        self.play(
            LaggedStart(
                FadeIn(input_layer, lag_ratio=0.05),
                FadeIn(hidden1, lag_ratio=0.05),
                FadeIn(hidden2, lag_ratio=0.05),
                FadeIn(output_layer, lag_ratio=0.05),
                lag_ratio=0.4
            ),
            run_time=5
        )
        
        self.play(Write(input_label), Write(output_label), run_time=2)
        self.wait(2)
        
        # Pulse through network
        for _ in range(2):
            self.play(
                LaggedStart(
                    input_layer.animate.set_opacity(1).scale(1.2).set_opacity(0.8).scale(1/1.2),
                    hidden1.animate.set_opacity(1).scale(1.2).set_opacity(0.8).scale(1/1.2),
                    hidden2.animate.set_opacity(1).scale(1.2).set_opacity(0.8).scale(1/1.2),
                    output_layer.animate.set_opacity(1).scale(1.2).set_opacity(0.8).scale(1/1.2),
                    lag_ratio=0.3
                ),
                run_time=3
            )
            self.wait(1)
        
        # Tasks performed
        tasks = Text("Noise Reduction • Clutter Suppression • Interference Mitigation", 
                    font_size=28, color=VIBRANT_ORANGE, weight=BOLD)
        self.add_fixed_in_frame_mobjects(tasks)
        tasks.to_edge(DOWN, buff=0.8)
        
        self.play(Write(tasks), run_time=2.5)
        self.wait(3)


# ============================================================================
# PART 4: AI TRAINING DATA - SIGNAL PROCESSING (13-25s)
# ============================================================================
class Part4(Scene):
    def construct(self):
        
        title = Text("Training Data: Signal Processing AI", font_size=50, color=TECH_CYAN, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        
        self.play(Write(title), run_time=2.5)
        self.wait(2)
        
        # Data types visualization
        data_types = [
            ("Raw I/Q Samples", TECH_CYAN, "Time-domain signal data"),
            ("Spectrograms", NEON_PINK, "Frequency-time representations"),
            ("Range-Doppler Maps", VIBRANT_ORANGE, "2D velocity-distance data"),
            ("Noise Patterns", TECH_CYAN, "Environmental interference samples"),
        ]
        
        data_group = VGroup()
        
        for i, (dtype, color, description) in enumerate(data_types):
            # Main box
            box = RoundedRectangle(width=10, height=0.9, corner_radius=0.15,
                                   color=color, stroke_width=4, fill_opacity=0.2)
            
            # Mini waveform visualization (Icon)
            if i == 0:  # Time domain
                wave = VGroup(*[
                    Line(ORIGIN, UP*0.3*np.sin(j*0.5), color=color, stroke_width=2)
                    .shift(RIGHT*j*0.08)
                    for j in range(15)
                ])
            elif i == 1:  # Spectrogram
                wave = VGroup(*[
                    Rectangle(width=0.08, height=0.3*np.random.random(), 
                             color=color, fill_opacity=0.6, stroke_width=1)
                    .shift(RIGHT*j*0.09)
                    for j in range(12)
                ])
            elif i == 2:  # Range-Doppler
                wave = VGroup(*[
                    Dot(RIGHT*j*0.1 + UP*k*0.1, radius=0.03, color=color)
                    for j in range(10) for k in range(3)
                ])
            else:  # Noise
                wave = VGroup(*[
                    Dot([np.random.uniform(-0.5, 0.5), np.random.uniform(-0.15, 0.15), 0],
                        radius=0.02, color=color)
                    for _ in range(40)
                ])
            
            # Position Icon
            wave.scale(0.8).move_to(box.get_left() + RIGHT*0.8)
            
            # Title (Positioned relative to icon)
            dtype_text = Text(dtype, font_size=28, color=color, weight=BOLD)
            dtype_text.next_to(wave, RIGHT, buff=0.4)
            
            # Description (Right aligned)
            desc_text = Text(description, font_size=20, color=TEXT_WHITE)
            desc_text.next_to(box.get_right(), LEFT, buff=0.5)
            
            item = VGroup(box, dtype_text, desc_text, wave)
            # FIX: Correct vertical spacing logic to stack downwards
            item.shift(UP*1.9 + DOWN*i*1.0)
            data_group.add(item)
        
        self.play(
            LaggedStart(*[FadeIn(item, shift=RIGHT*0.3) for item in data_group], lag_ratio=0.35),
            run_time=6
        )
        self.wait(3)
        
        # Key insight
        insight = Text("Millions of labeled samples needed!", font_size=34, color=VIBRANT_ORANGE, weight=BOLD)
        insight.to_edge(DOWN, buff=0.8)
        
        self.play(Write(insight), run_time=2.5)
        self.wait(4)


# ============================================================================
# PART 5: WHERE AI FITS - TARGET DETECTION (13-25s)
# ============================================================================
class Part5(ThreeDScene):
    def construct(self):
        
        title = Text("AI Stage 2: Target Detection", font_size=54, color=NEON_PINK, weight=BOLD)
        self.add_fixed_in_frame_mobjects(title)
        title.to_edge(UP, buff=0.5)
        
        self.play(Write(title), run_time=2.5)
        self.wait(2)
        
        self.set_camera_orientation(phi=70*DEGREES, theta=-60*DEGREES)
        
        # 3D Convolutional Neural Network
        # Layer 1 - Input (Range-Doppler map)
        layer1 = VGroup(*[
            Cube(side_length=0.15, color=TECH_CYAN, fill_opacity=0.6, stroke_width=1)
            .shift(LEFT*3 + RIGHT*i*0.18 + UP*j*0.18 + OUT*k*0.18)
            for i in range(5) for j in range(5) for k in range(3)
        ])
        
        # Layer 2 - Feature extraction
        layer2 = VGroup(*[
            Cube(side_length=0.2, color=NEON_PINK, fill_opacity=0.7, stroke_width=1)
            .shift(LEFT*1 + RIGHT*i*0.25 + UP*j*0.25 + OUT*k*0.25)
            for i in range(4) for j in range(4) for k in range(4)
        ])
        
        # Layer 3 - Deep features
        layer3 = VGroup(*[
            Cube(side_length=0.25, color=VIBRANT_ORANGE, fill_opacity=0.7, stroke_width=1)
            .shift(RIGHT*1.2 + RIGHT*i*0.3 + UP*j*0.3 + OUT*k*0.3)
            for i in range(3) for j in range(3) for k in range(3)
        ])
        
        # Output - Detection decision
        output = VGroup(*[
            Sphere(radius=0.2, color=TECH_CYAN, fill_opacity=0.9, resolution=(10, 10))
            .shift(RIGHT*3.5 + UP*(0.5-i*0.5))
            for i in range(3)
        ])
        
        # Labels
        input_label = Text("Range-Doppler\nMap", font_size=24, color=TECH_CYAN)
        output_label = Text("Detection:\nAircraft\nDrone\nBird", font_size=22, color=TECH_CYAN)
        
        self.add_fixed_in_frame_mobjects(input_label, output_label)
        input_label.to_edge(LEFT, buff=0.3).shift(UP*0.5)
        output_label.to_edge(RIGHT, buff=0.3).shift(UP*0.3)
        
        # Animation
        self.play(
            LaggedStart(
                FadeIn(layer1, lag_ratio=0.02),
                FadeIn(layer2, lag_ratio=0.02),
                FadeIn(layer3, lag_ratio=0.02),
                FadeIn(output, lag_ratio=0.1),
                lag_ratio=0.5
            ),
            run_time=6
        )
        
        self.play(Write(input_label), Write(output_label), run_time=2.5)
        self.wait(2)
        
        # Rotate for better view
        self.play(
            Rotate(VGroup(layer1, layer2, layer3, output), angle=180*DEGREES, axis=UP),
            run_time=4
        )
        self.wait(2)
        
        # AI task description
        task = Text("Classify: Target vs Clutter vs Noise", font_size=30, color=VIBRANT_ORANGE, weight=BOLD)
        self.add_fixed_in_frame_mobjects(task)
        task.to_edge(DOWN, buff=0.8)
        
        self.play(Write(task), run_time=2.5)
        self.wait(3)


# ============================================================================
# PART 6: AI TRAINING DATA - TARGET DETECTION (13-25s)
# ============================================================================
class Part6(Scene):
    def construct(self):
        
        title = Text("Training Data: Detection AI", font_size=54, color=TECH_CYAN, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        
        self.play(Write(title), run_time=2.5)
        self.wait(2)
        
        # Create radar PPI display with labeled targets
        radar_circle = Circle(radius=2.8, color=SUBTLE_NAVY, stroke_width=4)
        radar_circle.shift(DOWN*0.3)
        
        # Radar grid
        grid = VGroup()
        for angle in range(0, 360, 30):
            line = Line(radar_circle.get_center(), 
                       radar_circle.get_center() + 2.8*rotate_vector(UP, angle*DEGREES),
                       color=SUBTLE_NAVY, stroke_width=2)
            grid.add(line)
        
        for r in [0.9, 1.8, 2.7]:
            circle = Circle(radius=r, color=SUBTLE_NAVY, stroke_width=2)
            circle.move_to(radar_circle.get_center())
            grid.add(circle)
        
        self.play(Create(radar_circle), Create(grid), run_time=3)
        self.wait(1.5)
        
        # Different target types with labels
        targets = [
            (1.5, 30, "Aircraft", TECH_CYAN, "Large RCS"),
            (2.3, 100, "Drone", NEON_PINK, "Small RCS"),
            (1.1, 160, "Bird", VIBRANT_ORANGE, "Micro-Doppler"),
            (2.0, -80, "Clutter", "#888888", "Ground return"),
            (1.7, -140, "Weather", "#888888", "Rain/Snow"),
        ]
        
        target_dots = VGroup()
        labels_group = VGroup()
        
        for dist, angle, name, color, feature in targets:
            pos = radar_circle.get_center() + dist*(
                np.cos(angle*DEGREES)*RIGHT + np.sin(angle*DEGREES)*UP
            )
            
            # Target dot with glow
            dot = Dot(pos, radius=0.1, color=color)
            glow = Circle(radius=0.2, color=color, stroke_width=3, stroke_opacity=0.4).move_to(pos)
            
            # Label
            label_text = Text(f"{name}\n{feature}", font_size=18, color=color, weight=BOLD)
            label_box = Rectangle(
                width=label_text.width+0.2, height=label_text.height+0.15,
                color=color, stroke_width=2, fill_opacity=0.25
            )
            label_group = VGroup(label_box, label_text)
            label_text.move_to(label_box.get_center())
            
            # Position label
            if angle > 0:
                label_group.next_to(dot, UP, buff=0.2)
            else:
                label_group.next_to(dot, DOWN, buff=0.2)
            
            target_dots.add(VGroup(glow, dot))
            labels_group.add(label_group)
        
        self.play(
            LaggedStart(*[FadeIn(target, scale=1.5) for target in target_dots], lag_ratio=0.3),
            run_time=4
        )
        self.wait(2)
        
        self.play(
            LaggedStart(*[FadeIn(label, shift=DOWN*0.2) for label in labels_group], lag_ratio=0.3),
            run_time=4
        )
        self.wait(3)
        
        # Dataset requirement
        requirement = Text("Need 100K+ labeled radar returns per class", 
                          font_size=30, color=VIBRANT_ORANGE, weight=BOLD)
        requirement.to_edge(DOWN, buff=0.7)
        
        self.play(Write(requirement), run_time=2.5)
        self.wait(4)


# ============================================================================
# PART 7: WHERE AI FITS - CLASSIFICATION (13-25s)
# ============================================================================
class Part7(ThreeDScene):
    def construct(self):
        
        title = Text("AI Stage 3: Target Classification", font_size=50, color=NEON_PINK, weight=BOLD)
        self.add_fixed_in_frame_mobjects(title)
        title.to_edge(UP, buff=0.5)
        
        self.play(Write(title), run_time=2.5)
        self.wait(2)
        
        self.set_camera_orientation(phi=75*DEGREES, theta=-70*DEGREES)
        
        # Deep 3D Neural Network for classification
        # More complex architecture
        layers_config = [
            (6, LEFT*4, TECH_CYAN, 0.10),      # Input
            (10, LEFT*2.5, NEON_PINK, 0.12),   # Conv1
            (10, LEFT*1, VIBRANT_ORANGE, 0.12),     # Conv2
            (8, RIGHT*0.5, TECH_CYAN, 0.14),   # Conv3
            (6, RIGHT*2, NEON_PINK, 0.16),     # FC1
            (4, RIGHT*3.5, VIBRANT_ORANGE, 0.18),   # Output
        ]
        
        network_layers = []
        
        for num_neurons, x_pos, color, radius in layers_config:
            layer = VGroup(*[
                Sphere(radius=radius, color=color, fill_opacity=0.75, resolution=(10, 10))
                .shift(x_pos + UP*(2-i*4/(num_neurons-1)))
                for i in range(num_neurons)
            ])
            
            # Add depth variation
            for i, neuron in enumerate(layer):
                offset = np.sin(i*0.5)*0.3
                neuron.shift(OUT*offset)
            
            network_layers.append(layer)
        
        # Create connections between layers
        connections = VGroup()
        for i in range(len(network_layers)-1):
            for n1 in network_layers[i][:3]:  # Limit connections for clarity
                for n2 in network_layers[i+1][:3]:
                    line = Line3D(
                        n1.get_center(), n2.get_center(),
                        color=SUBTLE_NAVY, stroke_width=0.5, stroke_opacity=0.3
                    )
                    connections.add(line)
        
        # Labels
        class_labels = VGroup(
            Text("Fighter", font_size=20, color=VIBRANT_ORANGE),
            Text("Bomber", font_size=20, color=VIBRANT_ORANGE),
            Text("Drone", font_size=20, color=VIBRANT_ORANGE),
            Text("Bird", font_size=20, color=VIBRANT_ORANGE),
        )
        
        self.add_fixed_in_frame_mobjects(*class_labels)
        
        # Position labels next to the output layer (RIGHT*3.5)
        # Arrange vertically and center relative to the output nodes
        class_labels.arrange(DOWN, buff=0.8, aligned_edge=LEFT)
        class_labels.move_to(RIGHT*4.5)
        
        # Animate network creation
        self.play(Create(connections), run_time=3)
        self.wait(1)
        
        self.play(
            LaggedStart(*[
                FadeIn(layer, lag_ratio=0.1) for layer in network_layers
            ], lag_ratio=0.3),
            run_time=5
        )
        
        self.play(
            LaggedStart(*[Write(label) for label in class_labels], lag_ratio=0.2),
            run_time=2.5
        )
        self.wait(2)
        
        # Pulse through network
        for _ in range(2):
            self.play(
                LaggedStart(*[
                    layer.animate.set_fill(opacity=1).scale(1.15).set_fill(opacity=0.75).scale(1/1.15)
                    for layer in network_layers
                ], lag_ratio=0.2),
                run_time=3.5
            )
            self.wait(1)
        
        # Task description
        task = Text("Multi-class classification with 95%+ accuracy", 
                   font_size=28, color=TECH_CYAN, weight=BOLD)
        self.add_fixed_in_frame_mobjects(task)
        task.to_edge(DOWN, buff=0.8)
        
        self.play(Write(task), run_time=2.5)
        self.wait(3)


# ============================================================================
# PART 8: AI TRAINING DATA - CLASSIFICATION (13-25s)
# ============================================================================
class Part8(Scene):
    def construct(self):
        
        title = Text("Training Data: Classification AI", font_size=50, color=TECH_CYAN, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        
        self.play(Write(title), run_time=2.5)
        self.wait(2)
        
        # Feature types needed
        features = [
            ("RCS Profile", TECH_CYAN, "Radar Cross Section patterns"),
            ("Micro-Doppler", NEON_PINK, "Wing/rotor modulation"),
            ("Jet Engine Modulation", VIBRANT_ORANGE, "JEM signature"),
            ("Polarization", TECH_CYAN, "HH, VV, HV, VH data"),
            ("Multi-band Fusion", NEON_PINK, "X, S, L band combined"),
        ]
        
        feature_grid = VGroup()
        
        for i, (feat_name, color, description) in enumerate(features):
            # Feature container
            container = RoundedRectangle(
                width=11, height=0.9, corner_radius=0.15,
                color=color, stroke_width=4, fill_opacity=0.18
            )
            
            # Icon (data symbol)
            icon = VGroup(
                Circle(radius=0.15, color=color, fill_opacity=0.6, stroke_width=2),
                Text("□", font_size=20, color=color).move_to(ORIGIN)
            )
            icon.move_to(container.get_left() + RIGHT*0.5)
            
            # Feature name
            name_text = Text(feat_name, font_size=28, color=color, weight=BOLD)
            name_text.move_to(container.get_left() + RIGHT*2.3)
            
            # Description
            desc_text = Text(description, font_size=20, color=TEXT_WHITE)
            desc_text.move_to(container.get_right() + LEFT*2.8)
            
            item = VGroup(container, icon, name_text, desc_text)
            item.shift(UP*1.8 + DOWN*i*0.9)
            feature_grid.add(item)
        
        self.play(
            LaggedStart(*[FadeIn(item, shift=RIGHT*0.4) for item in feature_grid], lag_ratio=0.3),
            run_time=6
        )
        self.wait(3)
        
        # Data augmentation note
        augmentation = VGroup(
            Text("Data Augmentation Techniques:", font_size=32, color=VIBRANT_ORANGE, weight=BOLD),
            Text("• Add synthetic noise  • Rotate/flip  • Time scaling  • SNR variation", 
                 font_size=24, color=TEXT_WHITE)
        ).arrange(DOWN*0.6, buff=0.3)
        augmentation.to_edge(DOWN, buff=0.8)
        
        self.play(Write(augmentation), run_time=3.5)
        self.wait(4)


# ============================================================================
# PART 9: WHERE AI FITS - TRACKING (13-25s)
# ============================================================================
class Part9(ThreeDScene):
    def construct(self):
        
        title = Text("AI Stage 4: Target Tracking", font_size=54, color=NEON_PINK, weight=BOLD)
        self.add_fixed_in_frame_mobjects(title)
        title.to_edge(UP, buff=0.5)
        
        self.play(Write(title), run_time=2.5)
        self.wait(2)
        
        self.set_camera_orientation(phi=60*DEGREES, theta=-45*DEGREES)
        
        # Recurrent Neural Network (LSTM) for tracking
        # Sequential processing visualization
        
        # Time steps
        time_steps = 5
        lstm_cells = []
        
        for t in range(time_steps):
            # LSTM cell structure
            cell_box = Cube(side_length=0.6, color=TECH_CYAN, 
                           fill_opacity=0.4, stroke_width=3)
            cell_box.shift(LEFT*3 + RIGHT*t*1.5 + UP*0.3)
            
            # Internal gates representation (small spheres)
            gates = VGroup(*[
                Sphere(radius=0.08, color=NEON_PINK, fill_opacity=0.8, resolution=(8, 8))
                .shift(cell_box.get_center() + UP*0.15*i + RIGHT*0.15*j)
                for i in [-1, 1] for j in [-1, 1]
            ])
            
            lstm_cells.append(VGroup(cell_box, gates))
        
        # Hidden state connections
        connections = VGroup(*[
            Arrow3D(lstm_cells[i][0].get_right(), lstm_cells[i+1][0].get_left(),
                   color=VIBRANT_ORANGE, thickness=0.02)
            for i in range(time_steps-1)
        ])
        
        # Input/output arrows
        inputs = VGroup(*[
            Arrow3D(cell[0].get_center() + DOWN*0.8, cell[0].get_bottom(),
                   color=TECH_CYAN, thickness=0.015)
            for cell in lstm_cells
        ])
        
        outputs = VGroup(*[
            Arrow3D(cell[0].get_top(), cell[0].get_center() + UP*0.8,
                   color=NEON_PINK, thickness=0.015)
            for cell in lstm_cells
        ])
        
        # Time labels
        time_labels = VGroup(*[
            Text(f"t-{time_steps-1-i}", font_size=18, color=TEXT_WHITE)
            for i in range(time_steps)
        ])
        
        self.add_fixed_in_frame_mobjects(*time_labels)
        for i, label in enumerate(time_labels):
            label.to_edge(DOWN, buff=1.5).shift(LEFT*3 + RIGHT*i*1.5)
        
        # Animate
        self.play(
            LaggedStart(*[FadeIn(cell) for cell in lstm_cells], lag_ratio=0.25),
            run_time=4
        )
        
        self.play(Create(connections), run_time=2.5)
        self.wait(1.5)
        
        self.play(
            Create(inputs), Create(outputs),
            LaggedStart(*[Write(label) for label in time_labels], lag_ratio=0.2),
            run_time=3
        )
        self.wait(2)
        
        # Show data flow
        for _ in range(2):
            self.play(
                LaggedStart(*[
                    cell[0].animate.set_fill(opacity=0.8).set_fill(opacity=0.4)
                    for cell in lstm_cells
                ], lag_ratio=0.2),
                run_time=2.5
            )
            self.wait(0.5)
        
        # Task description
        task = Text("Predict future position & velocity", 
                   font_size=30, color=VIBRANT_ORANGE, weight=BOLD)
        self.add_fixed_in_frame_mobjects(task)
        task.to_edge(DOWN, buff=0.5)
        
        self.play(Write(task), run_time=2.5)
        self.wait(3)


# ============================================================================
# PART 10: AI TRAINING DATA - TRACKING (13-25s)
# ============================================================================
class Part10(Scene):
    def construct(self):
        
        title = Text("Training Data: Tracking AI", font_size=54, color=TECH_CYAN, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        
        self.play(Write(title), run_time=2.5)
        self.wait(2)
        
        # Sequential trajectory visualization
        axes = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            z_range=[0, 3, 1],
            x_length=6,
            y_length=6,
            z_length=3,
            axis_config={"color": SUBTLE_NAVY, "stroke_width": 2}
        )
        
        # Multiple trajectories
        trajectories = [
            # Straight line
            ([(-4, -3, 0.5), (-2, -1, 0.8), (0, 1, 1.2), (2, 3, 1.5), (4, 4, 1.8)], TECH_CYAN, "Linear"),
            # Curved path
            ([(-3, 2, 0.5), (-1, 3, 1), (1, 2.5, 1.5), (3, 1, 2), (4, -1, 2.3)], NEON_PINK, "Curved"),
            # Maneuvering
            ([(-2, -4, 0.5), (0, -3, 1), (1, -1, 1.2), (1, 1, 1.5), (0, 3, 2)], VIBRANT_ORANGE, "Maneuver"),
        ]
        
        traj_objects = VGroup()
        
        for points, color, traj_type in trajectories:
            # Points
            dots = VGroup(*[
                Dot3D(point=np.array(p), radius=0.08, color=color)
                for p in points
            ])
            
            # Connecting path
            path = VMobject(color=color, stroke_width=4)
            path.set_points_as_corners([np.array(p) for p in points])
            
            # Velocity vectors
            vectors = VGroup(*[
                Arrow(
                    start=np.array(points[i]),
                    end=np.array(points[i]) + 0.5*(np.array(points[i+1]) - np.array(points[i])),
                    color=color, stroke_width=3, buff=0
                )
                for i in range(len(points)-1)
            ])
            
            traj_objects.add(VGroup(dots, path, vectors))
        
        # Labels
        labels = VGroup(*[
            Text(traj_type, font_size=24, color=color, weight=BOLD)
            .to_edge(LEFT, buff=0.5).shift(UP*1.5 + DOWN*i*0.6)
            for i, (_, color, traj_type) in enumerate(trajectories)
        ])
        
        self.play(Create(axes), run_time=2.5)
        self.wait(1.5)
        
        # Animate trajectories sequentially
        for i, traj in enumerate(traj_objects):
            self.play(
                FadeIn(traj[0], lag_ratio=0.2),  # Dots
                Create(traj[1]),                  # Path
                run_time=2.5
            )
            self.play(
                LaggedStart(*[GrowArrow(vec) for vec in traj[2]], lag_ratio=0.3),
                Write(labels[i]),
                run_time=2
            )
            self.wait(1)
        
        # Data requirement
        requirement = Text("Need: Position + Velocity + Acceleration over time", 
                          font_size=28, color=VIBRANT_ORANGE, weight=BOLD)
        requirement.to_edge(DOWN, buff=0.8)
        
        self.play(Write(requirement), run_time=2.5)
        self.wait(4)


# ============================================================================
# PART 11: WHERE AI FITS - PARAMETER OPTIMIZATION (13-25s)
# ============================================================================
class Part11(ThreeDScene):
    def construct(self):
        
        title = Text("AI Stage 5: Adaptive Waveform Design", font_size=48, color=NEON_PINK, weight=BOLD)
        self.add_fixed_in_frame_mobjects(title)
        title.to_edge(UP, buff=0.5)
        
        self.play(Write(title), run_time=2.5)
        self.wait(2)
        
        self.set_camera_orientation(phi=70*DEGREES, theta=-50*DEGREES)
        
        # Reinforcement Learning Agent
        # State -> Agent -> Action loop
        
        # Environment (radar scene)
        environment = Cube(side_length=2, color=SUBTLE_NAVY, 
                          fill_opacity=0.2, stroke_width=3)
        environment.shift(LEFT*3)
        
        env_label = Text("Radar\nEnvironment", font_size=22, color=TEXT_WHITE)
        self.add_fixed_in_frame_mobjects(env_label)
        env_label.to_edge(LEFT, buff=0.3).shift(UP*0.5)
        
        # AI Agent (brain)
        agent = VGroup()
        
        # Central processor
        brain_core = Sphere(radius=0.6, color=NEON_PINK, 
                           fill_opacity=0.7, resolution=(15, 15))
        
        # Neural connections around brain
        connections_brain = VGroup(*[
            Line3D(
                brain_core.get_center(),
                brain_core.get_center() + 0.8*np.array([
                    np.cos(i*45*DEGREES), 
                    np.sin(i*45*DEGREES), 
                    0.3*np.sin(i*22.5*DEGREES)
                ]),
                color=VIBRANT_ORANGE, stroke_width=2
            )
            for i in range(8)
        ])
        
        agent = VGroup(brain_core, connections_brain)
        agent.shift(RIGHT*1)
        
        agent_label = Text("RL Agent", font_size=26, color=NEON_PINK, weight=BOLD)
        self.add_fixed_in_frame_mobjects(agent_label)
        agent_label.shift(UP*2.3 + RIGHT*0.8)
        
        # Action output (waveform parameters)
        action_box = RoundedRectangle(
            width=2, height=1.5, corner_radius=0.2,
            color=TECH_CYAN, stroke_width=4, fill_opacity=0.2
        )
        action_box.shift(RIGHT*4)
        
        action_label = Text("Waveform\nParameters", font_size=20, color=TECH_CYAN)
        self.add_fixed_in_frame_mobjects(action_label)
        action_label.to_edge(RIGHT, buff=0.3)
        
        # Arrows
        state_arrow = Arrow3D(environment.get_right(), brain_core.get_left(),
                             color=TECH_CYAN, thickness=0.03)
        action_arrow = Arrow3D(brain_core.get_right(), action_box.get_left() + LEFT*0.3,
                              color=NEON_PINK, thickness=0.03)
        reward_arrow = CurvedArrow(
            action_box.get_bottom() + DOWN*0.5,
            brain_core.get_bottom() + DOWN*0.3,
            color=VIBRANT_ORANGE, angle=-TAU/4
        )      
        # Labels on arrows
        state_text = Text("State", font_size=18, color=TECH_CYAN)
        action_text = Text("Action", font_size=18, color=NEON_PINK)
        reward_text = Text("Reward", font_size=18, color=VIBRANT_ORANGE)
        
        self.add_fixed_in_frame_mobjects(state_text, action_text, reward_text)
        state_text.shift(LEFT*1.2 + UP*0.8)
        action_text.shift(RIGHT*2.5 + UP*0.8)
        reward_text.shift(RIGHT*1.5 + DOWN*1.8)
        
        # Animate
        self.play(
            FadeIn(environment),
            Write(env_label),
            run_time=2
        )
        self.wait(1.5)
        
        self.play(
            FadeIn(agent),
            Write(agent_label),
            run_time=2.5
        )
        self.wait(1.5)
        
        self.play(
            Create(state_arrow),
            Write(state_text),
            run_time=2
        )
        self.wait(1)
        
        self.play(
            FadeIn(action_box),
            Write(action_label),
            Create(action_arrow),
            Write(action_text),
            run_time=2.5
        )
        self.wait(1.5)
        
        self.play(
            Create(reward_arrow),
            Write(reward_text),
            run_time=2
        )
        self.wait(2)
        
        # Show learning loop
        for _ in range(2):
            self.play(
                Flash(brain_core, color=NEON_PINK, flash_radius=1, num_lines=12),
                connections_brain.animate.set_stroke(opacity=1).set_stroke(opacity=0.5),
                run_time=1.5
            )
            self.wait(0.5)
        
        # Task
        task = Text("Optimizes: Pulse width, PRF, bandwidth, power", 
                   font_size=26, color=VIBRANT_ORANGE, weight=BOLD)
        self.add_fixed_in_frame_mobjects(task)
        task.to_edge(DOWN, buff=0.8)
        
        self.play(Write(task), run_time=2.5)
        self.wait(3)


# ============================================================================
# PART 12: AI TRAINING DATA - WAVEFORM OPTIMIZATION (13-25s)
# ============================================================================
class Part12(Scene):
    def construct(self):
        
        title = Text("Training Data: Waveform Optimization", font_size=48, color=TECH_CYAN, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        
        self.play(Write(title), run_time=2.5)
        self.wait(2)
        
        # Simulation-based training
        sim_title = Text("Simulation Environment", font_size=36, color=NEON_PINK, weight=BOLD)
        sim_title.shift(UP*2.5)
        
        self.play(Write(sim_title), run_time=2)
        self.wait(1.5)
        
        # Training components
        components = [
            ("Target Scenarios", TECH_CYAN, 
             "Multiple targets, speeds, RCS"),
            ("Clutter Models", NEON_PINK, 
             "Ground, sea, weather clutter"),
            ("Interference", VIBRANT_ORANGE, 
             "Jamming, multipath, EMI"),
            ("Sensor Constraints", TECH_CYAN, 
             "Power, bandwidth, PRF limits"),
            ("Performance Metrics", NEON_PINK, 
             "Detection prob, false alarms"),
        ]
        
        comp_grid = VGroup()
        
        for i, (comp_name, color, description) in enumerate(components):
            # Box
            box = RoundedRectangle(
                width=10.5, height=0.85, corner_radius=0.15,
                color=color, stroke_width=4, fill_opacity=0.2
            )
            
            # Icon
            if i == 0:
                icon = Triangle(color=color, fill_opacity=0.6, stroke_width=2).scale(0.25)
            elif i == 1:
                icon = Square(color=color, fill_opacity=0.6, stroke_width=2).scale(0.2)
            elif i == 2:
                icon = Star(n=5, color=color, fill_opacity=0.6, stroke_width=2, outer_radius=0.2)
            elif i == 3:
                icon = RegularPolygon(6, color=color, fill_opacity=0.6, stroke_width=2).scale(0.2)
            else:
                icon = Circle(color=color, fill_opacity=0.6, stroke_width=2, radius=0.18)
            
            icon.move_to(box.get_left() + RIGHT*0.5)

            # Component name
            name_text = Text(comp_name, font_size=28, color=color, weight=BOLD)
            name_text.next_to(icon, RIGHT, buff=0.4)
            
            # Description
            desc_text = Text(description, font_size=20, color=TEXT_WHITE)
            desc_text.next_to(box.get_right(), LEFT, buff=0.5)
            
            item = VGroup(box, icon, name_text, desc_text)
            item.shift(UP*1.6 + DOWN*i*0.85)
            comp_grid.add(item)
        
        self.play(
            LaggedStart(*[FadeIn(item, shift=RIGHT*0.3) for item in comp_grid], lag_ratio=0.3),
            run_time=6
        )
        self.wait(3)
        
        # Reward function
        reward = VGroup(
            Text("Reward Function:", font_size=32, color=VIBRANT_ORANGE, weight=BOLD),
            Text("R = P_detection - λ₁·P_false_alarm - λ₂·Power - λ₃·Bandwidth", 
                 font_size=24, color=TEXT_WHITE)
        ).arrange(DOWN, buff=0.3)
        reward.to_edge(DOWN, buff=0.8)
        
        self.play(Write(reward), run_time=3.5)
        self.wait(4)


# ============================================================================
# PART 13: WHERE AI FITS - INTERFERENCE MITIGATION (13-25s)
# ============================================================================
class Part13(ThreeDScene):
    def construct(self):
        
        title = Text("AI Stage 6: Interference Mitigation", font_size=50, color=NEON_PINK, weight=BOLD)
        self.add_fixed_in_frame_mobjects(title)
        title.to_edge(UP, buff=0.5)
        
        self.play(Write(title), run_time=2.5)
        self.wait(2)
        
        self.set_camera_orientation(phi=65*DEGREES, theta=-55*DEGREES)
        
        # Autoencoder architecture for noise reduction
        # Encoder
        encoder_layers = []
        sizes = [8, 6, 4, 2]  # Compression
        colors = [TECH_CYAN, NEON_PINK, VIBRANT_ORANGE, NEON_PINK]
        
        for i, (size, color) in enumerate(zip(sizes, colors)):
            layer = VGroup(*[
                Sphere(radius=0.12, color=color, fill_opacity=0.75, resolution=(10, 10))
                .shift(LEFT*4 + RIGHT*i*1.8 + UP*(2-j*4/(size-1 if size > 1 else 1)))
                for j in range(size)
            ])
            encoder_layers.append(layer)
        
        # Decoder (mirror)
        decoder_layers = []
        sizes_dec = [4, 6, 8]
        colors_dec = [VIBRANT_ORANGE, NEON_PINK, TECH_CYAN]
        
        for i, (size, color) in enumerate(zip(sizes_dec, colors_dec)):
            layer = VGroup(*[
                Sphere(radius=0.12, color=color, fill_opacity=0.75, resolution=(10, 10))
                .shift(RIGHT*0.5 + RIGHT*i*1.8 + UP*(2-j*4/(size-1 if size > 1 else 1)))
                for j in range(size)
            ])
            decoder_layers.append(layer)
        
        # Latent space (bottleneck)
        latent = encoder_layers[-1]
        
        # Labels
        input_label = Text("Noisy\nSignal", font_size=22, color=TECH_CYAN)
        latent_label = Text("Latent\nCode", font_size=20, color=NEON_PINK)
        output_label = Text("Clean\nSignal", font_size=22, color=TECH_CYAN)
        
        self.add_fixed_in_frame_mobjects(input_label, latent_label, output_label)
        input_label.to_edge(LEFT, buff=0.3).shift(UP*0.3)
        latent_label.shift(UP*2.8)
        output_label.to_edge(RIGHT, buff=0.3).shift(UP*0.3)
        
        # Animate encoder
        self.play(
            LaggedStart(*[
                FadeIn(layer, lag_ratio=0.1) for layer in encoder_layers
            ], lag_ratio=0.35),
            run_time=4
        )
        
        self.play(Write(input_label), Write(latent_label), run_time=2)
        self.wait(1.5)
        
        # Animate decoder
        self.play(
            LaggedStart(*[
                FadeIn(layer, lag_ratio=0.1) for layer in decoder_layers
            ], lag_ratio=0.35),
            run_time=4
        )
        
        self.play(Write(output_label), run_time=2)
        self.wait(2)
        
        # Show compression-decompression flow
        for _ in range(2):
            # Forward pass
            all_layers = encoder_layers + decoder_layers
            self.play(
                LaggedStart(*[
                    layer.animate.set_fill(opacity=1).scale(1.15).set_fill(opacity=0.75).scale(1/1.15)
                    for layer in all_layers
                ], lag_ratio=0.15),
                run_time=3.5
            )
            self.wait(0.8)
        
        # Task
        task = Text("Removes: Jamming, EMI, Multipath interference", 
                   font_size=28, color=VIBRANT_ORANGE, weight=BOLD)
        self.add_fixed_in_frame_mobjects(task)
        task.to_edge(DOWN, buff=0.8)
        
        self.play(Write(task), run_time=2.5)
        self.wait(3)


# ============================================================================
# PART 14: AI TRAINING DATA - INTERFERENCE MITIGATION (13-25s)
# ============================================================================
class Part14(Scene):
    def construct(self):
        
        title = Text("Training Data: Interference Mitigation", font_size=48, color=TECH_CYAN, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        
        self.play(Write(title), run_time=2.5)
        self.wait(2)
        
        # Paired data visualization
        subtitle = Text("Paired Training Samples", font_size=32, color=NEON_PINK, weight=BOLD)
        subtitle.shift(UP*2.5)
        
        self.play(Write(subtitle), run_time=2)
        self.wait(1.5)
        
        # Show spectrogram pairs
        # Clean + Interference = Noisy
        axes_clean = Axes(
            x_range=[0, 10, 2], y_range=[0, 5, 1],
            x_length=3.5, y_length=2.5,
            axis_config={"color": SUBTLE_NAVY, "stroke_width": 2}
        ).shift(LEFT*5 + UP*0.3)
        
        axes_interference = axes_clean.copy().shift(RIGHT*4.5)
        axes_noisy = axes_clean.copy().shift(RIGHT*9)
        
        # Clean signal
        clean_signal = axes_clean.plot(
            lambda x: 2.5 + np.sin(2*x),
            color=TECH_CYAN, stroke_width=4
        )
        
        # Interference
        interference = axes_interference.plot(
            lambda x: 1.5 + 0.8*np.sin(8*x),
            color=NEON_PINK, stroke_width=4
        )
        
        # Noisy (sum)
        noisy_signal = axes_noisy.plot(
            lambda x: 2.5 + np.sin(2*x) + 1.5 + 0.8*np.sin(8*x),
            color=VIBRANT_ORANGE, stroke_width=4
        )
        
        # Labels
        label_clean = Text("Clean\nSignal", font_size=24, color=TECH_CYAN, weight=BOLD)
        label_clean.next_to(axes_clean, DOWN, buff=0.3)
        
        label_interf = Text("Interference", font_size=24, color=NEON_PINK, weight=BOLD)
        label_interf.next_to(axes_interference, DOWN, buff=0.3)
        
        label_noisy = Text("Noisy\nSignal", font_size=24, color=VIBRANT_ORANGE, weight=BOLD)
        label_noisy.next_to(axes_noisy, DOWN, buff=0.3)
        
        # Plus and equals signs
        plus = Text("+", font_size=48, color=TEXT_WHITE, weight=BOLD)
        plus.move_to((axes_clean.get_right() + axes_interference.get_left())/2)
        
        equals = Text("=", font_size=48, color=TEXT_WHITE, weight=BOLD)
        equals.move_to((axes_interference.get_right() + axes_noisy.get_left())/2)
        
        # Animate
        self.play(
            Create(axes_clean),
            Create(clean_signal),
            Write(label_clean),
            run_time=2.5
        )
        self.wait(1.5)
        
        self.play(Write(plus), run_time=1)
        
        self.play(
            Create(axes_interference),
            Create(interference),
            Write(label_interf),
            run_time=2.5
        )
        self.wait(1.5)
        
        self.play(Write(equals), run_time=1)
        
        self.play(
            Create(axes_noisy),
            Create(noisy_signal),
            Write(label_noisy),
            run_time=2.5
        )
        self.wait(2)
        
        # Training approach
        approach = VGroup(
            Text("Training Approach:", font_size=30, color=VIBRANT_ORANGE, weight=BOLD),
            Text("Input: Noisy Signal  →  Target: Clean Signal", font_size=26, color=TEXT_WHITE)
        ).arrange(DOWN, buff=0.3)
        approach.to_edge(DOWN, buff=0.8)
        
        self.play(Write(approach), run_time=3)
        self.wait(4)


# ============================================================================
# PART 15: WHERE AI FITS - BEAMFORMING (13-25s)
# ============================================================================
class Part15(ThreeDScene):
    def construct(self):
        
        title = Text("AI Stage 7: Adaptive Beamforming", font_size=52, color=NEON_PINK, weight=BOLD)
        self.add_fixed_in_frame_mobjects(title)
        title.to_edge(UP, buff=0.5)
        
        self.play(Write(title), run_time=2.5)
        self.wait(2)
        
        self.set_camera_orientation(phi=75*DEGREES, theta=-60*DEGREES)
        
        # Antenna array
        num_antennas = 8
        antenna_array = VGroup(*[
            Cylinder(radius=0.1, height=0.8, color=TECH_CYAN, 
                    fill_opacity=0.7, stroke_width=2)
            .rotate(90*DEGREES, axis=RIGHT)
            .shift(LEFT*3 + RIGHT*i*0.6 + DOWN*1.5)
            for i in range(num_antennas)
        ])
        
        # Neural network for weight calculation
        # Input: Array signals
        input_nodes = VGroup(*[
            Sphere(radius=0.1, color=TECH_CYAN, fill_opacity=0.8, resolution=(8, 8))
            .shift(LEFT*2.5 + RIGHT*i*0.6 + UP*0.3)
            for i in range(num_antennas)
        ])
        
        # Hidden layer
        hidden_nodes = VGroup(*[
            Sphere(radius=0.15, color=NEON_PINK, fill_opacity=0.8, resolution=(10, 10))
            .shift(UP*1.0 + LEFT*1 + RIGHT*i*0.8)
            for i in range(6)
        ])
        
        # Output: Weights
        output_nodes = VGroup(*[
            Sphere(radius=0.12, color=VIBRANT_ORANGE, fill_opacity=0.8, resolution=(8, 8))
            .shift(RIGHT*2 + RIGHT*i*0.6 + UP*0.3)
            for i in range(num_antennas)
        ])
        
        # Beams (cones from array)
        main_beam = Cone(base_radius=1.5, height=3, color=TECH_CYAN, 
                        fill_opacity=0.2, stroke_width=2)
        main_beam.rotate(90*DEGREES, axis=RIGHT)
        main_beam.shift(DOWN*0.2)
        
        # Labels
        array_label = Text("Antenna\nArray", font_size=22, color=TECH_CYAN)
        
        # New Labels for clarity
        input_label = Text("Signal Data", font_size=18, color=TECH_CYAN)
        nn_label = Text("Neural Net\nWeight Calculator", font_size=20, color=NEON_PINK, weight=BOLD)
        output_label = Text("Phase Weights", font_size=18, color=VIBRANT_ORANGE)
        
        beam_label = Text("Adaptive\nBeam", font_size=22, color=TECH_CYAN)
        
        self.add_fixed_in_frame_mobjects(array_label, input_label, nn_label, output_label, beam_label)
        
        # Position labels
        array_label.to_edge(LEFT, buff=0.3).shift(DOWN*2.0)
        
        # Position labels relative to 3D positions logic (projected roughly)
        input_label.shift(LEFT*2.5 + UP*1.2)
        nn_label.shift(UP*2.2) # Lowered from 2.8 to avoid title overlap
        output_label.shift(RIGHT*2.5 + UP*1.2)
        
        beam_label.to_edge(RIGHT, buff=0.3).shift(UP*1)
        
        # Animate
        self.play(
            LaggedStart(*[FadeIn(ant, scale=0.5) for ant in antenna_array], lag_ratio=0.15),
            Write(array_label),
            run_time=3
        )
        self.wait(1)
        
        # Show flow: Antenna -> Signal -> NN -> Weights
        self.play(
            FadeIn(input_nodes, shift=UP*0.5),
            Write(input_label),
            run_time=2
        )
        
        self.play(
            FadeIn(hidden_nodes, scale=0.5),
            Write(nn_label),
            run_time=2
        )
        
        self.play(
            FadeIn(output_nodes, shift=UP*0.5),
            Write(output_label),
            run_time=2
        )
        self.wait(1.5)
        
        # Show beam formation
        self.play(
            FadeIn(main_beam, scale=0.5),
            Write(beam_label),
            run_time=2.5
        )
        self.wait(2)
        
        # Beam steering animation
        for angle in [20, -20, 0]:
            self.play(
                Rotate(main_beam, angle=angle*DEGREES, axis=UP),
                Flash(hidden_nodes, color=NEON_PINK, flash_radius=0.5),
                output_nodes.animate.set_color(TECH_CYAN).set_color(VIBRANT_ORANGE),
                run_time=2
            )
            self.wait(0.5)
        
        # Task
        task = Text("Maximizes SINR, nulls interference directions", 
                   font_size=28, color=VIBRANT_ORANGE, weight=BOLD)
        self.add_fixed_in_frame_mobjects(task)
        task.to_edge(DOWN, buff=0.8)
        
        self.play(Write(task), run_time=2.5)
        self.wait(3)


# ============================================================================
# PART 16: COMPLETE AI-RADAR PIPELINE (13-25s)
# ============================================================================
class Part16(Scene):
    def construct(self):
        
        title = Text("Complete AI-Enhanced Radar Pipeline", font_size=48, color=TECH_CYAN, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        
        self.play(Write(title), run_time=2.5)
        self.wait(2)
        
        # Full pipeline stages
        stages = [
            ("Raw Signal", UP*2.5 + LEFT*5, TECH_CYAN),
            ("AI: Preprocessing", UP*2.5 + LEFT*2, NEON_PINK),
            ("AI: Detection", UP*2.5 + RIGHT*1.5, VIBRANT_ORANGE),
            ("AI: Classification", UP*0.5 + RIGHT*4, TECH_CYAN),
            ("AI: Tracking", DOWN*1 + RIGHT*4, NEON_PINK),
            ("AI: Beamforming", DOWN*1 + LEFT*4, VIBRANT_ORANGE),
            ("AI: Waveform Opt", DOWN*1 + ORIGIN, TECH_CYAN),
            ("Decision Output", DOWN*2.5 + LEFT*2, NEON_PINK),
        ]
        
        stage_boxes = VGroup()
        stage_labels = VGroup()
        
        for stage_name, pos, color in stages:
            box = RoundedRectangle(
                width=2.2, height=0.8, corner_radius=0.15,
                color=color, stroke_width=4, fill_opacity=0.25
            )
            box.move_to(pos)
            
            label = Text(stage_name, font_size=20, color=TEXT_WHITE, weight=BOLD)
            label.move_to(box.get_center())
            
            stage_boxes.add(box)
            stage_labels.add(label)
        
        # Connecting arrows
        connections = VGroup(
            Arrow(stage_boxes[0].get_right(), stage_boxes[1].get_left(), 
                  color=TEXT_WHITE, stroke_width=3, buff=0.1),
            Arrow(stage_boxes[1].get_right(), stage_boxes[2].get_left(), 
                  color=TEXT_WHITE, stroke_width=3, buff=0.1),
            Arrow(stage_boxes[2].get_bottom(), stage_boxes[3].get_top(), 
                  color=TEXT_WHITE, stroke_width=3, buff=0.1),
            Arrow(stage_boxes[3].get_bottom(), stage_boxes[4].get_top(), 
                  color=TEXT_WHITE, stroke_width=3, buff=0.1),
            Arrow(stage_boxes[4].get_left(), stage_boxes[6].get_right(), 
                  color=TEXT_WHITE, stroke_width=3, buff=0.1),
            Arrow(stage_boxes[6].get_left(), stage_boxes[5].get_right(), 
                  color=TEXT_WHITE, stroke_width=3, buff=0.1),
            Arrow(stage_boxes[5].get_bottom(), stage_boxes[7].get_top(), 
                  color=TEXT_WHITE, stroke_width=3, buff=0.1),
        )
        
        # Feedback loops
        feedback1 = CurvedArrow(
            stage_boxes[7].get_right() + RIGHT*0.3,
            stage_boxes[6].get_bottom() + DOWN*0.3,
            color=VIBRANT_ORANGE, stroke_width=3
        )
        feedback2 = CurvedArrow(
            stage_boxes[4].get_top() + UP*0.3,
            stage_boxes[2].get_right() + RIGHT*0.3,
            color=NEON_PINK, stroke_width=3
        )
        
        # Animate pipeline
        self.play(
            LaggedStart(*[
                AnimationGroup(FadeIn(box), Write(label))
                for box, label in zip(stage_boxes, stage_labels)
            ], lag_ratio=0.2),
            run_time=6
        )
        self.wait(2)
        
        self.play(
            LaggedStart(*[GrowArrow(arrow) for arrow in connections], lag_ratio=0.25),
            run_time=4
        )
        self.wait(2)
        
        self.play(
            Create(feedback1),
            Create(feedback2),
            run_time=2.5
        )
        self.wait(2)
        
        # Flow animation
        for _ in range(2):
            self.play(
                LaggedStart(*[
                    box.animate.set_stroke(width=7).set_stroke(width=4)
                    for box in stage_boxes
                ], lag_ratio=0.15),
                run_time=3
            )
            self.wait(0.5)
        
        # Message
        message = Text("7 AI models working together!", font_size=34, color=VIBRANT_ORANGE, weight=BOLD)
        message.to_edge(DOWN, buff=0.8)
        
        self.play(Write(message), run_time=2.5)
        self.wait(3)


# ============================================================================
# PART 17: TRAINING INFRASTRUCTURE (13-25s)
# ============================================================================
class Part17(Scene):
    def construct(self):
        
        title = Text("Training Infrastructure Requirements", font_size=48, color=NEON_PINK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        
        self.play(Write(title), run_time=2.5)
        self.wait(2)
        
        # Hardware requirements
        hw_title = Text("Hardware Needs", font_size=36, color=TECH_CYAN, weight=BOLD)
        hw_title.shift(LEFT*3.5 + UP*2.0)
        
        hardware = [
            ("GPU Cluster", "8x A100 GPUs", TECH_CYAN),
            ("Storage", "100TB+ SSD", NEON_PINK),
            ("RAM", "512GB+ DDR5", VIBRANT_ORANGE),
            ("Network", "100Gbps", TECH_CYAN),
        ]
        
        hw_group = VGroup()
        for i, (hw_name, spec, color) in enumerate(hardware):
            box = RoundedRectangle(
                width=5, height=0.7, corner_radius=0.12,
                color=color, stroke_width=3, fill_opacity=0.2
            )
            
            name = Text(hw_name, font_size=20, color=color, weight=BOLD)
            name.move_to(box.get_left() + RIGHT*0.2 + np.array([name.width/2, 0, 0]))
            
            spec_text = Text(spec, font_size=18, color=TEXT_WHITE)
            spec_text.move_to(box.get_right() + LEFT*0.2 + np.array([-spec_text.width/2, 0, 0]))
            
            item = VGroup(box, name, spec_text)
            # FIX: Correct vertical spacing logic to stack downwards
            item.shift(LEFT*3.5 + UP*1.2 + DOWN*i*0.9)
            hw_group.add(item)
        
        # Software stack
        sw_title = Text("Software Stack", font_size=36, color=NEON_PINK, weight=BOLD)
        sw_title.shift(RIGHT*3.5 + UP*2.0)
        
        software = [
            ("PyTorch / TF", NEON_PINK),
            ("CUDA / cuDNN", VIBRANT_ORANGE),
            ("MLflow", TECH_CYAN),
            ("Ray / Horovod", NEON_PINK),
        ]
        
        sw_group = VGroup()
        for i, (sw_name, color) in enumerate(software):
            box = RoundedRectangle(
                width=3, height=0.7, corner_radius=0.12,
                color=color, stroke_width=3, fill_opacity=0.2
            )
            
            name = Text(sw_name, font_size=24, color=color, weight=BOLD)
            name.move_to(box.get_center())
            
            item = VGroup(box, name)
            # FIX: Correct vertical spacing logic to stack downwards
            item.shift(RIGHT*3.5 + UP*1.2 + DOWN*i*0.9)
            sw_group.add(item)
        
        # Animate
        self.play(Write(hw_title), run_time=2)
        self.play(
            LaggedStart(*[FadeIn(item, shift=RIGHT*0.3) for item in hw_group], lag_ratio=0.3),
            run_time=4
        )
        self.wait(2)
        
        self.play(Write(sw_title), run_time=2)
        self.play(
            LaggedStart(*[FadeIn(item, shift=LEFT*0.3) for item in sw_group], lag_ratio=0.3),
            run_time=4
        )
        self.wait(2)
        
        # Training time estimate
        time_est = VGroup(
            Text("Training Time:", font_size=32, color=VIBRANT_ORANGE, weight=BOLD),
            Text("2-4 weeks per model", font_size=28, color=TEXT_WHITE)
        ).arrange(DOWN, buff=0.2)
        time_est.to_edge(DOWN, buff=0.8)
        
        self.play(Write(time_est), run_time=2.5)
        self.wait(4)


# ============================================================================
# PART 18: DEPLOYMENT & REAL-TIME PERFORMANCE (13-25s)
# ============================================================================
class Part18(ThreeDScene):
    def construct(self):
        
        title = Text("Deployment: Real-Time Performance", font_size=50, color=TECH_CYAN, weight=BOLD)
        self.add_fixed_in_frame_mobjects(title)
        title.to_edge(UP, buff=0.5)
        
        self.play(Write(title), run_time=2.5)
        self.wait(2)
        
        self.set_camera_orientation(phi=70*DEGREES, theta=-50*DEGREES)
        
        # Edge device (embedded GPU)
        edge_device = Prism(dimensions=[2, 1.2, 0.3], color=SUBTLE_NAVY, 
                           fill_opacity=0.7, stroke_width=3)
        edge_device.shift(DOWN*1)
        
        # GPU chip visualization
        gpu_chip = VGroup(*[
            Cube(side_length=0.15, color=TECH_CYAN, fill_opacity=0.8, stroke_width=1)
            .shift(edge_device.get_center() + UP*0.2 + RIGHT*(i-2)*0.2 + UP*(j-1)*0.2)
            for i in range(5) for j in range(3)
        ])
        
        device_label = Text("Edge GPU\n(Jetson AGX)", font_size=24, color=TECH_CYAN, weight=BOLD)
        self.add_fixed_in_frame_mobjects(device_label)
        device_label.shift(DOWN*2.3)
        
        self.play(
            FadeIn(edge_device),
            FadeIn(gpu_chip, lag_ratio=0.05),
            Write(device_label),
            run_time=3
        )
        self.wait(2)
        
        # Data flow
        # Input
        input_data = Cylinder(radius=0.3, height=0.5, color=NEON_PINK, 
                             fill_opacity=0.6, stroke_width=2)
        input_data.rotate(90*DEGREES, axis=RIGHT)
        input_data.shift(LEFT*3 + UP*0.5)
        
        input_label = Text("Radar\nData", font_size=20, color=NEON_PINK)
        self.add_fixed_in_frame_mobjects(input_label)
        input_label.shift(LEFT*3 + UP*1.8)
        
        # Output
        output_data = Cylinder(radius=0.3, height=0.5, color=VIBRANT_ORANGE, 
                              fill_opacity=0.6, stroke_width=2)
        output_data.rotate(90*DEGREES, axis=RIGHT)
        output_data.shift(RIGHT*3 + UP*0.5)
        
        output_label = Text("Detection\nResult", font_size=20, color=VIBRANT_ORANGE)
        self.add_fixed_in_frame_mobjects(output_label)
        output_label.shift(RIGHT*3 + UP*1.8)
        
        # Arrows
        input_arrow = Arrow3D(input_data.get_right(), edge_device.get_left() + LEFT*0.3,
                             color=NEON_PINK, thickness=0.03)
        output_arrow = Arrow3D(edge_device.get_right() + RIGHT*0.3, output_data.get_left(),
                              color=VIBRANT_ORANGE, thickness=0.03)
        
        self.play(
            FadeIn(input_data),
            Write(input_label),
            run_time=2
        )
        self.wait(1)
        
        self.play(Create(input_arrow), run_time=1.5)
        
        # Processing animation
        for _ in range(3):
            self.play(
                gpu_chip.animate.set_fill(opacity=1).set_fill(opacity=0.8),
                Flash(edge_device, color=TECH_CYAN, flash_radius=1.5, num_lines=16),
                run_time=1.2
            )
            self.wait(0.3)
        
        self.play(Create(output_arrow), run_time=1.5)
        
        self.play(
            FadeIn(output_data),
            Write(output_label),
            run_time=2
        )
        self.wait(2)
        
        # Performance metrics
        metrics = VGroup(
            Text("Latency: <50ms", font_size=26, color=TECH_CYAN),
            Text("Throughput: 100 frames/s", font_size=26, color=NEON_PINK),
            Text("Power: <30W", font_size=26, color=VIBRANT_ORANGE),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        
        self.add_fixed_in_frame_mobjects(*metrics)
        metrics.to_edge(LEFT, buff=0.5).shift(DOWN*1.5)
        
        self.play(
            LaggedStart(*[Write(metric) for metric in metrics], lag_ratio=0.4),
            run_time=3
        )
        self.wait(4)


# ============================================================================
# PART 19: FUTURE TRENDS & CHALLENGES (13-25s)
# ============================================================================
class Part19(Scene):
    def construct(self):
        
        title = Text("Future: AI-Radar Evolution", font_size=54, color=NEON_PINK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        
        self.play(Write(title), run_time=2.5)
        self.wait(2)
        
        # Split into two columns
        # Left: Emerging Trends
        trends_title = Text("Emerging Trends", font_size=34, color=TECH_CYAN, weight=BOLD)
        trends_title.shift(LEFT*3.2 + UP*2.2)
        
        trends = [
            ("Federated Learning", "Train across multiple radars"),
            ("Few-Shot Learning", "Adapt with minimal data"),
            ("Neural Architecture Search", "Auto-design networks"),
            ("Quantum ML", "Next-gen processing"),
        ]
        
        trends_group = VGroup()
        for i, (trend_name, description) in enumerate(trends):
            # Star icon
            star = Star(n=5, outer_radius=0.15, color=TECH_CYAN, 
                       fill_opacity=0.7, stroke_width=2)
            
            # Text
            name = Text(trend_name, font_size=24, color=TECH_CYAN, weight=BOLD)
            desc = Text(description, font_size=18, color=TEXT_WHITE)
            
            text_group = VGroup(name, desc).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
            
            item = VGroup(star, text_group)
            text_group.next_to(star, RIGHT, buff=0.3)
            
            # FIX: Correct vertical spacing logic to stack downwards
            item.shift(LEFT*5 + UP*1.2 + DOWN*i*1.1)
            trends_group.add(item)
        
        # Right: Challenges
        challenges_title = Text("Key Challenges", font_size=34, color=VIBRANT_ORANGE, weight=BOLD)
        challenges_title.shift(RIGHT*2.5 + UP*2.2)
        
        challenges = [
            ("Adversarial Robustness", "Resist spoofing attacks"),
            ("Explainability", "Trust AI decisions"),
            ("Data Scarcity", "Limited labeled samples"),
            ("Real-time Constraints", "Ultra-low latency"),
        ]
        
        challenges_group = VGroup()
        for i, (chal_name, description) in enumerate(challenges):
            # Warning icon
            warning = RegularPolygon(n=3, color=VIBRANT_ORANGE, 
                                    fill_opacity=0.7, stroke_width=2)
            warning.rotate(180*DEGREES).scale(0.35)
            
            # Text
            name = Text(chal_name, font_size=24, color=VIBRANT_ORANGE, weight=BOLD)
            desc = Text(description, font_size=18, color=TEXT_WHITE)
            
            text_group = VGroup(name, desc).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
            
            item = VGroup(warning, text_group)
            text_group.next_to(warning, RIGHT, buff=0.3)
            
            # FIX: Correct vertical spacing logic to stack downwards
            item.shift(RIGHT*1.25 + UP*1.2 + DOWN*i*1.1)
            challenges_group.add(item)
        
        # Animate
        self.play(Write(trends_title), run_time=2)
        self.play(
            LaggedStart(*[
                AnimationGroup(
                    FadeIn(item[0], scale=1.5),
                    Write(item[1])
                )
                for item in trends_group
            ], lag_ratio=0.35),
            run_time=5
        )
        self.wait(2)
        
        self.play(Write(challenges_title), run_time=2)
        self.play(
            LaggedStart(*[
                AnimationGroup(
                    FadeIn(item[0], scale=1.5),
                    Write(item[1])
                )
                for item in challenges_group
            ], lag_ratio=0.35),
            run_time=5
        )
        self.wait(3)
        
        # Bottom message
        message = Text("The future is intelligent radar systems!", 
                      font_size=36, color=NEON_PINK, weight=BOLD)
        message.to_edge(DOWN, buff=0.8)
        
        self.play(Write(message), run_time=2.5)
        self.wait(4)


# ============================================================================
# PART 20: SUMMARY & CONCLUSION (13-25s)
# ============================================================================
class Part20(ThreeDScene):
    def construct(self):
        
        # Main title
        main_title = Text("AI in Radar: Complete Integration", font_size=52, color=TECH_CYAN, weight=BOLD)
        self.add_fixed_in_frame_mobjects(main_title)
        main_title.to_edge(UP, buff=0.2)
        
        self.play(Write(main_title), run_time=3)
        self.wait(2)
        
        self.set_camera_orientation(phi=70*DEGREES, theta=-60*DEGREES)
        
        # 7 AI stages in 3D circle
        stages = [
            "Signal Processing",
            "Detection",
            "Classification",
            "Tracking",
            "Beamforming",
            "Waveform Opt",
            "Interference"
        ]
        
        colors = [TECH_CYAN, NEON_PINK, VIBRANT_ORANGE, TECH_CYAN, 
                 NEON_PINK, VIBRANT_ORANGE, TECH_CYAN]
        
        radius = 2.1
        stage_objects = VGroup()
        
        for i, (stage, color) in enumerate(zip(stages, colors)):
            angle = i * (360 / len(stages)) * DEGREES
            pos = radius * (np.cos(angle)*RIGHT + np.sin(angle)*UP)
            
            # Stage sphere
            sphere = Sphere(radius=0.35, color=color, fill_opacity=0.8, 
                           resolution=(12, 12))
            sphere.move_to(pos)
            
            # Label
            label = Text(stage, font_size=16, color=color, weight=BOLD)
            self.add_fixed_in_frame_mobjects(label)
            
            # Position label
            label_angle = i * (360 / len(stages))
            if 45 < label_angle < 135:
                label.next_to(sphere, UP*1.25, buff=0.3)
            elif 135 < label_angle < 225:
                label.next_to(sphere, LEFT, buff=0.3)
            elif 225 < label_angle < 315:
                label.next_to(sphere, DOWN, buff=0.3)
            else:
                label.next_to(sphere, RIGHT, buff=0.3)
            
            stage_objects.add(VGroup(sphere, label))
        
        # Central AI brain
        central_brain = Sphere(radius=0.8, color=NEON_PINK, 
                              fill_opacity=0.6, resolution=(20, 20))
        
        brain_label = Text("AI Core", font_size=28, color=NEON_PINK, weight=BOLD)
        self.add_fixed_in_frame_mobjects(brain_label)
        brain_label.shift(UP*0.3)
        
        # Connections from center to stages
        connections = VGroup(*[
            Line3D(ORIGIN, stage[0].get_center(), color=SUBTLE_NAVY, 
                  stroke_width=3, stroke_opacity=0.5)
            for stage in stage_objects
        ])
        
        # Animate
        self.play(
            FadeIn(central_brain, scale=0.5),
            Write(brain_label),
            run_time=2.5
        )
        self.wait(1.5)
        
        self.play(Create(connections), run_time=2)
        self.wait(1)
        
        self.play(
            LaggedStart(*[
                AnimationGroup(
                    FadeIn(stage[0], scale=0.5),
                    Write(stage[1])
                )
                for stage in stage_objects
            ], lag_ratio=0.2),
            run_time=5
        )
        self.wait(2)
        
        # Rotate the whole system
        full_system = VGroup(central_brain, connections, 
                            *[stage[0] for stage in stage_objects])
        
        self.play(
            Rotate(full_system, angle=360*DEGREES, axis=UP),
            run_time=5
        )
        self.wait(2)
        
        # Pulse effect
        for _ in range(2):
            self.play(
                central_brain.animate.set_fill(opacity=1).scale(1.2).set_fill(opacity=0.6).scale(1/1.2),
                LaggedStart(*[
                    stage[0].animate.set_fill(opacity=1).scale(1.15).set_fill(opacity=0.8).scale(1/1.15)
                    for stage in stage_objects
                ], lag_ratio=0.1),
                run_time=2.5
            )
            self.wait(0.5)
        
        # Final messages
        key_points = VGroup(
            Text("✓ 7 AI Integration Points", font_size=28, color=TECH_CYAN),
            Text("✓ Multi-Modal Training Data", font_size=28, color=NEON_PINK),
            Text("✓ Real-Time Edge Deployment", font_size=28, color=VIBRANT_ORANGE),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        
        self.add_fixed_in_frame_mobjects(*key_points)
        key_points.to_corner(DL, buff=1.0)
        
        self.play(
            LaggedStart(*[Write(point) for point in key_points], lag_ratio=0.4),
            run_time=3.5
        )
        self.wait(3)
        
        # Final message
        final_text = Text("AI + Radar = Next-Gen Defense & Autonomous Systems", 
                         font_size=28, color=VIBRANT_ORANGE, weight=BOLD)
        self.add_fixed_in_frame_mobjects(final_text)
        final_text.to_edge(DOWN, buff=1.0)
        
        self.play(Write(final_text), run_time=3)
        self.wait(3)
        
        # Sparkle finale
        sparkles = VGroup(*[
            Star(n=5, outer_radius=0.15, 
                color=np.random.choice([TECH_CYAN, NEON_PINK, VIBRANT_ORANGE]),
                fill_opacity=0.8, stroke_width=2)
            .move_to([np.random.uniform(-6, 6), np.random.uniform(-3, 3), np.random.uniform(-1, 1)])
            for _ in range(30)
        ])
        
        self.add_fixed_in_frame_mobjects(sparkles)
        
        self.play(
            LaggedStart(*[FadeIn(star, scale=2) for star in sparkles], lag_ratio=0.03),
            run_time=2.5
        )
        self.wait(2)
        
        # Fade all
        self.play(
            FadeOut(main_title, brain_label, key_points, final_text, 
                   sparkles, full_system, connections),
            *[FadeOut(stage[1]) for stage in stage_objects],
            run_time=2.5
        )
        self.wait(1)