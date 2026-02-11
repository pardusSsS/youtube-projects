from manim import *
import numpy as np

# Vibrant Space Tech Color Palette
DEEP_NAVY = "#020B1F"
ELECTRIC_CYAN = "#00F0FF"
NEON_PINK = "#FF0055"
VIBRANT_ORANGE = "#FF9F00"
SUBTLE_NAVY = "#1E2A45"
SOFT_GREEN = "#00FF88"

# YouTube Shorts Configuration (9:16 aspect ratio)
config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 14.0
config.frame_width = 14.0 * (1080 / 1920)  # ~7.875
config.background_color = DEEP_NAVY


class DatabaseShort(Scene):
    """How Databases Work & Store Data (YouTube Shorts Version) - Educational"""
    
    def construct(self):
        # ========== PART 1: Hook Question ==========
        hook = Text("Where does your data\nactually go?", font_size=42, color=WHITE)
        hook.move_to(ORIGIN)
        
        question_mark = Text("🤔", font_size=80)
        question_mark.next_to(hook, DOWN, buff=0.5)
        
        self.play(Write(hook), run_time=1.2)
        self.play(FadeIn(question_mark, scale=0.5), run_time=0.6)
        self.wait(1.0)
        
        self.play(FadeOut(hook), FadeOut(question_mark), run_time=0.5)
        
        # ========== PART 2: Title ==========
        title = Text("DATABASE", font_size=56, color=ELECTRIC_CYAN, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        
        subtitle = Text("The Brain of Your App", font_size=26, color=WHITE)
        subtitle.next_to(title, DOWN, buff=0.2)
        
        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(subtitle, shift=UP), run_time=0.5)
        self.wait(0.5)
        
        # ========== PART 3: What is a Database? ==========
        definition_box = RoundedRectangle(
            width=7, height=1.8, corner_radius=0.2,
            stroke_color=ELECTRIC_CYAN, stroke_width=2,
            fill_color=SUBTLE_NAVY, fill_opacity=0.5
        )
        definition_box.move_to(UP * 0.5)
        
        definition = Text(
            "A database is an organized\ncollection of data stored\non a computer",
            font_size=24, color=WHITE, line_spacing=1.3
        )
        definition.move_to(definition_box.get_center())
        
        self.play(FadeIn(definition_box), run_time=0.4)
        self.play(Write(definition), run_time=1.5)
        self.wait(1.0)
        
        self.play(FadeOut(definition_box), FadeOut(definition), run_time=0.4)
        
        # ========== PART 4: Real World Example ==========
        example_title = Text("Think of it like...", font_size=28, color=NEON_PINK)
        example_title.next_to(subtitle, DOWN, buff=0.6)
        
        # Filing cabinet analogy
        cabinet = VGroup()
        cabinet_body = Rectangle(width=2.2, height=2.8, fill_color=SUBTLE_NAVY,
                                 fill_opacity=0.8, stroke_color=ELECTRIC_CYAN, stroke_width=2)
        
        # Drawer slots
        for i in range(3):
            drawer = Rectangle(width=1.8, height=0.7, fill_color=DEEP_NAVY,
                              fill_opacity=0.8, stroke_color=SOFT_GREEN, stroke_width=1)
            drawer.move_to(cabinet_body.get_center() + UP * (0.85 - i * 0.85))
            handle = Circle(radius=0.08, fill_color=VIBRANT_ORANGE, fill_opacity=1)
            handle.move_to(drawer.get_center())
            cabinet.add(drawer, handle)
        
        cabinet.add(cabinet_body)
        cabinet.move_to(LEFT * 2 + DOWN * 1.5)
        
        filing_label = Text("Filing Cabinet", font_size=18, color=WHITE)
        filing_label.next_to(cabinet, DOWN, buff=0.3)
        
        # Database icon
        db_body = Rectangle(width=2.2, height=1.6, fill_color=SUBTLE_NAVY,
                           fill_opacity=0.8, stroke_color=ELECTRIC_CYAN, stroke_width=3)
        db_top = Ellipse(width=2.2, height=0.5, fill_color=SUBTLE_NAVY,
                        fill_opacity=1, stroke_color=ELECTRIC_CYAN, stroke_width=3)
        db_bottom = Ellipse(width=2.2, height=0.5, fill_color=SUBTLE_NAVY,
                           fill_opacity=0.8, stroke_color=ELECTRIC_CYAN, stroke_width=3)
        db_top.move_to(db_body.get_top())
        db_bottom.move_to(db_body.get_bottom())
        
        database = VGroup(db_body, db_bottom, db_top)
        database.move_to(RIGHT * 2 + DOWN * 1.5)
        
        db_label = Text("Database", font_size=18, color=WHITE)
        db_label.next_to(database, DOWN, buff=0.3)
        
        # Equals sign
        equals = Text("=", font_size=48, color=VIBRANT_ORANGE)
        equals.move_to(DOWN * 1.5)
        
        self.play(FadeIn(example_title), run_time=0.5)
        self.play(DrawBorderThenFill(cabinet), FadeIn(filing_label), run_time=1.0)
        self.play(FadeIn(equals), run_time=0.4)
        self.play(DrawBorderThenFill(database), FadeIn(db_label), run_time=1.0)
        self.wait(1.0)
        
        # Clear for next section
        self.play(
            FadeOut(example_title), FadeOut(cabinet), FadeOut(filing_label),
            FadeOut(equals), FadeOut(database), FadeOut(db_label),
            run_time=0.5
        )
        
        # ========== PART 5: How Data is Organized ==========
        organize_title = Text("Data is Organized in TABLES", font_size=28, color=SOFT_GREEN)
        organize_title.next_to(subtitle, DOWN, buff=0.5)
        
        self.play(FadeIn(organize_title, shift=DOWN), run_time=0.6)
        
        # Create table header
        header_bg = Rectangle(width=6.5, height=0.55, fill_color=NEON_PINK,
                             fill_opacity=0.3, stroke_width=0)
        header_bg.move_to(DOWN * 0.3)
        
        headers = VGroup(
            Text("ID", font_size=18, color=NEON_PINK),
            Text("Name", font_size=18, color=NEON_PINK),
            Text("Email", font_size=18, color=NEON_PINK),
        ).arrange(RIGHT, buff=1.2)
        headers.move_to(header_bg.get_center())
        
        # Table rows with data
        data = [
            ("1", "Alice", "alice@mail.com"),
            ("2", "Bob", "bob@mail.com"),
            ("3", "Carol", "carol@mail.com"),
        ]
        
        rows = VGroup()
        for i, (id_val, name, email) in enumerate(data):
            row_bg = Rectangle(width=6.5, height=0.5, 
                              fill_color=SUBTLE_NAVY if i % 2 == 0 else DEEP_NAVY,
                              fill_opacity=0.5, stroke_width=0)
            row_content = VGroup(
                Text(id_val, font_size=16, color=ELECTRIC_CYAN),
                Text(name, font_size=16, color=WHITE),
                Text(email, font_size=14, color=VIBRANT_ORANGE),
            ).arrange(RIGHT, buff=0.8)
            row_content.move_to(row_bg.get_center())
            rows.add(VGroup(row_bg, row_content))
        
        rows.arrange(DOWN, buff=0.05)
        rows.next_to(header_bg, DOWN, buff=0.05)
        
        # Table border
        table_group = VGroup(header_bg, headers, rows)
        table_border = RoundedRectangle(
            width=table_group.width + 0.3, height=table_group.height + 0.3,
            corner_radius=0.1, stroke_color=SUBTLE_NAVY, stroke_width=2
        )
        table_border.move_to(table_group.get_center())
        
        self.play(FadeIn(table_border), run_time=0.3)
        self.play(FadeIn(header_bg), Write(headers), run_time=0.8)
        
        for row in rows:
            self.play(FadeIn(row, shift=LEFT), run_time=0.4)
        
        self.wait(0.8)
        
        # Highlight a Row
        row_highlight = SurroundingRectangle(rows[1], color=SOFT_GREEN, buff=0.1, stroke_width=4)
        row_text = Text("Row", font_size=24, color=SOFT_GREEN)
        # Position below the entire table
        row_text.next_to(table_border, DOWN, buff=0.5)
        # Shift slightly to match the row's horizontal center if needed, or just center it relative to table
        
        row_arrow = Arrow(
            row_text.get_top(), row_highlight.get_bottom(),
            color=SOFT_GREEN, stroke_width=4, buff=0.1
        )
        
        self.play(Create(row_highlight), run_time=0.5)
        self.play(GrowArrow(row_arrow), Write(row_text), run_time=0.5)
        self.wait(1.0)
        
        # Highlight a Column (Name column)
        # Create a group of all items in the second column to surround
        col_items = VGroup(headers[1])
        for row in rows:
            # row[1] is row_content, row[1][1] is the Name text
            col_items.add(row[1][1])
            
        col_highlight = SurroundingRectangle(col_items, color=ELECTRIC_CYAN, buff=0.15, stroke_width=4)
        col_text = Text("Column", font_size=24, color=ELECTRIC_CYAN)
        col_text.next_to(col_highlight, UP, buff=0.5)
        
        col_arrow = Arrow(
            col_text.get_bottom(), col_highlight.get_top(),
            color=ELECTRIC_CYAN, stroke_width=4, buff=0.1
        )
        
        self.play(FadeOut(row_highlight), FadeOut(row_text), FadeOut(row_arrow), run_time=0.3)
        self.play(Create(col_highlight), run_time=0.5)
        self.play(GrowArrow(col_arrow), Write(col_text), run_time=0.5)
        self.wait(1.0)
        
        # Clear
        self.play(
            FadeOut(organize_title), FadeOut(table_border), FadeOut(header_bg),
            FadeOut(headers), FadeOut(rows), 
            FadeOut(col_highlight), FadeOut(col_text), FadeOut(col_arrow),
            run_time=0.5
        )
        
        # ========== PART 6: CRUD Operations ==========
        crud_title = Text("4 Basic Operations", font_size=28, color=VIBRANT_ORANGE)
        crud_title.next_to(subtitle, DOWN, buff=0.5)
        
        self.play(FadeIn(crud_title), run_time=0.5)
        
        # CRUD boxes
        operations = [
            ("C", "CREATE", "Add new data", SOFT_GREEN),
            ("R", "READ", "Get data", ELECTRIC_CYAN),
            ("U", "UPDATE", "Change data", VIBRANT_ORANGE),
            ("D", "DELETE", "Remove data", NEON_PINK),
        ]
        
        crud_boxes = VGroup()
        for letter, name, desc, color in operations:
            box = RoundedRectangle(
                width=3.2, height=1.1, corner_radius=0.15,
                stroke_color=color, stroke_width=3,
                fill_color=color, fill_opacity=0.15
            )
            letter_text = Text(letter, font_size=32, color=color, weight=BOLD)
            name_text = Text(name, font_size=16, color=WHITE)
            desc_text = Text(desc, font_size=12, color=SUBTLE_NAVY)
            
            content = VGroup(letter_text, name_text, desc_text).arrange(DOWN, buff=0.08)
            content.move_to(box.get_center())
            crud_boxes.add(VGroup(box, content))
        
        # Arrange in 2x2 grid
        crud_grid = VGroup(
            VGroup(crud_boxes[0], crud_boxes[1]).arrange(RIGHT, buff=0.3),
            VGroup(crud_boxes[2], crud_boxes[3]).arrange(RIGHT, buff=0.3)
        ).arrange(DOWN, buff=0.3)
        crud_grid.move_to(DOWN * 1.2)
        
        for box in crud_boxes:
            self.play(FadeIn(box, scale=0.9), run_time=0.5)
        
        self.wait(1.2)
        
        # Clear
        self.play(FadeOut(crud_title), FadeOut(crud_grid), run_time=0.5)
        
        # ========== PART 7: Where is Data Stored? ==========
        storage_title = Text("Where is Data Stored?", font_size=28, color=ELECTRIC_CYAN)
        storage_title.next_to(subtitle, DOWN, buff=0.5)
        
        self.play(FadeIn(storage_title), run_time=0.5)
        
        # Hard drive icon
        hdd = VGroup()
        hdd_body = RoundedRectangle(width=2.5, height=1.5, corner_radius=0.2,
                                    fill_color=SUBTLE_NAVY, fill_opacity=0.8,
                                    stroke_color=ELECTRIC_CYAN, stroke_width=2)
        disk = Circle(radius=0.4, stroke_color=VIBRANT_ORANGE, stroke_width=2)
        disk.move_to(hdd_body.get_center() + LEFT * 0.3)
        center_dot = Circle(radius=0.08, fill_color=VIBRANT_ORANGE, fill_opacity=1)
        center_dot.move_to(disk.get_center())
        hdd.add(hdd_body, disk, center_dot)
        hdd.move_to(DOWN * 0.8)
        
        hdd_label = Text("Hard Drive / SSD", font_size=18, color=WHITE)
        hdd_label.next_to(hdd, DOWN, buff=0.3)
        
        # Data persistence note
        persist_note = VGroup(
            Text("💾 Data stays even when", font_size=18, color=SOFT_GREEN),
            Text("power is turned off!", font_size=18, color=SOFT_GREEN),
        ).arrange(DOWN, buff=0.1)
        persist_note.next_to(hdd_label, DOWN, buff=0.5)
        
        self.play(DrawBorderThenFill(hdd), FadeIn(hdd_label), run_time=1.0)
        self.play(FadeIn(persist_note, shift=UP), run_time=0.8)
        self.wait(1.0)
        
        # Clear
        self.play(
            FadeOut(storage_title), FadeOut(hdd), FadeOut(hdd_label), FadeOut(persist_note),
            run_time=0.5
        )
        
        # ========== PART 8: Summary ==========
        summary_title = Text("Key Takeaways", font_size=32, color=NEON_PINK)
        summary_title.next_to(subtitle, DOWN, buff=0.6)
        
        takeaways = VGroup(
            Text("✓ Databases organize data in tables", font_size=20, color=WHITE),
            Text("✓ Tables have columns and rows", font_size=20, color=WHITE),
            Text("✓ CRUD: Create, Read, Update, Delete", font_size=20, color=WHITE),
            Text("✓ Data is stored on disk permanently", font_size=20, color=WHITE),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        takeaways.move_to(DOWN * 0.8)
        
        self.play(FadeIn(summary_title), run_time=0.5)
        
        for takeaway in takeaways:
            self.play(FadeIn(takeaway, shift=RIGHT), run_time=0.5)
        
        self.wait(1.5)
        
        # Final highlight
        self.play(
            *[takeaway.animate.set_color(SOFT_GREEN) for takeaway in takeaways],
            run_time=0.5
        )
        self.play(
            *[takeaway.animate.set_color(WHITE) for takeaway in takeaways],
            run_time=0.5
        )
        
        self.wait(1.0)
