from manim import *
from manim_slides import Slide
from theme import *
import numpy as np

class ApplicationExample(Slide):
    def construct(self):
        # 1. Headline
        title = create_header("Application to Hobby Rocket")
        self.play(Write(title))
        
        transition_text = Tex("Applying the methods to our initial rocket physics problem.", font_size=24, color=GRAY)
        transition_text.to_edge(DOWN)
        self.play(FadeIn(transition_text))
        
        self.next_slide()
        self.play(FadeOut(transition_text))

        # Problem Setup - Cleaner Layout
        col1 = VGroup(
            MathTex(r"M_{dry} = 1.0 \text{ kg}", font_size=28),
            MathTex(r"M_{fuel_0} = 0.9 \text{ kg}", font_size=28),
            MathTex(r"q = 0.3 \text{ kg/s}", font_size=28),
            MathTex(r"t_{burn} = 3.0 \text{ s}", font_size=28),
            MathTex(r"v_e = 300 \text{ m/s}", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT)
        
        col2 = VGroup(
            MathTex(r"M(t) = 1.0 + 0.9 \left(1 - \frac{t}{3}\right)^2", font_size=28),
            MathTex(r"M'(t) = -0.6 \left(1 - \frac{t}{3}\right)", font_size=28),
            MathTex(r"a(t) = -\frac{M'(t)}{M(t)} v_e - g", font_size=28),
            MathTex(r"g = 9.81 \text{ m/s}^2", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT)
        
        setup_group = VGroup(col1, col2).arrange(RIGHT, buff=1.5).next_to(title, DOWN, buff=0.8)
        
        self.play(Write(col1))
        self.play(Write(col2))
        self.next_slide()

        # graph section
        self.play(FadeOut(setup_group))
        
        graph_title = Tex("Comparison with $h=2.0\text{s}$", font_size=32, color=COLORS["highlight"])
        graph_title.next_to(title, DOWN, buff=0.2)
        self.play(Write(graph_title))
        
        # Better axes bounds
        ax = Axes(
            x_range=[0, 20.001, 2],
            y_range=[-100, 300, 50],
            axis_config={"include_numbers": True},
            x_length=8.5,
            y_length=4.5
        )
        
        labels = ax.get_axis_labels(x_label="t \text{ (s)}", y_label="v \text{ (m/s)}")
        graph_group = VGroup(ax, labels)
        
        # Position with nice margins from bottom and left
        graph_group.to_edge(DOWN, buff=0.5).to_edge(LEFT, buff=1.5)
        
        self.play(Create(graph_group))
        
        # --- Analytical Solution ---
        def exact_m(t):
            if t > 3: return 1.0
            return 1.0 + 0.9 * (1 - t/3)**2

        def exact_v(t):
            return 300 * np.log(1.9 / exact_m(t)) - 9.81 * t

        def f(t):
            if t >= 3: return -9.81
            num = 0.6 * (1 - t/3)
            den = 1.0 + 0.9 * (1 - t/3)**2
            return (num / den) * 300 - 9.81
            
        analytical_graph = ax.plot(exact_v, x_range=[0, 20], color=COLORS["exact_solution"], use_smoothing=True)
        
        # Legend
        legend = VGroup(
            VGroup(Line(color=COLORS["exact_solution"]).set_length(0.5), Tex("Exact", font_size=24)),
            VGroup(Line(color=COLORS["forward_euler"]).set_length(0.5), Tex("Forward Euler", font_size=24)),
            VGroup(Line(color=COLORS["backward_euler"]).set_length(0.5), Tex("Backward Euler", font_size=24)),
            VGroup(Line(color=COLORS["rk4"]).set_length(0.5), Tex("RK4", font_size=24))
        )
        for row in legend:
            row.arrange(RIGHT, buff=0.2)
        legend.arrange(DOWN, aligned_edge=LEFT)
        
        max_right = legend.get_right()[0]
        for row in legend:
            ph = Tex("Err: +00000.0", font_size=24).set_opacity(0)
            ph.next_to(row, RIGHT, buff=0)
            ph.set_x(max_right + 0.4, direction=LEFT)
            row.add(ph)
            
        legend_box = always_redraw(lambda: SurroundingRectangle(legend, color=GRAY, buff=0.2))
        legend_group = VGroup(legend_box, legend).to_edge(RIGHT, buff=1.0).align_to(ax, UP)
        
        self.play(Create(analytical_graph))
        # Fade in box AND first legend row
        self.play(FadeIn(legend_box), FadeIn(legend[0]))
        self.next_slide()

        def get_exact_area(t_end):
            if t_end <= 0: return 0.0
            t_fine = np.linspace(0, t_end, 1000)
            v_fine = [exact_v(t) for t in t_fine]
            return np.trapezoid(v_fine, t_fine)

        # --- Numerical Solvers ---
        h = 2.0
        t_vals = np.arange(0, 22.0, h)

        def draw_method(color_key, method_func, legend_idx):
            pts = [0.0]
            lines = VGroup()
            dots = VGroup(Dot(ax.c2p(0, 0), color=COLORS[color_key]))
            
            self.play(FadeIn(legend[legend_idx]), run_time=0.5)
            
            num_area = 0.0
            t_end_sim = 0.0
            t_history = [0.0]
            
            for i in range(len(t_vals)-1):
                t_curr = t_vals[i]
                v_curr = pts[-1]
                v_next = method_func(t_curr, v_curr, h)
                pts.append(v_next)
                
                step_area = (v_curr + v_next) / 2.0 * h
                
                if v_next < -100:
                    if v_curr >= -100:
                        lines.add(Line(ax.c2p(t_curr, v_curr), ax.c2p(t_curr+h, v_next), color=COLORS[color_key]))
                        dots.add(Dot(ax.c2p(t_curr+h, v_next), color=COLORS[color_key]))
                        num_area += step_area
                        t_end_sim = t_curr + h
                        t_history.append(t_end_sim)
                    break
                    
                lines.add(Line(ax.c2p(t_curr, v_curr), ax.c2p(t_curr + h, v_next), color=COLORS[color_key]))
                dots.add(Dot(ax.c2p(t_curr + h, v_next), color=COLORS[color_key]))
                num_area += step_area
                t_end_sim = t_curr + h
                t_history.append(t_end_sim)
            
            self.play(Create(lines), FadeIn(dots), run_time=1.5)
            
            # --- Visual Area Shadow ---
            num_points_c2p = [ax.c2p(t, v) for t, v in zip(t_history, pts)]
            fine_t = np.linspace(t_history[-1], 0, 100)
            exact_points_c2p = [ax.c2p(t, exact_v(t)) for t in fine_t]
            
            error_area = Polygon(
                *num_points_c2p,
                *exact_points_c2p,
                fill_color=COLORS[color_key],
                fill_opacity=0.3,
                stroke_width=0
            )
            self.play(FadeIn(error_area))
            
            exact_area = get_exact_area(t_end_sim)
            error_val = num_area - exact_area
            
            err_text = Tex(rf"Err: {error_val:+.1f}", font_size=24, color=COLORS[color_key])
            err_text.move_to(legend[legend_idx][2], aligned_edge=LEFT)
            self.play(Transform(legend[legend_idx][2], err_text))
            
            self.next_slide()
            self.play(FadeOut(error_area))

        # 1. Forward Euler Test
        def fe_step(t, v, dt):
            return v + dt * f(t)
        draw_method("forward_euler", fe_step, 1)

        # 2. Backward Euler Test
        def be_step(t, v, dt):
            return v + dt * f(t + dt)
        draw_method("backward_euler", be_step, 2)
        
        # 3. RK4 Test
        def rk4_step(t, v, dt):
            k1 = f(t)
            k2 = f(t + dt/2)
            k3 = f(t + dt/2)
            k4 = f(t + dt)
            return v + dt * (k1 + 2*k2 + 2*k3 + k4) / 6
        draw_method("rk4", rk4_step, 3)

