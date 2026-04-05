from manim import *
from manim_slides import Slide
from theme import *

class ProblemDemonstration(Slide):
    def construct(self):
        
        # text elements
        header_1 = create_header("Problem: Rocket Trajectory")
        
        # placeholder labels
        equation_label = Text(
            "At t=0:",
            font_size=24,
            color=GRAY,
            line_spacing=1.2
        )
        
        equation_label_variant = Text(
            "Initial Conditions:",
            font_size=24,
            color=GRAY,
            line_spacing=1.2
        )
        
        
        
        formula1 = MathTex(
            r"M(t)",
            r" = M_{dry} + M_{fuel}(t)",
            r"\text{ - non-increasing function} \implies \frac{\mathrm{d}M(t)}{\mathrm{d}t} \leq 0",
            r"M(0) = M_{dry} + M_{fuel_0}",
            r"v(0) = 0",
            r"P|_{t=0} = 0",
            font_size=32
        )
        
        formula2 = MathTex(
            r"M_{fuel}(t) = \begin{cases} M_{fuel_0} \left( 1 - \frac{t}{t_{burn}} \right)^2 & \text{if } 0 \leq t \leq t_{burn} \\ 0 & \text{if } t > t_{burn} \end{cases}",
            font_size=32
        )

        formula3 = MathTex(
            r"t_{burn} = \frac{M_{fuel_0}}{q}",
            font_size=32
        )
        
        formula4 = MathTex(
            r"q = 0.3",
            font_size=32
        )
        
        # group elements
        basic_group = VGroup(equation_label, VGroup(formula1[0], formula1[1]))
        basic_group.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        
        fuel_group = VGroup(formula2, formula3, formula4)
        fuel_group.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        # group math blocks
        eq_block_1 = VGroup(basic_group, fuel_group)
        
        # 2. Arrange them vertically, aligning their left edges
        eq_block_1.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        # 3. Define where the center of the right column should be
        RIGHT_COLUMN_CENTER = RIGHT * 2
        
        # 4. Move the entire left-aligned block to that position
        eq_block_1.move_to(RIGHT_COLUMN_CENTER)
        
        eq2_header = Tex(
            r"At arbitrary time $t$:",
            font_size=32,
            color=GRAY
        )
        
        formula5 = MathTex(
            r"P|_{t}",
            r" = ",
            r"M(t) \cdot \vec{v}(t)",
            font_size=40
        )
        
        eq2_header_2 = Tex(
            r"Then at $t + \mathrm{d}t$:",
            font_size=32,
            color=GRAY
        )

        formula_6 = MathTex(
            r"M(t + \mathrm{d}t)",
            r" = M(t) + ",
            r"\left(",
            r"\frac{M(t + \mathrm{d}t) - M(t)}{\mathrm{d}t}",
            r"\right)",
            r"\mathrm{d}t",
            font_size=32
        )

        eq_block_2 = VGroup(eq2_header, formula5, eq2_header_2, formula_6)
        eq_block_2.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        eq_block_1.scale_to_fit_height(min(eq_block_1.height, config.frame_height - 2.5))
        eq_block_2.scale_to_fit_height(min(eq_block_2.height, config.frame_height - 2.5))
        
        eq_block_2.align_to(eq_block_1, LEFT)
        eq_block_2.align_to(eq_block_1, UP)

        # rocket graphics
        body = Rectangle(width=1.0, height=3.0, fill_color=GRAY, fill_opacity=1, stroke_color=WHITE)
        
        # Rocket Nose Cone (A gray triangle on top of the body)
        tip = Triangle()
        tip.scale(0.6)
        tip.set_fill(GRAY, opacity=1)
        tip.next_to(body, UP, buff=0)
        
        # fins
        fin_right = Polygon(
            [0, 0, 0], [0.5, -0.5, 0], [0.5, -1.2, 0], [0, -1.0, 0], 
            fill_color=BLUE, fill_opacity=1, stroke_color=WHITE
        )
        fin_right.next_to(body, RIGHT, buff=0, aligned_edge=DOWN)
        
        fin_left = fin_right.copy()
        fin_left.flip(UP) # Create symmetrical left fin
        fin_left.next_to(body, LEFT, buff=0, aligned_edge=DOWN)
        
        # Rocket Engine Exhaust (A trapezoid at the bottom)
        engine = Polygon(
            [0, 0, 0], [0.8, 0, 0], [0.6, -0.4, 0], [0.2, -0.4, 0],
            fill_color=LIGHT_GRAY, fill_opacity=1, stroke_color=WHITE
        )
        # Position slightly offset under the body
        engine.next_to(body, DOWN, buff=0) 
        
        # flare (exhaust)
        flare = Triangle()
        flare.scale(0.3)
        #flare.rotate(-PI/2) # Point it down
        flare.set_fill(ORANGE, opacity=0.8)
        flare.set_stroke(YELLOW, width=3)
        flare.next_to(engine, DOWN, buff=0)
        
        flare_label = MathTex(r"M_e", r" = ", r"-\frac{\mathrm{d}M(t)}{\mathrm{d}t}\mathrm{d}t", color=ORANGE, font_size=24)
        
        # combine
        everything_but_flare = VGroup(tip, body, fin_left, fin_right, engine)
        
        # Combine everything into one manageable 'rocket' object
        rocket = VGroup(everything_but_flare, flare)
        
        # layout
        LEFT_COLUMN_CENTER = LEFT * 3.5 + DOWN * 0.5 
        rocket.move_to(LEFT_COLUMN_CENTER)
        flare_label.next_to(flare, LEFT, buff=0.1)
        
        # equation positioning
        eq_block_1.move_to(RIGHT_COLUMN_CENTER)
        eq_block_2.align_to(eq_block_1, LEFT)
        eq_block_2.align_to(eq_block_1, UP)

        # anchor for numerator
        fraction_part = formula_6[3]
        numerator_anchor = MathTex(r"M(t + \mathrm{d}t) - M(t)", font_size=32)
        numerator_anchor.move_to(fraction_part)
        numerator_anchor.align_to(fraction_part, UP)
        numerator_anchor.scale_to_fit_width(fraction_part.width * 0.92)

        numerator_brace = Brace(numerator_anchor, UP, buff=0.05)
        numerator_brace_label = Tex(
            "mass of exhausted fuel",
            font_size=24,
            color=GRAY
        )
        numerator_brace_label.next_to(numerator_brace, UP, buff=0.05)

        fraction_group = VGroup(formula_6[2], formula_6[3], formula_6[4])
        derivative_term = MathTex(
            r"\frac{\mathrm{d}M(t)}{\mathrm{d}t}",
            font_size=32
        )
        derivative_term.move_to(fraction_group)
        derivative_term.align_to(fraction_group, LEFT)

        velocity_vector = Arrow(
            start=ORIGIN, 
            end=UP * 1, 
            color=YELLOW, 
            buff=0,
            max_tip_length_to_length_ratio=0.15
        )
        
        # 2. Get the anchor coordinate from your rocket
        # You can use tip.get_center() or tip.get_top() depending on where 
        # you want the tail of the arrow to originate.
        anchor_point = tip.get_center() 
        
        # 3. Snap the vector to the rocket
        # We tell it to start at the anchor, and end 1 unit above the anchor
        velocity_vector.put_start_and_end_on(
            anchor_point, 
            anchor_point + UP * 1
        )
        
        # Optional: Add a 'v' label next to the tip of the arrow
        v_label = MathTex(r"\vec{v}(t)", r" + \mathrm{d}\vec{v}", color=YELLOW, font_size=32)
        v_label[1].next_to(v_label[0], RIGHT, buff=0.1)
        v_label.next_to(velocity_vector.get_end(), RIGHT, buff=0.1)
        
        # Group them so they appear together
        v_group = VGroup(velocity_vector, v_label)
        
        # exhaust velocity
        exhaust_velocity_vector = Arrow(
            start=ORIGIN, 
            end=DOWN * 0.7, 
            color=GREEN, 
            buff=0,
            max_tip_length_to_length_ratio=0.15
        )
        
        # exhaust anchor
        exhaust_anchor_point = flare.get_center() 
        
        # 3. Snap the vector to the rocket
        # We tell it to start at the anchor, and end 1 unit above the anchor
        exhaust_velocity_vector.put_start_and_end_on(
            exhaust_anchor_point, 
            exhaust_anchor_point + DOWN * 0.7
        )
        
        # label
        v_e_label = MathTex(r"\vec{v}_e", color=GREEN, font_size=32)
        v_e_label_wrt_rocket = MathTex(
            r"\text{w.r.t. rocket: } ",
            r"\vec{v}(t)",
            r" + \mathrm{d}\vec{v}",
            r" - ",
            r"\vec{v}_e",
            color=GREEN, font_size=24
        )
        v_e_label.next_to(exhaust_velocity_vector.get_end(), RIGHT, buff=0.1)
        v_e_label_wrt_rocket.next_to(v_e_label, RIGHT, buff=0.2)
        
        # group them
        v_group = VGroup(exhaust_velocity_vector, v_e_label)

        formula_7 = MathTex(
            r"P|_{t+\mathrm{d}t}", # 0
            r" = ", # 1
            r"M(t+\mathrm{d}t)", # 2 (from formula_6[0])
            r" \cdot ", # 3
            r"\left(", # 4
            r"\vec{v}(t)", # 5 (from v_label[0])
            r" + \mathrm{d}\vec{v}", # 6 (from v_label[1])
            r"\right)", # 7
            r" + ", # 8
            r"\left(", # 9
            r"-\frac{\mathrm{d}M(t)}{\mathrm{d}t}\mathrm{d}t", # 10 (from flare_label[2])
            r"\right)", # 11
            r" \cdot ", # 12
            r"\left(", # 13
            r"\vec{v}(t)", # 14 (from v_e_label_wrt_rocket[1])
            r" + \mathrm{d}\vec{v}", # 15 (from v_e_label_wrt_rocket[2])
            r" - ", # 16 (from v_e_label_wrt_rocket[3])
            r"\vec{v}_e", # 17 (from v_e_label_wrt_rocket[4])
            r"\right)", # 18
            font_size=29
        )
        formula_7.next_to(formula_6, DOWN, aligned_edge=LEFT, buff=0.5)
        
        # animation
        self.play(FadeIn(header_1, shift=UP))
        
        # Pause before showing the problem details
        self.next_slide()
        
        # rocket & equations
        self.play(
            Write(everything_but_flare),
            Write(basic_group, lag_ratio=0.5) # Lag the formula slightly after the label
        )
        
        self.next_slide()
        
        # fuel
        self.play(
            Write(fuel_group)
        )
        
        self.next_slide()
        
        self.play(
            Unwrite(fuel_group)
        )
        self.play(
            Unwrite(formula1[1], lag_ratio=0.5)
        )
        formula1[2].next_to(formula1[0], RIGHT, buff=0.15)
        formula1[3].next_to(formula1[0], DOWN, aligned_edge=LEFT, buff=0.2)
        formula1[4].next_to(formula1[3], DOWN, aligned_edge=LEFT, buff=0.2)
        formula1[5].next_to(formula1[4], DOWN, aligned_edge=LEFT, buff=0.2)
        equation_label_variant.move_to(equation_label, aligned_edge=LEFT)
        
        self.play(
            ReplacementTransform(equation_label, equation_label_variant),
            Write(formula1[2], lag_ratio=0.1),
            Write(formula1[3], lag_ratio=0.2),
            Write(formula1[4], lag_ratio=0.3),
            Write(formula1[5], lag_ratio=0.4)
        )

        self.next_slide()
        
        self.play(
            ReplacementTransform(equation_label_variant, eq2_header),
            FadeOut(eq_block_1),
            FadeOut(formula1[2]),
            FadeOut(formula1[3]),
            FadeOut(formula1[4]),
            FadeOut(formula1[5])
        )
        
        self.play(GrowArrow(velocity_vector), Write(v_label[0]))
        
        self.next_slide()
        
        self.play(
            Write(formula5),
        )
        
        self.next_slide()
        
        self.play(
            Write(eq2_header_2),
        )
        
        self.play(
            Write(v_label[1]),
            Write(formula_6)
        )

        self.next_slide() # Pause before introducing the numerator annotation.

        self.play(
            GrowFromCenter(numerator_brace),
            FadeIn(numerator_brace_label, shift=UP * 0.1)
        )

        self.next_slide() # pause before collapse

        self.play(
            FadeOut(numerator_brace),
            FadeOut(numerator_brace_label),
            TransformMatchingShapes(
                fraction_group,
                derivative_term,
                path_arc=0.12,
                run_time=1.8
            ),
            formula_6[5].animate.next_to(derivative_term, RIGHT, buff=0.06)
        )
        
        self.next_slide() # pause next part
        
        self.play(Write(flare))
        
        self.next_slide() # pause
        
        self.play(GrowArrow(exhaust_velocity_vector), Write(v_e_label))
        
        self.next_slide() # Pause to talk about the exhaust velocity vector and its significance.
        
        self.play(Write(v_e_label_wrt_rocket[0]))
        
        self.play(
            TransformFromCopy(v_label[0], v_e_label_wrt_rocket[1]),
            TransformFromCopy(v_label[1], v_e_label_wrt_rocket[2]),
        )
        
        self.play(
            Write(v_e_label_wrt_rocket[3]),
            TransformFromCopy(v_e_label, v_e_label_wrt_rocket[4])
        )
        
        self.next_slide() # Pause to talk about the relative velocity of the exhaust with respect to the rocket and how it factors into the momentum change.
        
        self.play(Write(flare_label))
        
        self.next_slide() # pause momentum
        
        self.play(
            Write(formula_7[0]),
            Write(formula_7[1])
        )
        
        self.next_slide() # add rocket component
        
        self.play(
            TransformFromCopy(formula_6[0], formula_7[2]),
            Write(formula_7[3]),
            Write(formula_7[4]),
            TransformFromCopy(v_label[0], formula_7[5]),
            TransformFromCopy(v_label[1], formula_7[6]),
            Write(formula_7[7])
        )
        
        self.next_slide() # indicate
        
        rocket_momentum_part = VGroup(*formula_7[2:8])
        rocket_label = Tex("momentum of rocket", font_size=24, color=YELLOW)
        rocket_label.next_to(rocket_momentum_part, DOWN, buff=0.15)
        
        self.play(
            FadeIn(rocket_label, shift=UP*0.1),
            Indicate(rocket_momentum_part)
        )
        
        self.next_slide() # add exhaust
        
        self.play(
            FadeOut(rocket_label),
            Write(formula_7[8]),
            Write(formula_7[9]),
            TransformFromCopy(flare_label[2], formula_7[10]),
            Write(formula_7[11])
        )
        
        self.play(
            Write(formula_7[12]),
            Write(formula_7[13]),
            TransformFromCopy(v_e_label_wrt_rocket[1], formula_7[14]),
            TransformFromCopy(v_e_label_wrt_rocket[2], formula_7[15]),
            TransformFromCopy(v_e_label_wrt_rocket[3], formula_7[16]),
            TransformFromCopy(v_e_label_wrt_rocket[4], formula_7[17]),
            Write(formula_7[18])
        )
        
        self.next_slide() # indicate exhaust
        
        exhaust_momentum_part = VGroup(*formula_7[9:19])
        exhaust_label = Tex("momentum of exhaust", font_size=24, color=GREEN)
        exhaust_label.next_to(exhaust_momentum_part, DOWN, buff=0.15)
        
        self.play(
            FadeIn(exhaust_label, shift=UP*0.1),
            Indicate(exhaust_momentum_part)
        )
        
        self.next_slide() # conservation
        
        conservation_label = Tex(
            r"Let's write down momentum change: $P|_{t+\mathrm{d}t} - P|_{t} = -M(t)\vec{g}\mathrm{d}t$",
            font_size=28,
            color=YELLOW
        )
        conservation_label.next_to(formula_7, DOWN, buff=0.7)
        
        self.play(
            FadeOut(exhaust_label),
            FadeIn(conservation_label, shift=UP*0.1)
        )
        
        self.next_slide() # final eq
        
        final_eq = MathTex(
            r"-M(t)\vec{g}\mathrm{d}t", # 0
            r" = ", # 1
            r"\left(", # 2
            r"M(t)", # 3
            r" + ", # 4
            r"\frac{\mathrm{d}M(t)}{\mathrm{d}t}\mathrm{d}t", # 5
            r"\right)", # 6
            r" \cdot ", # 7
            r"\left(", # 8
            r"\vec{v}(t)", # 9
            r" + \mathrm{d}\vec{v}", # 10
            r"\right)", # 11
            r" + ", # 12
            r"\left(", # 13
            r"-\frac{\mathrm{d}M(t)}{\mathrm{d}t}\mathrm{d}t", # 14
            r"\right)", # 15
            r" \cdot ", # 16
            r"\left(", # 17
            r"\vec{v}(t)", # 18
            r" + \mathrm{d}\vec{v}", # 19
            r" - ", # 20
            r"\vec{v}_e", # 21
            r"\right)", # 22
            r" - M(t) \cdot \vec{v}(t)", # 23
            font_size=28
        )
        final_eq.next_to(header_1, DOWN, aligned_edge=LEFT, buff=1.0)
        
        # In case the equation is too long to fit horizontally even when left-aligned,
        # we can scale it down if its width exceeds a certain threshold, or just scale it
        # generally slightly smaller so it fits completely within the scene bounds.
        final_eq.scale_to_fit_width(min(final_eq.width, config.frame_width - 1.0))
        # Re-align after potential scaling
        final_eq.next_to(header_1, DOWN, aligned_edge=LEFT, buff=1.0)
        
        fade_out_group = VGroup(
            everything_but_flare, flare, flare_label,
            velocity_vector, v_label, exhaust_velocity_vector, v_e_label, v_e_label_wrt_rocket,
            eq2_header, formula5[0], formula5[1], eq2_header_2,
            formula_6[0], formula_6[1], derivative_term, formula_6[5],
            formula_7[0], formula_7[1], formula_7[2], conservation_label
        )
        
        self.play(
            FadeOut(fade_out_group),
            ReplacementTransform(formula5[2], final_eq[0]),
            Write(final_eq[1]),
            Write(final_eq[2]), # left paren
            ReplacementTransform(formula_6[2], final_eq[3]), # M(t)
            Write(final_eq[4]), # +
            ReplacementTransform(formula_6[3], final_eq[5]), # dM/dt dt part
            ReplacementTransform(formula_6[4], final_eq[5]), # this and previous is from Taylor expansion
            Write(final_eq[6]), # right paren
            *[ReplacementTransform(formula_7[i], final_eq[i+4]) for i in range(3, 19)]
        )
        
        self.next_slide() # Introduce second line, expanding brackets
        
        # Second line equation
        final_eq_2 = MathTex(
            r"M(t) \cdot \vec{v}(t)", # 0
            r" = ", # 1
            r"M(t)", # 2
            r"\vec{v}(t)", # 3
            r" + M(t)", # 4
            r"\mathrm{d}\vec{v}", # 5
            r" + ", # 6
            r"\frac{\mathrm{d}M(t)}{\mathrm{d}t}\mathrm{d}t", # 7
            r"\vec{v}(t)", # 8
            r" + ", # 9
            r"\frac{\mathrm{d}M(t)}{\mathrm{d}t}\mathrm{d}t", # 10
            r"\mathrm{d}\vec{v}", # 11
            r" - ", # 12
            r"\frac{\mathrm{d}M(t)}{\mathrm{d}t}\mathrm{d}t", # 13
            r"\vec{v}(t)", # 14
            r" - ", # 15
            r"\frac{\mathrm{d}M(t)}{\mathrm{d}t}\mathrm{d}t", # 16
            r"\mathrm{d}\vec{v}", # 17
            r" + ", # 18
            r"\frac{\mathrm{d}M(t)}{\mathrm{d}t}\mathrm{d}t", # 19
            r"\vec{v}_e", # 20
            font_size=28
        )
        final_eq_2.next_to(final_eq, DOWN, aligned_edge=LEFT, buff=0.5)
        final_eq_2.scale_to_fit_width(min(final_eq_2.width, config.frame_width - 1.0))
        final_eq_2.next_to(final_eq, DOWN, aligned_edge=LEFT, buff=0.5)
        
        self.play(
            Write(final_eq_2[0]),
            Write(final_eq_2[1])
        )
        
        self.next_slide() # Expand first bracket
        
        self.play(
            TransformFromCopy(final_eq[3], final_eq_2[2]),
            TransformFromCopy(final_eq[9], final_eq_2[3])
        )
        self.play(
            TransformFromCopy(final_eq[3], final_eq_2[4][1:]), # M(t)
            Write(final_eq_2[4][0]), # +
            TransformFromCopy(final_eq[10], final_eq_2[5])
        )
        self.play(
            Write(final_eq_2[6]), # +
            TransformFromCopy(final_eq[5], final_eq_2[7]),
            TransformFromCopy(final_eq[9], final_eq_2[8])
        )
        self.play(
            Write(final_eq_2[9]), # +
            TransformFromCopy(final_eq[5], final_eq_2[10]),
            TransformFromCopy(final_eq[10], final_eq_2[11])
        )
        
        self.next_slide() # Expand second bracket (exhaust mass)
        
        # Notice how final_eq[14] is the whole negative fraction
        self.play(
            Write(final_eq_2[12]), # -
            TransformFromCopy(final_eq[14][1:], final_eq_2[13]), # skip the - inside the copied element
            TransformFromCopy(final_eq[18], final_eq_2[14])
        )
        self.play(
            Write(final_eq_2[15]), # -
            TransformFromCopy(final_eq[14][1:], final_eq_2[16]),
            TransformFromCopy(final_eq[19], final_eq_2[17])
        )
        self.play(
            Write(final_eq_2[18]), # + (two negatives make a positive)
            TransformFromCopy(final_eq[14][1:], final_eq_2[19]),
            TransformFromCopy(final_eq[21], final_eq_2[20])
        )
        
        self.next_slide() # Highlight and cancel M(t)v(t)
        
        self.play(
            Indicate(final_eq_2[0], color=RED),
            Indicate(VGroup(final_eq_2[2], final_eq_2[3]), color=RED)
        )
        cross_1 = Cross(final_eq_2[0])
        cross_2 = Cross(VGroup(final_eq_2[2], final_eq_2[3]))
        self.play(Create(cross_1), Create(cross_2))
        
        self.next_slide() # Highlight and cancel (dM/dt)dt v(t)
        
        term_pos_v = VGroup(final_eq_2[6], final_eq_2[7], final_eq_2[8])
        term_neg_v = VGroup(final_eq_2[12], final_eq_2[13], final_eq_2[14])
        self.play(
            Indicate(term_pos_v, color=BLUE),
            Indicate(term_neg_v, color=BLUE)
        )
        cross_3 = Cross(term_pos_v)
        cross_4 = Cross(term_neg_v)
        self.play(Create(cross_3), Create(cross_4))
        
        self.next_slide() # Highlight and cancel (dM/dt)dt dv
        
        term_pos_dv = VGroup(final_eq_2[9], final_eq_2[10], final_eq_2[11])
        term_neg_dv = VGroup(final_eq_2[15], final_eq_2[16], final_eq_2[17])
        self.play(
            Indicate(term_pos_dv, color=ORANGE),
            Indicate(term_neg_dv, color=ORANGE)
        )
        cross_5 = Cross(term_pos_dv)
        cross_6 = Cross(term_neg_dv)
        self.play(Create(cross_5), Create(cross_6))
        
        self.next_slide() # Construct final simplifed line 3
        
        final_eq_3 = MathTex(
            r"0", # 0
            r" = ", # 1
            r"M(t)", # 2
            r"\mathrm{d}\vec{v}", # 3
            r" + ", # 4
            r"\frac{\mathrm{d}M(t)}{\mathrm{d}t}\mathrm{d}t", # 5
            r"\vec{v}_e", # 6
            font_size=28
        )
        final_eq_3.next_to(final_eq_2, DOWN, aligned_edge=LEFT, buff=0.5)
        
        self.play(
            Write(final_eq_3[0]),
            TransformFromCopy(final_eq_2[1], final_eq_3[1])
        )
        self.play(
            TransformFromCopy(final_eq_2[4][1:], final_eq_3[2]),
            TransformFromCopy(final_eq_2[5], final_eq_3[3]),
            TransformFromCopy(final_eq_2[18], final_eq_3[4]),
            TransformFromCopy(final_eq_2[19], final_eq_3[5]),
            TransformFromCopy(final_eq_2[20], final_eq_3[6])
        )
        
        self.next_slide() # Clean up to make room
        
        clean_group = VGroup(final_eq, final_eq_2, cross_1, cross_2, cross_3, cross_4, cross_5, cross_6)
        self.play(
            FadeOut(clean_group),
            final_eq_3.animate.next_to(header_1, DOWN, aligned_edge=LEFT, buff=1.0)
        )
        
        self.next_slide() # Multiply by 1/dt
        
        operation_1 = Tex(r"$/ \cdot \frac{1}{\mathrm{d}t}$", font_size=24, color=YELLOW)
        operation_1.next_to(final_eq_3, RIGHT, buff=0.5)
        
        self.play(Write(operation_1))
        
        final_eq_4 = MathTex(
            r"0", # 0
            r" = ", # 1
            r"M(t)", # 2
            r"\frac{\mathrm{d}\vec{v}}{\mathrm{d}t}", # 3
            r" + ", # 4
            r"\frac{\mathrm{d}M(t)}{\mathrm{d}t}", # 5
            r"\vec{v}_e", # 6
            font_size=28
        )
        final_eq_4.next_to(final_eq_3, DOWN, aligned_edge=LEFT, buff=0.5)
        
        self.play(
            TransformFromCopy(final_eq_3[0], final_eq_4[0]),
            TransformFromCopy(final_eq_3[1], final_eq_4[1]),
            TransformFromCopy(final_eq_3[2], final_eq_4[2]),
            TransformFromCopy(final_eq_3[3], final_eq_4[3]),
            TransformFromCopy(final_eq_3[4], final_eq_4[4]),
            TransformFromCopy(final_eq_3[5], final_eq_4[5]),
            TransformFromCopy(final_eq_3[6], final_eq_4[6])
        )
        
        self.next_slide() # Multiply by 1/M(t)
        
        operation_2 = Tex(r"$/ \cdot \frac{1}{M(t)}$", font_size=24, color=YELLOW)
        operation_2.next_to(final_eq_4, RIGHT, buff=0.5)
        
        self.play(Write(operation_2))
        
        final_eq_5 = MathTex(
            r"0", # 0
            r" = ", # 1
            r"\frac{\mathrm{d}\vec{v}}{\mathrm{d}t}", # 2
            r" + ", # 3
            r"\frac{1}{M(t)}", # 4
            r"\frac{\mathrm{d}M(t)}{\mathrm{d}t}", # 5
            r"\vec{v}_e", # 6
            font_size=28
        )
        final_eq_5.next_to(final_eq_4, DOWN, aligned_edge=LEFT, buff=0.5)
        
        self.play(
            TransformFromCopy(final_eq_4[0], final_eq_5[0]),
            TransformFromCopy(final_eq_4[1], final_eq_5[1]),
            TransformFromCopy(final_eq_4[3], final_eq_5[2]), # M(t) vanishes, dv/dt falls down
            TransformFromCopy(final_eq_4[4], final_eq_5[3]),
            Write(final_eq_5[4]), # New 1/M(t) term
            TransformFromCopy(final_eq_4[5], final_eq_5[5]),
            TransformFromCopy(final_eq_4[6], final_eq_5[6])
        )
        
        self.next_slide() # Rearrange to final form
        
        final_eq_6 = MathTex(
            r"\frac{\mathrm{d}\vec{v}}{\mathrm{d}t}", # 0
            r" = ", # 1
            r"-", # 2
            r"\frac{1}{M(t)}", # 3
            r"\frac{\mathrm{d}M(t)}{\mathrm{d}t}", # 4
            r"\vec{v}_e", # 5
            font_size=36,
            color=YELLOW
        )
        final_eq_6.next_to(final_eq_5, DOWN, aligned_edge=LEFT, buff=0.7)
        
        self.play(
            TransformFromCopy(final_eq_5[2], final_eq_6[0]),
            TransformFromCopy(final_eq_5[1], final_eq_6[1]),
            Write(final_eq_6[2]), # Dropping in the negative sign
            TransformFromCopy(final_eq_5[4], final_eq_6[3]),
            TransformFromCopy(final_eq_5[5], final_eq_6[4]),
            TransformFromCopy(final_eq_5[6], final_eq_6[5])
        )
        
        box = SurroundingRectangle(final_eq_6, color=WHITE, buff=0.2)
        final_label = Tex("Final differential equation of velocity", font_size=24, color=YELLOW)
        final_label.next_to(box, DOWN, buff=0.3)
        self.play(Create(box), FadeIn(final_label, shift=UP*0.1))

        self.next_slide()
        
        transition_text = Tex("Before solving this complex ODE, let's look at numerical methods on a simpler test equation.", font_size=24, color=GRAY)
        transition_text.to_edge(DOWN)
        self.play(FadeIn(transition_text))