from manim import *
import numpy as np

# Configure for YouTube Shorts (Vertical 9:16)
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9.0
config.frame_height = 16.0

config.background_color = "#020B1F"

class Part10Short(Scene):
    # ── yardımcı: bir görsel + çerçeve + label grubu yaratır ──────────────
    def _make_card(self, path: str, label_text: str, frame_color: str, position: np.ndarray):
        # ── görsel (Scale reduced) ──
        img = ImageMobject(path)
        img.set_height(2.6)                       
        img.set_width(3.1)                        
        img.move_to(position + UP*0.5)            

        # ── parlak çerçeve (Compatible size) ──
        w, h = 3.3, 2.9                          
        frame = RoundedRectangle(
            width=w, height=h,
            corner_radius=0.15,
            stroke_color=frame_color,
            stroke_width=5,
            fill_color=frame_color,
            fill_opacity=0.08
        ).move_to(img.get_center())

        # ── alt label ──
        label = Text(label_text, font_size=32, color=frame_color, weight=BOLD)
        label.next_to(frame, DOWN, buff=0.20)

        return img, frame, label

    # ── yardımcı: beam-pattern çizgisi (küçük fan) ──────────────────────
    def _make_beam(self, center_point, half_angle: float, length: float, color: str, n_rays: int = 11):
        rays = VGroup()
        for a in np.linspace(-half_angle, half_angle, n_rays):
            end = center_point + length * np.array([np.sin(a), -np.cos(a), 0])   # aşağı yönlü fan
            rays.add(Line(center_point, end, color=color, stroke_width=3))
        return rays

    # ── construct ────────────────────────────────────────────────────────
    def construct(self):
        # ════════════ BAŞLIK ════════════
        title = Text("Antenna Beam\nPattern Comparison", font_size=48, color="#FFFFFF", weight=BOLD, line_spacing=1.2)
        title.to_edge(UP, buff=1.0)
        
        # ════════════ KONUMLAR (2x2 Grid) ════════════
        # Sol üst, Sağ üst, Sol alt, Sağ alt
        # Parabolic ve Phased Array aşağı indirildi (UP*3.8 -> UP*1.5)
        # Alt satır da çakışmayı önlemek için aşağı çekildi (DOWN*2.8 -> DOWN*3.9)
        positions = [
            LEFT*2.2 + UP*1.5,   # Parabolic
            RIGHT*2.2 + UP*1.5,  # Phased
            LEFT*2.2 + DOWN*3.9, # Slot
            RIGHT*2.2 + DOWN*3.9 # Horn
        ]

        # ════════════ KART VERILERI ════════════
        cards_data = [
            ("parabolic.jpeg", "Parabolic",    "#00F0FF"),
            ("phased.jpeg",    "Phased Array", "#FF0055"),
            ("slot.jpeg",      "Slot Array",   "#00F0FF"),
            ("horn.jpeg",      "Horn",         "#FF9F00"),
        ]

        # beam parametreleri  (half_angle_rad, renk)
        beam_params = [
            (PI / 18,  "#00F0FF"),   # Parabolic  → çok dar
            (PI / 12,  "#FF0055"),   # Phased     → dar
            (PI / 7,   "#00F0FF"),   # Slot       → orta
            (PI / 5,   "#FF9F00"),   # Horn       → geniş
        ]

        # ════════════ BAŞLIĞI ÇIZ ════════════
        self.play(Write(title), run_time=2.0)
        self.wait(1.0)

        # ════════════ KARTLARI OLUŞTUR VE GÖSTER ════════════
        for idx, ((path, lbl, color), pos) in enumerate(zip(cards_data, positions)):
            img, frame, label = self._make_card(path, lbl, color, pos)

            # Çerçeve ve Görsel
            self.play(
                FadeIn(frame, scale=0.9),
                FadeIn(img, scale=0.9),
                run_time=1.0
            )
            
            # Label
            self.play(Write(label), run_time=0.8)

            # Beam Pattern
            half_ang, beam_color = beam_params[idx]
            beam_origin = label.get_bottom() + DOWN * 0.2
            beam = self._make_beam(beam_origin, half_ang, length=0.75, color=beam_color, n_rays=13)

            self.play(
                LaggedStart(*[Create(ray) for ray in beam], lag_ratio=0.08),
                run_time=1.2
            )
            self.wait(0.5)

        # ════════════ ALT NOT ════════════


        self.wait(4)
