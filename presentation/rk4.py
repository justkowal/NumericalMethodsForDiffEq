from manim import *
from manim_slides import Slide
import numpy as np

class RungeKutta4(Slide):
    def construct(self):
        
        header = Text("Runge-Kutta 4th Order (RK4)", font_size=24)
        header.to_corner(UL)
        
        self.play(Write(header))
        self.next_slide()

        axes = Axes(
            x_range=[0, 6.5, 1],
            y_range=[0, 6.5, 1],
            x_length=8,
            y_length=5,
            axis_config={"include_numbers": True},
        ).shift(DOWN * 0.5 + LEFT * 1)
        
        axes_labels = axes.get_axis_labels(x_label="t", y_label="y(t)")
        self.play(Create(axes), Write(axes_labels))
        
        def exact_sol(t):
            return np.sin(t) + 0.5 * t + 1
            
        def deriv(t, y):
            return np.cos(t) + 0.5
            
        true_curve = axes.plot(exact_sol, x_range=[0, 5.5], color=BLUE)
        curve_label = MathTex("y(t)", color=BLUE).next_to(true_curve.get_end(), UP)
        
        t0 = 0
        y0 = exact_sol(t0)
        start_dot = Dot(axes.c2p(t0, y0), color=YELLOW)
        start_label = MathTex("(t_0, y_0)", font_size=24, color=YELLOW).next_to(start_dot, UL, buff=0.1)
        
        self.play(FadeIn(start_dot), Write(start_label))
        self.play(Create(true_curve), FadeIn(curve_label))
        self.next_slide()

        ode_text = MathTex(r"\frac{\mathrm{d} y}{\mathrm{d} t} = f(t,y) = \cos(t) + 0.5", font_size=28)
        ode_text.to_corner(UR)
        self.play(Write(ode_text))
        
        rk4_formula_1 = MathTex(r"k_1 = f(t_n, y_n)", font_size=20)
        rk4_formula_2 = MathTex(r"k_2 = f(t_n + \frac{\Delta t}{2}, y_n + \frac{\Delta t}{2} k_1)", font_size=20)
        rk4_formula_3 = MathTex(r"k_3 = f(t_n + \frac{\Delta t}{2}, y_n + \frac{\Delta t}{2} k_2)", font_size=20)
        rk4_formula_4 = MathTex(r"k_4 = f(t_n + \Delta t, y_n + \Delta t k_3)", font_size=20)
        rk4_formula_5 = MathTex(
            "y_{n+1} = y_n +", 
            "\\frac{\\Delta t}{6}", 
            "(k_1 +", 
            "2", 
            "k_2 +", 
            "2", 
            "k_3 + k_4)",
            font_size=20
        )
        
        formulas = VGroup(rk4_formula_1, rk4_formula_2, rk4_formula_3, rk4_formula_4, rk4_formula_5)
        formulas.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        formulas.next_to(ode_text, DOWN, buff=0.5).align_to(ode_text, RIGHT)
        
        self.play(Write(formulas))
        self.next_slide()

        dt = 1.0
        n_steps = 5
        
        t_current = t0
        y_current = y0
        current_dot = start_dot
        
        rk4_points = [axes.c2p(t_current, y_current)]
        rk4_mobjects = VGroup()
        
        for i in range(n_steps):
            is_slow = (i == 0)
            anim_run_time = 1.5 if is_slow else 0.4
            
            k1 = deriv(t_current, y_current)
            k2 = deriv(t_current + dt/2, y_current + dt/2 * k1)
            k3 = deriv(t_current + dt/2, y_current + dt/2 * k2)
            k4 = deriv(t_current + dt, y_current + dt * k3)
            
            y_next = y_current + dt/6 * (k1 + 2*k2 + 2*k3 + k4)
            t_next = t_current + dt
            
            next_dot = Dot(axes.c2p(t_next, y_next), color=GREEN)
            rk4_segment = Line(axes.c2p(t_current, y_current), axes.c2p(t_next, y_next), color=GREEN)
            
            p0_pt = np.array([t_current, y_current, 0])
            p1_pt = np.array([t_current + dt/2, y_current + k1 * dt/2, 0])
            p2_pt = np.array([t_current + dt/2, y_current + k2 * dt/2, 0])
            p3_pt = np.array([t_current + dt, y_current + k3 * dt, 0])
            
            v1_start = p0_pt
            v1_end = p0_pt + np.array([dt, k1 * dt, 0])
            
            v2_start = p1_pt
            v2_end = p1_pt + np.array([dt, k2 * dt, 0])
            
            v3_start = p2_pt
            v3_end = p2_pt + np.array([dt, k3 * dt, 0])
            
            v4_start = p3_pt
            v4_end = p3_pt + np.array([dt, k4 * dt, 0])
            
            vec1 = Arrow(axes.c2p(*v1_start)[:3], axes.c2p(*v1_end)[:3], color=ORANGE, buff=0, max_tip_length_to_length_ratio=0.15)
            vec2 = Arrow(axes.c2p(*v2_start)[:3], axes.c2p(*v2_end)[:3], color=TEAL, buff=0, max_tip_length_to_length_ratio=0.15)
            vec3 = Arrow(axes.c2p(*v3_start)[:3], axes.c2p(*v3_end)[:3], color=PURPLE, buff=0, max_tip_length_to_length_ratio=0.15)
            vec4 = Arrow(axes.c2p(*v4_start)[:3], axes.c2p(*v4_end)[:3], color=MAROON, buff=0, max_tip_length_to_length_ratio=0.15)
            
            dot1 = Dot(axes.c2p(*p1_pt), color=ORANGE, radius=0.06)
            dot2 = Dot(axes.c2p(*p2_pt), color=TEAL, radius=0.06)
            dot3 = Dot(axes.c2p(*p3_pt), color=PURPLE, radius=0.06)
            
            guide1 = DashedLine(axes.c2p(*p0_pt), axes.c2p(*p1_pt), color=ORANGE, stroke_opacity=0.7)
            guide2 = DashedLine(axes.c2p(*p0_pt), axes.c2p(*p2_pt), color=TEAL, stroke_opacity=0.7)
            guide3 = DashedLine(axes.c2p(*p0_pt), axes.c2p(*p3_pt), color=PURPLE, stroke_opacity=0.7)
            
            vert1 = DashedLine(axes.c2p(*p1_pt), axes.c2p(t_current + dt/2, 0), color=ORANGE, stroke_opacity=0.5)
            vert2 = DashedLine(axes.c2p(*p2_pt), axes.c2p(t_current + dt/2, 0), color=TEAL, stroke_opacity=0.5)
            vert3 = DashedLine(axes.c2p(*p3_pt), axes.c2p(t_current + dt, 0), color=PURPLE, stroke_opacity=0.5)
            vert4 = DashedLine(axes.c2p(t_current + dt, y_current + k4 * dt), axes.c2p(t_current + dt, 0), color=MAROON, stroke_opacity=0.5)
            
            w1_start = p0_pt
            w1_end = w1_start + np.array([dt/6, k1 * dt/6, 0])
            
            w2_start = w1_end
            w2_end = w2_start + np.array([dt*2/6, k2 * dt*2/6, 0])
            
            w3_start = w2_end
            w3_end = w3_start + np.array([dt*2/6, k3 * dt*2/6, 0])
            
            w4_start = w3_end
            w4_end = w4_start + np.array([dt/6, k4 * dt/6, 0])
            
            w_vec1 = Arrow(axes.c2p(*w1_start)[:3], axes.c2p(*w1_end)[:3], color=ORANGE, buff=0, max_tip_length_to_length_ratio=0.25)
            w_vec2 = Arrow(axes.c2p(*w2_start)[:3], axes.c2p(*w2_end)[:3], color=TEAL, buff=0, max_tip_length_to_length_ratio=0.25)
            w_vec3 = Arrow(axes.c2p(*w3_start)[:3], axes.c2p(*w3_end)[:3], color=PURPLE, buff=0, max_tip_length_to_length_ratio=0.25)
            w_vec4 = Arrow(axes.c2p(*w4_start)[:3], axes.c2p(*w4_end)[:3], color=MAROON, buff=0, max_tip_length_to_length_ratio=0.25)
            
            if is_slow:
                self.play(Indicate(current_dot, color=YELLOW, scale_factor=1.5))
                
                # k1
                self.play(Indicate(rk4_formula_1, color=YELLOW))
                self.play(Create(vec1))
                self.next_slide()
                
                # k2
                self.play(Indicate(rk4_formula_2, color=YELLOW))
                self.play(Create(guide1), FadeIn(dot1), Create(vert1))
                self.play(Create(vec2))
                self.next_slide()
                
                # k3
                self.play(Indicate(rk4_formula_3, color=YELLOW))
                self.play(Create(guide2), FadeIn(dot2), Create(vert2))
                self.play(Create(vec3))
                self.next_slide()
                
                # k4
                self.play(Indicate(rk4_formula_4, color=YELLOW))
                self.play(Create(guide3), FadeIn(dot3), Create(vert3))
                self.play(Create(vec4))
                self.next_slide()
                
                # weighted sum
                self.play(Indicate(rk4_formula_5, color=GREEN))
                self.play(
                    ReplacementTransform(vec1, w_vec1),
                    ReplacementTransform(vec2, w_vec2),
                    ReplacementTransform(vec3, w_vec3),
                    ReplacementTransform(vec4, w_vec4),
                    FadeOut(guide1), FadeOut(guide2), FadeOut(guide3),
                    FadeOut(vert1), FadeOut(vert2), FadeOut(vert3), FadeOut(vert4),
                    FadeOut(dot1), FadeOut(dot2), FadeOut(dot3),
                    run_time=2.0
                )
                self.next_slide()
                
                self.play(Create(rk4_segment), FadeIn(next_dot), run_time=anim_run_time)
                self.play(FadeOut(w_vec1), FadeOut(w_vec2), FadeOut(w_vec3), FadeOut(w_vec4))
                self.next_slide()
            else:
                fast_rt = 0.2
                self.play(Indicate(rk4_formula_1, color=YELLOW, run_time=fast_rt))
                self.play(Create(vec1), run_time=fast_rt)
                
                self.play(Indicate(rk4_formula_2, color=YELLOW, run_time=fast_rt))
                self.play(Create(guide1), FadeIn(dot1), Create(vert1), Create(vec2), run_time=fast_rt)
                
                self.play(Indicate(rk4_formula_3, color=YELLOW, run_time=fast_rt))
                self.play(Create(guide2), FadeIn(dot2), Create(vert2), Create(vec3), run_time=fast_rt)
                
                self.play(Indicate(rk4_formula_4, color=YELLOW, run_time=fast_rt))
                self.play(Create(guide3), FadeIn(dot3), Create(vert3), Create(vec4), run_time=fast_rt)
                
                self.play(Indicate(rk4_formula_5, color=GREEN, run_time=fast_rt))
                self.play(
                    ReplacementTransform(vec1, w_vec1),
                    ReplacementTransform(vec2, w_vec2),
                    ReplacementTransform(vec3, w_vec3),
                    ReplacementTransform(vec4, w_vec4),
                    FadeOut(guide1), FadeOut(guide2), FadeOut(guide3),
                    FadeOut(vert1), FadeOut(vert2), FadeOut(vert3), FadeOut(vert4),
                    FadeOut(dot1), FadeOut(dot2), FadeOut(dot3),
                    run_time=0.4
                )
                self.play(Create(rk4_segment), FadeIn(next_dot), run_time=0.4)
                self.play(FadeOut(w_vec1), FadeOut(w_vec2), FadeOut(w_vec3), FadeOut(w_vec4), run_time=0.3)
                
            rk4_mobjects.add(next_dot, rk4_segment)
            
            t_current = t_next
            y_current = y_next
            current_dot = next_dot
            rk4_points.append(axes.c2p(t_current, y_current))
            
        self.next_slide()
        
        accuracy_title = Text("High Precision of RK4", font_size=20, color=GREEN)
        accuracy_text = Text("The approximation very closely\nfollows the analytical solution", font_size=16)
        
        accuracy_group = VGroup(accuracy_title, accuracy_text).arrange(DOWN, aligned_edge=RIGHT)
        accuracy_group.to_corner(UR).shift(DOWN * 4)
        
        self.play(Write(accuracy_group))
        self.next_slide()
        
        true_curve_points = [
            axes.c2p(t, exact_sol(t)) 
            for t in np.linspace(t0, t0 + n_steps * dt, 100)
        ]
        
        area_polygon = Polygon(
            *true_curve_points, *reversed(rk4_points),
            fill_color=GREEN,
            fill_opacity=0.8,
            stroke_width=0
        )
        
        self.play(FadeIn(area_polygon))
        self.next_slide()

        self.play(FadeOut(area_polygon), FadeOut(accuracy_group))
        self.next_slide()

        elements_to_fade = VGroup(
            header, axes, axes_labels, true_curve, curve_label,
            start_dot, start_label, rk4_mobjects, ode_text
        )
        
        self.play(
            FadeOut(elements_to_fade),
            formulas.animate.move_to(UP * 0.5).scale(2.0)
        )
        self.next_slide()
        
        # highlight weights
        self.play(
            rk4_formula_5[1].animate.set_color(YELLOW),
            rk4_formula_5[3].animate.set_color(YELLOW),
            rk4_formula_5[5].animate.set_color(YELLOW),
            run_time=1.5
        )
        self.next_slide()
        
        question = Text("Why we use these weights?", font_size=32, color=YELLOW)
        question.next_to(formulas, DOWN, buff=0.8)
        self.play(Write(question))
        self.next_slide()
