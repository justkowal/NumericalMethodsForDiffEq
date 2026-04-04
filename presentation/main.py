from manim import *
from manim_slides import Slide
from title import TitleCard
from problem import ProblemDemonstration
from euler import EulerMethod
from rk4 import RungeKutta4
from rk4_explain import RK4Derivation
from rk4_landscape import RK4_Error_Landscape
from application import ApplicationExample

class NumericalMethodsPresentation(Slide):
    def construct(self):
        def do_wipe():
            if self.mobjects:
                self.wipe(self.mobjects, [])

        # title
        TitleCard.construct(self)
        do_wipe()
        
        # problem
        ProblemDemonstration.construct(self)
        
        self.next_slide()
        do_wipe()
        
        # euler
        EulerMethod.construct(self)
        
        self.next_slide()
        do_wipe()
        
        # rk4
        RungeKutta4.construct(self)
        
        self.next_slide()
        do_wipe()
        
        # rk4 derivation
        RK4Derivation.construct(self)
        
        self.next_slide()
        do_wipe()
        
        # application example
        ApplicationExample.construct(self)

        self.next_slide()
        do_wipe()
        
        # rk4 landscape
        RK4_Error_Landscape.construct(self)