from manim import *
from manim_slides import Slide

class RK4Derivation(Slide):
    def construct(self):
        title = Text("The Classic RK4 Method", font_size=40).to_edge(UP)
        self.play(FadeIn(title))
        
        k1 = MathTex("k_1", "=", "f(t_n, y_n)").scale(0.8)
        k2 = MathTex("k_2", "=", "f(t_n + ", "\\frac{1}{2}", "\\Delta t", ", y_n + ", "\\frac{1}{2}", "\\Delta t", " ", "k_1)").scale(0.8)
        k3 = MathTex("k_3", "=", "f(t_n + ", "\\frac{1}{2}", "\\Delta t", ", y_n + ", "\\frac{1}{2}", "\\Delta t", " ", "k_2)").scale(0.8)
        k4 = MathTex("k_4", "=", "f(t_n + ", "1", "\\Delta t", ", y_n + ", "1", "\\Delta t", " ", "k_3)").scale(0.8)
        
        y_next = MathTex("y_{n+1}", "=", "y_n + ", "\\Delta t", "\\left(", "\\frac{1}{6}", "k_1 + ", "\\frac{2}{6}", "k_2 + ", "\\frac{2}{6}", "k_3 + ", "\\frac{1}{6}", "k_4\\right)").scale(0.8)
        
        classic_group = VGroup(k1, k2, k3, k4, y_next).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
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
            anims.append(part.animate.set_color(YELLOW))
        for part in cyan_parts:
            anims.append(part.animate.set_color(TEAL))
            
        self.play(*anims)
        
        question = Text("Why do we use these specific weights?", font_size=36, color=YELLOW).to_edge(DOWN)
        self.play(Write(question))
        
        self.next_slide()
        
        title2 = Text("Step 1: The General 4-Stage Form", font_size=40).to_edge(UP)
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
        gen_group.move_to(ORIGIN)
        
        g_k2[3].set_color(YELLOW)
        g_k2[6].set_color(YELLOW)
        g_k3[3].set_color(YELLOW)
        g_k3[6].set_color(YELLOW)
        g_k3[10].set_color(YELLOW)
        g_k4[3].set_color(YELLOW)
        g_k4[6].set_color(YELLOW)
        g_k4[10].set_color(YELLOW)
        g_k4[14].set_color(YELLOW)
        
        g_y_next[5].set_color(YELLOW)
        g_y_next[7].set_color(YELLOW)
        g_y_next[9].set_color(YELLOW)
        g_y_next[11].set_color(YELLOW)
        
        for eq in [g_k2, g_k3, g_k4, g_y_next]:
            for part in eq:
                if "\\Delta t" in part.get_tex_string():
                    part.set_color(TEAL)
        
        self.play(
            TransformMatchingTex(k1, g_k1),
            TransformMatchingTex(k2, g_k2),
            TransformMatchingTex(k3, g_k3),
            TransformMatchingTex(k4, g_k4),
            TransformMatchingTex(y_next, g_y_next),
        )
        self.next_slide()
        
        goal_text = Text("Goal: Solve for a, b, and c", font_size=36, color=YELLOW).to_edge(DOWN)
        self.play(Write(goal_text))
        self.next_slide()
        
        self.play(FadeOut(gen_group), FadeOut(goal_text))
        
        title3 = Text("Step 2: Taylor Expansion of True Solution", font_size=36).to_edge(UP)
        self.play(Transform(title, title3))
        
        # exact solution
        y_taylor = MathTex(r"y(t_{n+1}) = y_n + \Delta t y' + \frac{\Delta t^2}{2} y'' + \mathcal{O}(\Delta t^3)").scale(0.8)
        chain_rule = MathTex(r"y' = f(t_n, y_n) = f, \quad y'' = f_t + f_y f").scale(0.8).set_color(TEAL)
        y_taylor_sub = MathTex(r"y(t_{n+1}) = y_n + \Delta t ", "f", r" + \frac{\Delta t^2}{2} (", "f_t + f_y f", r") + \mathcal{O}(\Delta t^3)").scale(0.8)
        
        taylor_group = VGroup(y_taylor, chain_rule, y_taylor_sub).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        
        self.play(FadeIn(y_taylor))
        self.next_slide()
        self.play(FadeIn(chain_rule))
        self.next_slide()
        self.play(FadeIn(y_taylor_sub))
        self.next_slide()
        
        self.play(FadeOut(taylor_group))
        
        title3_5 = Text("Step 3: Multivariable Expansion of RK stages", font_size=36).to_edge(UP)
        self.play(Transform(title, title3_5))
        
        multi_taylor = MathTex(r"f(t + \delta t, y + \delta y) \approx f + \delta t f_t + \delta y f_y").scale(0.8)
        
        k2_expansion1 = MathTex(r"k_2 = f(t_n + c_2 \Delta t, y_n + a_{21} \Delta t k_1)").scale(0.8)
        k2_expansion2 = MathTex(r"k_2 \approx f + (c_2 \Delta t)f_t + (a_{21} \Delta t f)f_y").scale(0.8)
        k2_expansion3 = MathTex(r"k_2 \approx f + \Delta t(c_2 f_t + a_{21} f f_y)").scale(0.8)
        
        k2_group = VGroup(multi_taylor, k2_expansion1, k2_expansion2, k2_expansion3).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        
        self.play(FadeIn(multi_taylor))
        self.next_slide()
        self.play(FadeIn(k2_expansion1))
        self.next_slide()
        self.play(FadeIn(k2_expansion2))
        self.next_slide()
        self.play(FadeIn(k2_expansion3))
        self.next_slide()
        
        self.play(FadeOut(k2_group))
        
        title3_6 = Text("Step 4: Matching the Coefficients", font_size=36).to_edge(UP)
        self.play(Transform(title, title3_6))
        
        rk_approx = MathTex(r"y_{n+1} \approx y_n + \Delta t(b_1 f + b_2(f + \Delta t c_2 f_t + \Delta t a_{21} f f_y) + \dots)").scale(0.7)
        rk_grouped = MathTex(r"y_{n+1} \approx y_n + \Delta t(b_1 + b_2 + \dots)f + \Delta t^2(b_2 c_2 + \dots)f_t + \dots").scale(0.7)
        
        match_group = VGroup(y_taylor_sub.copy(), rk_approx, rk_grouped).arrange(DOWN, buff=0.6).move_to(ORIGIN).shift(UP * 0.5)
        
        self.play(FadeIn(match_group[0])) # True solution
        self.play(FadeIn(match_group[1])) # RK solution substitute
        self.next_slide()
        self.play(TransformMatchingTex(match_group[1].copy(), match_group[2]))
        self.next_slide()
        
        match_eq1 = MathTex(r"\Rightarrow \sum b_i = 1", color=YELLOW).scale(0.8).next_to(match_group, DOWN, buff=0.4)
        match_eq2 = MathTex(r"\Rightarrow \sum b_i c_i = \frac{1}{2}", color=TEAL).scale(0.8).next_to(match_eq1, DOWN, buff=0.2)
        
        self.play(Write(match_eq1))
        self.next_slide()
        
        self.play(Write(match_eq2))
        self.next_slide()
        
        self.play(FadeOut(match_group), FadeOut(match_eq1), FadeOut(match_eq2))
        
        title4 = Text("The Order Conditions (4th Order)", font_size=36).to_edge(UP)
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
        
        col1 = VGroup(Text("First Order", font_size=20, color=TEAL), eq1, Text("Second Order", font_size=20, color=TEAL), eq2).arrange(DOWN, buff=0.2)
        col2 = VGroup(Text("Third Order", font_size=20, color=TEAL), eq3, eq4, Text("Consistency", font_size=20, color=TEAL), eq9, eq10, eq11).arrange(DOWN, buff=0.2)
        col3 = VGroup(Text("Fourth Order", font_size=20, color=TEAL), eq5, eq6, eq7, eq8).arrange(DOWN, buff=0.2)
        
        cond_group = VGroup(col1, col2, col3).arrange(RIGHT, buff=0.8).next_to(title, DOWN, buff=0.5)
        
        self.play(FadeIn(cond_group))
        self.next_slide()
        
        math_prob = Text("11 Equations, but 13 Unknowns.", font_size=32, color=RED).to_edge(DOWN)
        self.play(Write(math_prob))
        self.next_slide()
        
        self.play(FadeOut(cond_group), FadeOut(math_prob))
        
        title5 = Text("Underdetermined System = Infinite Solutions", font_size=40).to_edge(UP)
        degree_text = Text("(Degrees of Freedom)", font_size=32).next_to(title5, DOWN)
        
        self.play(Transform(title, title5), FadeIn(degree_text))
        self.next_slide()
        
        choice_text = Text("The Classic Choice:", font_size=32, color=YELLOW)
        choice_c2 = MathTex("c_2 = \\frac{1}{2}")
        choice_c3 = MathTex("c_3 = \\frac{1}{2}")
        
        choice_group = VGroup(choice_text, choice_c2, choice_c3).arrange(DOWN).move_to(ORIGIN).shift(UP*0.5)
        
        self.play(FadeIn(choice_group))
        self.next_slide()
        
        choice_group = VGroup(choice_text, choice_c2, choice_c3).arrange(DOWN).move_to(ORIGIN).shift(UP*0.5)
        self.play(FadeIn(choice_group))
        self.next_slide()
        
        collapse_text = Text("Yields the famous weights:", font_size=32, color=TEAL).next_to(choice_group, DOWN, buff=0.5)
        
        weights1 = MathTex("b_1 = \\frac{1}{6}, \\quad b_2 = \\frac{1}{3}")
        weights2 = MathTex("b_3 = \\frac{1}{3}, \\quad b_4 = \\frac{1}{6}")
        
        weights_group = VGroup(weights1, weights2).arrange(DOWN).next_to(collapse_text, DOWN, buff=0.3)
        
        self.play(FadeIn(collapse_text), FadeIn(weights_group))
        self.next_slide()
        
        self.play(FadeOut(choice_group), FadeOut(collapse_text), FadeOut(weights_group), FadeOut(degree_text))
        
        title6 = Text("The Classic RK4 Method", font_size=40).to_edge(UP)
        self.play(Transform(title, title6))
        
        final_y_next = MathTex("y_{n+1}", "=", "y_n + ", "\\frac{\\Delta t}{6}", "(", "k_1 + ", "2", "k_2 + ", "2", "k_3 + ", "k_4)")
        final_y_next.scale(1.2).move_to(ORIGIN)
        final_y_next[3].set_color(YELLOW)
        final_y_next[6].set_color(YELLOW)
        final_y_next[8].set_color(YELLOW)
        
        self.play(FadeIn(final_y_next))
        
        simpson = Text("Simpson's 1/3 Rule Weights: 1 - 4 - 1", font_size=24, color=GRAY).next_to(final_y_next, DOWN, buff=1.0)
        rk4_w = Text("RK4 Weights: 1 - 2 - 2 - 1", font_size=24, color=YELLOW).next_to(simpson, UP, buff=0.2)
        
        self.play(FadeIn(rk4_w), FadeIn(simpson))
        self.next_slide()
        
        self.play(FadeOut(rk4_w), FadeOut(simpson))
        
        transition_1 = Tex("But remember...", font_size=40, color=RED).next_to(final_y_next, DOWN, buff=0.8)
        self.play(Write(transition_1))
        self.next_slide()
        
        transition_2 = Tex("We had 2 Degrees of Freedom ($c_2$ and $c_3$).", font_size=36).next_to(transition_1, DOWN, buff=0.3)
        self.play(FadeIn(transition_2))
        self.next_slide()
        
        transition_3 = Tex("Every point $(c_2, c_3)$ creates an entirely new, valid 4th-order method.", font_size=36).next_to(transition_2, DOWN, buff=0.3)
        self.play(FadeIn(transition_3))
        self.next_slide()
        
        transition_4 = Text("Is the classic choice the best choice? Let's map the error.", font_size=36, color=YELLOW).to_edge(DOWN)
        self.play(Write(transition_4))
        self.next_slide()
