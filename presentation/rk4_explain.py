from manim import *
from manim_slides import Slide
from theme import *

class RK4Derivation(Slide):
    def construct(self):
        title = create_header("The Classic RK4 Method")
        self.play(FadeIn(title))
        
        k1 = MathTex("k_1", "=", "f(t_n, y_n)").scale(0.8)
        k2 = MathTex("k_2", "=", "f(t_n + ", "\\frac{1}{2}", "\\Delta t", ", y_n + ", "\\frac{1}{2}", "\\Delta t", " ", "k_1)").scale(0.8)
        k3 = MathTex("k_3", "=", "f(t_n + ", "\\frac{1}{2}", "\\Delta t", ", y_n + ", "\\frac{1}{2}", "\\Delta t", " ", "k_2)").scale(0.8)
        k4 = MathTex("k_4", "=", "f(t_n + ", "1", "\\Delta t", ", y_n + ", "1", "\\Delta t", " ", "k_3)").scale(0.8)
        
        y_next = MathTex("y_{n+1}", "=", "y_n + ", "\\Delta t", "\\left(", "\\frac{1}{6}", "k_1 + ", "\\frac{2}{6}", "k_2 + ", "\\frac{2}{6}", "k_3 + ", "\\frac{1}{6}", "k_4\\right)").scale(0.8)
        
        classic_group = VGroup(k1, k2, k3, k4, y_next).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        classic_group.scale_to_fit_height(min(classic_group.height, config.frame_height - 2.5))
        classic_group.move_to(ORIGIN)

        # fade in steps
        for eq in [k1, k2, k3, k4, y_next]:
            self.play(FadeIn(eq), run_time=0.5)
            
        self.next_slide()
        
        # highlight numbers
        yellow_parts = [
            k2[3], k2[6],
            k3[3], k3[6],
            k4[3], k4[6],
            y_next[5], y_next[7], y_next[9], y_next[11]
        ]
        
        cyan_parts = [
            k2[4], k2[7],
            k3[4], k3[7],
            k4[4], k4[7],
            y_next[3]
        ]
        
        anims = []
        for part in yellow_parts:
            anims.append(part.animate.set_color(COLORS["highlight"]))
        for part in cyan_parts:
            anims.append(part.animate.set_color(COLORS["k2"]))
            
        self.play(*anims)
        
        question = Text("Why do we use these specific weights?", font_size=36, color=COLORS["highlight"]).to_edge(DOWN)
        self.play(Write(question))
        
        self.next_slide()
        
        title2 = create_header("Step 1: The General 4-Stage Form")
        self.play(
            FadeOut(question),
            Transform(title, title2)
        )
        
        g_k1 = MathTex("k_1", "=", "f(t_n, y_n)").scale(0.8)
        g_k2 = MathTex("k_2", "=", "f(t_n + ", "c_2", "\\Delta t", ", y_n + ", "a_{21}", "\\Delta t", " ", "k_1)").scale(0.8)
        g_k3 = MathTex("k_3", "=", "f(t_n + ", "c_3", "\\Delta t", ", y_n + ", "a_{31}", "\\Delta t", " ", "k_1 + ", "a_{32}", "\\Delta t", " ", "k_2)").scale(0.8)
        g_k4 = MathTex("k_4", "=", "f(t_n + ", "c_4", "\\Delta t", ", y_n + ", "a_{41}", "\\Delta t", " ", "k_1 + ", "a_{42}", "\\Delta t", " ", "k_2 + ", "a_{43}", "\\Delta t", " ", "k_3)").scale(0.8)
        
        g_y_next = MathTex("y_{n+1}", "=", "y_n + ", "\\Delta t", "\\left(", "b_1", "k_1 + ", "b_2", "k_2 + ", "b_3", "k_3 + ", "b_4", "k_4\\right)").scale(0.8)
        
        gen_group = VGroup(g_k1, g_k2, g_k3, g_k4, g_y_next).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        gen_group.scale_to_fit_height(min(gen_group.height, config.frame_height - 2.5))
        gen_group.move_to(ORIGIN)
        
        g_k2[3].set_color(COLORS["highlight"])
        g_k2[6].set_color(COLORS["highlight"])
        g_k3[3].set_color(COLORS["highlight"])
        g_k3[6].set_color(COLORS["highlight"])
        g_k3[10].set_color(COLORS["highlight"])
        g_k4[3].set_color(COLORS["highlight"])
        g_k4[6].set_color(COLORS["highlight"])
        g_k4[10].set_color(COLORS["highlight"])
        g_k4[14].set_color(COLORS["highlight"])
        
        g_y_next[5].set_color(COLORS["highlight"])
        g_y_next[7].set_color(COLORS["highlight"])
        g_y_next[9].set_color(COLORS["highlight"])
        g_y_next[11].set_color(COLORS["highlight"])
        
        for eq in [g_k2, g_k3, g_k4, g_y_next]:
            for part in eq:
                if "\\Delta t" in part.get_tex_string():
                    part.set_color(COLORS["k2"])
        
        self.play(
            TransformMatchingTex(k1, g_k1),
            TransformMatchingTex(k2, g_k2),
            TransformMatchingTex(k3, g_k3),
            TransformMatchingTex(k4, g_k4),
            TransformMatchingTex(y_next, g_y_next),
        )
        self.next_slide()
        
        goal_text = Text("Goal: Solve for a, b, and c", font_size=36, color=COLORS["highlight"]).to_edge(DOWN)
        self.play(Write(goal_text))
        self.next_slide()
        
        self.play(FadeOut(gen_group), FadeOut(goal_text))
        
        title3 = create_header("Step 2: Taylor Expansion & Matching")
        self.play(Transform(title, title3))
        
        y_true = MathTex(r"y_{true} = y_n + \Delta t y' + \dots + \frac{\Delta t^4}{24} y^{(4)} + ", r"\mathcal{O}(\Delta t^5)").scale(0.8)
        y_true[1].set_color(COLORS["backward_euler"])
        y_rk = MathTex(r"y_{RK} = y_n + \Delta t(b_1 k_1 + b_2 k_2 + b_3 k_3 + b_4 k_4)").scale(0.8)
        
        taylor_group = VGroup(y_true, y_rk).arrange(DOWN, buff=0.8).move_to(ORIGIN)
        
        self.play(FadeIn(y_true))
        self.next_slide()
        self.play(FadeIn(y_rk))
        self.next_slide()
        
        match_text = Text("Match coefficients up to 4th order", font_size=32, color=COLORS["highlight"]).next_to(taylor_group, DOWN, buff=0.8)
        self.play(Write(match_text))
        self.next_slide()
        
        self.play(FadeOut(taylor_group), FadeOut(match_text))
        
        title4 = create_header("The Order Conditions (4th Order)")
        self.play(Transform(title, title4))
        
        cond_scale = 0.55
        
        # o(dt)
        eq1 = MathTex("\\sum_{i} b_i = 1").scale(cond_scale)
        # o(dt^2)
        eq2 = MathTex("\\sum_{i} b_i c_i = \\frac{1}{2}").scale(cond_scale)
        # o(dt^3)
        eq3 = MathTex("\\sum_{i} b_i c_i^2 = \\frac{1}{3}").scale(cond_scale)
        eq4 = MathTex("\\sum_{i,j} b_i a_{ij} c_j = \\frac{1}{6}").scale(cond_scale)
        # o(dt^4)
        eq5 = MathTex("\\sum_{i} b_i c_i^3 = \\frac{1}{4}").scale(cond_scale)
        eq6 = MathTex("\\sum_{i,j} b_i c_i a_{ij} c_j = \\frac{1}{8}").scale(cond_scale)
        eq7 = MathTex("\\sum_{i,j} b_i a_{ij} c_j^2 = \\frac{1}{12}").scale(cond_scale)
        eq8 = MathTex("\\sum_{i,j,k} b_i a_{ij} a_{jk} c_k = \\frac{1}{24}").scale(cond_scale)
        # consistency
        eq9 = MathTex("\\sum_{j} a_{2j} = c_2").scale(cond_scale)
        eq10 = MathTex("\\sum_{j} a_{3j} = c_3").scale(cond_scale)
        eq11 = MathTex("\\sum_{j} a_{4j} = c_4").scale(cond_scale)
        
        col1 = VGroup(Text("First Order", font_size=20, color=COLORS["k2"]), eq1, Text("Second Order", font_size=20, color=COLORS["k2"]), eq2).arrange(DOWN, buff=0.2)
        col2 = VGroup(Text("Third Order", font_size=20, color=COLORS["k2"]), eq3, eq4, Text("Consistency", font_size=20, color=COLORS["k2"]), eq9, eq10, eq11).arrange(DOWN, buff=0.2)
        col3 = VGroup(Text("Fourth Order", font_size=20, color=COLORS["k2"]), eq5, eq6, eq7, eq8).arrange(DOWN, buff=0.2)
        
        cond_group = VGroup(col1, col2, col3).arrange(RIGHT, buff=0.8).next_to(title, DOWN, buff=0.5)
        cond_group.scale_to_fit_height(min(cond_group.height, config.frame_height - 3.0))
        
        self.play(FadeIn(col1, shift=UP*0.5), run_time=0.5)
        self.play(FadeIn(col2, shift=UP*0.5), run_time=0.5)
        self.play(FadeIn(col3, shift=UP*0.5), run_time=0.5)
        self.next_slide()
        
        math_prob = Text("11 Equations, but 13 Unknowns.", font_size=32, color=COLORS["backward_euler"]).to_edge(DOWN)
        self.play(Write(math_prob))
        self.next_slide()
        
        self.play(FadeOut(cond_group), FadeOut(math_prob))
        
        title5 = create_header("Underdetermined System = Infinite Solutions")
        degree_text = Text("(Degrees of Freedom)", font_size=32).next_to(title5, DOWN)
        
        self.play(Transform(title, title5), FadeIn(degree_text))
        self.next_slide()
        
        choice_text = Text("The Classic Choice:", font_size=32, color=COLORS["highlight"])
        choice_c2 = MathTex("c_2 = \\frac{1}{2}")
        choice_c3 = MathTex("c_3 = \\frac{1}{2}")
        
        choice_col = VGroup(choice_text, choice_c2, choice_c3).arrange(DOWN, buff=0.3)
        
        arrow = MathTex("\\Rightarrow").scale(2)
        
        collapse_text = Text("Yields these weights:", font_size=32, color=COLORS["k2"])
        weights1 = MathTex("b_1 = \\frac{1}{6}, \\quad b_2 = \\frac{1}{3}")
        weights2 = MathTex("b_3 = \\frac{1}{3}, \\quad b_4 = \\frac{1}{6}")
        
        weights_col = VGroup(collapse_text, weights1, weights2).arrange(DOWN, buff=0.3)
        
        horiz_group = VGroup(choice_col, arrow, weights_col).arrange(RIGHT, buff=1.0)
        
        self.play(FadeIn(choice_col))
        self.next_slide()
        
        self.play(FadeIn(arrow), FadeIn(weights_col))
        self.next_slide()
        
        self.play(FadeOut(horiz_group), FadeOut(degree_text))
        
        title6 = create_header("The Classic RK4 Method")
        self.play(Transform(title, title6))
        
        final_y_next = MathTex("y_{n+1}", "=", "y_n + ", "\\frac{\\Delta t}{6}", "(", "k_1 + ", "2", "k_2 + ", "2", "k_3 + ", "k_4)")
        final_y_next.scale(1.2).move_to(ORIGIN)
        final_y_next[3].set_color(COLORS["highlight"])
        final_y_next[6].set_color(COLORS["highlight"])
        final_y_next[8].set_color(COLORS["highlight"])
        
        self.play(FadeIn(final_y_next))
        
        simpson = Text("Simpson's 1/3 Rule Weights: 1 - 4 - 1", font_size=24, color=GRAY).next_to(final_y_next, DOWN, buff=1.0)
        rk4_w = Text("RK4 Weights: 1 - 2 - 2 - 1", font_size=24, color=COLORS["highlight"]).next_to(simpson, UP, buff=0.2)
        
        self.play(FadeIn(rk4_w), FadeIn(simpson))
        self.next_slide()
        
        self.play(FadeOut(rk4_w), FadeOut(simpson))
        
        transition_1 = Tex("Remaining 2 Degrees of Freedom: $(c_2, c_3)$", font_size=36, color=COLORS["backward_euler"]).next_to(final_y_next, DOWN, buff=0.8)
        self.play(Write(transition_1))
        self.next_slide()
        
        transition_2 = Tex("Each pair forms a valid 4th-order method.", font_size=36).next_to(transition_1, DOWN, buff=0.4)
        self.play(FadeIn(transition_2))
        self.next_slide()
        
        plte_text = Tex(r"The unmatched $\mathcal{O}(\Delta t^5)$ error is the \textbf{Principal Local Truncation Error (PLTE)}", font_size=36, color=COLORS["highlight"]).next_to(transition_2, DOWN, buff=0.4)
        self.play(Write(plte_text))
        self.next_slide()
        
        self.play(FadeOut(transition_1), FadeOut(transition_2), FadeOut(plte_text), FadeOut(final_y_next))
        
        title7 = create_header("What is PLTE?")
        self.play(Transform(title, title7))
        
        plte_def = Tex(r"It measures the \textbf{inherent error} introduced in a \textbf{single step}.", font_size=36).move_to(UP*0.5)
        plte_formula = MathTex(r"\text{Local Error} \approx \text{PLTE}(c_2, c_3) \cdot \Delta t^5", font_size=40, color=COLORS["backward_euler"]).next_to(plte_def, DOWN, buff=0.8)
        plte_goal = Tex("Different $(c_2, c_3)$ pairs change the magnitude of this error.", font_size=36).next_to(plte_formula, DOWN, buff=0.8)
        
        self.play(FadeIn(plte_def))
        self.next_slide()
        self.play(Write(plte_formula))
        self.next_slide()
        self.play(FadeIn(plte_goal))
        self.next_slide()
