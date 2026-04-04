from manim import *
from manim_slides import Slide

class RK4_Error_Landscape(Slide, MovingCameraScene):
    def construct(self):
        # title
        title = Text("Mapping the Landscape (log10 Error)", font_size=36).to_edge(UP)
        
        self.play(Write(title))
        self.next_slide()

        axes = Axes(
            x_range=[0, 1.0, 0.2],
            y_range=[0, 1.0, 0.2],
            x_length=5.5, 
            y_length=5.5,
            axis_config={
                "include_tip": False, 
                "font_size": 24,
                "color": WHITE
            },
            tips=False
        ).add_coordinates()
        
        x_label = MathTex("c_2", font_size=24).next_to(axes.x_axis, RIGHT)
        y_label = MathTex("c_3", font_size=24).next_to(axes.y_axis, UP)
        labels = VGroup(x_label, y_label)

        # heatmap setup
        heatmap_img = ImageMobject("rk4_heatmap.png")
        heatmap_img.stretch_to_fit_width(axes.x_axis.get_length())
        heatmap_img.stretch_to_fit_height(axes.y_axis.get_length())
        heatmap_img.move_to(axes.c2p(0.5, 0.5)) 

        landscape_group = Group(heatmap_img, axes, labels)
        landscape_group.move_to(ORIGIN).shift(DOWN * 0.3 + LEFT * 1.5)
        
        # colors
        turbo_colors = [
            "#23171b", "#4062e0", "#19c6e3", 
            "#25d05a", "#f5d13d", "#eb3c23", "#7a0403"
        ]
        
        grad_colors = color_gradient(turbo_colors, 100)
        gradient_rect = VGroup(*[
            Rectangle(width=0.4, height=5.5/100, stroke_width=0, fill_opacity=1, fill_color=c)
            for c in grad_colors
        ]).arrange(UP, buff=0)
        
        colorbar_axis = NumberLine(
            x_range=[-2, 4, 1],
            length=5.5,
            include_numbers=True,
            font_size=20,
            numbers_to_include=[-2, 0, 2, 4],
        )
        colorbar_axis.rotate(90 * DEGREES)
        for num in colorbar_axis.numbers:
            num.rotate(-90 * DEGREES)

        colorbar_axis.move_to(gradient_rect.get_center()).shift(RIGHT * 0.6)
        scale_title = Text("log10(Error)", font_size=20).next_to(gradient_rect, UP, buff=0.1)
        
        colorbar_group = VGroup(gradient_rect, colorbar_axis, scale_title)
        colorbar_group.next_to(landscape_group, RIGHT, buff=0.75)
        colorbar_group.match_y(axes)

        def hyperbola_func(x):
            return (4*x - 3) / (6*x - 4)

        # within bounds
        left_branch = axes.plot(hyperbola_func, x_range=[0, 0.5], color=RED)
        right_branch = axes.plot(hyperbola_func, x_range=[0.75, 1.0], color=RED)
        rk3_curve = VGroup(left_branch, right_branch)

        # label branch
        rk3_label = Text("RK3 residuals", font_size=15, color=RED).next_to(right_branch, UP, buff=0.1)
        rk3_group = VGroup(rk3_curve, rk3_label)

        std_pt = Dot(axes.c2p(0.5, 0.5), color=BLUE, radius=0.1)
        std_label = Text("Classic RK4", font_size=20, color=BLUE).next_to(std_pt, UP, buff=0.1)
        
        # kutta's method
        kutta_pt = Dot(axes.c2p(1/3, 2/3), color=GREEN, radius=0.08)
        kutta_label = Text("Kutta 3/8", font_size=15, color=GREEN).next_to(kutta_pt, UP, buff=0.1)
        kutta_sublabel = Text("Minimized error for the average ODE case.", font_size=12, color=GREEN, stroke_width=0.2, stroke_color=WHITE).next_to(kutta_pt, DOWN, buff=0.05)
        
        # ralston's
        ralston_pt = Dot(axes.c2p(0.4, 0.45), color=ORANGE, radius=0.08)
        ralston_label = Text("Ralston's", font_size=15, color=ORANGE).next_to(ralston_pt, LEFT, buff=0.1)
        ralston_sublabel = Text("Best for solving edge-case ODEs.", font_size=12, color=ORANGE, stroke_width=0.2, stroke_color=WHITE).next_to(ralston_pt, DOWN, buff=0.05)

        # show heatmap
        self.play(Create(axes), Write(labels))
        self.play(FadeIn(heatmap_img))
        self.play(FadeIn(colorbar_group))
        self.add(axes, labels) 
        self.next_slide()

        # plot points
        self.play(FadeIn(std_pt, scale=0.5), Write(std_label))
        self.play(
            FadeIn(kutta_pt, scale=0.5), Write(kutta_label),
            FadeIn(ralston_pt, scale=0.5), Write(ralston_label)
        )
        self.next_slide()
        
        self.play(Indicate(std_pt))
        self.next_slide()
        self.play(
            Indicate(kutta_pt), Indicate(ralston_pt)
        )
        self.next_slide()
        
        self.play(Indicate(kutta_pt), Write(kutta_sublabel))
        self.next_slide()
        
        self.play(FadeOut(kutta_sublabel),Indicate(ralston_pt), Write(ralston_sublabel))
        self.next_slide()
        
        # more landmarks
        self.play(FadeOut(ralston_sublabel), Write(rk3_group))
        self.next_slide()
        # cleanup
        self.play(FadeOut(title), FadeOut(axes), FadeOut(labels), FadeOut(heatmap_img), FadeOut(colorbar_group), FadeOut(std_pt), FadeOut(std_label), FadeOut(kutta_pt), FadeOut(kutta_label), FadeOut(ralston_pt), FadeOut(ralston_label), FadeOut(rk3_group))
