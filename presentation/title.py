from manim import *
from manim_slides import Slide
from theme import *

class TitleCard(Slide):
    def construct(self):
        title = Text(
            "Numerical Methods\nfor solving differential equations", 
            font_size=56, 
            weight=BOLD,
            line_spacing=1.2 
        )
        
        subtitle = Text(
            "Comparison of Euler and Runge-Kutta Methods\nin theoretical cases and practical applications", 
            font_size=TEXT_SIZE_SUB, 
            color=COLORS["forward_euler"],
        )
        
        author = Text("Jakub Kowal, 2026", font_size=TEXT_SIZE_SUB, color=GRAY)
        
        titles_group = VGroup(title, subtitle).arrange(DOWN, buff=0.8)
        titles_group.move_to(ORIGIN) 
        
        author.to_edge(DOWN, buff=1.0)
        
        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.play(FadeIn(author, shift=UP))
        
        self.next_slide()
        self.play(
            FadeOut(title, shift=UP), 
            FadeOut(subtitle, shift=DOWN),
            FadeOut(author, shift=DOWN)
        )