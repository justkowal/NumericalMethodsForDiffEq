from manim import *
from manim_slides import Slide
from title import TitleCard
from problem import ProblemDemonstration
from euler import EulerMethod
from rk4 import RungeKutta4
from rk4_explain import RK4Derivation
from rk4_landscape import RK4_Error_Landscape

from application import ApplicationExample
from application_stm import STM32Application
from closing_nummeth import WhyNumericalMethods
from application_realtime import HardwareBenchmarks
import csv
import os
import numpy as np

class NumericalMethodsPresentation(Slide):
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
        self.wait_time_between_slides = 0.1
        self.skip_reversing = True
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
        
        # rk4 landscape
        RK4_Error_Landscape.construct(self)

        self.next_slide()
        do_wipe()
        
        # application example
        ApplicationExample.construct(self)

        self.next_slide()
        do_wipe()

        # STM32 application section
        STM32Application.construct(self)

        self.next_slide()
        do_wipe()
        
        HardwareBenchmarks.construct(self)

        self.next_slide()
        do_wipe()
    
        # Closing: Why Numerical Methods?
        WhyNumericalMethods.construct(self)