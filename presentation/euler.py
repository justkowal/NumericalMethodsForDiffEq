from manim import *
from manim_slides import Slide

class EulerMethod(Slide):
    def construct(self):
        
        header_1 = Text("Euler's Method", font_size=24)
        header_1.to_corner(UL)
        
        self.play(Write(header_1))
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
        self.next_slide()
        
        def exact_sol(t):
            return np.sin(t) + 0.5 * t + 1
            
        true_curve = axes.plot(exact_sol, x_range=[0, 5.5], color=BLUE)
        curve_label = MathTex("y(t)", color=BLUE).next_to(true_curve.get_end(), UP)
        
        t0 = 0
        y0 = exact_sol(t0)
        start_dot = Dot(axes.c2p(t0, y0), color=YELLOW)
        start_label = MathTex("(t_0, y_0)", font_size=24, color=YELLOW).next_to(start_dot, UL, buff=0.1)
        self.play(FadeIn(start_dot), Write(start_label))
        self.next_slide()

        # show true solution
        self.play(Create(true_curve), FadeIn(curve_label))
        self.next_slide()

        def deriv(t, y):
            return np.cos(t) + 0.5
        
        # ode text
        ode_text = MathTex(r"\frac{\mathrm{d} y}{\mathrm{d} t} = f(t,y) = \cos(t) + 0.5", font_size=32)
        ode_text.to_corner(UR)
        self.play(Write(ode_text))
        self.next_slide()
        
        # euler formula
        euler_formula = MathTex(r"y_{n+1} = y_n + \Delta t \cdot f(t_n, y_n)", font_size=32)
        euler_formula.next_to(ode_text, DOWN, buff=0.5)
        self.play(Write(euler_formula))
        self.next_slide()
        
        dt = 1.0
        n_steps = 5
        
        t_current = t0
        y_current = y0
        current_dot = start_dot
        
        euler_points = [axes.c2p(t_current, y_current)]
        forward_mobjects = VGroup()
        
        for i in range(n_steps):
            is_slow = (i < 2)
            anim_run_time = 1.0 if is_slow else 0.4
            
            slope = deriv(t_current, y_current)
            t_next = t_current + dt
            y_next = y_current + slope * dt
            
            # tangent line
            dt_tg = 1.0 # doubled 
            true_tg_start = axes.c2p(t_current - dt_tg, exact_sol(t_current) - slope * dt_tg)
            true_tg_end = axes.c2p(t_current + dt_tg, exact_sol(t_current) + slope * dt_tg)
            tangent_line = Line(true_tg_start, true_tg_end, color=RED)
            
            self.play(Create(tangent_line), run_time=anim_run_time)
            if is_slow:
                self.next_slide()
                
            # indicate last point
            self.play(Indicate(current_dot, color=YELLOW, scale_factor=1.5), run_time=anim_run_time)
            
            # move to point
            euler_pt = axes.c2p(t_current, y_current)
            self.play(tangent_line.animate.move_to(euler_pt), run_time=anim_run_time)
            if is_slow:
                self.next_slide()
                
            # dashed line
            orient_start = euler_pt
            orient_end = axes.c2p(t_current + dt * 1.2, y_current + slope * dt * 1.2)
            dotted_tangent = DashedLine(orient_start, orient_end, color=RED)
            
            self.play(ReplacementTransform(tangent_line, dotted_tangent), run_time=anim_run_time)
            if is_slow:
                self.next_slide()
                
            # dt/dy triangles
            if is_slow:
                dt_line = DashedLine(axes.c2p(t_current, y_current), axes.c2p(t_next, y_current), color=WHITE)
                dy_line = DashedLine(axes.c2p(t_next, y_current), axes.c2p(t_next, y_next), color=WHITE)
                dt_label = MathTex(r"\Delta t", font_size=24).next_to(dt_line, DOWN, buff=0.1)
                dy_label = MathTex(r"\Delta y", font_size=24).next_to(dy_line, RIGHT, buff=0.1)
                
                self.play(Create(dt_line), Write(dt_label), run_time=anim_run_time)
                self.play(Create(dy_line), Write(dy_label), run_time=anim_run_time)
                self.next_slide()
                
            # new point & segment
            next_dot = Dot(axes.c2p(t_next, y_next), color=YELLOW)
            self.play(FadeIn(next_dot), run_time=anim_run_time)
            
            euler_segment = Line(axes.c2p(t_current, y_current), axes.c2p(t_next, y_next), color=YELLOW)
            self.play(Create(euler_segment), run_time=anim_run_time * (1.5 if is_slow else 1.0))
            if is_slow:
                self.next_slide()
                
            forward_mobjects.add(next_dot, euler_segment)
            
            # cleanup
            if is_slow:
                self.play(
                    FadeOut(dt_line, dt_label, dy_line, dy_label, dotted_tangent),
                    run_time=0.5
                )
            else:
                self.play(FadeOut(dotted_tangent), run_time=0.2)
                
            t_current = t_next
            y_current = y_next
            current_dot = next_dot
            
            euler_points.append(axes.c2p(t_current, y_current))

        self.next_slide()
        
        true_curve_points = [
            axes.c2p(t, exact_sol(t)) 
            for t in np.linspace(t0, t0 + n_steps * dt, 100)
        ]
        
        # closed polygon
        area_polygon = Polygon(
            *true_curve_points, *reversed(euler_points),
            fill_color=RED,
            fill_opacity=0.3,
            stroke_width=0
        )
        
        divergence_text = Text(
            "Approximation diverges significantly\nfrom analytical solution",
            font_size=20,
            color=RED,
            t2c={"diverges significantly": RED}
        )
        divergence_text.next_to(area_polygon, DOWN, buff=0.1).shift(DOWN * 0.2 + RIGHT * 1.5)

        self.play(FadeIn(area_polygon), Write(divergence_text))
        self.next_slide()
        
        self.play(
            FadeOut(area_polygon),
            FadeOut(divergence_text),
            run_time=0.5
        )
        
        reason_title = Text("Why the Divergence?", font_size=20, color=YELLOW)
        reason_text_1 = Text("Euler assumes the rate of change", font_size=16)
        reason_text_2 = Text("is constant across the entire step.", font_size=16)
        
        reason_group = VGroup(reason_title, reason_text_1, reason_text_2).arrange(DOWN, aligned_edge=RIGHT)
        # position on side
        reason_group.to_corner(UR).shift(DOWN * 2.5)
        
        self.play(Write(reason_group), run_time=1.5)
        self.next_slide(auto_next=True)
        
        tangent_tracker_pt = ValueTracker(t0)
        
        def get_tangent_line():
            t_val = tangent_tracker_pt.get_value()
            y_val = exact_sol(t_val)
            s = deriv(t_val, y_val)
            t_len = 0.8
            return Line(
                axes.c2p(t_val - t_len, y_val - s * t_len),
                axes.c2p(t_val + t_len, y_val + s * t_len),
                color=ORANGE
            )
            
        moving_tangent = always_redraw(get_tangent_line)
        moving_dot = always_redraw(lambda: Dot(axes.c2p(tangent_tracker_pt.get_value(), exact_sol(tangent_tracker_pt.get_value())), color=ORANGE, radius=DEFAULT_DOT_RADIUS))
        
        slope_label = MathTex(r"\text{True Slope changes!}", font_size=32, color=ORANGE)
        slope_label.add_updater(lambda m: m.next_to(moving_tangent, RIGHT, buff=0.1))
        
        self.play(Create(moving_tangent), FadeIn(moving_dot), Write(slope_label))
        self.next_slide(loop=True)
        self.play(
            tangent_tracker_pt.animate.set_value(t0 + dt * 2),
            run_time=4.0,
            rate_func=there_and_back
        )
        
        self.next_slide()
        
        self.play(
            FadeOut(moving_tangent),
            FadeOut(moving_dot),
            FadeOut(slope_label),
            FadeOut(reason_group),
            run_time=0.5
        )
        
        header_forward = Text("Forward Euler's Method", font_size=24)
        header_forward.to_corner(UL)
        self.play(Transform(header_1, header_forward))
        self.next_slide()

        self.play(
            FadeOut(forward_mobjects),
            FadeOut(header_1),
            FadeOut(euler_formula),
        )
        self.next_slide()
        
        header_2 = Text("Backward Euler's Method", font_size=24)
        header_2.to_corner(UL)
        
        self.play(Write(header_2))
        self.next_slide()
        
        backward_euler_formula = MathTex(r"y_{n+1} = y_n + \Delta t \cdot f(t_{n+1}, y_{n+1})", font_size=32)
        backward_euler_formula.next_to(ode_text, DOWN, buff=0.5)
        self.play(Write(backward_euler_formula))
        self.next_slide()

        t_current = t0
        y_current = y0
        current_dot = start_dot
        
        backward_mobjects = VGroup()
        backward_points = [axes.c2p(t_current, y_current)]
        
        for i in range(n_steps):
            is_slow = (i < 2)
            anim_run_time = 1.0 if is_slow else 0.4
            
            t_next = t_current + dt
            slope = deriv(t_next, y_current) 
            y_next = y_current + slope * dt
            
            eval_point = axes.c2p(t_next, exact_sol(t_next))
            eval_dot = Dot(eval_point, color=PURPLE)
            
            eval_arrow = Arrow(
                start=axes.c2p(t_current, 0),
                end=axes.c2p(t_next, 0),
                color=PURPLE,
                buff=0,
                stroke_width=4,
                max_tip_length_to_length_ratio=0.1
            )
            eval_label = MathTex(r"t_{n+1}", font_size=24, color=PURPLE).next_to(eval_arrow, DOWN, buff=0.1)
            eval_line = DashedLine(axes.c2p(t_next, 0), eval_point, color=PURPLE)
            
            if is_slow:
                self.play(Create(eval_arrow), Write(eval_label), run_time=anim_run_time/2)
                self.play(Create(eval_line), FadeIn(eval_dot), run_time=anim_run_time/2)
                self.next_slide()
            
            dt_tg = 1.0 
            true_tg_start = axes.c2p(t_next - dt_tg, exact_sol(t_next) - slope * dt_tg)
            true_tg_end = axes.c2p(t_next + dt_tg, exact_sol(t_next) + slope * dt_tg)
            tangent_line = Line(true_tg_start, true_tg_end, color=PURPLE)
            self.play(Create(tangent_line), run_time=anim_run_time)
            if is_slow:
                self.next_slide()
                
            self.play(Indicate(current_dot, color=YELLOW, scale_factor=1.5), run_time=anim_run_time)
            
            euler_pt = axes.c2p(t_current, y_current)
            if is_slow:
                self.play(
                    tangent_line.animate.move_to(euler_pt), 
                    FadeOut(eval_line), 
                    FadeOut(eval_dot),
                    FadeOut(eval_arrow),
                    FadeOut(eval_label),
                    run_time=anim_run_time
                )
                self.next_slide()
            else:
                self.play(tangent_line.animate.move_to(euler_pt), run_time=anim_run_time)
                
            orient_start = euler_pt
            orient_end = axes.c2p(t_current + dt * 1.2, y_current + slope * dt * 1.2)
            dotted_tangent = DashedLine(orient_start, orient_end, color=PURPLE)
            self.play(ReplacementTransform(tangent_line, dotted_tangent), run_time=anim_run_time)
            if is_slow:
                self.next_slide()
                
            if is_slow:
                dt_line = DashedLine(axes.c2p(t_current, y_current), axes.c2p(t_next, y_current), color=WHITE)
                dy_line = DashedLine(axes.c2p(t_next, y_current), axes.c2p(t_next, y_next), color=WHITE)
                dt_label = MathTex(r"\Delta t", font_size=24).next_to(dt_line, DOWN, buff=0.1)
                dy_label = MathTex(r"\Delta y", font_size=24).next_to(dy_line, RIGHT, buff=0.1)
                self.play(Create(dt_line), Write(dt_label), run_time=anim_run_time)
                self.play(Create(dy_line), Write(dy_label), run_time=anim_run_time)
                self.next_slide()
                
            next_dot = Dot(axes.c2p(t_next, y_next), color=PURPLE)
            self.play(FadeIn(next_dot), run_time=anim_run_time)
            
            euler_segment = Line(axes.c2p(t_current, y_current), axes.c2p(t_next, y_next), color=PURPLE)
            self.play(Create(euler_segment), run_time=anim_run_time * (1.5 if is_slow else 1.0))
            if is_slow:
                self.next_slide()
                
            backward_mobjects.add(next_dot, euler_segment)
            if is_slow:
                self.play(FadeOut(dt_line, dt_label, dy_line, dy_label, dotted_tangent), run_time=0.5)
            else:
                self.play(FadeOut(dotted_tangent), run_time=0.2)
                
            t_current = t_next
            y_current = y_next
            current_dot = next_dot
            backward_points.append(axes.c2p(t_current, y_current))

        self.next_slide()
        
        true_curve_points = [
            axes.c2p(t, exact_sol(t)) 
            for t in np.linspace(t0, t0 + n_steps * dt, 100)
        ]
        
        area_polygon_backward = Polygon(
            *true_curve_points, *reversed(backward_points),
            fill_color=PURPLE,
            fill_opacity=0.3,
            stroke_width=0
        )
        
        divergence_text_backward = Text(
            "Better, but still not precise",
            font_size=20,
            color=PURPLE,
            t2c={"not precise": RED, "Better": GREEN}
        )
        divergence_text_backward.next_to(area_polygon_backward, DOWN, buff=0.1).shift(DOWN * 0.2 + RIGHT * 1.5)

        self.play(FadeIn(area_polygon_backward), Write(divergence_text_backward))
        self.next_slide()
