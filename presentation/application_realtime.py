from manim import *
from manim_slides import Slide
import csv
import os
import numpy as np
from theme import *

# Manual theme colors
COLORS = {
    "rk4": RED,
    "euler": GREEN,
    "exact": YELLOW,
    "background": "#1a1a1a"
}

class HardwareBenchmarks(Slide):
    # Disable caching to prevent overhead with large datasets
    disable_caching = True

    def load_csv_data(self, filename):
        """Loads simulation data from the specified CSV file."""
        data = []
        filepath = os.path.join("..", "implementation", "rocket_rs_stm32", filename)
        
        try:
            with open(filepath, 'r') as f:
                reader = csv.reader(f)
                next(reader) # Skip header
                for row in reader:
                    if not row or any("DONE" in col for col in row):
                        continue
                    try:
                        # Columns: ExecutionTime(us), SimulationTime(s), Velocity(m/s)
                        exec_time = float(row[0])
                        sim_time = float(row[1])
                        velocity = float(row[2])
                        data.append((sim_time, velocity, exec_time))
                    except (ValueError, IndexError):
                        continue
        except FileNotFoundError:
            return []
        return data

    def construct(self):
        # --- Slide 1: Introduction ---
        title = create_header("Trying the algorithms on real hardware")
        self.play(FadeIn(title, shift=UP))

        # --- Data Loading ---
        rk4_data = self.load_csv_data("rk4_slow_h_default.csv")
        euler_data = self.load_csv_data("euler_slow_h_default.csv")

        # --- Dynamic Scale Calculation ---
        all_points = rk4_data + euler_data
        if all_points:
            max_t_data = max(p[0] for p in all_points)
            max_v_data = max(p[1] for p in all_points)
            min_v_data = min(p[1] for p in all_points)
        else:
            max_t_data, max_v_data, min_v_data = 10.0, 150.0, -20.0

        t_range_max = float(np.ceil(max_t_data * 1.05))
        v_range_max = float(np.ceil(max_v_data / 10) * 10 + 20)
        v_range_min = float(np.floor(min_v_data / 10) * 10 - 20)

        # --- Exact Solution Parameters ---
        M_DRY, M_FUEL_0, T_BURN, V_E = 100.0, 500.0, 50.0, 2500.0
        G, RHO_0, AREA, C_D = 9.81, 1.225, 0.5, 0.4

        def solve_exact_high_res(t_max, steps=1000):
            dt = t_max / steps
            t_vals, v_vals, v = [0.0], [0.0], 0.0
            for i in range(steps):
                t = i * dt
                m_t = M_DRY + M_FUEL_0 * (1.0 - t / T_BURN)**2 if t < T_BURN else M_DRY
                thrust = (-( -2.0 * M_FUEL_0 / T_BURN * (1.0 - t / T_BURN) ) / m_t) * V_E if t < T_BURN else 0.0
                v += (thrust - G - (0.5 * RHO_0 * v * abs(v) * C_D * AREA) / m_t) * dt
                t_vals.append(t + dt); v_vals.append(v)
            return t_vals, v_vals

        t_exact_table, v_exact_table = solve_exact_high_res(t_range_max)
        def exact_v_func(t): return np.interp(t, t_exact_table, v_exact_table)

        # --- Axes Setup ---
        ax = Axes(
            x_range=[0, t_range_max, t_range_max / 5], 
            y_range=[v_range_min, v_range_max, (v_range_max - v_range_min) / 5],
            axis_config={"include_numbers": True},
            x_length=8, y_length=5, tips=False
        ).shift(DOWN*0.5).to_edge(LEFT, buff=1.0)
        
        self.play(Create(ax), Write(ax.get_axis_labels(x_label="t (s)", y_label="v (m/s)")))
        
        # Bypass ax.plot adaptive sampler to prevent 68k point explosion
        exact_path = VMobject(color=COLORS["exact"])
        exact_path.set_points_as_corners([ax.c2p(t, v) for t, v in zip(t_exact_table, v_exact_table)])
        self.play(Create(exact_path))

        # Legend with Error decimal counters
        legend = VGroup(*[
            VGroup(
                Line(color=c, stroke_width=6).set_length(0.4), 
                Tex(t, font_size=22), 
                VGroup(Tex("Err:", font_size=20), DecimalNumber(0.0, num_decimal_places=2, font_size=20))
            )
            for c, t in [(COLORS["exact"], "Exact"), (COLORS["rk4"], "RK4 (h=0.04)"), 
                         (COLORS["euler"], "Euler (h=0.04)")]
        ])
        for row in legend: 
            row[1].next_to(row[0], RIGHT)
            row[2].arrange(RIGHT, buff=0.1).next_to(row[1], RIGHT, buff=0.4)
            
        legend.arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT, buff=0.5).align_to(ax, UP)
        self.play(FadeIn(legend[0][0:2]))

        def visualize_error(data, color, idx):
            if not data: return
            
            error_val_mobj = legend[idx][2][1]
            error_val_mobj.set_color(color)
            error_val_mobj.set_value(0.0)

            self.play(FadeIn(legend[idx][0:2]), FadeIn(legend[idx][2]), run_time=0.5)

            # Pre-calculate the total accurate final error using ALL the data points
            total_final_error = 0.0
            for i in range(len(data)-1):
                t1, v1, _ = data[i]
                t2, v2, _ = data[i+1]
                dt = t2 - t1
                total_final_error += abs(((exact_v_func(t1) + exact_v_func(t2))/2) - ((v1 + v2)/2)) * dt

            # Define intro and rest data
            intro_limit = 10
            intro_data = data[:intro_limit+1]
            raw_rest_data = data[intro_limit:]
            
            # --- CULLING POINTS FOR RENDERING SPEED ---
            step_skip = max(1, len(raw_rest_data) // 150)
            plottable_rest_data = raw_rest_data[::step_skip]
            if plottable_rest_data[-1][0] != raw_rest_data[-1][0]:
                plottable_rest_data.append(raw_rest_data[-1])

            # PHASE 1: Real-Time Intro (10 steps)
            intro_lines = VGroup()
            for i in range(len(intro_data)-1):
                t1, v1, _ = intro_data[i]
                t2, v2, _ = intro_data[i+1]
                intro_lines.add(Line(ax.c2p(t1, v1), ax.c2p(t2, v2), color=color, stroke_width=6))
            
            self.play(Create(intro_lines, lag_ratio=1), run_time=1.0, rate_func=linear)

            # PHASE 2: Speedup Phase
            if len(plottable_rest_data) > 1:
                fast_path = VMobject(color=color, stroke_width=6)
                fast_path.set_points_as_corners([ax.c2p(t, v) for t, v, e in plottable_rest_data])
                
                anim_duration = (len(raw_rest_data) / 10.0)

                self.play(
                    Create(fast_path),
                    run_time=max(0.5, anim_duration),
                    rate_func=linear
                )

            # Reveal final error AT THE END
            # FIXED: DecimalNumber requires a ValueTracker and an updater to visibly redraw during an animation
            err_tracker = ValueTracker(0.0)
            error_val_mobj.add_updater(lambda m: m.set_value(err_tracker.get_value()))
            self.play(err_tracker.animate.set_value(total_final_error), run_time=0.5)
            error_val_mobj.clear_updaters()

            # PHASE 3: Error Area Polygon
            poly_points = [ax.c2p(p[0], p[1]) for p in (intro_data + plottable_rest_data)]
            exact_pts_poly = [ax.c2p(t, exact_v_func(t)) for t in np.linspace(data[-1][0], 0, 30)]
            error_poly = Polygon(*poly_points, *exact_pts_poly, fill_color=color, fill_opacity=0.3, stroke_width=0)
            
            self.play(FadeIn(error_poly))
            self.next_slide()
            self.play(FadeOut(error_poly))

        # Render methods sequentially
        methods = [(rk4_data, COLORS["rk4"], 1), 
                   (euler_data, COLORS["euler"], 2)]
                    
        for d, c, i in methods:
            visualize_error(d, c, i)

        self.play(FadeOut(VGroup(ax, legend, title, exact_path, *[m[0:2] for m in legend], *[m[2] for m in legend])))
        self.next_slide()