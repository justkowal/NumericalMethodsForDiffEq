from manim import *

TEXT_SIZE_HEADER = 32
TEXT_SIZE_BODY = 24
TEXT_SIZE_SUB = 24
TEXT_SIZE_MATH = 28

COLORS = {
    "exact_solution": WHITE,
    "forward_euler": BLUE,
    "backward_euler": RED,
    "rk4": GREEN,
    "highlight": YELLOW,
    "k1": ORANGE,
    "k2": TEAL,
    "k3": PURPLE,
    "k4": MAROON
}

def create_header(text):
    return Text(text, font_size=TEXT_SIZE_HEADER).to_corner(UL)