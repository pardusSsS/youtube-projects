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

# ========================== PART 1: THE HOOK (3-6s) ==========================
class Part1(Scene):
    """Instant Hook - NAVAL RADAR: How Warships Hunt Fighter Jets"""
    def construct(self):
        # Dramatic title
        title = Text("NAVAL RADAR", font_size=96, color=TECH_CYAN, weight=BOLD)
        subtitle = Text("How Warships Hunt Fighter Jets", font_size=42, color=NEON_PINK)
        subtitle.next_to(title, DOWN, buff=0.3)
        
        # Radar pulse ring effect
        pulse_rings = VGroup(*[
            Circle(radius=0.5 + i*0.8, stroke_width=4-i*0.5, color=TECH_CYAN, stroke_opacity=1-i*0.2)
            for i in range(5)
        ]).move_to(ORIGIN)
        
        # Warship silhouette
        ship = self.create_ship_silhouette().scale(0.6).to_edge(DOWN, buff=0.8)
        
        # Fighter jet
        jet = self.create_jet_silhouette().scale(0.3).to_corner(UR, buff=1)
        
        # Animations - FAST!
        self.play(
            FadeIn(title, scale=1.5),
            run_time=0.5
        )
        self.play(
            FadeIn(subtitle, shift=UP*0.5),
            FadeIn(ship, shift=UP),
            FadeIn(jet, shift=LEFT),
            run_time=0.8
        )
        
        # Radar pulse animation
        for ring in pulse_rings:
            self.add(ring)
            self.play(
                ring.animate.scale(3).set_opacity(0),
                run_time=0.3
            )
            self.remove(ring)
        
        # Final flash
        flash = Rectangle(width=20, height=12, fill_color=TECH_CYAN, fill_opacity=0.3, stroke_width=0)
        self.play(FadeIn(flash), run_time=0.2)
        self.play(FadeOut(flash), run_time=0.2)
        
        self.wait(0.5)
    
    def create_ship_silhouette(self):
        hull = Polygon(
            [-3, 0, 0], [-2.5, -0.5, 0], [2.5, -0.5, 0], [3, 0, 0], [2.8, 0.2, 0], [-2.8, 0.2, 0],
            fill_color=SUBTLE_NAVY, fill_opacity=1, stroke_color=TECH_CYAN, stroke_width=3
        )
        tower = Rectangle(width=1.2, height=1.5, fill_color=SUBTLE_NAVY, fill_opacity=1,
                         stroke_color=TECH_CYAN, stroke_width=2).move_to([0, 0.95, 0])
        radar = Line([-0.3, 1.7, 0], [0.3, 1.7, 0], stroke_width=4, color=NEON_PINK)
        return VGroup(hull, tower, radar)
    
    def create_jet_silhouette(self):
        body = Polygon(
            [0, 0, 0], [2, 0.2, 0], [2.5, 0, 0], [2, -0.2, 0], [0, 0, 0],
            fill_color=SUBTLE_NAVY, fill_opacity=1, stroke_color=NEON_PINK, stroke_width=2
        )
        wing = Polygon(
            [0.8, 0, 0], [1.2, 0.8, 0], [1.8, 0.8, 0], [1.5, 0, 0],
            fill_color=SUBTLE_NAVY, fill_opacity=1, stroke_color=NEON_PINK, stroke_width=2
        )
        wing2 = wing.copy().flip(UP)
        tail = Polygon(
            [0.2, 0, 0], [0, 0.4, 0], [0.4, 0.3, 0],
            fill_color=SUBTLE_NAVY, fill_opacity=1, stroke_color=NEON_PINK, stroke_width=2
        )
        return VGroup(body, wing, wing2, tail)


# ========================== PART 2: WARSHIP PLATFORM (15-18s) ==========================
class Part2(ThreeDScene):
    """The Warship Platform - 3D warship with radar components"""
    def construct(self):
        self.set_camera_orientation(phi=70*DEGREES, theta=-45*DEGREES)
        
        # Title
        title = Text("THE WARSHIP PLATFORM", font_size=48, color=TECH_CYAN)
        title.to_edge(UP)
        
        question = Text("How does this floating fortress detect threats?", 
                       font_size=28, color=TEXT_WHITE)
        question.next_to(title, DOWN, buff=0.3)
        
        # Build 3D warship
        hull = self.create_hull()
        superstructure = self.create_superstructure()
        radar_mast = self.create_radar_mast()
        
        ship = VGroup(hull, superstructure, radar_mast)
        
        # Labels
        label1 = Text("Phased Array\nRadar Panels", font_size=20, color=VIBRANT_ORANGE)
        label1.move_to([3, 2, 0])
        arrow1 = Arrow(label1.get_left(), [1, 1.5, 0], color=VIBRANT_ORANGE, stroke_width=2)
        
        label2 = Text("Combat\nInformation\nCenter", font_size=18, color=TECH_CYAN)
        label2.move_to([-3, 1, 0])
        
        # Add fixed in frame
        self.add_fixed_in_frame_mobjects(title, question, label1, arrow1, label2)
        
        # Animations
        self.play(Write(title), run_time=1)
        self.play(FadeIn(question), run_time=0.8)
        self.wait(1)
        
        self.play(FadeIn(hull), run_time=1.5)
        self.play(FadeIn(superstructure), run_time=1.5)
        self.play(FadeIn(radar_mast), run_time=1.5)
        
        # Rotate view
        self.move_camera(theta=-90*DEGREES, run_time=3)
        
        self.play(FadeIn(label1), Create(arrow1), run_time=1)
        self.play(FadeIn(label2), run_time=1)
        
        # Continue rotation
        self.move_camera(theta=-180*DEGREES, run_time=4)
        
        self.wait(2)
    
    def create_hull(self):
        hull = Prism(dimensions=[6, 1, 1.5]).set_color(SUBTLE_NAVY)
        hull.set_stroke(TECH_CYAN, width=1)
        return hull
    
    def create_superstructure(self):
        tower = Prism(dimensions=[2, 1.5, 1]).move_to([0, 1, 0])
        tower.set_color(SUBTLE_NAVY).set_stroke(TECH_CYAN, width=1)
        return tower
    
    def create_radar_mast(self):
        mast = Prism(dimensions=[0.3, 1.5, 0.3]).move_to([0, 2.5, 0])
        mast.set_color(SUBTLE_NAVY).set_stroke(TECH_CYAN, width=1)
        
        # Radar panels (represented as rectangles)
        panel1 = Rectangle(width=0.8, height=0.6, fill_color=NEON_PINK, 
                          fill_opacity=0.8, stroke_color=NEON_PINK, stroke_width=2)
        panel1.rotate(PI/2, axis=UP).move_to([0.2, 2.8, 0])
        
        panel2 = panel1.copy().rotate(PI/2, axis=UP).move_to([0, 2.8, 0.2])
        
        return VGroup(mast, panel1, panel2)


# ========================== PART 3: PHASED ARRAY RADAR (15-18s) ==========================
class Part3(Scene):
    """Radar Antenna Architecture - Phased Array Grid"""
    def construct(self):
        title = Text("PHASED ARRAY RADAR", font_size=48, color=TECH_CYAN)
        title.to_edge(UP)
        
        subtitle = Text("Electronic Beam Steering - No Moving Parts", font_size=28, color=NEON_PINK)
        subtitle.next_to(title, DOWN, buff=0.2)
        
        # Create antenna grid
        grid_size = 8
        element_size = 0.35
        antenna_grid = VGroup()
        
        for i in range(grid_size):
            for j in range(grid_size):
                element = Square(side_length=element_size, 
                               fill_color=SUBTLE_NAVY, fill_opacity=1,
                               stroke_color=TECH_CYAN, stroke_width=2)
                element.move_to([
                    (i - grid_size/2 + 0.5) * (element_size + 0.1),
                    (j - grid_size/2 + 0.5) * (element_size + 0.1) - 0.5,
                    0
                ])
                antenna_grid.add(element)
        
        # Explanation
        explanation = VGroup(
            Text("Each element transmits with", font_size=24, color=TEXT_WHITE),
            Text("controlled phase delay", font_size=24, color=VIBRANT_ORANGE),
        ).arrange(RIGHT, buff=0.2)
        explanation.to_edge(DOWN, buff=1)
        
        # Animations
        self.play(Write(title), run_time=1)
        self.play(FadeIn(subtitle), run_time=0.8)
        self.wait(1)
        
        # Build grid element by element
        self.play(
            LaggedStart(*[FadeIn(elem, scale=0.5) for elem in antenna_grid],
                       lag_ratio=0.02),
            run_time=3
        )
        
        self.wait(1)
        
        # Animate beam steering - elements light up in wave pattern
        for angle in [0, 30, -30, 15]:
            self.animate_beam_steering(antenna_grid, grid_size, angle)
        
        self.play(Write(explanation), run_time=1.5)
        self.wait(3)
    
    def animate_beam_steering(self, grid, size, angle_deg):
        angle_rad = angle_deg * DEGREES
        
        # Calculate phase delays based on angle and ensure non-negative
        for idx, elem in enumerate(grid):
            i = idx // size
            j = idx % size
            # Normalize delay to be between 0 and 1
            delay = abs((i * np.sin(angle_rad) + j * np.cos(angle_rad)) / size)
            elem.delay = delay
        
        # Sort by delay and animate in sequence
        sorted_elems = sorted(grid, key=lambda e: e.delay)
        
        # Animate elements lighting up
        self.play(
            LaggedStart(*[
                elem.animate.set_fill(TECH_CYAN, opacity=0.8).set_stroke(NEON_PINK)
                for elem in sorted_elems
            ], lag_ratio=0.05),
            run_time=1
        )
        
        # Reset elements
        self.play(
            LaggedStart(*[
                elem.animate.set_fill(SUBTLE_NAVY, opacity=1).set_stroke(TECH_CYAN)
                for elem in sorted_elems
            ], lag_ratio=0.02),
            run_time=0.5
        )


# ========================== PART 4: SIGNAL GENERATOR (13-16s) ==========================
class Part4(Scene):
    """The Signal Generator - Pulse formation and PRF"""
    def construct(self):
        title = Text("THE SIGNAL GENERATOR", font_size=48, color=TECH_CYAN)
        title.to_edge(UP)
        
        # Transmitter block diagram
        tx_box = Rectangle(width=3, height=1.5, fill_color=SUBTLE_NAVY, 
                          fill_opacity=1, stroke_color=TECH_CYAN, stroke_width=3)
        tx_label = Text("TRANSMITTER", font_size=24, color=TEXT_WHITE)
        tx_group = VGroup(tx_box, tx_label).move_to(LEFT*4)
        
        # Antenna
        antenna = VGroup(
            Line(ORIGIN, UP*1.5, stroke_width=4, color=NEON_PINK),
            Line(LEFT*0.5+UP*1.5, RIGHT*0.5+UP*1.5, stroke_width=4, color=NEON_PINK),
            *[Line(UP*1.5, UP*1.5 + rotate_vector(UP*0.3, a), stroke_width=2, color=NEON_PINK)
              for a in [PI/6, -PI/6, PI/4, -PI/4]]
        ).move_to(RIGHT*2)
        
        # Connection line
        connection = Arrow(tx_box.get_right(), antenna.get_left(), 
                          stroke_width=3, color=VIBRANT_ORANGE)
        
        # Pulse timing diagram
        axes = Axes(
            x_range=[0, 10, 1], y_range=[0, 1.5, 0.5],
            x_length=8, y_length=2,
            axis_config={"color": SUBTLE_NAVY}
        ).to_edge(DOWN, buff=1)
        
        # Create pulse waveform
        pulse_points = []
        for t in np.linspace(0, 10, 500):
            if int(t) % 3 < 0.5:  # Pulse every 3 units, duration 0.5
                pulse_points.append([t, 1, 0])
            else:
                pulse_points.append([t, 0.1, 0])
        
        pulse_line = axes.plot_line_graph(
            x_values=[p[0] for p in pulse_points],
            y_values=[p[1] for p in pulse_points],
            line_color=TECH_CYAN, stroke_width=3,
            add_vertex_dots=False
        )
        
        prf_label = Text("PRF = Pulse Repetition Frequency", font_size=24, color=VIBRANT_ORANGE)
        prf_label.next_to(axes, UP, buff=0.3)
        
        # Animations
        self.play(Write(title), run_time=1)
        self.wait(0.5)
        
        self.play(FadeIn(tx_group), run_time=1)
        self.play(GrowArrow(connection), run_time=0.8)
        self.play(FadeIn(antenna), run_time=1)
        
        self.wait(1)
        
        self.play(
            Create(axes),
            run_time=1.5
        )
        
        self.play(
            Create(pulse_line),
            run_time=3
        )
        
        self.play(Write(prf_label), run_time=1)
        
        # Animate pulses being transmitted
        for _ in range(3):
            pulse = Circle(radius=0.1, fill_color=NEON_PINK, fill_opacity=1, stroke_width=0)
            pulse.move_to(antenna.get_top())
            self.add(pulse)
            self.play(
                pulse.animate.scale(5).set_opacity(0).shift(RIGHT*2),
                run_time=0.6
            )
            self.remove(pulse)
        
        self.wait(2)


# ========================== PART 5: FIGHTER JET PROFILE (18-22s) ==========================
class Part5(Scene):
    """The Target - Fighter Jet and RCS Concept - IMPROVED VERSION"""
    def construct(self):
        # Background
        self.camera.background_color = DEEP_NAVY
        
        # Title and intro question
        title = Text("RADAR CROSS SECTION (RCS)", font_size=44, color=TECH_CYAN)
        title.to_edge(UP, buff=0.4)
        
        question = Text("How 'visible' is the target to radar?", font_size=28, color=TEXT_WHITE)
        question.next_to(title, DOWN, buff=0.3)
        
        self.play(Write(title), run_time=1)
        self.play(FadeIn(question), run_time=0.8)
        self.wait(1)
        
        # RCS Definition Box
        definition_box = RoundedRectangle(
            width=10, height=1.8, corner_radius=0.2,
            fill_color=SUBTLE_NAVY, fill_opacity=0.8,
            stroke_color=TECH_CYAN, stroke_width=2
        ).move_to(ORIGIN)
        
        definition_text = VGroup(
            Text("RCS = Effective reflecting area of target", font_size=24, color=TEXT_WHITE),
            Text("Measured in square meters (m²)", font_size=20, color=VIBRANT_ORANGE),
        ).arrange(DOWN, buff=0.2)
        definition_text.move_to(definition_box)
        
        self.play(FadeIn(definition_box), Write(definition_text), run_time=1.5)
        self.wait(1.5)
        
        # Move definition up
        self.play(
            VGroup(definition_box, definition_text).animate.scale(0.7).to_edge(UP, buff=0.5),
            FadeOut(title), FadeOut(question),
            run_time=1
        )
        
        # Create comparison: Different objects with different RCS
        comparison_title = Text("RCS Comparison", font_size=32, color=VIBRANT_ORANGE)
        comparison_title.move_to(UP*1.5)
        
        # Objects: Bird, Stealth Jet, Commercial Plane, Ship
        objects_data = [
            ("Bird", "0.01 m²", 0.3, TECH_CYAN),
            ("Stealth Jet", "0.1 m²", 0.5, NEON_PINK),
            ("Fighter Jet", "5 m²", 1.0, VIBRANT_ORANGE),
            ("Commercial\nPlane", "100 m²", 1.8, TEXT_WHITE),
        ]
        
        objects_group = VGroup()
        for i, (name, rcs, size, color) in enumerate(objects_data):
            # Create circle representing RCS size
            circle = Circle(radius=size * 0.5, color=color, stroke_width=3, fill_opacity=0.3, fill_color=color)
            label = Text(name, font_size=16, color=color)
            rcs_text = Text(rcs, font_size=14, color=TEXT_WHITE)
            
            obj_group = VGroup(circle, label, rcs_text)
            label.next_to(circle, DOWN, buff=0.1)
            rcs_text.next_to(label, DOWN, buff=0.05)
            
            objects_group.add(obj_group)
        
        objects_group.arrange(RIGHT, buff=0.8)
        objects_group.move_to(DOWN*0.3)
        
        self.play(FadeIn(comparison_title), run_time=0.8)
        
        # Animate each object appearing
        for obj in objects_group:
            self.play(FadeIn(obj), run_time=0.6)
        
        self.wait(2)
        
        # Clear and show jet angle visualization
        self.play(
            FadeOut(objects_group), FadeOut(comparison_title),
            FadeOut(definition_box), FadeOut(definition_text),
            run_time=0.8
        )
        
        # Angle-dependent RCS explanation
        angle_title = Text("RCS Changes with Viewing Angle", font_size=36, color=TECH_CYAN)
        angle_title.to_edge(UP, buff=0.5)
        
        self.play(Write(angle_title), run_time=1)
        
        # Create jet silhouette from different angles
        # Front view (small RCS)
        front_view = self.create_jet_front()
        front_view.scale(0.8).move_to(LEFT*4)
        front_label = Text("FRONT VIEW", font_size=18, color=TECH_CYAN)
        front_label.next_to(front_view, UP, buff=0.2)
        front_rcs = Text("RCS: 0.1 - 1 m²", font_size=16, color=TECH_CYAN)
        front_rcs.next_to(front_view, DOWN, buff=0.2)
        front_indicator = Text("✓ SMALL", font_size=20, color=TECH_CYAN, weight=BOLD)
        front_indicator.next_to(front_rcs, DOWN, buff=0.1)
        
        # Side view (large RCS)
        side_view = self.create_jet_side()
        side_view.scale(0.8).move_to(ORIGIN)
        side_label = Text("SIDE VIEW", font_size=18, color=NEON_PINK)
        side_label.next_to(side_view, UP, buff=0.2)
        side_rcs = Text("RCS: 10 - 50 m²", font_size=16, color=NEON_PINK)
        side_rcs.next_to(side_view, DOWN, buff=0.2)
        side_indicator = Text("✗ LARGE", font_size=20, color=NEON_PINK, weight=BOLD)
        side_indicator.next_to(side_rcs, DOWN, buff=0.1)
        
        # Bottom view (very large RCS)
        bottom_view = self.create_jet_bottom()
        bottom_view.scale(0.8).move_to(RIGHT*4)
        bottom_label = Text("BOTTOM VIEW", font_size=18, color=VIBRANT_ORANGE)
        bottom_label.next_to(bottom_view, UP, buff=0.2)
        bottom_rcs = Text("RCS: 50 - 100 m²", font_size=16, color=VIBRANT_ORANGE)
        bottom_rcs.next_to(bottom_view, DOWN, buff=0.2)
        bottom_indicator = Text("✗ VERY LARGE", font_size=20, color=VIBRANT_ORANGE, weight=BOLD)
        bottom_indicator.next_to(bottom_rcs, DOWN, buff=0.1)
        
        # Show each view
        self.play(
            FadeIn(front_view), Write(front_label), Write(front_rcs),
            run_time=1
        )
        self.play(Write(front_indicator), run_time=0.5)
        
        self.play(
            FadeIn(side_view), Write(side_label), Write(side_rcs),
            run_time=1
        )
        self.play(Write(side_indicator), run_time=0.5)
        
        self.play(
            FadeIn(bottom_view), Write(bottom_label), Write(bottom_rcs),
            run_time=1
        )
        self.play(Write(bottom_indicator), run_time=0.5)
        
        self.wait(1.5)
        
        # Final takeaway
        takeaway_box = RoundedRectangle(
            width=11, height=1.2, corner_radius=0.15,
            fill_color=DEEP_NAVY, fill_opacity=0.9,
            stroke_color=VIBRANT_ORANGE, stroke_width=2
        ).to_edge(DOWN, buff=0.3)
        
        takeaway = Text(
            "Stealth aircraft are designed to minimize frontal RCS!",
            font_size=24, color=VIBRANT_ORANGE
        )
        takeaway.move_to(takeaway_box)
        
        self.play(FadeIn(takeaway_box), Write(takeaway), run_time=1.5)
        self.wait(2)
    
    def create_jet_front(self):
        """Create front-view jet silhouette (small cross-section)"""
        # Simple front view: fuselage circle + wing tips
        fuselage = Circle(radius=0.3, fill_color=SUBTLE_NAVY, fill_opacity=1,
                         stroke_color=TECH_CYAN, stroke_width=2)
        wing_left = Line(LEFT*1.2, LEFT*0.3, color=TECH_CYAN, stroke_width=3)
        wing_right = Line(RIGHT*0.3, RIGHT*1.2, color=TECH_CYAN, stroke_width=3)
        tail = Line(UP*0.1, UP*0.5, color=TECH_CYAN, stroke_width=3)
        
        return VGroup(fuselage, wing_left, wing_right, tail)
    
    def create_jet_side(self):
        """Create side-view jet silhouette (large cross-section)"""
        # Side view profile
        body = Polygon(
            [-1.5, 0, 0], [-1.2, 0.15, 0], [0.8, 0.2, 0], [1.5, 0.05, 0],
            [1.5, -0.05, 0], [0.5, -0.15, 0], [-1.2, -0.1, 0], [-1.5, 0, 0],
            fill_color=SUBTLE_NAVY, fill_opacity=1,
            stroke_color=NEON_PINK, stroke_width=2
        )
        tail = Polygon(
            [0.8, 0.2, 0], [1.1, 0.7, 0], [1.3, 0.6, 0], [1.0, 0.2, 0],
            fill_color=SUBTLE_NAVY, fill_opacity=1,
            stroke_color=NEON_PINK, stroke_width=2
        )
        cockpit = Circle(radius=0.12, fill_color=TECH_CYAN, fill_opacity=0.5,
                        stroke_color=TECH_CYAN, stroke_width=1).move_to([-0.8, 0.1, 0])
        
        return VGroup(body, tail, cockpit)
    
    def create_jet_bottom(self):
        """Create bottom-view jet silhouette (very large cross-section)"""
        # Bottom view showing full wing area
        body = Polygon(
            [-1.8, 0, 0], [1.8, 0, 0], [1.5, 0.2, 0], [-1.5, 0.2, 0],
            fill_color=SUBTLE_NAVY, fill_opacity=1,
            stroke_color=VIBRANT_ORANGE, stroke_width=2
        )
        wing_left = Polygon(
            [-0.3, 0, 0], [-1.5, -1.0, 0], [-0.8, -0.9, 0], [-0.2, -0.2, 0],
            fill_color=SUBTLE_NAVY, fill_opacity=1,
            stroke_color=VIBRANT_ORANGE, stroke_width=2
        )
        wing_right = Polygon(
            [0.3, 0, 0], [1.5, -1.0, 0], [0.8, -0.9, 0], [0.2, -0.2, 0],
            fill_color=SUBTLE_NAVY, fill_opacity=1,
            stroke_color=VIBRANT_ORANGE, stroke_width=2
        )
        tail_left = Polygon(
            [-1.3, 0.1, 0], [-1.6, 0.5, 0], [-1.4, 0.5, 0], [-1.2, 0.15, 0],
            fill_color=SUBTLE_NAVY, fill_opacity=1,
            stroke_color=VIBRANT_ORANGE, stroke_width=2
        )
        tail_right = Polygon(
            [1.3, 0.1, 0], [1.6, 0.5, 0], [1.4, 0.5, 0], [1.2, 0.15, 0],
            fill_color=SUBTLE_NAVY, fill_opacity=1,
            stroke_color=VIBRANT_ORANGE, stroke_width=2
        )
        
        return VGroup(body, wing_left, wing_right, tail_left, tail_right)


# ========================== PART 6: EM WAVE PROPAGATION (18-22s) ==========================
class Part6(ThreeDScene):
    """Electromagnetic Wave Propagation in 3D"""
    def construct(self):
        self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES)
        
        title = Text("ELECTROMAGNETIC WAVE PROPAGATION", font_size=40, color=TECH_CYAN)
        title.to_edge(UP)
        
        # Wave equation
        formula = MathTex(r"c = \lambda \times f", font_size=48, color=VIBRANT_ORANGE)
        formula.to_corner(DR, buff=0.5)
        
        formula_labels = VGroup(
            Text("c = speed of light", font_size=20, color=TEXT_WHITE),
            Text("λ = wavelength", font_size=20, color=TEXT_WHITE),
            Text("f = frequency", font_size=20, color=TEXT_WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        formula_labels.next_to(formula, LEFT, buff=0.5)
        
        # Add fixed in frame
        self.add_fixed_in_frame_mobjects(title, formula, formula_labels)
        
        # 3D Axes
        axes = ThreeDAxes(
            x_range=[-4, 4, 1], y_range=[-2, 2, 1], z_range=[-2, 2, 1],
            x_length=8, y_length=4, z_length=4
        )
        
        # Create EM wave (E and B fields)
        t_tracker = ValueTracker(0)
        
        def e_field_wave(u):
            return axes.c2p(u, np.sin(u - t_tracker.get_value()), 0)
        
        def b_field_wave(u):
            return axes.c2p(u, 0, np.sin(u - t_tracker.get_value()))
        
        e_wave = always_redraw(lambda: ParametricFunction(
            e_field_wave, t_range=[-4, 4, 0.1],
            color=TECH_CYAN, stroke_width=4
        ))
        
        b_wave = always_redraw(lambda: ParametricFunction(
            b_field_wave, t_range=[-4, 4, 0.1],
            color=NEON_PINK, stroke_width=4
        ))
        
        # Labels for E and B
        e_label = Text("E-Field", font_size=24, color=TECH_CYAN)
        e_label.move_to([0, 2.5, 0])
        b_label = Text("B-Field", font_size=24, color=NEON_PINK)
        b_label.move_to([2, 0, 0])
        
        self.add_fixed_in_frame_mobjects(e_label, b_label)
        
        # Animations
        self.play(Write(title), run_time=1)
        self.wait(0.5)
        
        self.play(Create(axes), run_time=1.5)
        
        self.add(e_wave, b_wave)
        self.play(FadeIn(e_label), FadeIn(b_label), run_time=1)
        
        # Animate wave propagation
        self.play(
            t_tracker.animate.set_value(4*PI),
            run_time=6,
            rate_func=linear
        )
        
        self.play(Write(formula), run_time=1)
        self.play(FadeIn(formula_labels), run_time=1)
        
        # Rotate camera
        self.move_camera(
            theta=45*DEGREES,
            run_time=4
        )
        self.play(
            t_tracker.animate.set_value(8*PI),
            run_time=4,
            rate_func=linear
        )
        
        self.wait(2)


# ========================== PART 7: RADAR PULSE JOURNEY (18-22s) ==========================
class Part7(Scene):
    """The Radar Pulse Journey - From Ship to Target"""
    def construct(self):
        title = Text("THE RADAR PULSE JOURNEY", font_size=48, color=TECH_CYAN)
        title.to_edge(UP)
        
        # Ship on left
        ship = self.create_ship().scale(0.5).to_edge(LEFT, buff=1).shift(DOWN*1.5)
        
        # Jet on right
        jet = self.create_jet().scale(0.3).to_edge(RIGHT, buff=1).shift(UP*1)
        
        # Distance indicator
        distance_line = DashedLine(
            ship.get_right() + RIGHT*0.5,
            jet.get_left() + LEFT*0.5,
            stroke_width=2, color=SUBTLE_NAVY, dash_length=0.2
        )
        distance_label = Text("Distance: R", font_size=24, color=VIBRANT_ORANGE)
        distance_label.next_to(distance_line, DOWN)
        
        # Time tracker
        time_display = VGroup(
            Text("Time: ", font_size=28, color=TEXT_WHITE),
            DecimalNumber(0, num_decimal_places=2, font_size=28, color=TECH_CYAN),
            Text(" μs", font_size=28, color=TEXT_WHITE)
        ).arrange(RIGHT, buff=0.1).to_corner(UR, buff=0.5)
        
        time_tracker = time_display[1]
        
        # Animations
        self.play(Write(title), run_time=1)
        self.play(FadeIn(ship), FadeIn(jet), run_time=1)
        self.play(Create(distance_line), Write(distance_label), run_time=1)
        self.play(FadeIn(time_display), run_time=0.5)
        
        self.wait(1)
        
        # Create and animate radar pulses
        for _ in range(3):
            pulse = VGroup()
            for i in range(5):
                arc = Arc(radius=0.3+i*0.15, angle=PI/3, arc_center=ship.get_right(),
                         stroke_width=4-i*0.6, color=TECH_CYAN, stroke_opacity=1-i*0.15)
                arc.rotate(-PI/6, about_point=ship.get_right())
                pulse.add(arc)
            
            # Pulse travels to target
            self.add(pulse)
            self.play(
                pulse.animate.shift(RIGHT*8).scale(3).set_opacity(0.3),
                time_tracker.animate.set_value(33.3),  # ~10km at speed of light
                run_time=2.5,
                rate_func=linear
            )
            self.remove(pulse)
            
            # Flash on jet
            flash = Circle(radius=0.3, fill_color=NEON_PINK, fill_opacity=0.8, stroke_width=0)
            flash.move_to(jet.get_center())
            self.play(FadeIn(flash, scale=0.5), run_time=0.2)
            self.play(FadeOut(flash, scale=2), run_time=0.3)
            
            time_tracker.set_value(0)
        
        # Timeline explanation
        timeline = self.create_timeline().to_edge(DOWN, buff=0.5)
        self.play(FadeIn(timeline), run_time=1.5)
        
        self.wait(3)
    
    def create_ship(self):
        hull = Polygon(
            [-2, 0, 0], [-1.5, -0.3, 0], [1.5, -0.3, 0], [2, 0, 0],
            fill_color=SUBTLE_NAVY, fill_opacity=1, stroke_color=TECH_CYAN, stroke_width=3
        )
        tower = Rectangle(width=0.8, height=1, fill_color=SUBTLE_NAVY, 
                         fill_opacity=1, stroke_color=TECH_CYAN, stroke_width=2)
        tower.move_to([0, 0.5, 0])
        return VGroup(hull, tower)
    
    def create_jet(self):
        body = Polygon(
            [0, 0, 0], [1.5, 0.15, 0], [2, 0, 0], [1.5, -0.15, 0],
            fill_color=SUBTLE_NAVY, fill_opacity=1, stroke_color=NEON_PINK, stroke_width=2
        )
        wing = Polygon([0.6, 0, 0], [1, 0.5, 0], [1.3, 0.4, 0], [1, 0, 0],
                      fill_color=SUBTLE_NAVY, fill_opacity=1, stroke_color=NEON_PINK, stroke_width=2)
        return VGroup(body, wing, wing.copy().flip(UP))
    
    def create_timeline(self):
        line = Line(LEFT*5, RIGHT*5, stroke_width=3, color=SUBTLE_NAVY)
        markers = VGroup()
        labels = ["Pulse\nTransmit", "Travel\nTime", "Target\nHit", "Echo\nReturn", "Signal\nReceived"]
        for i, label in enumerate(labels):
            dot = Dot(point=LEFT*5 + RIGHT*i*2.5, color=TECH_CYAN, radius=0.1)
            text = Text(label, font_size=16, color=TEXT_WHITE).next_to(dot, DOWN, buff=0.2)
            markers.add(VGroup(dot, text))
        return VGroup(line, markers)


# ========================== PART 8: TARGET REFLECTION (20-25s) ==========================
class Part8(Scene):
    """Target Reflection - The Echo - IMPROVED VERSION"""
    def construct(self):
        self.camera.background_color = DEEP_NAVY
        
        # Title and intro question
        title = Text("THE ECHO: TARGET REFLECTION", font_size=44, color=NEON_PINK)
        title.to_edge(UP, buff=0.4)
        
        question = Text("What happens when radar hits the target?", font_size=28, color=TEXT_WHITE)
        question.next_to(title, DOWN, buff=0.3)
        
        self.play(Write(title), run_time=1)
        self.play(FadeIn(question), run_time=0.8)
        self.wait(1)
        
        self.play(FadeOut(question), run_time=0.5)
        
        # Scene setup: Ship on left, Jet on right
        ship = self.create_ship().scale(0.5).move_to(LEFT*5 + DOWN*0.5)
        ship_label = Text("RADAR", font_size=16, color=TECH_CYAN).next_to(ship, DOWN, buff=0.15)
        
        jet = self.create_jet().scale(0.6).move_to(RIGHT*4 + DOWN*0.5)
        jet_label = Text("TARGET", font_size=16, color=NEON_PINK).next_to(jet, DOWN, buff=0.15)
        
        # Distance indicator
        distance_line = DashedLine(ship.get_right(), jet.get_left(), color=SUBTLE_NAVY, dash_length=0.2)
        distance_text = Text("Distance: R", font_size=20, color=TEXT_WHITE).next_to(distance_line, UP, buff=0.1)
        
        self.play(FadeIn(ship), FadeIn(ship_label), run_time=0.8)
        self.play(FadeIn(jet), FadeIn(jet_label), run_time=0.8)
        self.play(Create(distance_line), Write(distance_text), run_time=0.8)
        self.wait(0.5)
        
        # Step 1: Transmit pulse
        step1_box = self.create_step_indicator("STEP 1: Transmit Pulse", TECH_CYAN)
        step1_box.to_corner(UL, buff=1.0)
        self.play(FadeIn(step1_box), run_time=0.5)
        
        # Power indicator
        power_bar = self.create_power_bar(3.0, "Transmitted Power: 100%", TECH_CYAN)
        power_bar.to_corner(DL, buff=0.5)
        self.play(FadeIn(power_bar), run_time=0.5)
        
        # Animate pulse traveling
        pulse = self.create_pulse(TECH_CYAN)
        pulse.move_to(ship.get_right())
        
        self.add(pulse)
        self.play(
            pulse.animate.move_to(jet.get_center()).scale(0.5).set_opacity(0.6),
            run_time=1.5
        )
        self.remove(pulse)
        
        # Step 2: Target reflection
        step2_box = self.create_step_indicator("STEP 2: Target Reflects Signal", NEON_PINK)
        step2_box.next_to(step1_box, DOWN, buff=0.3)
        self.play(FadeIn(step2_box), run_time=0.5)
        
        # Flash on target
        flash = Circle(radius=0.4, fill_color=VIBRANT_ORANGE, fill_opacity=0.9, stroke_width=0)
        flash.move_to(jet.get_center())
        self.play(GrowFromCenter(flash), run_time=0.3)
        
        # Scatter waves in all directions
        scatter_waves = VGroup()
        for angle in range(0, 360, 45):
            wave = Arc(radius=0.2, angle=PI/4, arc_center=jet.get_center(),
                      stroke_width=3, color=NEON_PINK)
            wave.rotate(angle*DEGREES, about_point=jet.get_center())
            scatter_waves.add(wave)
        
        self.play(
            FadeOut(flash),
            *[wave.animate.scale(3).set_opacity(0.3) for wave in scatter_waves],
            run_time=1.5
        )
        self.remove(scatter_waves)
        
        # Show that most energy is lost
        loss_text = Text("Most energy scatters away!", font_size=22, color=NEON_PINK)
        loss_text.move_to(jet.get_center() + UP*1.2)
        self.play(FadeIn(loss_text), run_time=0.5)
        self.wait(0.5)
        self.play(FadeOut(loss_text), run_time=0.3)
        
        # Step 3: Echo returns
        step3_box = self.create_step_indicator("STEP 3: Echo Returns to Radar", VIBRANT_ORANGE)
        step3_box.next_to(step2_box, DOWN, buff=0.3)
        self.play(FadeIn(step3_box), run_time=0.5)
        
        # Echo pulse (much weaker)
        echo = self.create_pulse(NEON_PINK, weak=True)
        echo.move_to(jet.get_center())
        
        self.add(echo)
        self.play(
            echo.animate.move_to(ship.get_right()).scale(0.5).set_opacity(0.3),
            run_time=1.5
        )
        self.remove(echo)
        
        # Update power bar to show received power
        power_bar_weak = self.create_power_bar(0.3, "Received Power: ~0.0001%", NEON_PINK)
        power_bar_weak.next_to(power_bar, RIGHT, buff=0.8)
        
        self.play(FadeIn(power_bar_weak), run_time=0.8)
        
        # Comparison arrow
        comparison_arrow = Arrow(power_bar.get_right() + RIGHT*0.1, power_bar_weak.get_left() + LEFT*0.1, 
                                 color=VIBRANT_ORANGE, stroke_width=3, buff=0.1)
        comparison_text = Text("HUGE LOSS!", font_size=16, color=VIBRANT_ORANGE)
        comparison_text.next_to(comparison_arrow, UP, buff=0.05)
        
        self.play(Create(comparison_arrow), Write(comparison_text), run_time=0.8)
        self.wait(1)
        
        # Clear ALL previous elements before showing formula
        self.play(
            FadeOut(step1_box), FadeOut(step2_box), FadeOut(step3_box),
            FadeOut(distance_line), FadeOut(distance_text),
            FadeOut(power_bar), FadeOut(power_bar_weak),
            FadeOut(comparison_arrow), FadeOut(comparison_text),
            FadeOut(ship), FadeOut(ship_label),
            FadeOut(jet), FadeOut(jet_label),
            run_time=0.8
        )
        
        # R^4 Law explanation
        r4_title = Text("The R⁴ Problem", font_size=40, color=VIBRANT_ORANGE)
        r4_title.to_edge(UP, buff=0.5)
        
        self.play(
            Transform(title, r4_title),
            run_time=0.8
        )
        
        # Formula - centered
        formula = MathTex(
            r"P_{received} \propto \frac{1}{R^4}",
            font_size=56, color=VIBRANT_ORANGE
        ).move_to(UP*1)
        
        self.play(Write(formula), run_time=1.5)
        
        # Explanation - properly positioned below formula
        explanation = VGroup(
            Text("• Signal travels TO target: loses 1/R²", font_size=24, color=TECH_CYAN),
            Text("• Signal returns FROM target: loses 1/R² again", font_size=24, color=NEON_PINK),
            Text("• Total loss: 1/R² × 1/R² = 1/R⁴", font_size=24, color=VIBRANT_ORANGE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        explanation.next_to(formula, DOWN, buff=0.6)
        
        for line in explanation:
            self.play(Write(line), run_time=0.7)
        
        self.wait(0.5)
        
        # Example - at bottom with proper spacing
        example_box = RoundedRectangle(
            width=11, height=1.2, corner_radius=0.15,
            fill_color=SUBTLE_NAVY, fill_opacity=0.9,
            stroke_color=TECH_CYAN, stroke_width=2
        ).to_edge(DOWN, buff=0.4)
        
        example_text = VGroup(
            Text("Example: Double the distance → Signal becomes ", font_size=22, color=TEXT_WHITE),
            Text("16× weaker!", font_size=24, color=NEON_PINK, weight=BOLD)
        ).arrange(RIGHT, buff=0.15)
        example_text.move_to(example_box)
        
        self.play(FadeIn(example_box), Write(example_text), run_time=1.2)
        self.wait(2)
    
    def create_ship(self):
        hull = Polygon(
            [-1.5, 0, 0], [-1, -0.25, 0], [1, -0.25, 0], [1.5, 0, 0],
            fill_color=SUBTLE_NAVY, fill_opacity=1, stroke_color=TECH_CYAN, stroke_width=2
        )
        tower = Rectangle(width=0.6, height=0.8, fill_color=SUBTLE_NAVY, 
                         fill_opacity=1, stroke_color=TECH_CYAN, stroke_width=2)
        tower.move_to([0, 0.4, 0])
        antenna = Line([0, 0.8, 0], [0, 1.2, 0], color=TECH_CYAN, stroke_width=3)
        return VGroup(hull, tower, antenna)
    
    def create_jet(self):
        body = Polygon(
            [-1, 0, 0], [0, 0.15, 0], [1.2, 0.08, 0], [1.5, 0, 0],
            [1.2, -0.08, 0], [0, -0.15, 0], [-1, 0, 0],
            fill_color=SUBTLE_NAVY, fill_opacity=1, stroke_color=NEON_PINK, stroke_width=2
        )
        wing = Polygon(
            [-0.2, 0, 0], [0.2, 0.6, 0], [0.6, 0.5, 0], [0.3, 0, 0],
            fill_color=SUBTLE_NAVY, fill_opacity=1, stroke_color=NEON_PINK, stroke_width=2
        )
        return VGroup(body, wing, wing.copy().flip(UP))
    
    def create_step_indicator(self, text, color):
        box = RoundedRectangle(
            width=5.5, height=0.6, corner_radius=0.1,
            fill_color=DEEP_NAVY, fill_opacity=0.9,
            stroke_color=color, stroke_width=2
        )
        label = Text(text, font_size=18, color=color)
        label.move_to(box)
        return VGroup(box, label)
    
    def create_power_bar(self, width, label_text, color):
        bar = Rectangle(width=width, height=0.4, fill_color=color, fill_opacity=0.8,
                       stroke_color=color, stroke_width=2)
        label = Text(label_text, font_size=14, color=TEXT_WHITE)
        label.next_to(bar, UP, buff=0.1)
        return VGroup(bar, label)
    
    def create_pulse(self, color, weak=False):
        waves = VGroup()
        opacity = 0.4 if weak else 0.8
        stroke = 2 if weak else 4
        for i in range(3):
            arc = Arc(radius=0.2+i*0.1, angle=PI/3, 
                     stroke_width=stroke-i*0.5, color=color, stroke_opacity=opacity-i*0.1)
            arc.rotate(-PI/6)
            waves.add(arc)
        return waves


# ========================== PART 9: DOPPLER EFFECT (20-25s) ==========================
class Part9(Scene):
    """The Doppler Effect - Detecting Motion"""
    def construct(self):
        title = Text("THE DOPPLER EFFECT", font_size=48, color=TECH_CYAN)
        title.to_edge(UP)
        
        subtitle = Text("Motion = Frequency Shift", font_size=32, color=VIBRANT_ORANGE)
        subtitle.next_to(title, DOWN, buff=0.2)
        
        # Doppler equation
        doppler_eq = MathTex(
            r"f_d = \frac{2 v_r f_0}{c}",
            font_size=48, color=VIBRANT_ORANGE
        )
        doppler_eq.to_edge(DOWN, buff=1)
        
        eq_labels = VGroup(
            MathTex(r"f_d = \text{Doppler shift}", font_size=24, color=TEXT_WHITE),
            MathTex(r"v_r = \text{radial velocity}", font_size=24, color=TEXT_WHITE),
            MathTex(r"f_0 = \text{transmitted frequency}", font_size=24, color=TEXT_WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        eq_labels.next_to(doppler_eq, LEFT, buff=1)
        
        # Scene setup - ship and jet
        ship = self.create_ship().scale(0.4).move_to(LEFT*5 + DOWN*1)
        jet = self.create_jet().scale(0.25).move_to(RIGHT*3 + DOWN*1)
        
        # Wave visualization boxes
        tx_box = Rectangle(width=3, height=2, stroke_color=SUBTLE_NAVY, stroke_width=2)
        tx_box.move_to(LEFT*3)
        tx_label = Text("Transmitted", font_size=20, color=TECH_CYAN).next_to(tx_box, UP)
        
        rx_box = Rectangle(width=3, height=2, stroke_color=SUBTLE_NAVY, stroke_width=2)
        rx_box.move_to(RIGHT*3)
        rx_label = Text("Received", font_size=20, color=NEON_PINK).next_to(rx_box, UP)
        
        # Create waves
        tx_wave = self.create_wave(wavelength=0.5, color=TECH_CYAN, box_width=2.8)
        tx_wave.move_to(tx_box.get_center())
        
        rx_wave = self.create_wave(wavelength=0.35, color=NEON_PINK, box_width=2.8)  # Compressed
        rx_wave.move_to(rx_box.get_center())
        
        freq_comparison = Text("Higher frequency = Target approaching!", 
                              font_size=24, color=TEXT_WHITE)
        freq_comparison.move_to(UP*1.8)
        
        # Animations
        self.play(Write(title), run_time=1)
        self.play(FadeIn(subtitle), run_time=0.8)
        
        self.play(FadeIn(ship), FadeIn(jet), run_time=1)
        
        # Animate jet moving toward ship
        velocity_arrow = Arrow(jet.get_left(), jet.get_left() + LEFT*1.5,
                              color=VIBRANT_ORANGE, stroke_width=4)
        vel_label = Text("v", font_size=24, color=VIBRANT_ORANGE).next_to(velocity_arrow, UP, buff=0.1)
        
        self.play(GrowArrow(velocity_arrow), Write(vel_label), run_time=1)
        
        self.play(
            jet.animate.shift(LEFT*1.5),
            velocity_arrow.animate.shift(LEFT*1.5),
            vel_label.animate.shift(LEFT*1.5),
            run_time=2
        )
        
        # Show wave comparison
        self.play(
            FadeIn(tx_box), Write(tx_label),
            FadeIn(rx_box), Write(rx_label),
            run_time=1
        )
        
        self.play(Create(tx_wave), run_time=1.5)
        self.play(Create(rx_wave), run_time=1.5)
        
        self.play(Write(freq_comparison), run_time=1)
        
        # Highlight compression
        brace = Brace(rx_wave, DOWN, color=VIBRANT_ORANGE)
        brace_text = Text("Compressed!", font_size=18, color=VIBRANT_ORANGE)
        brace_text.next_to(brace, DOWN, buff=0.1)
        self.play(Create(brace), Write(brace_text), run_time=1)
        
        self.wait(1)
        
        # Show equation
        self.play(Write(doppler_eq), run_time=1.5)
        self.play(FadeIn(eq_labels), run_time=1)
        
        self.wait(3)
    
    def create_ship(self):
        hull = Polygon(
            [-2, 0, 0], [-1.5, -0.3, 0], [1.5, -0.3, 0], [2, 0, 0],
            fill_color=SUBTLE_NAVY, fill_opacity=1, stroke_color=TECH_CYAN, stroke_width=3
        )
        tower = Rectangle(width=0.6, height=0.8, fill_color=SUBTLE_NAVY,
                         fill_opacity=1, stroke_color=TECH_CYAN, stroke_width=2)
        tower.move_to([0, 0.4, 0])
        return VGroup(hull, tower)
    
    def create_jet(self):
        body = Polygon(
            [0, 0, 0], [1.5, 0.1, 0], [2, 0, 0], [1.5, -0.1, 0],
            fill_color=SUBTLE_NAVY, fill_opacity=1, stroke_color=NEON_PINK, stroke_width=2
        )
        return body
    
    def create_wave(self, wavelength, color, box_width):
        points = []
        x = -box_width/2
        while x <= box_width/2:
            y = 0.4 * np.sin(2*PI*x/wavelength)
            points.append([x, y, 0])
            x += 0.05
        return VMobject(stroke_color=color, stroke_width=3).set_points_smoothly(
            [np.array(p) for p in points]
        )


# ========================== PART 10: RANGE CALCULATION (18-22s) ==========================
class Part10(Scene):
    """Range Calculation - Time of Flight - IMPROVED LAYOUT"""
    def construct(self):
        self.camera.background_color = DEEP_NAVY
        
        title = Text("RANGE CALCULATION", font_size=44, color=TECH_CYAN)
        title.to_edge(UP, buff=0.4)
        
        # Intro question
        question = Text("How do we calculate target distance?", font_size=26, color=TEXT_WHITE)
        question.next_to(title, DOWN, buff=0.3)
        
        self.play(Write(title), run_time=1)
        self.play(FadeIn(question), run_time=0.7)
        self.wait(1)
        self.play(FadeOut(question), run_time=0.4)
        
        # STEP 1: Show basic concept with diagram first (top half)
        diagram_title = Text("The Concept:", font_size=24, color=VIBRANT_ORANGE)
        diagram_title.move_to(UP*2.5 + LEFT*3)
        
        # Horizontal diagram - wider and centered
        ship_point = Dot(LEFT*5, color=TECH_CYAN, radius=0.12)
        ship_label = Text("Radar", font_size=18, color=TECH_CYAN).next_to(ship_point, DOWN, buff=0.15)
        
        target_point = Dot(RIGHT*2, color=NEON_PINK, radius=0.12)
        target_label = Text("Target", font_size=18, color=NEON_PINK).next_to(target_point, DOWN, buff=0.15)
        
        # Arrows for pulse travel
        outward_arrow = Arrow(LEFT*4.8, RIGHT*1.8, color=TECH_CYAN, stroke_width=3, buff=0.1)
        outward_label = Text("Pulse →", font_size=16, color=TECH_CYAN).next_to(outward_arrow, UP, buff=0.08)
        
        return_arrow = Arrow(RIGHT*1.8, LEFT*4.8, color=NEON_PINK, stroke_width=3, buff=0.1)
        return_arrow.shift(DOWN*0.4)
        return_label = Text("← Echo", font_size=16, color=NEON_PINK).next_to(return_arrow, DOWN, buff=0.08)
        
        # Distance brace
        distance_brace = Brace(VGroup(ship_point, target_point), UP, color=VIBRANT_ORANGE)
        distance_text = Text("R = Distance", font_size=20, color=VIBRANT_ORANGE)
        distance_text.next_to(distance_brace, UP, buff=0.1)
        
        diagram = VGroup(ship_point, ship_label, target_point, target_label,
                        outward_arrow, outward_label, return_arrow, return_label,
                        distance_brace, distance_text)
        diagram.move_to(UP*1.5)
        
        self.play(FadeIn(diagram_title), run_time=0.5)
        self.play(
            FadeIn(ship_point), Write(ship_label),
            FadeIn(target_point), Write(target_label),
            run_time=0.8
        )
        self.play(GrowArrow(outward_arrow), Write(outward_label), run_time=0.7)
        self.play(GrowArrow(return_arrow), Write(return_label), run_time=0.7)
        self.play(Create(distance_brace), Write(distance_text), run_time=0.7)
        
        self.wait(0.5)
        
        # STEP 2: Equations on left side
        eq_title = Text("The Math:", font_size=24, color=VIBRANT_ORANGE)
        eq_title.move_to(DOWN*0.3 + LEFT*4.5)
        
        eq_step1 = MathTex(r"\text{Distance} = \text{Speed} \times \text{Time}", 
                          font_size=28, color=TEXT_WHITE)
        eq_step2 = MathTex(r"2R = c \times t", font_size=32, color=TECH_CYAN)
        eq_final = MathTex(r"R = \frac{c \times t}{2}", font_size=40, color=VIBRANT_ORANGE)
        
        equations = VGroup(eq_step1, eq_step2, eq_final).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        equations.next_to(eq_title, DOWN, buff=0.25, aligned_edge=LEFT)
        
        eq_box = SurroundingRectangle(eq_final, color=VIBRANT_ORANGE, buff=0.15, stroke_width=2)
        
        self.play(FadeIn(eq_title), run_time=0.5)
        self.play(Write(eq_step1), run_time=0.8)
        self.play(Write(eq_step2), run_time=0.8)
        self.play(Write(eq_final), Create(eq_box), run_time=1)
        
        self.wait(0.5)
        
        # STEP 3: Numerical example on right side
        example_title = Text("Example:", font_size=24, color=VIBRANT_ORANGE, weight=BOLD)
        
        example_lines = VGroup(
            MathTex(r"t = 66.7 \, \mu s", font_size=26, color=TEXT_WHITE),
            MathTex(r"c = 3 \times 10^8 \text{ m/s}", font_size=26, color=TEXT_WHITE),
            MathTex(r"R = \frac{3 \times 10^8 \times 66.7 \times 10^{-6}}{2}", font_size=24, color=TECH_CYAN),
            MathTex(r"R = 10 \text{ km}", font_size=32, color=VIBRANT_ORANGE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        example_group = VGroup(example_title, example_lines).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        example_group.move_to(DOWN*0.8 + RIGHT*3)
        
        example_box = SurroundingRectangle(example_group, color=SUBTLE_NAVY, 
                                           buff=0.2, stroke_width=2, fill_opacity=0.3, fill_color=DEEP_NAVY)
        
        self.play(FadeIn(example_box), run_time=0.3)
        self.play(Write(example_title), run_time=0.5)
        for line in example_lines:
            self.play(Write(line), run_time=0.6)
        
        # Result highlight
        result_highlight = SurroundingRectangle(example_lines[-1], color=NEON_PINK, buff=0.1, stroke_width=2)
        self.play(Create(result_highlight), run_time=0.5)
        
        # Key insight at bottom
        insight_box = RoundedRectangle(
            width=12, height=0.8, corner_radius=0.1,
            fill_color=SUBTLE_NAVY, fill_opacity=0.8,
            stroke_color=TECH_CYAN, stroke_width=2
        ).to_edge(DOWN, buff=0.3)
        
        insight_text = Text("Key: Divide by 2 because signal travels TO target and BACK!", 
                           font_size=20, color=TEXT_WHITE)
        insight_text.move_to(insight_box)
        
        self.play(FadeIn(insight_box), Write(insight_text), run_time=1)
        
        self.wait(2)


# ========================== PART 11: BEAM STEERING (18-22s) ==========================
class Part11(ThreeDScene):
    """Angle Determination - Phased Array Beam Steering in 3D - IMPROVED LAYOUT"""
    def construct(self):
        # Camera Setup
        self.set_camera_orientation(phi=60*DEGREES, theta=-45*DEGREES, zoom=0.8)
        
        # 2D FIXED ELEMENTS (Overlays)
        # ---------------------------------------------------------
        # Title Section (Top Center)
        title = Text("BEAM STEERING", font_size=40, color=TECH_CYAN)
        subtitle = Text("Scanning for Targets in 3D Space", font_size=24, color=VIBRANT_ORANGE)
        header = VGroup(title, subtitle).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.3)
        
        # Phase Control Panel (Bottom Left)
        panel_box = RoundedRectangle(width=4, height=2.5, corner_radius=0.1, 
                                   fill_color=DEEP_NAVY, fill_opacity=0.8, stroke_color=TECH_CYAN)
        panel_title = Text("Phase Shifters", font_size=20, color=TECH_CYAN).next_to(panel_box, UP, buff=0, aligned_edge=LEFT).shift(DOWN*0.3+RIGHT*0.2)
        
        # Bars representing phase delays
        bars = VGroup(*[
            Rectangle(width=0.4, height=1, fill_color=NEON_PINK, fill_opacity=0.8, stroke_width=0)
            for _ in range(5)
        ]).arrange(RIGHT, buff=0.2).move_to(panel_box).shift(DOWN*0.2)
        
        phase_panel = VGroup(panel_box, panel_title, bars).to_corner(DL, buff=0.5)
        
        # Angle Info (Bottom Right)
        angle_box = RoundedRectangle(width=3, height=1.5, corner_radius=0.1,
                                   fill_color=DEEP_NAVY, fill_opacity=0.8, stroke_color=VIBRANT_ORANGE)
        angle_text = Text("Azimuth: 0°", font_size=24, color=TEXT_WHITE).move_to(angle_box).shift(UP*0.2)
        elev_text = Text("Elevation: 0°", font_size=24, color=TEXT_WHITE).move_to(angle_box).shift(DOWN*0.2)
        angle_panel = VGroup(angle_box, angle_text, elev_text).to_corner(DR, buff=0.5)

        # Add all 2D elements to frame
        self.add_fixed_in_frame_mobjects(header, phase_panel, angle_panel)
        
        # 3D SCENE ELEMENTS
        # ---------------------------------------------------------
        # 3D Axes for context (faded)
        axes = ThreeDAxes(
            x_range=[-4, 4, 1], y_range=[-4, 4, 1], z_range=[-1, 5, 1],
            x_length=8, y_length=8, z_length=5,
            axis_config={"stroke_opacity": 0.5, "stroke_width": 2}
        )
        
        # Antenna Grid
        antenna = self.create_antenna_array()
        
        # ANIMATION SEQUENCE
        # ---------------------------------------------------------
        self.play(Write(header), run_time=1)
        self.play(Create(axes), FadeIn(antenna), run_time=1.5)
        
        # Target Positions: [x, y, z]
        targets = [
            ([3, 0, 3], "RT", 45, 30),   # Right
            ([-3, 2, 3], "LF", -45, 40), # Left-Back
            ([0, 3, 2], "CT", 0, 60)     # Center-High
        ]
        
        beam = None
        
        for pos, label, az, el in targets:
            target_dot = Dot3D(point=pos, color=NEON_PINK, radius=0.2)
            target_halo = Dot3D(point=pos, color=NEON_PINK, radius=0.4).set_opacity(0.3)
            
            # Update Info Panel
            new_angle_text = Text(f"Azimuth: {az}°", font_size=24, color=TECH_CYAN).move_to(angle_box).shift(UP*0.2)
            new_elev_text = Text(f"Elevation: {el}°", font_size=24, color=TECH_CYAN).move_to(angle_box).shift(DOWN*0.2)
            
            # Animate Phase Bars (Staircase effect for steering)
            # Simple simulation: random heights relative to position to imply change
            new_bars = VGroup(*[
                Rectangle(width=0.4, height=0.5 + 0.3*np.sin(i + az), fill_color=NEON_PINK, fill_opacity=0.8, stroke_width=0)
                for i in range(5)
            ]).arrange(RIGHT, buff=0.2).move_to(panel_box).shift(DOWN*0.2)

            # Create Beam
            new_beam = self.create_beam_cone(pos)
            
            self.play(
                FadeIn(target_dot), FadeIn(target_halo),
                Transform(angle_text, new_angle_text),
                Transform(elev_text, new_elev_text),
                Transform(bars, new_bars),
                run_time=0.5
            )
            
            if beam:
                self.play(Transform(beam, new_beam), run_time=0.8)
            else:
                beam = new_beam
                self.play(FadeIn(beam), run_time=0.8)
            
            self.wait(0.5)
            
        # Final Sweep Animation
        self.move_camera(theta=-10*DEGREES, phi=50*DEGREES, run_time=3)
        self.wait(1)

    def create_antenna_array(self):
        base = Square(side_length=2, fill_color=SUBTLE_NAVY, fill_opacity=0.5, stroke_color=TECH_CYAN)
        elements = VGroup()
        for x in np.linspace(-0.8, 0.8, 5):
            for y in np.linspace(-0.8, 0.8, 5):
                dot = Dot3D(point=[x, y, 0], color=TECH_CYAN, radius=0.06)
                elements.add(dot)
        return VGroup(base, elements)

    def create_beam_cone(self, target_point):
        """Creates a semi-transparent cone pointing to target"""
        # Simplification: Line + multiple circles getting smaller
        start = np.array([0,0,0])
        end = np.array(target_point)
        
        # Main beam line
        line = Line3D(start, end, color=TECH_CYAN, thickness=0.02)
        
        # Cone sections approx
        sections = VGroup()
        for t in np.linspace(0.1, 1, 5):
            pos = start + (end - start) * t
            radius = 0.5 * t 
            # Note: In ThreeDScene, Circle is 2D. We need to rotate it to face camera or perpendicular to line
            # Creating a simple sphere/dot cloud or similar is easier in Manim for "Volume"
            # For efficiency, we use a glowing line
        beam_glow = Line3D(start, end, color=TECH_CYAN, thickness=0.1)
        beam_glow.set_opacity(0.3)
        return VGroup(line, beam_glow)


# ========================== PART 12: 3D TRACKING (20-25s) ==========================
class Part12(ThreeDScene):
    """Tracking in 3D Space - Complete Coordinate System - WITH VALUES"""
    def construct(self):
        self.set_camera_orientation(phi=65*DEGREES, theta=-45*DEGREES)
        
        title = Text("3D TARGET TRACKING", font_size=40, color=TECH_CYAN)
        title.to_edge(UP, buff=0.3)
        
        # Value Trackers
        range_val = ValueTracker(0)
        azimuth_val = ValueTracker(0)
        elev_val = ValueTracker(0)
        
        # Coordinate display with values
        # Sea Surface Grid (XY Plane)
        sea_grid = NumberPlane(
            x_range=[-6, 6, 1], y_range=[-6, 6, 1],
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            },
            axis_config={"include_numbers": False}
        )
        sea_grid.set_fill(color=DEEP_NAVY, opacity=0.3)
        
        # Coordinate display with values (HUD Style)
        coord_box = RoundedRectangle(width=4.0, height=2.2, color=TECH_CYAN, fill_color=DEEP_NAVY, fill_opacity=0.8, corner_radius=0.1)
        coord_box.set_stroke(width=1)
        coord_box.to_corner(UR, buff=0.3)
        coord_title = Text("TARGET DATA", font_size=20, color=TECH_CYAN, weight=BOLD).next_to(coord_box, UP, buff=0.1, aligned_edge=LEFT)
        
        # Labels and Numbers inside the box - Position relative to Top-Left of Box
        start_pos = coord_box.get_corner(UL) + RIGHT*0.2 + DOWN*0.5
        
        # Range
        r_label = Text("RANGE:", font_size=16, color=TECH_CYAN, font="Monospace").move_to(start_pos, aligned_edge=LEFT)
        r_num = DecimalNumber(0, num_decimal_places=2, unit=" km", font_size=16, color=TECH_CYAN)
        r_num.next_to(r_label, RIGHT, buff=0.5)
        r_num.add_updater(lambda d: d.set_value(range_val.get_value()))
        
        # Azimuth
        az_label = Text("AZIMUTH:", font_size=16, color=NEON_PINK, font="Monospace").next_to(r_label, DOWN, buff=0.3, aligned_edge=LEFT)
        az_num = DecimalNumber(0, num_decimal_places=1, unit="^\\circ", font_size=16, color=NEON_PINK)
        az_num.next_to(az_label, RIGHT, buff=0.5)
        az_num.add_updater(lambda d: d.set_value(azimuth_val.get_value()))
        
        # Elevation
        el_label = Text("ELEVATION:", font_size=16, color=VIBRANT_ORANGE, font="Monospace").next_to(az_label, DOWN, buff=0.3, aligned_edge=LEFT)
        el_num = DecimalNumber(0, num_decimal_places=1, unit="^\\circ", font_size=16, color=VIBRANT_ORANGE)
        el_num.next_to(el_label, RIGHT, buff=0.5)
        el_num.add_updater(lambda d: d.set_value(elev_val.get_value()))
        
        coord_group = VGroup(coord_box, coord_title, r_label, r_num, az_label, az_num, el_label, el_num)
        
        ship_label = Text("SHIP RADAR", font_size=16, color=TECH_CYAN, weight=BOLD).move_to(DOWN*1.5 + LEFT*0.5)

        # Add fixed title generally
        self.add_fixed_in_frame_mobjects(title, ship_label)
        
        # 3D coordinate system (Modified)
        axes = ThreeDAxes(
            x_range=[-5, 5, 1], y_range=[-5, 5, 1], z_range=[0, 5, 1],
            x_length=7, y_length=7, z_length=4,
            axis_config={"color": SUBTLE_NAVY}
        )
        
        # Ship at origin
        ship_marker = Dot3D(point=ORIGIN, color=TECH_CYAN, radius=0.1)
        ship_ring = Circle(radius=0.3, color=TECH_CYAN, stroke_width=1).rotate(PI/2, axis=RIGHT) # Flat on surface? No, 3D scene.
        # Let's just use a simple 3D shape for ship
        ship_cone = Cone(base_radius=0.2, height=0.5, direction=UP, show_base=True, fill_color=SUBTLE_NAVY, fill_opacity=0.8, stroke_color=TECH_CYAN)
        
        # Target
        # Initial position
        init_pos = np.array([-4, -2, 2])
        target = Dot3D(point=init_pos, color=NEON_PINK, radius=0.15)
        target.set_z_index(10) # Ensure it's on top
        
        # Trail
        trail = TracedPath(target.get_center, dissipating_time=2, stroke_opacity=[0, 1], stroke_color=NEON_PINK, stroke_width=2)
        
        # Tracking visualizers (Lines)
        # UPDATER FUNCTION
        def update_tracking(mob):
            pos = target.get_center()
            x, y, z = pos[0], pos[1], pos[2]
            
            # Update Trackers
            r = np.sqrt(x**2 + y**2 + z**2)
            az = np.degrees(np.arctan2(y, x))
            if az < 0: az += 360
            el = np.degrees(np.arcsin(z / r)) if r > 0 else 0
            
            range_val.set_value(r * 2.5) # Scale for realistic km
            azimuth_val.set_value(az)
            elev_val.set_value(el)

        # Use Line for updaters as it is more robust than Line3D for continuous updates
        dynamic_range = Line(ORIGIN, init_pos, color=TECH_CYAN, stroke_opacity=0.6)
        dynamic_proj = Line(ORIGIN, [init_pos[0], init_pos[1], 0], color=NEON_PINK, stroke_opacity=0.3)
        dynamic_height = Line([init_pos[0], init_pos[1], 0], init_pos, color=VIBRANT_ORANGE, stroke_opacity=0.8)
        
        dynamic_range.add_updater(lambda m: m.put_start_and_end_on(ORIGIN, target.get_center()))
        dynamic_proj.add_updater(lambda m: m.put_start_and_end_on(ORIGIN, [target.get_center()[0], target.get_center()[1], 0]))
        dynamic_height.add_updater(lambda m: m.put_start_and_end_on([target.get_center()[0], target.get_center()[1], 0], target.get_center()))
        
        # Add target updater
        target.add_updater(lambda m: update_tracking(m))

        # Animations
        self.play(Write(title), run_time=1)
        self.play(Create(axes), Create(sea_grid), FadeIn(ship_cone), run_time=1.5)
        
        # Add HUD elements efficiently - avoiding 3D ghosting
        self.add_fixed_in_frame_mobjects(coord_group)
        # Animate appearance by manually setting opacity? 
        # For now, just add them. If we want animation, we should create them with 0 opacity first.
        # But 'add_fixed...' puts them on screen. 
        # Let's try simpler formatting: just add them, assume user wants to see them.
        
        self.add(target, trail, dynamic_range, dynamic_proj, dynamic_height)
        self.play(FadeIn(target), run_time=0.5)
        
        # Move target along a spiral path
        path_points = [
            np.array([-4 + t*0.8, -2 + t*0.5 + np.sin(t*2), 2 + t*0.2 + np.cos(t)])
            for t in np.linspace(0, 10, 300)
        ]
        
        path_mobj = VMobject()
        path_mobj.set_points_smoothly(path_points)
        
        # Camera rotation
        self.begin_ambient_camera_rotation(rate=0.1)
        
        self.play(
            MoveAlongPath(target, path_mobj),
            run_time=8,
            rate_func=linear
        )
        
        self.wait(1)


# ========================== PART 13: RADAR EQUATION (18-22s) ==========================
class Part13(Scene):
    """The Radar Range Equation - Step by Step"""
    def construct(self):
        title = Text("THE RADAR EQUATION", font_size=48, color=TECH_CYAN)
        title.to_edge(UP)
        
        # Build equation step by step
        eq_parts = [
            MathTex(r"P_r = ", font_size=42, color=TEXT_WHITE),
            MathTex(r"\frac{P_t \cdot G^2 \cdot \lambda^2 \cdot \sigma}{(4\pi)^3 \cdot R^4}", 
                   font_size=42, color=VIBRANT_ORANGE),
        ]
        
        full_equation = VGroup(*eq_parts).arrange(RIGHT, buff=0.1)
        full_equation.move_to(ORIGIN)
        
        # Variable explanations
        var_explanations = VGroup(
            MathTex(r"P_r", r" = \text{Received Power}", font_size=28),
            MathTex(r"P_t", r" = \text{Transmitted Power}", font_size=28),
            MathTex(r"G", r" = \text{Antenna Gain}", font_size=28),
            MathTex(r"\lambda", r" = \text{Wavelength}", font_size=28),
            MathTex(r"\sigma", r" = \text{Radar Cross Section}", font_size=28),
            MathTex(r"R", r" = \text{Range to Target}", font_size=28),
        )
        
        for exp in var_explanations:
            exp[0].set_color(TECH_CYAN)
            exp[1].set_color(TEXT_WHITE)
        
        var_explanations.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        var_explanations.to_edge(LEFT, buff=0.5).shift(DOWN*0.5)
        
        # R^4 emphasis
        r4_box = VGroup(
            Text("KEY INSIGHT:", font_size=28, color=VIBRANT_ORANGE, weight=BOLD),
            MathTex(r"R^4 \text{ in denominator}", font_size=32, color=NEON_PINK),
            Text("Double the range →", font_size=24, color=TEXT_WHITE),
            Text("Signal 16x weaker!", font_size=28, color=NEON_PINK, weight=BOLD)
        ).arrange(DOWN, buff=0.2)
        r4_box.to_edge(RIGHT, buff=0.5)
        
        r4_rectangle = SurroundingRectangle(r4_box, color=NEON_PINK, buff=0.3, stroke_width=2)
        
        # Animations
        self.play(Write(title), run_time=1)
        self.wait(0.5)
        
        # Show equation parts
        self.play(Write(eq_parts[0]), run_time=1)
        self.play(Write(eq_parts[1]), run_time=2)
        
        # Box the equation
        eq_box = SurroundingRectangle(full_equation, color=TECH_CYAN, buff=0.2, stroke_width=3)
        self.play(Create(eq_box), run_time=0.8)
        
        # Move equation up
        self.play(
            VGroup(full_equation, eq_box).animate.shift(UP*1.5),
            run_time=1
        )
        
        # Show explanations one by one
        for exp in var_explanations:
            self.play(Write(exp), run_time=0.6)
        
        self.wait(1)
        
        # Emphasize R^4
        self.play(FadeIn(r4_box), Create(r4_rectangle), run_time=1.5)
        
        # Highlight R^4 in equation
        r4_highlight = SurroundingRectangle(
            eq_parts[1][0][17:21],  # R^4 portion
            color=NEON_PINK, buff=0.1, stroke_width=3
        )
        self.play(Create(r4_highlight), run_time=1)
        
        self.wait(3)


# ========================== PART 14: SIGNAL-TO-NOISE RATIO (15-18s) ==========================
class Part14(Scene):
    """Signal-to-Noise Ratio Analysis"""
    def construct(self):
        title = Text("SIGNAL-TO-NOISE RATIO", font_size=48, color=TECH_CYAN)
        title.to_edge(UP)
        
        subtitle = Text("Can we see the target through the noise?", font_size=28, color=TEXT_WHITE)
        subtitle.next_to(title, DOWN, buff=0.2)
        
        # Create signal visualization
        axes = Axes(
            x_range=[0, 10, 1], y_range=[-2, 3, 1],
            x_length=10, y_length=4,
            axis_config={"color": SUBTLE_NAVY}
        ).shift(DOWN*0.5)
        
        # Noise floor
        np.random.seed(42)
        noise_points = [[x, 0.3*np.random.randn(), 0] for x in np.linspace(0, 10, 200)]
        noise_line = VMobject(stroke_color=SUBTLE_NAVY, stroke_width=2)
        noise_line.set_points_smoothly([axes.c2p(p[0], p[1], 0) for p in noise_points])
        
        # Signal with noise
        signal_points = []
        for x in np.linspace(0, 10, 200):
            noise = 0.3 * np.random.randn()
            signal = 1.5 if 4 < x < 6 else 0
            signal_points.append([x, signal + noise, 0])
        
        signal_line = VMobject(stroke_color=TECH_CYAN, stroke_width=3)
        signal_line.set_points_smoothly([axes.c2p(p[0], p[1], 0) for p in signal_points])
        
        # Detection threshold line
        threshold = DashedLine(
            axes.c2p(0, 0.8, 0), axes.c2p(10, 0.8, 0),
            stroke_width=3, color=NEON_PINK, dash_length=0.1
        )
        threshold_label = Text("Detection Threshold", font_size=20, color=NEON_PINK)
        threshold_label.next_to(threshold, UP, buff=0.1).shift(RIGHT*2)
        
        # Target indicator
        target_arrow = Arrow(
            axes.c2p(5, 2.5, 0), axes.c2p(5, 1.8, 0),
            color=VIBRANT_ORANGE, stroke_width=4
        )
        target_label = Text("TARGET DETECTED!", font_size=22, color=VIBRANT_ORANGE, weight=BOLD)
        target_label.next_to(target_arrow, UP, buff=0.1)
        
        # SNR equation
        snr_eq = MathTex(r"SNR = \frac{P_{signal}}{P_{noise}}", font_size=36, color=VIBRANT_ORANGE)
        snr_eq.to_corner(DR, buff=0.5)
        
        # Labels
        noise_label = Text("Noise Floor", font_size=18, color=SUBTLE_NAVY)
        noise_label.move_to(axes.c2p(8, 0.5, 0))
        
        # Animations
        self.play(Write(title), run_time=1)
        self.play(FadeIn(subtitle), run_time=0.8)
        
        self.play(Create(axes), run_time=1)
        
        # Show noise first
        self.play(Create(noise_line), run_time=2)
        self.play(Write(noise_label), run_time=0.5)
        
        # Add threshold
        self.play(Create(threshold), Write(threshold_label), run_time=1)
        
        # Show signal emerging from noise
        self.play(Transform(noise_line, signal_line), run_time=2)
        
        # Point out target
        self.play(GrowArrow(target_arrow), Write(target_label), run_time=1)
        
        # Show equation
        self.play(Write(snr_eq), run_time=1.5)
        
        self.wait(3)


# ========================== PART 15: CLUTTER REJECTION (18-22s) ==========================
class Part15(Scene):
    """Clutter Rejection - Filtering Unwanted Returns"""
    def construct(self):
        title = Text("CLUTTER REJECTION", font_size=48, color=TECH_CYAN)
        title.to_edge(UP)
        
        subtitle = Text("Separating targets from environmental noise", font_size=28, color=TEXT_WHITE)
        subtitle.next_to(title, DOWN, buff=0.2)
        
        # PPI scope display (circular radar display)
        ppi_radius = 2.5
        ppi_circle = Circle(radius=ppi_radius, stroke_color=TECH_CYAN, stroke_width=3)
        ppi_center = Dot(ORIGIN, color=TECH_CYAN, radius=0.08)
        
        # Range rings
        range_rings = VGroup(*[
            Circle(radius=r, stroke_color=SUBTLE_NAVY, stroke_width=1)
            for r in [0.5, 1, 1.5, 2, 2.5]
        ])
        
        ppi_label = Text("PPI Display", font_size=22, color=TECH_CYAN)
        ppi_label.next_to(ppi_circle, DOWN, buff=0.3)
        
        # Clutter (random dots representing sea clutter, weather)
        np.random.seed(42)
        clutter = VGroup()
        for _ in range(80):
            r = np.random.uniform(0.3, ppi_radius)
            theta = np.random.uniform(0, 2*PI)
            size = np.random.uniform(0.02, 0.08)
            dot = Dot(point=[r*np.cos(theta), r*np.sin(theta), 0],
                     color=NEON_PINK, radius=size)
            dot.set_opacity(np.random.uniform(0.3, 0.7))
            clutter.add(dot)
        
        # Real targets (distinct returns)
        targets = VGroup(
            Dot(point=[1.5, 0.8, 0], color=VIBRANT_ORANGE, radius=0.12),
            Dot(point=[-1, 1.5, 0], color=VIBRANT_ORANGE, radius=0.12),
            Dot(point=[0.5, -1.8, 0], color=VIBRANT_ORANGE, radius=0.12),
        )
        
        # Before/After labels
        before_label = Text("BEFORE FILTERING", font_size=24, color=NEON_PINK, weight=BOLD)
        before_label.to_corner(UL, buff=0.5)
        
        after_label = Text("AFTER MTI/CFAR", font_size=24, color=TECH_CYAN, weight=BOLD)
        after_label.to_corner(UL, buff=0.5)
        
        # Filter techniques
        filter_box = VGroup(
            Text("Filtering Techniques:", font_size=22, color=TEXT_WHITE, weight=BOLD),
            Text("• MTI: Moving Target Indication", font_size=18, color=TECH_CYAN),
            Text("• CFAR: Constant False Alarm Rate", font_size=18, color=TECH_CYAN),
            Text("• Doppler Processing", font_size=18, color=TECH_CYAN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        filter_box.to_corner(DR, buff=0.5)
        
        # Animations
        self.play(Write(title), run_time=1)
        self.play(FadeIn(subtitle), run_time=0.8)
        
        # Build PPI display
        self.play(Create(ppi_circle), Create(range_rings), FadeIn(ppi_center), run_time=1)
        self.play(Write(ppi_label), run_time=0.5)
        
        # Show cluttered display
        self.play(Write(before_label), run_time=0.5)
        self.play(FadeIn(clutter), run_time=1.5)
        self.play(FadeIn(targets), run_time=0.5)
        
        self.wait(1)
        
        # Show filter techniques
        self.play(FadeIn(filter_box), run_time=1)
        
        self.wait(1)
        
        # Apply filtering - fade out clutter, keep targets
        self.play(
            ReplacementTransform(before_label, after_label),
            clutter.animate.set_opacity(0.05),
            targets.animate.set_color(TECH_CYAN).scale(1.3),
            run_time=2
        )
        
        # Highlight targets
        target_circles = VGroup(*[
            Circle(radius=0.25, stroke_color=VIBRANT_ORANGE, stroke_width=3).move_to(t.get_center())
            for t in targets
        ])
        
        self.play(
            *[Create(c) for c in target_circles],
            run_time=1
        )
        
        self.wait(3)


# ========================== PART 16: TARGET CLASSIFICATION (15-18s) ==========================
class Part16(Scene):
    """Target Classification - Identifying What We're Tracking"""
    def construct(self):
        title = Text("TARGET CLASSIFICATION", font_size=40, color=TECH_CYAN, weight=BOLD)
        title.to_edge(UP)
        
        subtitle = Text("SIGNATURE ANALYSIS DETECTED", font_size=20, color=VIBRANT_ORANGE, font="Monospace")
        subtitle.next_to(title, DOWN, buff=0.1)
        
        # Background Grid (Tech style)
        grid = NumberPlane(
            x_range=[-8, 8, 1], y_range=[-5, 5, 1],
            background_line_style={"stroke_color": TEAL, "stroke_opacity": 0.15, "stroke_width": 1},
            axis_config={"include_numbers": False}
        )
        
        # Analysis Panel Container
        panel_width = 10.0
        panel_height = 4.5
        panel_bg = RoundedRectangle(width=panel_width, height=panel_height, corner_radius=0.2, 
                                   fill_color=DEEP_NAVY, fill_opacity=0.8, stroke_color=TECH_CYAN, stroke_width=2)
        panel_bg.move_to(RIGHT * 1.5) # Shift panel to the right to make room on the left
        
        panel_title = Text("TARGET DATABASE MATCHING", font_size=18, color=TECH_CYAN, weight=BOLD).next_to(panel_bg, UP, buff=0.1, aligned_edge=LEFT)
        
        # Create three target profiles inside the panel
        targets = VGroup()
        labels = ["FIGHTER JET", "COMMERCIAL", "DRONE / UAV"]
        rcs_values = ["1-5 m²", "50-100 m²", "0.01-0.1 m²"]
        speeds = ["Mach 1.5+", "500 km/h", "100 km/h"]
        colors = [NEON_PINK, SUBTLE_NAVY, VIBRANT_ORANGE] # Subtle Navy used for Commercial text might be too dark, switch to LIGHT_GREY or similiar if needed. Using TEXT_WHITE for now.
        colors_display = [NEON_PINK, TEXT_WHITE, VIBRANT_ORANGE] 
        
        # Calculate cell width
        cell_width = panel_width / 3.2
        
        for i, (label, rcs, speed, color) in enumerate(zip(labels, rcs_values, speeds, colors_display)):
            # Profile Card
            card = RoundedRectangle(width=cell_width, height=3.5, corner_radius=0.1,
                                   fill_color=SUBTLE_NAVY, fill_opacity=0.4, stroke_color=color, stroke_width=1)
            
            # Content
            l_text = Text(label, font_size=18, color=color, weight=BOLD).move_to(card.get_top() + DOWN*0.5)
            
            # Data fields
            rcs_box = VGroup(
                Text("RCS", font_size=12, color=TEAL, font="Monospace"),
                Text(rcs, font_size=14, color=TEXT_WHITE, weight=BOLD)
            ).arrange(DOWN, buff=0.1)
            
            spd_box = VGroup(
                Text("SPEED", font_size=12, color=TEAL, font="Monospace"),
                Text(speed, font_size=14, color=TEXT_WHITE, weight=BOLD)
            ).arrange(DOWN, buff=0.1)
            
            data_row = VGroup(rcs_box, spd_box).arrange(RIGHT, buff=0.3).move_to(card.get_center() + DOWN*0.2)
            
            # Placeholder for image/icon (using simple geometry for now)
            icon = Circle(radius=0.4, color=color, fill_opacity=0.2, stroke_width=2).move_to(card.get_top() + DOWN*1.5)
            if i == 0: icon = Triangle(color=color, fill_opacity=0.2).scale(0.4).move_to(icon)
            elif i == 1: icon = Square(side_length=0.7, color=color, fill_opacity=0.2).move_to(icon)
            
            full_card = VGroup(card, l_text, data_row, icon)
            
            # Position relative to panel center
            # Panel is shifted to RIGHT*1.5
            # We need to arrange them inside the panel
            # Local position
            x_rel = (i - 1) * (cell_width + 0.15) 
            full_card.move_to(panel_bg.get_center() + np.array([x_rel, 0, 0]))
            targets.add(full_card)
        
        # Scanning Line
        scanner = Line(UP*2.2, DOWN*2.2, color=TECH_CYAN, stroke_width=4)
        scanner.set_shadow(0.5)
        
        # Status Bar
        status_bar = Rectangle(width=14, height=0.6, fill_color=SUBTLE_NAVY, fill_opacity=1, stroke_width=0).to_edge(DOWN, buff=0)
        status_text = Text("SYSTEM STATUS: ANALYZING SIGNATURE PATTERNS...", font_size=20, color=VIBRANT_ORANGE, font="Monospace")
        status_text.move_to(status_bar)
        
        # Animations
        self.play(FadeIn(grid), Write(title), run_time=1)
        self.play(Write(subtitle), run_time=0.5)
        
        self.play(Create(panel_bg), Write(panel_title), FadeIn(status_bar), Write(status_text), run_time=1)
        
        self.play(LaggedStart(*[FadeIn(t, shift=UP*0.2) for t in targets], lag_ratio=0.2), run_time=1.5)
        
        # Scanning Animation
        scanner.move_to(panel_bg.get_left())
        self.add(scanner)
        self.play(
            scanner.animate.move_to(panel_bg.get_right()),
            run_time=2,
            rate_func=linear
        )
        self.play(FadeOut(scanner), run_time=0.2)
        
        # Classification Result Logic (Highlighting the match)
        match_idx = 0 # Fighter Jet
        status_match = Text("MATCH CONFIRMED: FIGHTER JET (92%)", font_size=20, color=NEON_PINK, weight=BOLD, font="Monospace").move_to(status_bar)
        
        self.play(
            targets[match_idx].animate.scale(1.1).set_color(NEON_PINK),
            targets[1].animate.set_opacity(0.3),
            targets[2].animate.set_opacity(0.3),
            Transform(status_text, status_match),
            run_time=0.8
        )
        
        self.wait(1)
        
        # Confidence bars details logic replaced by simplified highlighting for cleaner look
        # If user wants bars, we can add them below the cards, but space is tight.
        # Let's verify this cleaner layout first.
        
        # Signature analysis text (re-added with better positioning)
        analysis_text = VGroup(
            Text("Signature Analysis:", font_size=24, color=VIBRANT_ORANGE, weight=BOLD),
            Text("• RCS Pattern", font_size=20, color=TEXT_WHITE),
            Text("• Doppler Signature", font_size=20, color=TEXT_WHITE),
            Text("• Flight Characteristics", font_size=20, color=TEXT_WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        # Position in the left empty space
        analysis_text.move_to(LEFT * 4.5) # Center vertically on screen by default?
        # Or align it beautifully
        analysis_text.to_edge(LEFT, buff=0.8).shift(UP*0.5)
        
        # Show analysis criteria
        self.play(FadeIn(analysis_text), run_time=1)
        
        highlight = SurroundingRectangle(targets[0], color=NEON_PINK, buff=0.15, stroke_width=4)
        self.play(Create(highlight), run_time=1)
        
        # Highlight winner
        self.play(
            targets[0].animate.set_stroke(color=NEON_PINK, width=6),
            run_time=0.5
        )
        
        
        self.wait(3)


# ========================== PART 17: COMBAT INFORMATION CENTER (18-22s) ==========================
class Part17(Scene):
    """The Combat Information Center - Tactical Display"""
    def construct(self):
        title = Text("COMBAT INFORMATION CENTER", font_size=42, color=TECH_CYAN)
        title.to_edge(UP)
        
        # Create tactical display
        display_radius = 3
        display = Circle(radius=display_radius, stroke_color=TECH_CYAN, stroke_width=2)
        
        # Range rings
        range_rings = VGroup(*[
            Circle(radius=r, stroke_color=SUBTLE_NAVY, stroke_width=1)
            for r in np.linspace(0.5, display_radius, 6)
        ])
        
        # Compass lines
        compass = VGroup(*[
            Line(ORIGIN, display_radius * np.array([np.cos(a), np.sin(a), 0]),
                stroke_color=SUBTLE_NAVY, stroke_width=1)
            for a in np.linspace(0, 2*PI, 12, endpoint=False)
        ])
        
        # Own ship marker
        ship_marker = RegularPolygon(n=3, radius=0.2, fill_color=TECH_CYAN, 
                                     fill_opacity=1, stroke_width=0)
        ship_marker.rotate(-PI/2)
        
        # Target tracks with velocity vectors
        targets = []
        target_data = [
            {"pos": [1.5, 1.2, 0], "vel": [-0.3, 0.1, 0], "label": "TGT-001", "threat": True},
            {"pos": [-1, 2, 0], "vel": [-0.2, -0.1, 0], "label": "TGT-002", "threat": False},
            {"pos": [2, -1, 0], "vel": [0.1, 0.3, 0], "label": "TGT-003", "threat": True},
        ]
        
        target_group = VGroup()
        for data in target_data:
            color = NEON_PINK if data["threat"] else SUBTLE_NAVY
            marker = Dot(point=data["pos"], color=color, radius=0.12)
            velocity = Arrow(
                start=np.array(data["pos"]),
                end=np.array(data["pos"]) + np.array(data["vel"]) * 2,
                color=color, stroke_width=2, buff=0
            )
            label = Text(data["label"], font_size=14, color=color)
            label.next_to(marker, UR, buff=0.1)
            target_group.add(VGroup(marker, velocity, label))
        
        # Engagement envelope
        envelope = Circle(radius=2, stroke_color=NEON_PINK, stroke_width=2, 
                         stroke_opacity=0.5).set_fill(NEON_PINK, opacity=0.1)
        envelope_label = Text("Weapons Range", font_size=16, color=NEON_PINK)
        envelope_label.move_to([2.3, 0, 0])
        
        # Status panel
        status = VGroup(
            Text("TRACK STATUS", font_size=20, color=VIBRANT_ORANGE, weight=BOLD),
            Text("Active Tracks: 3", font_size=16, color=TEXT_WHITE),
            Text("Hostile: 2", font_size=16, color=NEON_PINK),
            Text("Unknown: 1", font_size=16, color=SUBTLE_NAVY),
            Text("Weapons: READY", font_size=16, color=TECH_CYAN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        status.to_corner(UR, buff=0.3)
        
        # Animations
        self.play(Write(title), run_time=1)
        
        # Build tactical display
        self.play(Create(display), Create(range_rings), Create(compass), run_time=1.5)
        self.play(FadeIn(ship_marker), run_time=0.5)
        
        # Add targets
        for tgt in target_group:
            self.play(FadeIn(tgt), run_time=0.5)
        
        # Show engagement envelope
        self.play(FadeIn(envelope), Write(envelope_label), run_time=1)
        
        # Status panel
        self.play(FadeIn(status), run_time=1)
        
        # Animate radar sweep
        sweep = Line(ORIGIN, RIGHT*display_radius, stroke_color=TECH_CYAN, stroke_width=3)
        sweep.set_opacity(0.6)
        
        self.play(Rotate(sweep, angle=2*PI, about_point=ORIGIN), run_time=4, rate_func=linear)
        
        self.wait(2)


# ========================== PART 18: MULTI-SENSOR FUSION (15-18s) ==========================
class Part18(Scene):
    """Multi-Sensor Fusion - Combining Data Sources"""
    def construct(self):
        title = Text("MULTI-SENSOR FUSION", font_size=48, color=TECH_CYAN)
        title.to_edge(UP)
        
        subtitle = Text("Combining multiple sensor inputs for better accuracy", 
                       font_size=24, color=TEXT_WHITE)
        subtitle.next_to(title, DOWN, buff=0.2)
        
        # Sensor boxes
        sensors = VGroup()
        sensor_data = [
            ("Primary\nRadar", TECH_CYAN, "Range, Bearing\nVelocity"),
            ("Secondary\nRadar", NEON_PINK, "IFF, Altitude\nFlight Data"),
            ("ESM/ELINT", VIBRANT_ORANGE, "Emissions\nSignature"),
            ("IR/EO", TEXT_WHITE, "Visual ID\nThermal"),
        ]
        
        for name, color, data in sensor_data:
            box = VGroup(
                RoundedRectangle(width=2.5, height=2, corner_radius=0.2,
                                fill_color=DEEP_NAVY, fill_opacity=0.8,
                                stroke_color=color, stroke_width=3),
                Text(name, font_size=18, color=color, weight=BOLD),
                Text(data, font_size=12, color=TEXT_WHITE),
            )
            box[1].move_to(box[0].get_center() + UP*0.5)
            box[2].move_to(box[0].get_center() + DOWN*0.3)
            sensors.add(box)
        
        sensors.arrange(RIGHT, buff=0.3)
        sensors.move_to(UP*1.2) # Moved up from 0.5
        
        # Fusion processor
        fusion_box = VGroup(
            RoundedRectangle(width=4, height=1.5, corner_radius=0.2,
                            fill_color=VIBRANT_ORANGE, fill_opacity=0.2,
                            stroke_color=VIBRANT_ORANGE, stroke_width=3),
            Text("DATA FUSION\nPROCESSOR", font_size=20, color=VIBRANT_ORANGE, weight=BOLD)
        )
        fusion_box[1].move_to(fusion_box[0].get_center())
        fusion_box.move_to(DOWN*1.0) # Moved up from DOWN*1.8
        
        # Connection arrows
        arrows = VGroup()
        for sensor in sensors:
            arrow = Arrow(
                sensor.get_bottom(), fusion_box.get_top(),
                color=SUBTLE_NAVY, stroke_width=2, buff=0.1
            )
            arrows.add(arrow)
        
        # Output
        output_box = VGroup(
            RoundedRectangle(width=3.5, height=1.2, corner_radius=0.2,
                            fill_color=TECH_CYAN, fill_opacity=0.2,
                            stroke_color=TECH_CYAN, stroke_width=3),
            Text("FUSED TRACK\nHigh Confidence", font_size=18, color=TECH_CYAN, weight=BOLD)
        )
        output_box[1].move_to(output_box[0].get_center())
        output_box.move_to(DOWN*2.6) # Moved up from edge
        
        output_arrow = Arrow(fusion_box.get_bottom(), output_box.get_top(),
                            color=TECH_CYAN, stroke_width=3, buff=0.1)
        
        # Accuracy comparison
        accuracy_text = VGroup(
            Text("Single Sensor: ±50m", font_size=18, color=NEON_PINK),
            Text("Fused Data: ±5m", font_size=18, color=TECH_CYAN, weight=BOLD),
        ).arrange(RIGHT, buff=1)
        accuracy_text.next_to(output_box, RIGHT, buff=0.5)
        
        # Animations
        self.play(Write(title), run_time=1)
        self.play(FadeIn(subtitle), run_time=0.8)
        
        # Show sensors
        for sensor in sensors:
            self.play(FadeIn(sensor), run_time=0.5)
        
        # Show connections
        self.play(*[GrowArrow(a) for a in arrows], run_time=1)
        
        # Show fusion processor
        self.play(FadeIn(fusion_box), run_time=1)
        
        # Data flowing animation (simple pulses along arrows)
        for _ in range(2):
            pulses = VGroup(*[
                Dot(a.get_start(), color=TECH_CYAN, radius=0.08)
                for a in arrows
            ])
            self.add(pulses)
            self.play(
                *[p.animate.move_to(arrows[i].get_end()) for i, p in enumerate(pulses)],
                run_time=0.8
            )
            self.remove(pulses)
        
        # Show output
        self.play(GrowArrow(output_arrow), run_time=0.5)
        self.play(FadeIn(output_box), run_time=1)
        
        # Show accuracy improvement
        self.play(FadeIn(accuracy_text), run_time=1)
        
        self.wait(2)


# ========================== PART 19: COMPLETE DETECTION SEQUENCE (20-25s) ==========================
class Part19(Scene):
    """Complete Detection Sequence - Replay of the Entire Process"""
    def construct(self):
        title = Text("THE COMPLETE DETECTION SEQUENCE", font_size=42, color=TECH_CYAN)
        title.to_edge(UP)
        
        # Mission Control Layout
        # 1. Tactical Frame
        frame = Rectangle(width=13.5, height=7.5, stroke_color=SUBTLE_NAVY, stroke_width=2)
        frame_corners = VGroup()
        for x in [-1, 1]:
            for y in [-1, 1]:
                c = VGroup(
                    Line(ORIGIN, RIGHT*0.5).move_to([x*6.75, y*3.75, 0]).align_to(frame, RIGHT if x==1 else LEFT),
                    Line(ORIGIN, UP*0.5).move_to([x*6.75, y*3.75, 0]).align_to(frame, UP if y==1 else DOWN)
                ).set_color(TECH_CYAN).set_stroke(width=4)
                frame_corners.add(c)
        
        # 2. Equation Data Bank (Right Side Panel)
        data_bank_bg = RoundedRectangle(width=4, height=5, corner_radius=0.1, 
                                       fill_color=DEEP_NAVY, fill_opacity=0.8, stroke_color=TECH_CYAN, stroke_width=1)
        data_bank_bg.to_edge(RIGHT, buff=0.5).shift(UP*0.5)
        
        data_bank_title = Text("SYSTEM PARAMETERS", font_size=16, color=TECH_CYAN, weight=BOLD).next_to(data_bank_bg, UP, buff=0.1, aligned_edge=RIGHT)
        
        # Prepare equation groups individually first
        eq1 = VGroup(Text("PROPAGATION SPEED:", font_size=12, color=TEAL, font="Monospace"),
                     MathTex(r"c = 3 \times 10^8 \text{ m/s}", font_size=20, color=TEXT_WHITE))
        eq2 = VGroup(Text("RANGE CALCULATION:", font_size=12, color=TEAL, font="Monospace"),
                     MathTex(r"R = \frac{c \cdot t}{2}", font_size=20, color=TECH_CYAN))
        eq3 = VGroup(Text("DOPPLER SHIFT:", font_size=12, color=TEAL, font="Monospace"),
                     MathTex(r"f_d = \frac{2v_r f_0}{c}", font_size=20, color=NEON_PINK))
        eq4 = VGroup(Text("RECEIVED POWER:", font_size=12, color=TEAL, font="Monospace"),
                     MathTex(r"P_r \propto \frac{1}{R^4}", font_size=20, color=VIBRANT_ORANGE))

        # Arrange internals of each group
        for eq in [eq1, eq2, eq3, eq4]:
            eq.arrange(DOWN, aligned_edge=LEFT, buff=0.1)

        # Now group them and arrange the main container
        equations_group = VGroup(eq1, eq2, eq3, eq4).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        equations_group.move_to(data_bank_bg.get_center())
        
        # 3. Main Action Area (Left Side)
        action_area = Rectangle(width=8.5, height=5, fill_opacity=0, stroke_opacity=0).to_edge(LEFT, buff=0.5).shift(UP*0.5)
        
        ship = self.create_mini_ship().scale(0.6).move_to(action_area.get_left() + RIGHT*1)
        jet = self.create_mini_jet().scale(0.4).move_to(action_area.get_right() + LEFT*1 + UP*1)
        
        # 4. Progress Flowchart (Bottom)
        progress_steps = ["TRANSMIT", "PROPAGATION", "REFLECTION", "ECHO", "PROCESSING", "TRACKING"]
        progress_bar = VGroup()
        
        for i, step in enumerate(progress_steps):
            # Reduced width from 1.8 to 1.4, height from 0.6 to 0.5
            box = RoundedRectangle(width=1.4, height=0.5, corner_radius=0.1, 
                                  fill_color=SUBTLE_NAVY, fill_opacity=0.5, stroke_color=SUBTLE_NAVY, stroke_width=1)
            # Reduced font size from 14 to 10
            txt = Text(step, font_size=10, color=TEXT_WHITE, weight=BOLD)
            txt.move_to(box)
            item = VGroup(box, txt)
            progress_bar.add(item)
            
            # Arrow to next
            if i < len(progress_steps) - 1:
                # Use a specific smaller length instead of scaling a large arrow
                arrow = Arrow(ORIGIN, RIGHT*0.5, color=SUBTLE_NAVY, buff=0, max_tip_length_to_length_ratio=0.5)
                progress_bar.add(arrow)
                
        progress_bar.arrange(RIGHT, buff=0.1)
        progress_bar.to_edge(DOWN, buff=0.5)
        
        # Animations
        self.play(
            FadeIn(frame), FadeIn(frame_corners), Write(title),
            FadeIn(data_bank_bg), Write(data_bank_title),
            FadeIn(progress_bar),
            run_time=1.5
        )
        self.play(FadeIn(ship), FadeIn(jet), FadeIn(equations_group), run_time=1)
        
        # Helper to highlight step
        def highlight_step(index, color=TECH_CYAN):
            # item 0 is step 1, item 1 is arrow, item 2 is step 2...
            # Steps are at indices 0, 2, 4, 6, 8, 10
            real_idx = index * 2
            
            # Reset all
            anims = []
            for i in range(0, len(progress_bar), 2):
                anims.append(progress_bar[i][0].animate.set_stroke(SUBTLE_NAVY, width=1).set_fill(SUBTLE_NAVY, 0.5))
                anims.append(progress_bar[i][1].animate.set_color(TEXT_WHITE))
            
            # Highlight current
            if real_idx < len(progress_bar):
                anims.append(progress_bar[real_idx][0].animate.set_stroke(color, width=3).set_fill(color, 0.2))
                anims.append(progress_bar[real_idx][1].animate.set_color(color))
                
            return anims

        # Helpeer to highlight equation
        def highlight_eq(index):
            anims = []
            for i, eq in enumerate(equations_group):
                if i == index:
                    anims.append(eq.animate.scale(1.1).set_opacity(1))
                    anims.append(eq[0].animate.set_color(VIBRANT_ORANGE))
                else:
                    anims.append(eq.animate.scale(1/1.1 if eq.height > 1 else 1).set_opacity(0.3))
                    anims.append(eq[0].animate.set_color(TEAL))
            return anims

        # Sequence
        
        # Step 1: Transmit
        self.play(*highlight_step(0), run_time=0.5)
        pulse = self.create_pulse().move_to(ship.get_right())
        self.play(FadeIn(pulse, scale=0.5), run_time=0.3)
        
        # Step 2: Propagation
        self.play(*highlight_step(1, VIBRANT_ORANGE), *highlight_eq(0), run_time=0.5) # Speed eq
        self.play(
            pulse.animate.move_to(jet.get_center()).scale(2).set_opacity(0.5),
            run_time=1.5
        )
        self.play(*highlight_eq(1), run_time=0.5) # Range eq (distance covered)
        
        # Step 3: Reflection
        self.play(*highlight_step(2, NEON_PINK), run_time=0.5)
        flash = Circle(radius=0.3, fill_color=NEON_PINK, fill_opacity=0.8, stroke_width=0)
        flash.move_to(jet.get_center())
        self.play(FadeIn(flash), FadeOut(pulse), run_time=0.3)
        
        # Step 4: Echo
        self.play(*highlight_step(3, NEON_PINK), *highlight_eq(3), run_time=0.5) # Power eq
        echo = self.create_pulse(color=NEON_PINK).move_to(jet.get_center())
        self.play(FadeOut(flash), FadeIn(echo), run_time=0.3)
        self.play(
            echo.animate.move_to(ship.get_right()).set_opacity(0.3),
            run_time=1.5
        )
        self.play(FadeOut(echo), run_time=0.2)
        
        # Step 5: Processing
        self.play(*highlight_step(4, TECH_CYAN), *highlight_eq(2), run_time=0.5) # Doppler eq
        process_flash = Circle(radius=0.5, stroke_color=TECH_CYAN, stroke_width=4)
        process_flash.move_to(ship.get_center())
        self.play(Create(process_flash), run_time=0.5)
        self.play(process_flash.animate.scale(0.3).set_opacity(0), run_time=0.5)
        
        # Step 6: Tracking
        self.play(*highlight_step(5, TECH_CYAN), run_time=0.5)
        track_box = RoundedRectangle(width=1.5, height=1, color=TECH_CYAN, stroke_width=2)
        track_box.move_to(jet.get_center())
        track_text = Text("TRACKED", font_size=12, color=TECH_CYAN, weight=BOLD).next_to(track_box, UP, buff=0.1)
        
        self.play(Create(track_box), Write(track_text), run_time=0.5)
        
        # Reset equations highlight
        self.play(
            *[eq.animate.set_opacity(1).scale(1) for eq in equations_group],
            *[eq[0].animate.set_color(TEAL) for eq in equations_group],
            run_time=1
        )
        
        self.wait(2)
        self.wait(2)

    
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


# ========================== PART 20: FINALE & OUTRO (15-18s) ==========================
class Part20(Scene):
    """The Finale - Summary and Outro"""
    def construct(self):
        # Final warship with radar sweep
        ship = self.create_final_ship().scale(0.8).to_edge(DOWN, buff=1.5)
        
        # Radar sweep animation
        sweep_line = Line(ORIGIN, UP*3, stroke_color=TECH_CYAN, stroke_width=4)
        sweep_line.move_to(ship.get_center() + UP*0.5, aligned_edge=DOWN)
        sweep_line.set_opacity(0.6)
        
        # Key takeaways
        takeaways = VGroup(
            Text("KEY TAKEAWAYS", font_size=36, color=VIBRANT_ORANGE, weight=BOLD),
            Text("✓ Radar uses radio waves to detect targets", font_size=24, color=TEXT_WHITE),
            Text("✓ Phased arrays steer beams electronically", font_size=24, color=TEXT_WHITE),
            Text("✓ Doppler effect reveals target velocity", font_size=24, color=TEXT_WHITE),
            Text("✓ Signal processing filters noise from targets", font_size=24, color=TEXT_WHITE),
            Text("✓ Multiple sensors provide complete picture", font_size=24, color=TEXT_WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        takeaways.to_edge(LEFT, buff=0.5).shift(UP*0.5)
        
        # Title
        title = Text("NAVAL RADAR DETECTION", font_size=48, color=TECH_CYAN, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        
        # Subscribe call-to-action
        cta = VGroup(
            Text("Like & Subscribe for more", font_size=28, color=NEON_PINK),
            Text("TECH EXPLAINED", font_size=32, color=TECH_CYAN, weight=BOLD),
        ).arrange(DOWN, buff=0.1)
        cta.to_corner(DR, buff=0.5)
        
        # Animations
        self.play(FadeIn(ship), run_time=1)
        
        # Start radar sweep
        self.add(sweep_line)
        sweep_anim = Rotate(sweep_line, angle=PI, about_point=ship.get_center() + UP*0.5,
                           rate_func=linear, run_time=4)
        
        self.play(Write(title), run_time=1)
        
        # Show takeaways during sweep
        self.play(sweep_anim, LaggedStart(*[
            FadeIn(t, shift=RIGHT*0.3) for t in takeaways
        ], lag_ratio=0.3), run_time=4)
        
        # Continue sweep
        self.play(
            Rotate(sweep_line, angle=PI, about_point=ship.get_center() + UP*0.5,
                  rate_func=linear),
            run_time=2
        )
        
        # Call to action
        self.play(FadeIn(cta, scale=1.2), run_time=1)
        
        # Final pulse effect
        pulse_rings = VGroup(*[
            Circle(radius=0.5+i*0.5, stroke_color=TECH_CYAN, stroke_width=3-i*0.5)
            for i in range(5)
        ])
        pulse_rings.move_to(ship.get_center() + UP*0.5)
        
        for ring in pulse_rings:
            self.add(ring)
            self.play(ring.animate.scale(2).set_opacity(0), run_time=0.4)
            self.remove(ring)
        
        # Fade out
        self.wait(1)
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=1.5
        )
        
        # End card
        end_text = Text("Thank you for watching!", font_size=48, color=TEXT_WHITE)
        self.play(FadeIn(end_text), run_time=1)
        self.wait(2)
    
    def create_final_ship(self):
        hull = Polygon(
            [-3, 0, 0], [-2.5, -0.5, 0], [2.5, -0.5, 0], [3, 0, 0], 
            [2.8, 0.2, 0], [-2.8, 0.2, 0],
            fill_color=SUBTLE_NAVY, fill_opacity=1, stroke_color=TECH_CYAN, stroke_width=3
        )
        tower = Rectangle(width=1.5, height=1.8, fill_color=SUBTLE_NAVY,
                         fill_opacity=1, stroke_color=TECH_CYAN, stroke_width=2)
        tower.move_to([0, 1.1, 0])
        
        radar = VGroup(
            Line([-0.4, 2, 0], [0.4, 2, 0], stroke_width=5, color=NEON_PINK),
            Line([0, 1.9, 0], [0, 2.3, 0], stroke_width=3, color=TECH_CYAN),
        )
        
        return VGroup(hull, tower, radar)
