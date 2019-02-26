#Peter Grajcar
#IV.C
#2017/2018
from getch_alt import *

ENTER = 0
SPACE = 1
ARROW_R = 2
ARROW_L = 3
ARROW_U = 4
ARROW_D = 5

def get_key():
    first = ord(getch())
    if first == 32:
        return SPACE
    elif first == 10:
        return ENTER
    elif first == 27 and ord(getch()) == 91:
        third = ord(getch())
        if third == 67:
            return ARROW_R
        elif third == 68:
            return ARROW_L
        elif third == 65:
            return ARROW_U
        elif third == 66:
            return ARROW_D
    else:
        return -1
