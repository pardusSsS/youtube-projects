from manim import *
import numpy as np

config.background_color = "#020B1F"

# ============================================================================
# PART 1: THE HOOK (3-6 seconds) - INSTANT ATTENTION GRABBER
# ============================================================================
class Part1(ThreeDScene):
    def construct(self):
        # Explosive title reveal with rotating 3D radar dish
        title = Text("RADAR ANTENNA\nTYPES", font_size=96, weight=BOLD, color="#00F0FF")
        title.set_stroke("#FF0055", width=3, background=True)
        
        # 3D radar dish silhouette
        dish = Surface(
            lambda u, v: np.array([
                2 * np.cos(u) * v,
                2 * np.sin(u) * v,
                -v**2
            ]),
            u_range=[0, TAU],
            v_range=[0, 1],
            resolution=(24, 12)
        )
        dish.set_color("#00F0FF")
        dish.set_opacity(0.7)
        dish.scale(0.8).shift(OUT * 2)
        
        # Rotating signal waves
        waves = VGroup(*[
            Circle(radius=0.5 + i*0.4, color="#FF0055", stroke_width=3).set_opacity(0.6)
            for i in range(5)
        ])
        
        self.play(
            SpinInFromNothing(title, run_time=1.2),
            Create(dish, run_time=1.5),
            LaggedStart(*[GrowFromCenter(w) for w in waves], lag_ratio=0.15, run_time=1.8)
        )
        self.play(
            Rotate(dish, angle=PI/3, axis=RIGHT, run_time=1),
            waves.animate.scale(2).set_opacity(0),
            run_time=1
        )
        self.wait(0.3)

# ============================================================================
# PART 2: INTRODUCTION - WHAT IS A RADAR ANTENNA? (13-20s)
# ============================================================================
class Part2(Scene):
    def construct(self):
        title = Text("What is a Radar Antenna?", font_size=56, color="#FFFFFF")
        title.to_edge(UP)
        
        # Simple radar system diagram
        antenna = Triangle(color="#00F0FF", fill_opacity=0.8).scale(0.8).rotate(-PI/2)
        antenna.shift(LEFT * 4)
        
        # Signal transmission
        signal_out = Arrow(LEFT * 3.2, RIGHT * 0, color="#FF9F00", stroke_width=6, max_tip_length_to_length_ratio=0.2)
        signal_label = Text("Electromagnetic\nWave", font_size=28, color="#FF9F00").next_to(signal_out, UP)
        
        # Target
        target = Circle(radius=0.4, color="#FF0055", fill_opacity=0.9).shift(RIGHT * 3)
        target_label = Text("Target", font_size=24, color="#FFFFFF").next_to(target, DOWN)
        
        # Return signal
        signal_back = Arrow(RIGHT * 2.6, LEFT * 3.2, color="#00F0FF", stroke_width=6, max_tip_length_to_length_ratio=0.2)
        signal_back.shift(DOWN * 0.5)
        
        desc = Text("The component that transmits and receives\nelectromagnetic waves", 
                   font_size=32, color="#FFFFFF").to_edge(DOWN, buff=1)
        
        self.play(Write(title), run_time=2)
        self.wait(2)
        self.play(FadeIn(antenna, scale=1.3), run_time=2)
        self.wait(1.5)
        self.play(GrowArrow(signal_out), Write(signal_label), run_time=2.5)
        self.wait(1.5)
        self.play(FadeIn(target, scale=0.5), Write(target_label), run_time=2)
        self.wait(1.5)
        self.play(GrowArrow(signal_back), run_time=2.5)
        self.wait(1.5)
        self.play(Write(desc), run_time=2.5)
        self.wait(3)

# ============================================================================
# PART 3: ANTENNA CLASSIFICATION OVERVIEW (15-22s)
# ============================================================================
class Part3(Scene):
    def construct(self):
        title = Text("Classification of Radar Antennas", font_size=52, color="#00F0FF")
        title.to_edge(UP)
        
        # Main categories
        main_box = Rectangle(width=5, height=1.5, color="#FFFFFF", stroke_width=3)
        main_label = Text("Radar\nAntennas", font_size=36, color="#FFFFFF")
        main_group = VGroup(main_box, main_label).shift(UP * 2)
        
        # Branch lines
        line_left = Line(main_box.get_bottom(), DOWN * 0.5 + LEFT * 3.5, color="#FF9F00", stroke_width=4)
        line_right = Line(main_box.get_bottom(), DOWN * 0.5 + RIGHT * 3.5, color="#FF9F00", stroke_width=4)
        
        # Categories
        cat1_box = Rectangle(width=4, height=1.2, color="#00F0FF", stroke_width=3).shift(DOWN * 1.5 + LEFT * 3.5)
        cat1_label = Text("Parabolic\nReflector", font_size=30, color="#FFFFFF")
        cat1 = VGroup(cat1_box, cat1_label.move_to(cat1_box))
        
        cat2_box = Rectangle(width=4, height=1.2, color="#FF0055", stroke_width=3).shift(DOWN * 1.5 + RIGHT * 3.5)
        cat2_label = Text("Phased\nArray", font_size=30, color="#FFFFFF")
        cat2 = VGroup(cat2_box, cat2_label.move_to(cat2_box))
        
        note = Text("We'll explore 4 major types in detail", font_size=28, color="#FF9F00").to_edge(DOWN)
        
        self.play(Write(title), run_time=2.5)
        self.wait(2)
        self.play(Create(main_group), run_time=2.5)
        self.wait(2)
        self.play(Create(line_left), Create(line_right), run_time=2)
        self.wait(1.5)
        self.play(FadeIn(cat1, shift=DOWN*0.5), run_time=2)
        self.wait(1)
        self.play(FadeIn(cat2, shift=DOWN*0.5), run_time=2)
        self.wait(2)
        self.play(Write(note), run_time=2.5)
        self.wait(3)

# ============================================================================
# PART 4: TYPE 1 - PARABOLIC REFLECTOR ANTENNA (16-23s)
# ============================================================================
class Part4(ThreeDScene):
    def construct(self):
        title = Text("Type 1: Parabolic Reflector Antenna", font_size=48, color="#00F0FF")
        title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        
        # 3D parabolic dish
        dish = Surface(
            lambda u, v: np.array([
                2.5 * np.cos(u) * v,
                2.5 * np.sin(u) * v,
                -1.2 * v**2
            ]),
            u_range=[0, TAU],
            v_range=[0, 1.2],
            resolution=(32, 16)
        )
        dish.set_color("#00F0FF")
        dish.set_opacity(0.85)
        dish.rotate(PI/2, axis=RIGHT)
        
        # Feed point at focus
        feed = Sphere(radius=0.15, resolution=(12, 12))
        feed.set_color("#FF9F00")
        feed.shift(OUT * 1.8)
        
        # Support structure
        support = Cylinder(radius=0.05, height=1.8, resolution=(8, 2))
        support.set_color("#FFFFFF")
        support.shift(OUT * 0.9)
        
        # Beam direction arrows
        beam_arrows = VGroup(*[
            Arrow3D(start=ORIGIN, end=IN*3, color="#FF0055", thickness=0.02).shift(OUT*0.2 + RIGHT*x + UP*y)
            for x in np.linspace(-0.5, 0.5, 3)
            for y in np.linspace(-0.5, 0.5, 3)
        ])
        
        self.set_camera_orientation(phi=70*DEGREES, theta=-45*DEGREES, distance=8)
        self.play(Write(title), run_time=2)
        self.wait(2)
        self.play(Create(dish), run_time=3.5)
        self.wait(2)
        self.play(FadeIn(support), GrowFromCenter(feed), run_time=2.5)
        self.wait(2)
        self.play(LaggedStart(*[Create(arr) for arr in beam_arrows], lag_ratio=0.1), run_time=3)
        self.wait(1.5)
        self.play(Rotate(dish, angle=PI/6, axis=UP, run_time=3), 
                  Rotate(feed, angle=PI/6, axis=UP, run_time=3),
                  Rotate(support, angle=PI/6, axis=UP, run_time=3),
                  Rotate(beam_arrows, angle=PI/6, axis=UP, run_time=3))
        self.wait(3)

# ============================================================================
# PART 5: PARABOLIC REFLECTOR - FOCUSING PRINCIPLE (17-24s)
# ============================================================================
class Part5(Scene):
    def construct(self):
        title = Text("Parabolic Focusing Principle", font_size=50, color="#FFFFFF")
        title.to_edge(UP)
        
        # 2D cross-section of parabola
        axes = Axes(x_range=[-3, 3], y_range=[0, 4], x_length=8, y_length=5,
                   axis_config={"color": "#1E2A45", "stroke_width": 2}).shift(DOWN*0.5)
        
        parabola = axes.plot(lambda x: 0.5 * x**2, color="#00F0FF", stroke_width=5)
        
        # Focus point
        focus = Dot(axes.c2p(0, 0.5), color="#FF9F00", radius=0.12)
        focus_label = Text("Focus (Feed)", font_size=28, color="#FF9F00").next_to(focus, RIGHT)
        
        # Incoming parallel rays
        rays = VGroup(*[
            Arrow(axes.c2p(x, 4), axes.c2p(x, 0.5*x**2), color="#FF0055", 
                 stroke_width=4, max_tip_length_to_length_ratio=0.15)
            for x in np.linspace(-2.5, 2.5, 7)
        ])
        
        # Reflected rays converging to focus
        reflected = VGroup()
        for x in np.linspace(-2.5, 2.5, 7):
            y_point = 0.5 * x**2
            reflected.add(Arrow(axes.c2p(x, y_point), axes.c2p(0, 0.5), 
                               color="#00F0FF", stroke_width=4, max_tip_length_to_length_ratio=0.2))
        
        explanation = Text("All rays converge at the focal point,\nmaximizing signal strength", 
                          font_size=30, color="#FFFFFF").to_edge(DOWN)
        
        self.play(Write(title), run_time=2)
        self.wait(2)
        self.play(Create(axes), Create(parabola), run_time=3)
        self.wait(2)
        self.play(FadeIn(focus, scale=0.5), Write(focus_label), run_time=2.5)
        self.wait(2)
        self.play(LaggedStart(*[GrowArrow(r) for r in rays], lag_ratio=0.15), run_time=3.5)
        self.wait(2)
        self.play(LaggedStart(*[GrowArrow(r) for r in reflected], lag_ratio=0.15), run_time=3.5)
        self.wait(2)
        self.play(Write(explanation), run_time=2.5)
        self.wait(3)

# ============================================================================
# PART 6: TYPE 2 - PHASED ARRAY ANTENNA INTRODUCTION (15-22s)
# ============================================================================
class Part6(Scene):
    def construct(self):
        title = Text("Type 2: Phased Array Antenna", font_size=50, color="#FF0055")
        title.to_edge(UP)
        
        # Array of antenna elements
        elements = VGroup(*[
            VGroup(
                Rectangle(width=0.3, height=0.8, color="#00F0FF", fill_opacity=0.7, stroke_width=3),
                Line(ORIGIN, DOWN*0.5, color="#FFFFFF", stroke_width=2).shift(DOWN*0.65)
            ).shift(RIGHT * x)
            for x in np.linspace(-5, 5, 11)
        ])
        elements.shift(UP*0.5)
        
        # Ground plane
        ground = Line(LEFT*6, RIGHT*6, color="#1E2A45", stroke_width=4).shift(DOWN*0.3)
        
        # Phase indicators
        phase_dots = VGroup(*[
            Dot(color="#FF9F00", radius=0.08).move_to(elem[0].get_top() + UP*0.3)
            for elem in elements
        ])
        
        # Beam pattern
        beam = VGroup(*[
            Arrow(elem[0].get_top(), elem[0].get_top() + UP*2 + RIGHT*0.5*i, 
                 color="#FF0055", stroke_width=3, max_tip_length_to_length_ratio=0.15)
            for i, elem in enumerate(elements)
        ])
        
        desc = Text("Electronic beam steering without mechanical movement", 
                   font_size=32, color="#FFFFFF").to_edge(DOWN)
        
        self.play(Write(title), run_time=2)
        self.wait(2)
        self.play(Create(ground), run_time=1.5)
        self.play(LaggedStart(*[FadeIn(elem, shift=DOWN*0.3) for elem in elements], lag_ratio=0.08), run_time=3)
        self.wait(2)
        self.play(LaggedStart(*[GrowFromCenter(dot) for dot in phase_dots], lag_ratio=0.08), run_time=2.5)
        self.wait(2)
        self.play(LaggedStart(*[GrowArrow(b) for b in beam], lag_ratio=0.1), run_time=3.5)
        self.wait(2)
        self.play(Write(desc), run_time=2.5)
        self.wait(3)

# ============================================================================
# PART 7: PHASED ARRAY - BEAM STEERING MECHANISM (18-25s)
# ============================================================================
class Part7(Scene):
    def construct(self):
        title = Text("Electronic Beam Steering", font_size=48, color="#00F0FF")
        title.to_edge(UP)
        
        # Array elements with phase control
        array = VGroup(*[
            Rectangle(width=0.4, height=1, color="#00F0FF", fill_opacity=0.6, stroke_width=3).shift(RIGHT*x)
            for x in np.linspace(-4, 4, 9)
        ])
        array.shift(UP*1)
        
        # Phase shift values
        phase_labels = VGroup(*[
            Text(f"{i*15}°", font_size=24, color="#FF9F00").next_to(elem, DOWN, buff=0.3)
            for i, elem in enumerate(array)
        ])
        
        # Initial beam (straight up)
        beam1 = VGroup(*[
            Arrow(elem.get_top(), elem.get_top() + UP*2.5, color="#FF0055", stroke_width=4)
            for elem in array
        ])
        
        # Steered beam (angled)
        beam2 = VGroup(*[
            Arrow(elem.get_top(), elem.get_top() + UP*2.5 + RIGHT*(0.3*i), 
                 color="#00F0FF", stroke_width=4)
            for i, elem in enumerate(array)
        ])
        
        label1 = Text("0° Phase Shift → Straight Beam", font_size=30, color="#FF0055").to_edge(DOWN, buff=1.5)
        label2 = Text("Progressive Phase → Steered Beam", font_size=30, color="#00F0FF").to_edge(DOWN, buff=1.5)
        
        self.play(Write(title), run_time=2)
        self.wait(2)
        self.play(LaggedStart(*[FadeIn(elem, scale=0.8) for elem in array], lag_ratio=0.1), run_time=3)
        self.wait(2)
        self.play(LaggedStart(*[GrowArrow(b) for b in beam1], lag_ratio=0.1), Write(label1), run_time=3)
        self.wait(3)
        self.play(
            Transform(beam1, beam2),
            Transform(label1, label2),
            LaggedStart(*[Write(lbl) for lbl in phase_labels], lag_ratio=0.1),
            run_time=4
        )
        self.wait(3)
        self.play(
            Transform(beam1, VGroup(*[
                Arrow(elem.get_top(), elem.get_top() + UP*2.5 + LEFT*(0.3*i), 
                     color="#FF9F00", stroke_width=4)
                for i, elem in enumerate(array)
            ])),
            run_time=3.5
        )
        self.wait(3)

# ============================================================================
# PART 8: TYPE 3 - SLOT ARRAY ANTENNA (16-23s)
# ============================================================================
class Part8(ThreeDScene):
    def construct(self):
        title = Text("Type 3: Slot Array Antenna", font_size=50, color="#00F0FF")
        title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        
        # Waveguide with slots
        waveguide = Prism(dimensions=[0.6, 0.6, 5], fill_color="#1E2A45", fill_opacity=0.9, stroke_color="#00F0FF", stroke_width=2)
        
        # Slots cut into waveguide
        slots = VGroup(*[
            Prism(dimensions=[0.1, 0.7, 0.3], fill_color="#FF0055", fill_opacity=0.95).shift(UP*y)
            for y in np.linspace(-2, 2, 9)
        ])
        
        # Radiation pattern from slots
        radiation = VGroup(*[
            VGroup(*[
                Arrow3D(start=UP*y, end=UP*y + OUT*1.5 + RIGHT*x*0.4, 
                       color="#FF9F00", thickness=0.015)
                for x in [-1, 0, 1]
            ])
            for y in np.linspace(-2, 2, 9)
        ])
        
        explanation = Text("Slots radiate electromagnetic waves\nalong the waveguide",font_size=30, color="#FFFFFF")
        explanation.to_corner(DL)
        self.add_fixed_in_frame_mobjects(explanation)
        
        self.set_camera_orientation(phi=70*DEGREES, theta=-60*DEGREES, distance=10)
        
        self.play(Write(title), run_time=2)
        self.wait(2)
        self.play(FadeIn(waveguide, scale=0.9), run_time=3)
        self.wait(2)
        self.play(LaggedStart(*[FadeIn(slot, shift=OUT*0.2) for slot in slots], lag_ratio=0.15), run_time=3.5)
        self.wait(2)
        self.play(
            LaggedStart(*[
                LaggedStart(*[Create(arr) for arr in rad_group], lag_ratio=0.1)
                for rad_group in radiation
            ], lag_ratio=0.2),
            run_time=4
        )
        self.wait(2)
        self.play(Write(explanation), run_time=2.5)
        self.wait(3)

# ============================================================================
# PART 9: TYPE 4 - HORN ANTENNA (15-22s)
# ============================================================================
class Part9(ThreeDScene):
    def construct(self):
        title = Text("Type 4: Horn Antenna", font_size=52, color="#FF9F00")
        title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        
        # Waveguide input
        waveguide = Prism(dimensions=[0.4, 0.4, 2], fill_color="#1E2A45", fill_opacity=0.9, stroke_color="#00F0FF", stroke_width=2)
        waveguide.shift(IN*2)
        
        # Horn flare (pyramidal)
        horn_points = [
            [-0.2, -0.2, -1],
            [0.2, -0.2, -1],
            [0.2, 0.2, -1],
            [-0.2, 0.2, -1],
            [-1.2, -1.2, 1],
            [1.2, -1.2, 1],
            [1.2, 1.2, 1],
            [-1.2, 1.2, 1]
        ]
        
        # Create horn as surface approximation
        horn = VGroup()
        for i in range(4):
            j = (i + 1) % 4
            face = Polygon(
                horn_points[i], horn_points[j], horn_points[j+4], horn_points[i+4],
                fill_color="#00F0FF", fill_opacity=0.6, stroke_color="#00F0FF", stroke_width=3
            )
            horn.add(face)
        
        # Radiating beam
        beam = VGroup(*[
            Arrow3D(start=[0, 0, 1], end=[x*2, y*2, 4], color="#FF0055", thickness=0.02)
            for x in np.linspace(-0.8, 0.8, 5)
            for y in np.linspace(-0.8, 0.8, 5)
        ])
        
        desc = Text("Wide bandwidth, directional radiation", font_size=32, color="#FFFFFF")
        desc.to_corner(DL)
        self.add_fixed_in_frame_mobjects(desc)
        
        self.set_camera_orientation(phi=65*DEGREES, theta=-50*DEGREES, distance=9)
        
        self.play(Write(title), run_time=2)
        self.wait(2)
        self.play(FadeIn(waveguide, scale=0.8), run_time=2.5)
        self.wait(2)
        self.play(LaggedStart(*[FadeIn(face, shift=OUT*0.3) for face in horn], lag_ratio=0.2), run_time=3.5)
        self.wait(2)
        self.play(LaggedStart(*[Create(arr) for arr in beam], lag_ratio=0.02), run_time=4)
        self.wait(2)
        self.play(Write(desc), run_time=2.5)
        self.wait(3)

# ============================================================================
# PART 10: BEAM PATTERN COMPARISON (18-25s)
# ============================================================================
class Part10(Scene):
    # ── yardımcı: bir görsel + çerçeve + label grubu yaratır ──────────────
    def _make_card(self, path: str, label_text: str, frame_color: str, x_pos: float):
        # ── görsel ──
        img = ImageMobject(path)
        img.set_height(2.2)                       # sabit yükseklik
        img.set_width(2.6)                        # sabit genişlik (stretch)
        img.move_to([x_pos, 0.55, 0])

        # ── parlak çerçeve ──
        w, h = 2.85, 2.45                        # çerçeve boyutları (görsel etrafında biraz boşluk)
        frame = RoundedRectangle(
            width=w, height=h,
            corner_radius=0.12,
            stroke_color=frame_color,
            stroke_width=4,
            fill_color=frame_color,
            fill_opacity=0.06
        ).move_to(img.get_center())

        # ── alt label ──
        label = Text(label_text, font_size=30, color=frame_color, weight=BOLD)
        label.next_to(frame, DOWN, buff=0.25)

        return img, frame, label

    # ── yardımcı: beam-pattern çizgisi (küçük fan) ──────────────────────
    def _make_beam(self, center_point, half_angle: float, length: float, color: str, n_rays: int = 11):
        rays = VGroup()
        for a in np.linspace(-half_angle, half_angle, n_rays):
            end = center_point + length * np.array([np.sin(a), -np.cos(a), 0])   # aşağı yönlü fan
            rays.add(Line(center_point, end, color=color, stroke_width=2.5))
        return rays

    # ── construct ────────────────────────────────────────────────────────
    def construct(self):
        # ════════════ BAŞLIK ════════════
        title = Text("Antenna Beam Pattern Comparison", font_size=46, color="#FFFFFF", weight=BOLD)
        title.to_edge(UP, buff=0.35)

        # ════════════ KART VERILERI  (yol, label, çerçeve rengi, x-konum) ════
        cards_data = [
            ("parabolic.jpeg", "Parabolic\nReflector", "#00F0FF", -4.35),
            ("phased.jpeg",    "Phased\nArray",        "#FF0055", -1.45),
            ("slot.jpeg",      "Slot\nArray",          "#00F0FF",  1.45),
            ("horn.jpeg",      "Horn\nAntenna",        "#FF9F00",  4.35),
        ]

        # beam parametreleri  (half_angle_rad, renk)
        beam_params = [
            (PI / 18,  "#00F0FF"),   # Parabolic  → çok dar
            (PI / 12,  "#FF0055"),   # Phased     → dar
            (PI / 7,   "#00F0FF"),   # Slot       → orta
            (PI / 5,   "#FF9F00"),   # Horn       → geniş
        ]

        # ════════════ BAŞLIĞI ÇIZ ════════════
        self.play(Write(title), run_time=2.2)
        self.wait(1.8)

        # ════════════ HER KART İÇİN: çerçeve → görsel → label → beam ════
        all_mobjects = []                          # temizlik için

        for idx, (path, lbl, color, x) in enumerate(cards_data):
            img, frame, label = self._make_card(path, lbl, color, x)

            # --- çerçeve + görsel ---
            self.play(
                FadeIn(frame, scale=0.92),
                run_time=1.4
            )
            self.play(
                FadeIn(img, scale=0.95),
                run_time=1.6
            )
            self.wait(0.6)

            # --- label ---
            self.play(Write(label), run_time=1.2)
            self.wait(0.4)

            # --- beam pattern (label'ın altında) ---
            half_ang, beam_color = beam_params[idx]
            beam_origin = label.get_bottom() + DOWN * 0.45
            beam = self._make_beam(beam_origin, half_ang, length=0.85, color=beam_color, n_rays=13)

            self.play(
                LaggedStart(*[Create(ray) for ray in beam], lag_ratio=0.06),
                run_time=1.4
            )
            self.wait(0.8)

            all_mobjects.extend([img, frame, label, beam])

        # ════════════ SONRAKI BEKLE ════════════
        self.wait(2.5)

        # ════════════ ALT NOT ════════════
        note = Text(
            "Beam width determines angular resolution and detection range",
            font_size=28, color="#FFFFFF"
        ).to_edge(DOWN, buff=0.45)

        self.play(Write(note), run_time=2.8)
        self.wait(3.2)

# ============================================================================
# PART 11: GAIN AND DIRECTIVITY CONCEPTS (17-24s)
# ============================================================================
class Part11(Scene):
    def construct(self):
        title = Text("Antenna Gain & Directivity", font_size=50, color="#00F0FF")
        title.to_edge(UP)
        
        # Isotropic radiator (omnidirectional)
        iso_label = Text("Isotropic\nRadiator", font_size=32, color="#1E2A45").shift(LEFT*4 + UP*2)
        iso_circle = Circle(radius=1.5, color="#1E2A45", stroke_width=4).shift(LEFT*4)
        iso_center = Dot(iso_circle.get_center(), color="#FFFFFF", radius=0.1)
        
        # Directional antenna
        dir_label = Text("Directional\nAntenna", font_size=32, color="#FF0055").shift(RIGHT*4 + UP*2)
        dir_center = Dot(color="#FFFFFF", radius=0.1).shift(RIGHT*4)
        
        # Elongated pattern showing gain
        dir_pattern = Ellipse(width=3.5, height=1.2, color="#FF0055", stroke_width=5).shift(RIGHT*4)
        dir_pattern.rotate(PI/2)
        
        # Gain formula
        gain_formula = MathTex(
            r"G = \frac{P_{directional}}{P_{isotropic}}",
            font_size=44,
            color="#FF9F00"
        ).shift(DOWN*1.5)
        
        explanation = Text("Directivity focuses power in specific directions", 
                          font_size=30, color="#FFFFFF").to_edge(DOWN)
        
        self.play(Write(title), run_time=2)
        self.wait(2)
        self.play(Write(iso_label), FadeIn(iso_center), run_time=2)
        self.play(Create(iso_circle), run_time=2.5)
        self.wait(2)
        self.play(Write(dir_label), FadeIn(dir_center), run_time=2)
        self.play(Create(dir_pattern), run_time=3)
        self.wait(2)
        self.play(Write(gain_formula), run_time=3)
        self.wait(2)
        self.play(Write(explanation), run_time=2.5)
        self.wait(3)

# ============================================================================
# PART 12: POLARIZATION TYPES (16-23s)
# ============================================================================
class Part12(ThreeDScene):
    def construct(self):
        title = Text("Signal Polarization", font_size=52, color="#FFFFFF")
        title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        
        # Linear polarization (vertical)
        linear_wave = ParametricFunction(
            lambda t: np.array([t, 0, 0.5*np.sin(2*PI*t)]),
            t_range=[0, 3],
            color="#00F0FF",
            stroke_width=6
        ).shift(LEFT*2)
        linear_label = Text("Linear\nPolarization", font_size=28, color="#00F0FF")
        linear_label.shift(LEFT*2 + DOWN*2)
        self.add_fixed_in_frame_mobjects(linear_label)
        
        # Circular polarization
        circular_wave = ParametricFunction(
            lambda t: np.array([t, 0.5*np.sin(2*PI*t), 0.5*np.cos(2*PI*t)]),
            t_range=[0, 3],
            color="#FF0055",
            stroke_width=6
        ).shift(RIGHT*2)
        circular_label = Text("Circular\nPolarization", font_size=28, color="#FF0055")
        circular_label.shift(RIGHT*2 + DOWN*2)
        self.add_fixed_in_frame_mobjects(circular_label)
        
        # Propagation direction arrows
        arrow_lin = Arrow3D(start=LEFT*2 + IN*0.5, end=LEFT*2 + OUT*0.5, color="#FFFFFF", thickness=0.02)
        arrow_circ = Arrow3D(start=RIGHT*2 + IN*0.5, end=RIGHT*2 + OUT*0.5, color="#FFFFFF", thickness=0.02)
        
        self.set_camera_orientation(phi=70*DEGREES, theta=-45*DEGREES, distance=10)
        
        self.play(Write(title), run_time=2)
        self.wait(2)
        self.play(Write(linear_label), run_time=2)
        self.play(Create(linear_wave), Create(arrow_lin), run_time=4)
        self.wait(2)
        self.play(Write(circular_label), run_time=2)
        self.play(Create(circular_wave), Create(arrow_circ), run_time=4)
        self.wait(3)
        self.play(
            Rotate(linear_wave, angle=TAU, axis=RIGHT, run_time=3),
            Rotate(circular_wave, angle=TAU, axis=RIGHT, run_time=3)
        )
        self.wait(3)

# ============================================================================
# PART 13: RADAR RANGE EQUATION (18-25s)
# ============================================================================
class Part13(Scene):
    def construct(self):
        title = Text("Radar Range Equation", font_size=52, color="#00F0FF")
        title.to_edge(UP)
        
        # Main equation
        equation = MathTex(
            r"R_{max} = \left(\frac{P_t G^2 \lambda^2 \sigma}{(4\pi)^3 P_{min}}\right)^{1/4}",
            font_size=52,
            color="#FFFFFF"
        ).shift(UP*1.5)
        
        # Parameter definitions
        params = VGroup(
            MathTex(r"P_t", r"\text{ = Transmit Power}", font_size=36, color="#FF9F00"),
            MathTex(r"G", r"\text{ = Antenna Gain}", font_size=36, color="#FF9F00"),
            MathTex(r"\lambda", r"\text{ = Wavelength}", font_size=36, color="#FF9F00"),
            MathTex(r"\sigma", r"\text{ = Target Cross-section}", font_size=36, color="#FF9F00"),
            MathTex(r"P_{min}", r"\text{ = Minimum Detectable Power}", font_size=36, color="#FF9F00")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(DOWN*1.5)
        
        note = Text("Antenna gain directly impacts maximum range", 
                   font_size=30, color="#00F0FF").to_edge(DOWN)
        
        self.play(Write(title), run_time=2)
        self.wait(2)
        self.play(Write(equation), run_time=4)
        self.wait(3)
        self.play(LaggedStart(*[FadeIn(param, shift=RIGHT*0.3) for param in params], lag_ratio=0.4), run_time=5)
        self.wait(3)
        self.play(Write(note), run_time=2.5)
        self.wait(3)

# ============================================================================
# PART 14: FREQUENCY BANDS AND ANTENNA SELECTION (17-24s)
# ============================================================================
class Part14(Scene):
    def construct(self):
        title = Text("Frequency Bands & Antenna Types", font_size=48, color="#FFFFFF")
        title.to_edge(UP)
        
        # Frequency spectrum
        spectrum = NumberLine(
            x_range=[0, 100, 10],
            length=11,
            include_numbers=False,
            color="#1E2A45",
            stroke_width=4
        ).shift(UP*1.5)
        
        # Band markers
        bands = VGroup(
            VGroup(
                Line(UP*0.3, DOWN*0.3, color="#00F0FF", stroke_width=4).move_to(spectrum.n2p(10)),
                Text("L-band\n1-2 GHz", font_size=22, color="#00F0FF").next_to(spectrum.n2p(10), DOWN, buff=0.5)
            ),
            VGroup(
                Line(UP*0.3, DOWN*0.3, color="#FF0055", stroke_width=4).move_to(spectrum.n2p(30)),
                Text("S-band\n2-4 GHz", font_size=22, color="#FF0055").next_to(spectrum.n2p(30), DOWN, buff=0.5)
            ),
            VGroup(
                Line(UP*0.3, DOWN*0.3, color="#FF9F00", stroke_width=4).move_to(spectrum.n2p(50)),
                Text("C-band\n4-8 GHz", font_size=22, color="#FF9F00").next_to(spectrum.n2p(50), DOWN, buff=0.5)
            ),
            VGroup(
                Line(UP*0.3, DOWN*0.3, color="#00F0FF", stroke_width=4).move_to(spectrum.n2p(70)),
                Text("X-band\n8-12 GHz", font_size=22, color="#00F0FF").next_to(spectrum.n2p(70), DOWN, buff=0.5)
            ),
            VGroup(
                Line(UP*0.3, DOWN*0.3, color="#FF0055", stroke_width=4).move_to(spectrum.n2p(90)),
                Text("Ku-band\n12-18 GHz", font_size=22, color="#FF0055").next_to(spectrum.n2p(90), DOWN, buff=0.5)
            )
        )
        
        # Application notes
        apps = VGroup(
            Text("Lower frequency → Larger antennas, longer range", font_size=28, color="#FFFFFF"),
            Text("Higher frequency → Smaller antennas, better resolution", font_size=28, color="#FFFFFF")
        ).arrange(DOWN, buff=0.5).shift(DOWN*2)
        
        self.play(Write(title), run_time=2)
        self.wait(2)
        self.play(Create(spectrum), run_time=2.5)
        self.wait(2)
        self.play(LaggedStart(*[FadeIn(band, shift=UP*0.2) for band in bands], lag_ratio=0.3), run_time=4)
        self.wait(3)
        self.play(LaggedStart(*[Write(app) for app in apps], lag_ratio=0.5), run_time=4)
        self.wait(4)

# ============================================================================
# PART 15: ANTENNA EFFICIENCY AND LOSSES (16-23s)
# ============================================================================
class Part15(Scene):
    def construct(self):
        title = Text("Antenna Efficiency & Losses", font_size=50, color="#FF0055")
        title.to_edge(UP)
        
        # Power flow diagram
        input_power = Rectangle(width=2.5, height=1.2, color="#00F0FF", fill_opacity=0.7, stroke_width=3)
        input_label = Text("Input\nPower", font_size=28, color="#FFFFFF").move_to(input_power)
        input_group = VGroup(input_power, input_label).shift(LEFT*4.5 + UP*1.5)
        
        # Loss branches
        loss1_arrow = Arrow(input_power.get_right(), RIGHT*0.5 + UP*2.2, color="#FF9F00", stroke_width=4)
        loss1_box = Rectangle(width=2.2, height=0.8, color="#FF9F00", stroke_width=2).move_to(loss1_arrow.get_end() + RIGHT*1.2)
        loss1_text = Text("Ohmic Losses", font_size=24, color="#FFFFFF").move_to(loss1_box)
        
        loss2_arrow = Arrow(input_power.get_right(), RIGHT*0.5 + UP*0, color="#FF9F00", stroke_width=4)
        loss2_box = Rectangle(width=2.2, height=0.8, color="#FF9F00", stroke_width=2).move_to(loss2_arrow.get_end() + RIGHT*1.2)
        loss2_text = Text("Mismatch", font_size=24, color="#FFFFFF").move_to(loss2_box)
        
        loss3_arrow = Arrow(input_power.get_right(), RIGHT*0.5 + DOWN*1.5, color="#FF9F00", stroke_width=4)
        loss3_box = Rectangle(width=2.2, height=0.8, color="#FF9F00", stroke_width=2).move_to(loss3_arrow.get_end() + RIGHT*1.2)
        loss3_text = Text("Polarization", font_size=24, color="#FFFFFF").move_to(loss3_box)
        
        # Radiated power
        rad_arrow = Arrow(input_power.get_right(), RIGHT*3.3 + UP*1.5, color="#00F0FF", stroke_width=6)
        rad_box = Rectangle(width=2.5, height=1.2, color="#00F0FF", fill_opacity=0.7, stroke_width=3).shift(RIGHT*4.5 + UP*1.5)
        rad_label = Text("Radiated\nPower", font_size=28, color="#FFFFFF").move_to(rad_box)
        
        # Efficiency formula
        efficiency = MathTex(r"\eta = \frac{P_{radiated}}{P_{input}} \times 100\%", 
                            font_size=42, color="#FF9F00").shift(DOWN*3.0)
        
        self.play(Write(title), run_time=2)
        self.wait(2)
        self.play(FadeIn(input_group, scale=0.9), run_time=2)
        self.wait(2)
        self.play(GrowArrow(loss1_arrow), FadeIn(loss1_box), Write(loss1_text), run_time=2.5)
        self.wait(1.5)
        self.play(GrowArrow(loss2_arrow), FadeIn(loss2_box), Write(loss2_text), run_time=2.5)
        self.wait(1.5)
        self.play(GrowArrow(loss3_arrow), FadeIn(loss3_box), Write(loss3_text), run_time=2.5)
        self.wait(2)
        self.play(GrowArrow(rad_arrow), FadeIn(rad_box), Write(rad_label), run_time=3)
        self.wait(2)
        self.play(Write(efficiency), run_time=3)
        self.wait(3)

# ============================================================================
# PART 16: SIDELOBE LEVELS (17-24s)
# ============================================================================
class Part16(Scene):
    def construct(self):
        title = Text("Antenna Sidelobe Levels", font_size=50, color="#00F0FF")
        title.to_edge(UP)
        
        # Polar radiation pattern
        axes = PolarPlane(
            radius_max=3,
            size=6,
            azimuth_step=8,
            radius_step=0.5,
            background_line_style={"stroke_color": "#1E2A45", "stroke_width": 1}
        ).shift(LEFT*0.5)
        
        # Main lobe (high gain in forward direction)
        main_lobe_points = []
        for angle in np.linspace(0, TAU, 200):
            # Create pattern with main lobe and sidelobes
            if -PI/6 < angle < PI/6:
                r = 2.5 * np.cos(angle * 3)**2  # Main lobe
            else:
                r = 0.3 + 0.2 * np.abs(np.sin(angle * 4))  # Sidelobes
            x = r * np.cos(angle)
            y = r * np.sin(angle)
            main_lobe_points.append(axes.pr2pt(r, angle))
        
        pattern = Polygon(*main_lobe_points, color="#FF0055", fill_opacity=0.6, stroke_width=4)
        
        # Labels
        main_label = Text("Main Lobe", font_size=28, color="#FF0055").shift(UP*2 + LEFT*0.5)
        main_arrow = Arrow(main_label.get_bottom(), UP*1.2 + LEFT*0.5, color="#FF0055", stroke_width=3)
        
        side_label = Text("Sidelobes", font_size=24, color="#FF9F00").shift(RIGHT*3 + DOWN*1)
        side_arrow = Arrow(side_label.get_left(), RIGHT*1.5 + DOWN*0.5, color="#FF9F00", stroke_width=3)
        
        note = Text("Lower sidelobes reduce interference and clutter", 
                   font_size=30, color="#FFFFFF").to_edge(DOWN)
        
        self.play(Write(title), run_time=2)
        self.wait(2)
        self.play(Create(axes), run_time=3)
        self.wait(2)
        self.play(DrawBorderThenFill(pattern), run_time=4)
        self.wait(2)
        self.play(Write(main_label), GrowArrow(main_arrow), run_time=2.5)
        self.wait(2)
        self.play(Write(side_label), GrowArrow(side_arrow), run_time=2.5)
        self.wait(2)
        self.play(Write(note), run_time=2.5)
        self.wait(3)

# ============================================================================
# PART 17: SYNTHETIC APERTURE RADAR (SAR) (18-25s)
# ============================================================================
class Part17(Scene):
    def construct(self):
        title = Text("Synthetic Aperture Radar (SAR)", font_size=48, color="#00F0FF")
        title.to_edge(UP)
        
        # Moving platform (aircraft/satellite)
        platform = VGroup(
            Triangle(color="#FFFFFF", fill_opacity=0.8).scale(0.3).rotate(-PI/2),
            Rectangle(width=0.6, height=0.2, color="#00F0FF", fill_opacity=0.9)
        ).arrange(RIGHT, buff=0.1).shift(UP*2 + LEFT*4)
        
        # Flight path
        path = DashedLine(LEFT*4.5 + UP*2, RIGHT*4.5 + UP*2, color="#1E2A45", stroke_width=3)
        
        # Multiple antenna positions
        positions = [LEFT*3 + UP*2, LEFT*1 + UP*2, RIGHT*1 + UP*2, RIGHT*3 + UP*2]
        antenna_dots = VGroup(*[Dot(pos, color="#FF9F00", radius=0.1) for pos in positions])
        
        # Ground target
        target = Rectangle(width=1, height=0.6, color="#FF0055", fill_opacity=0.8).shift(DOWN*1)
        target_label = Text("Target", font_size=24, color="#FFFFFF").next_to(target, DOWN)
        
        # Signal paths from multiple positions
        signals = VGroup(*[
            VGroup(
                DashedLine(pos, target.get_top(), color="#00F0FF", stroke_width=2),
                DashedLine(target.get_top(), pos, color="#FF0055", stroke_width=2)
            )
            for pos in positions
        ])
        
        explanation = Text("Combines signals from multiple positions\nto create large synthetic aperture", 
                          font_size=28, color="#FFFFFF").to_edge(DOWN)
        
        self.play(Write(title), run_time=2)
        self.wait(2)
        self.play(Create(path), run_time=2)
        self.play(FadeIn(platform, shift=RIGHT*0.5), run_time=2)
        self.wait(1.5)
        
        # Animate platform movement and signal collection
        for i, pos in enumerate(positions):
            self.play(platform.animate.move_to(pos), run_time=1.5)
            self.play(FadeIn(antenna_dots[i]), run_time=0.5)
            if i == 1:
                self.play(FadeIn(target, scale=0.8), Write(target_label), run_time=2)
            self.play(Create(signals[i]), run_time=2)
            self.wait(1)
        
        self.wait(2)
        self.play(Write(explanation), run_time=3)
        self.wait(3)

# ============================================================================
# PART 18: MIMO RADAR SYSTEMS (17-24s)
# ============================================================================
class Part18(Scene):
    def construct(self):
        title = Text("MIMO Radar Systems", font_size=52, color="#FF0055")
        title.to_edge(UP)
        
        # Transmit array
        tx_label = Text("Transmit Array", font_size=32, color="#00F0FF").shift(LEFT*4.5 + UP*2)
        tx_array = VGroup(*[
            Rectangle(width=0.3, height=0.6, color="#00F0FF", fill_opacity=0.7, stroke_width=2).shift(LEFT*4.5 + UP*y)
            for y in [0.8, 0, -0.8]
        ])
        
        # Receive array
        rx_label = Text("Receive Array", font_size=32, color="#FF9F00").shift(RIGHT*4.5 + UP*2)
        rx_array = VGroup(*[
            Rectangle(width=0.3, height=0.6, color="#FF9F00", fill_opacity=0.7, stroke_width=2).shift(RIGHT*4.5 + UP*y)
            for y in [1.2, 0.4, -0.4, -1.2]
        ])
        
        # Target area
        target_zone = Circle(radius=0.8, color="#FF0055", fill_opacity=0.5, stroke_width=3)
        
        # Multiple signal paths (different colors for different TX-RX pairs)
        colors = ["#00F0FF", "#FF0055", "#FF9F00"]
        signal_paths = VGroup()
        
        for i, tx in enumerate(tx_array):
            for j, rx in enumerate(rx_array):
                path = VGroup(
                    Arrow(tx.get_right(), target_zone.point_at_angle(PI/2 + i*0.3), 
                         color=colors[i % 3], stroke_width=2, max_tip_length_to_length_ratio=0.1),
                    Arrow(target_zone.point_at_angle(-PI/2 - j*0.3), rx.get_left(), 
                         color=colors[i % 3], stroke_width=2, max_tip_length_to_length_ratio=0.1, buff=0)
                )
                signal_paths.add(path)
        
        advantage = Text("Multiple independent channels\nincrease resolution & SNR", 
                        font_size=30, color="#FFFFFF").to_edge(DOWN)
        
        self.play(Write(title), run_time=2)
        self.wait(2)
        self.play(Write(tx_label), LaggedStart(*[FadeIn(tx, shift=RIGHT*0.2) for tx in tx_array], lag_ratio=0.3), run_time=3)
        self.wait(2)
        self.play(Write(rx_label), LaggedStart(*[FadeIn(rx, shift=LEFT*0.2) for rx in rx_array], lag_ratio=0.3), run_time=3)
        self.wait(2)
        self.play(FadeIn(target_zone, scale=0.5), run_time=2)
        self.wait(2)
        self.play(LaggedStart(*[Create(path) for path in signal_paths], lag_ratio=0.15), run_time=5)
        self.wait(2)
        self.play(Write(advantage), run_time=2.5)
        self.wait(3)

# ============================================================================
# PART 19: SUMMARY - KEY TAKEAWAYS (16-23s)
# ============================================================================
class Part19(Scene):
    def construct(self):
        title = Text("Key Takeaways", font_size=56, color="#FF9F00", weight=BOLD)
        title.to_edge(UP)
        
        takeaways = VGroup(
            Text("1. Parabolic Reflector: High gain, mechanical steering", font_size=32, color="#00F0FF"),
            Text("2. Phased Array: Electronic steering, rapid scanning", font_size=32, color="#FF0055"),
            Text("3. Slot Array: Compact, integrated waveguide design", font_size=32, color="#00F0FF"),
            Text("4. Horn Antenna: Wideband, calibration standard", font_size=32, color="#FF9F00"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.7).shift(UP*0.3)
        
        # Decorative icons for each type
        icons = VGroup(
            Triangle(color="#00F0FF", fill_opacity=0.6).scale(0.3).next_to(takeaways[0], LEFT),
            Square(color="#FF0055", fill_opacity=0.6).scale(0.3).next_to(takeaways[1], LEFT),
            Rectangle(width=0.3, height=0.6, color="#00F0FF", fill_opacity=0.6).next_to(takeaways[2], LEFT),
            Polygon([0, 0, 0], [0.3, 0.3, 0], [0.3, -0.3, 0], color="#FF9F00", fill_opacity=0.6).next_to(takeaways[3], LEFT)
        )
        
        bottom_note = Text("Selection depends on: Frequency, Range, Scanning Speed, Cost", 
                          font_size=28, color="#FFFFFF").to_edge(DOWN)
        
        self.play(Write(title), run_time=2)
        self.wait(2)
        
        for i, (takeaway, icon) in enumerate(zip(takeaways, icons)):
            self.play(
                FadeIn(icon, scale=0.5),
                Write(takeaway),
                run_time=2.5
            )
            self.wait(1.5)
        
        self.wait(2)
        self.play(Write(bottom_note), run_time=3)
        self.wait(4)

# ============================================================================
# PART 20: OUTRO (13-20s)
# ============================================================================
class Part20(ThreeDScene):
    def construct(self):
        # Final title card
        title = Text("RADAR ANTENNA\nTYPES", font_size=84, weight=BOLD, color="#00F0FF")
        title.set_stroke("#FF0055", width=4, background=True)
        self.add_fixed_in_frame_mobjects(title)
        
        # 3D antenna models rotating
        parabolic = Surface(
            lambda u, v: np.array([1.5*np.cos(u)*v, 1.5*np.sin(u)*v, -0.8*v**2]),
            u_range=[0, TAU], v_range=[0, 1],
            resolution=(20, 10)
        ).set_color("#00F0FF").set_opacity(0.7).shift(LEFT*3)
        
        array = VGroup(*[
            Prism(dimensions=[0.2, 0.2, 0.5]).set_color("#FF0055").shift(RIGHT*3 + UP*y)
            for y in np.linspace(-1, 1, 5)
        ])
        
        subtitle = Text("Understanding Signal Propagation", font_size=36, color="#FFFFFF")
        subtitle.to_edge(DOWN, buff=1.5)
        self.add_fixed_in_frame_mobjects(subtitle)
        
        self.set_camera_orientation(phi=70*DEGREES, theta=-60*DEGREES, distance=10)
        
        self.play(FadeIn(title, scale=1.2), run_time=2.5)
        self.wait(2)
        self.play(Create(parabolic), run_time=3)
        self.play(LaggedStart(*[FadeIn(elem, shift=DOWN*0.2) for elem in array], lag_ratio=0.2), run_time=3)
        self.wait(2)
        self.play(Write(subtitle), run_time=2)
        self.wait(1.5)
        self.play(
            Rotate(parabolic, angle=TAU, axis=UP, run_time=4),
            Rotate(array, angle=TAU, axis=UP, run_time=4),
            run_time=4
        )
        self.wait(3)