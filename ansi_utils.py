#Peter Grajcar
#IV.C
#2017/2018
#functions and constants for
#ANSI sequence formatting

BLACK = 30
RED = 31
GREEN = 32
YELLOW = 33
BLUE = 34
MAGENTA = 35
CYAN = 36
WHITE = 37

def ansi_print(x, y, text, color=WHITE, bold=False):
    print("\033[" + str(y) + ";" + str(x) + "H" +
            "\033[" + str(color) + (";1" if bold else "") + "m" +
            str(text) +
            "\033[0m" +
            "\033[23;0H"
            )

def clear_screen():
    print("\033c")
