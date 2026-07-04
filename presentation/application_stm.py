from manim import *
from manim_slides import Slide
from theme import *

class STM32Application(Slide):
    def construct(self):
        self.wait_time_between_slides = 0.1
        # --- Slide 0: What is an STM32? ---
        intro_title = Text("Algorithms on STM32", font_size=TEXT_SIZE_HEADER).to_corner(UL)
        self.play(Write(intro_title))
        
        intro_bullets = VGroup(
            Text("A microcontroller (MCU) - a tiny computer built onto a single chip.", font_size=16),
            Text("Used in embedded systems, electronics, and robotics.", font_size=16)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(intro_title, DOWN, buff=0.8).align_to(intro_title, LEFT)
        
        self.play(FadeIn(intro_bullets, shift=RIGHT))
        self.next_slide()

        chip = ImageMobject("stm32.png").scale_to_fit_height(2.5).move_to(DOWN * 0.8)
        
        self.play(GrowFromCenter(chip))
        
        spec_core = Text("CPU: ARM Cortex-M4", font_size=20, color=BLUE).next_to(chip, LEFT, buff=0.5)
        spec_speed = Text("Speed: up to 180 MHz", font_size=20, color=YELLOW).next_to(chip, RIGHT, buff=0.5)
        spec_mem = Text("Storage: 2MB Flash", font_size=20, color=GREEN).next_to(chip, UP, buff=0.5)
        spec_ram = Text("RAM: 384 KB", font_size=20, color=RED).next_to(chip, DOWN, buff=0.5)
        
        self.play(
            Write(spec_core),
            Write(spec_speed),
            Write(spec_mem),
            Write(spec_ram)
        )
        self.next_slide()

        # Wipe the screen before moving to the Clock Tree
        self.play(
            FadeOut(intro_title),
            FadeOut(intro_bullets),
            FadeOut(chip),
            FadeOut(spec_core),
            FadeOut(spec_speed),
            FadeOut(spec_mem),
            FadeOut(spec_ram)
        )
        self.wait(0.2)
        
        # --- Slide 1: Header ---
        title = Text("Clock Tree & Complexity Analysis", font_size=TEXT_SIZE_HEADER).to_corner(UL)
        self.add(title)
        
        model_subtitle = Text("STM32F469NI Clock Tree", font_size=24, color=GRAY_A).to_edge(UP, buff=1.2)
        self.play(FadeIn(model_subtitle))

        hse = VGroup(RoundedRectangle(height=1.0, width=1.8), Text("HSE (Ext)", font_size=18)).set_color(GREEN)
        hsi = VGroup(RoundedRectangle(height=1.0, width=1.8), Text("HSI (16MHz)", font_size=18)).set_color(ORANGE)
        lsi = VGroup(RoundedRectangle(height=1.0, width=1.8), Text("LSI (31kHz)", font_size=18)).set_color(RED)
        sources = VGroup(hse, hsi, lsi).arrange(DOWN, buff=0.5).to_edge(LEFT, buff=1).shift(DOWN*0.5)
        
        mux = Triangle().scale(0.4).rotate(-90 * DEGREES).next_to(sources, RIGHT, buff=1.5)
        mux_label = Text("SW Mux", font_size=16).next_to(mux, UP, buff=0.1)
        pll = VGroup(RoundedRectangle(height=1.2, width=1.8), Text("PLL", font_size=20)).next_to(mux, RIGHT, buff=1)
        sysclk = VGroup(Circle(radius=0.7), Text("SYSCLK", font_size=20)).to_edge(RIGHT, buff=1).shift(DOWN*0.5)
        
        line_hsi = Line(hsi.get_right(), mux.get_left())
        line_lsi = Line(lsi.get_right(), mux.get_left() + DOWN*0.2)
        line_mux_pll = Line(mux.get_right(), pll.get_left())
        line_pll_sys = Line(pll.get_right(), sysclk.get_left())
        
        clock_tree = VGroup(sources, mux, mux_label, pll, sysclk, line_hsi, line_lsi, line_mux_pll, line_pll_sys)
        self.play(Create(clock_tree))
        
        active_label = Text("Mode: High Performance (180 MHz)", font_size=24, color=YELLOW).next_to(clock_tree, DOWN, buff=0.5)
        path_high = VGroup(line_hsi, line_mux_pll, line_pll_sys).copy().set_color(YELLOW).set_stroke(width=6)
        self.play(Write(active_label), FadeIn(path_high))
        self.next_slide()

        # --- Slide 3: Transition to LSI ---
        switch_text = Tex("Bypassing the PLL: \\textbf{31 kHz}", font_size=24, color=WHITE).next_to(active_label, DOWN, buff=0.3)
        self.play(Write(switch_text))
        self.next_slide()
        
        new_label = Text("Mode: Ultra-Low Frequency (31 kHz)", font_size=24, color=RED).move_to(active_label)
        path_low = Line(lsi.get_right(), sysclk.get_left()).set_color(RED).set_stroke(width=6)
        
        self.play(
            FadeOut(path_high, pll, line_mux_pll, line_pll_sys),
            Transform(active_label, new_label),
            Create(path_low),
            switch_text.animate.set_color(RED)
        )
        self.next_slide()

        # --- Transition: Cleanup for Code Section ---
        self.play(FadeOut(clock_tree), FadeOut(model_subtitle), FadeOut(switch_text), FadeOut(active_label), FadeOut(path_low), FadeOut(title))

        # --- Slide 4: Euler Implementation ---
        euler_header = Text("Forward Euler Implementation", font_size=TEXT_SIZE_HEADER).to_corner(UL)
        self.play(Write(euler_header))

        euler_pseudo_str = """function EULER_FWD(time, state, step, f):
    rate <- f(time, state)
    next_state <- state + step * rate
    return next_state"""

        # Using formatter_style='monokai' for bright green comments
        euler_pseudo_code = Code(
            code_string=euler_pseudo_str,
            language="python",
            formatter_style="monokai",
            background="window",
        ).scale(0.7).to_edge(UP, buff=1.5)

        euler_rust_str = """let n = y.len();
let mut dydt = [0.0_f32; ODE_MAX_STATES];
dydt_fn(t, y, &mut dydt[..n])?;

for i in 0..n {
    y[i] += h * dydt[i];
}"""
        
        euler_rust = Code(
            code_string=euler_rust_str,
            language="rust",
            formatter_style="monokai",
            background="window",
        ).scale(0.7).next_to(euler_pseudo_code, DOWN, buff=0.5)

        self.play(Create(euler_pseudo_code))
        self.play(Create(euler_rust))
        self.next_slide()

        # --- Slide 5: RK4 Implementation ---
        self.play(FadeOut(euler_pseudo_code), FadeOut(euler_rust), FadeOut(euler_header))
        rk4_header = Text("Runge-Kutta 4th Order Implementation", font_size=TEXT_SIZE_HEADER).to_corner(UL)
        self.play(Write(rk4_header))

        rk4_pseudo_str = """function RK4(time, state, step, f):
    k1 <- f(time, state)
    k2 <- f(time + step/2, state + (step/2)*k1)
    k3 <- f(time + step/2, state + (step/2)*k2)
    k4 <- f(time + step, state + step*k3)
    
    next_state <- state + (step/6)*(k1 + 2*k2 + 2*k3 + k4)
    return next_state"""

        rk4_pseudo_code = Code(
            code_string=rk4_pseudo_str,
            language="python",
            formatter_style="monokai",
            background="window",
        ).scale(0.55).to_edge(UP, buff=1.4)

        rk4_rust_str = """// k1 eval (euler step)
dydt_fn(t, y, &mut k1[..n])?;

// k2 eval
dydt_fn(t + h_half, &y_temp[..n], &mut k2[..n])?;

// k3 eval
dydt_fn(t + h_half, &y_temp[..n], &mut k3[..n])?;

// k4 eval
dydt_fn(t + h, &y_temp[..n], &mut k4[..n])?;

// Weighted sum:
for i in 0..n {
    y[i] += h_sixth * (k1[i] + 2.0*k2[i] + 2.0*k3[i] + k4[i]);
}"""

        rk4_rust = Code(
            code_string=rk4_rust_str,
            language="rust",
            formatter_style="monokai",
            background="window",
        ).scale(0.55).next_to(rk4_pseudo_code, DOWN, buff=0.2)

        self.play(Create(rk4_pseudo_code))
        self.play(Create(rk4_rust))
        self.next_slide()

        # --- Slide 6: Conclusion ---
        self.play(FadeOut(rk4_pseudo_code), FadeOut(rk4_rust), FadeOut(rk4_header))
        self.next_slide()
        