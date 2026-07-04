from manim import *
from manim_slides import Slide
from theme import *

class WhyNumericalMethods(Slide):
    def construct(self):
        # --- NEW FINAL SLIDE: Why Numerical Methods? ---
        why_num_header = create_header("Why Numerical Methods?")
        self.play(FadeIn(why_num_header, shift=UP))
        
        question_text = Tex(
            "Why don't we use solutions derived analytically every time?",
            font_size=36,
            color=YELLOW
        ).next_to(why_num_header, DOWN, buff=0.3).align_to(why_num_header, LEFT)
        self.play(Write(question_text))
        
        self.next_slide()
        
        intro_drag = Tex(
            "Real-world rockets experience gravity and aerodynamic drag:",
            font_size=32
        ).next_to(question_text, DOWN, buff=0.4).align_to(question_text, LEFT)
        self.play(Write(intro_drag))
        
        real_ode = MathTex(
            r"\frac{\mathrm{d}v}{\mathrm{d}t}",
            r" = ",
            r"-\frac{1}{M(t)}\frac{\mathrm{d}M(t)}{\mathrm{d}t} v_e",
            r" - ",
            r"g",
            r" - ",
            r"\frac{\rho(y) v^2 C_d A}{2 M(t)}",
            font_size=36
        )
        real_ode.next_to(intro_drag, DOWN, buff=0.3).align_to(intro_drag, LEFT)
        
        # Explanations for terms
        term_thrust = Tex("Thrust", font_size=24, color=ORANGE).next_to(real_ode[2], DOWN, buff=0.3)
        term_gravity = Tex("Gravity", font_size=24, color=BLUE).next_to(real_ode[4], DOWN, buff=0.3)
        term_drag = Tex("Air Drag", font_size=24, color=RED).next_to(real_ode[6], DOWN, buff=0.3)
        
        self.play(Write(real_ode))
        self.play(FadeIn(term_thrust), FadeIn(term_gravity), FadeIn(term_drag))
        
        self.next_slide()
        
        # Density gradient
        density_eq = MathTex(
            r"\text{where air density gradient is: } \rho(y) = \rho_0 e^{-\frac{y}{H}}",
            font_size=32
        ).next_to(term_drag, DOWN, buff=0.3).align_to(intro_drag, LEFT)
        
        velocity_y_eq = MathTex(
            r"\text{and altitude is coupled: } v = \frac{\mathrm{d}y}{\mathrm{d}t}",
            font_size=32
        ).next_to(density_eq, DOWN, buff=0.15).align_to(density_eq, LEFT)
        
        self.play(Write(density_eq), Write(velocity_y_eq))
        
        self.next_slide()
        
        no_analytical = Tex(
            r"This coupled, non-linear ODE has \textbf{no analytical solution}.",
            font_size=32,
            color=RED
        ).next_to(velocity_y_eq, DOWN, buff=0.4).align_to(velocity_y_eq, LEFT)
        
        we_must_approx = Tex(
            r"We must approximate it using \textbf{numerical methods}.",
            font_size=32,
            color=WHITE
        ).next_to(no_analytical, DOWN, buff=0.15).align_to(no_analytical, LEFT)
        
        self.play(Write(no_analytical))
        self.play(Write(we_must_approx))
        
        self.next_slide()
        
        self.play(FadeOut(Group(*self.mobjects)))
        
        thanks_thats_all = Text("Thank you, that's all!", font_size=32)
        self.play(Write(thanks_thats_all))
        
        self.next_slide()