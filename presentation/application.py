from manim import *
from manim_slides import Slide
import numpy as np

class ApplicationExample(Slide):
    def construct(self):
        # 1. Headline
        title = Title("Application to Hobby Rocket")
        self.play(Write(title))
        self.next_slide()

        # parameters
        eq1 = MathTex(r"M_{dry} = 1.0 \text{ kg}", font_size=36)
        eq2 = MathTex(r"M_{fuel_0} = 0.9 \text{ kg}", font_size=36)
        eq3 = MathTex(r"q = 0.3 \text{ kg/s}", font_size=36)
        eq4 = MathTex(r"t_{burn} = \frac{0.9}{0.3} = 3.0 \text{ s}", font_size=36)
        eq5 = MathTex(r"v_e = 300 \text{ m/s}", font_size=36)
        
        params = VGroup(eq1, eq2, eq3, eq4, eq5).arrange(DOWN, aligned_edge=LEFT)
        params.to_corner(UL).shift(DOWN * 1.5)
        
        self.play(FadeIn(params))
        self.next_slide()
        
        # formulas
        f1 = MathTex(r"M(t) = 1.0 + 0.9 \left(1 - \frac{t}{3}\right)^2", font_size=36)
        f2 = MathTex(r"M'(t) = -0.6 \left(1 - \frac{t}{3}\right)", font_size=36)
        f3 = MathTex(r"a(t) = -\frac{1}{M(t)} M'(t) v_e - g", font_size=36)
        f4 = MathTex(r"g = 9.81 \text{ m/s}^2", font_size=36)
        
        funcs = VGroup(f1, f2, f3, f4).arrange(DOWN, aligned_edge=LEFT)
        funcs.next_to(params, DOWN, buff=0.7)
        self.play(Write(funcs))
        self.next_slide()

        # graph section
        self.play(FadeOut(params), FadeOut(funcs))
        
        graph_title_1 = Tex("Comparison: Analytical vs Forward Euler", font_size=32, color=YELLOW)
        graph_title_2 = Tex("vs Backward Euler vs RK4 ($h=5.0$)", font_size=32, color=YELLOW)
        graph_title = VGroup(graph_title_1, graph_title_2).arrange(DOWN)
        graph_title.next_to(title, DOWN, buff=0.2)
        self.play(Write(graph_title))
        
        # flight up to 20 seconds, max speed around 155 m/s (162 - 3*9.81 = 133 roughly)
        ax = Axes(
            x_range=[0, 20, 2],
            y_range=[0, 320, 40],
            axis_config={"include_numbers": True},
            x_length=9,
            y_length=4.2
        )
        labels = ax.get_axis_labels(x_label="t (s)", y_label="v (m/s)")
        
        graph_group = VGroup(ax, labels).next_to(graph_title, DOWN, buff=0.2)
        
        def exact_m(t):
            if t > 3: return 1.0
            return 1.0 + 0.9 * (1 - t/3)**2

        def exact_v(t):
            # v(t) = v_e * ln(M(0)/M(t)) - g*t
            return 300 * np.log(1.9 / exact_m(t)) - 9.81 * t
            
        def f(t):
            if t >= 3: return -9.81
            num = 0.6 * (1 - t/3)
            den = 1.0 + 0.9 * (1 - t/3)**2
            return (num / den) * 300 - 9.81
            
        analytical_graph = ax.plot(exact_v, x_range=[0, 18], color=WHITE)
        analytical_label = MathTex("\text{Exact}", color=WHITE, font_size=28).next_to(ax.c2p(2, exact_v(2)), UP)
        
        self.play(Create(graph_group))
        self.play(Create(analytical_graph), Write(analytical_label))
        self.next_slide()

        # prepare arrays
        h = 5.0
        t_vals = np.arange(0, 24.0, h)
        
        # 1. Forward Euler Animation
        legend_fe = Dot(color=BLUE)
        legend_fe_text = Tex("Forward Euler", font_size=24).next_to(legend_fe, RIGHT)
        legend_fe_group = VGroup(legend_fe, legend_fe_text)
        legend_fe_group.move_to(ax.c2p(15, 280))
        self.play(FadeIn(legend_fe_group))
        
        fe_pts = [0]
        fe_dots = VGroup(Dot(ax.c2p(0, 0), color=BLUE))
        self.play(FadeIn(fe_dots))
        
        fe_lines = VGroup()
        for i in range(len(t_vals)-1):
            t_curr = t_vals[i]
            v_curr = fe_pts[-1]
            slope = f(t_curr)
            v_next = v_curr + h * slope
            fe_pts.append(v_next)
            
            fe_lines.add(Line(ax.c2p(t_curr, v_curr), ax.c2p(t_curr + h, v_next), color=BLUE))
            
            if v_next < 0:
                break
        
        self.play(Create(fe_lines), run_time=2)
        self.next_slide()

        # 2. Backward Euler Animation
        legend_be = Dot(color=RED)
        legend_be_text = Tex("Backward Euler", font_size=24).next_to(legend_be, RIGHT)
        legend_be_group = VGroup(legend_be, legend_be_text).next_to(legend_fe_group, DOWN, aligned_edge=LEFT)
        self.play(FadeIn(legend_be_group))
        
        be_pts = [0]
        be_dots = VGroup(Dot(ax.c2p(0, 0), color=RED))
        
        be_lines = VGroup()
        for i in range(len(t_vals)-1):
            t_curr = t_vals[i]
            v_curr = be_pts[-1]
            t_next = t_curr + h
            slope = f(t_next) 
            v_next = v_curr + h * slope
            be_pts.append(v_next)
            
            be_lines.add(Line(ax.c2p(t_curr, v_curr), ax.c2p(t_curr + h, v_next), color=RED))
            
            if v_next < 0:
                break
            
        self.play(Create(be_lines), run_time=2)
        self.next_slide()
        
        # 3. RK4 Animation
        legend_rk = Dot(color=GREEN)
        legend_rk_text = Tex("RK4", font_size=24).next_to(legend_rk, RIGHT)
        legend_rk_group = VGroup(legend_rk, legend_rk_text).next_to(legend_be_group, DOWN, aligned_edge=LEFT)
        self.play(FadeIn(legend_rk_group))
        
        rk_pts = [0]
        rk_dots = VGroup(Dot(ax.c2p(0, 0), color=GREEN))
        
        rk_lines = VGroup()
        # let's animate the first step with vectors as requested by the user previously but they also said "run all 4 vectors visible".
        # Let's animate all vectors for RK4
        
        for i in range(len(t_vals)-1):
            t_curr = t_vals[i]
            v_curr = rk_pts[-1]
            t_next = t_curr + h
            
            k1 = f(t_curr)
            k2 = f(t_curr + h/2)
            k3 = f(t_curr + h/2)
            k4 = f(t_curr + h)
            avg_slope = (k1 + 2*k2 + 2*k3 + k4) / 6
            
            v_next = v_curr + h * avg_slope
            rk_pts.append(v_next)
            
            # Draw RK4 vectors
            v1 = Arrow(ax.c2p(t_curr, v_curr), ax.c2p(t_curr + h, v_curr + h*k1), color=ORANGE, buff=0, max_tip_length_to_length_ratio=0.1)
            v2 = Arrow(ax.c2p(t_curr + h/2, v_curr + (h/2)*k1), ax.c2p(t_curr + h, v_curr + (h/2)*k1 + (h/2)*k2), color=TEAL, buff=0, max_tip_length_to_length_ratio=0.1)
            v3 = Arrow(ax.c2p(t_curr + h/2, v_curr + (h/2)*k2), ax.c2p(t_curr + h, v_curr + (h/2)*k2 + (h/2)*k3), color=PURPLE, buff=0, max_tip_length_to_length_ratio=0.1)
            v4 = Arrow(ax.c2p(t_curr + h, v_curr + h*k3), ax.c2p(t_curr + h + h, v_curr + h*k3 + h*k4), color=MAROON, buff=0, max_tip_length_to_length_ratio=0.1)
            
            self.play(GrowArrow(v1), run_time=0.15)
            self.play(GrowArrow(v2), run_time=0.15)
            self.play(GrowArrow(v3), run_time=0.15)
            self.play(GrowArrow(v4), run_time=0.15)
            
            final_v = Arrow(ax.c2p(t_curr, v_curr), ax.c2p(t_curr + h, v_next), color=GREEN, buff=0, max_tip_length_to_length_ratio=0.1)
            self.play(ReplacementTransform(VGroup(v1, v2, v3, v4), final_v), run_time=0.2)
            
            seg = Line(ax.c2p(t_curr, v_curr), ax.c2p(t_curr + h, v_next), color=GREEN)
            rk_lines.add(seg)
            self.play(Create(seg), FadeOut(final_v), run_time=0.1)

            if v_next < 0:
                break

        self.next_slide()
