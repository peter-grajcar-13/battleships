###############################################
#### !NEMUSI SPRAVNE FUNGOVAT NA WINDOWS ! ####
#### !   KVOLI PODPORE ANSI SEKVENCII    ! ####
###############################################
#Peter Grajcar
#IV.C
#2017/2018
from ansi_utils import *
from controller import *
import random
import time

#constants
FIELD_SIZE = 10

#defines the shape of each type
SHIP_TYPE = [
    [ [1],
      [1] ],
    [ [1],
      [1],
      [1] ],
    [ [0, 1, 0],
      [1, 1, 1],
      [0, 1, 0] ]
]
#defines the count of each type available to the player
SHIP_COUNT = [2, 2, 1]
#maximum number of hits that can be done
MAX_HITS = 15


#initialize lists
field1 = [ [0]*FIELD_SIZE for x in range(FIELD_SIZE) ]
field2 = [ [0]*FIELD_SIZE for x in range(FIELD_SIZE) ]
shots1 = [ [0]*FIELD_SIZE for x in range(FIELD_SIZE) ]
shots2 = [ [0]*FIELD_SIZE for x in range(FIELD_SIZE) ]
hits1 = 0
hits2 = 0


def display(message="", error=""):
    #print logo
    offset = 21*" "
    print("\033[35;1m" + offset + " _  _ ______    __ __   ___ _  __\n" + offset + "|_)|_| |  | |  |_ (_ |_| | |_)(_\n" + offset + "|_)| | |  | |__|____)| |_|_|  __)\033[0m")

    #prints player1's table label
    ansi_print(15, 7, "Player 1", color=GREEN)
    #prints player2's table label
    ansi_print(55, 7, "Player 2", color=RED)

    #messages
    ansi_print(38 - len(message)//2, 20, message, color=GREEN)
    ansi_print(38 - len(error)//2, 22, error, color=RED)

    #controls
    ansi_print(27, 24, "(Use arrows and space)")

    #prints "A B C D E F G H" table header row
    for x in range(FIELD_SIZE):
        #for player 1
        ansi_print(10 + x*2, 8, chr(65+x), bold=True )
        #for player 2
        ansi_print(50 + x*2, 8, chr(65+x), bold=True )

    #prints "1 2 3 4 5 6 7 8" table header column
    for y in range(FIELD_SIZE):
        #for player 1
        ansi_print(8, 9 + y, y, bold=True )
        #for player 2
        ansi_print(48, 9 + y, y, bold=True )

    #fills in the table with data
    for y in range(FIELD_SIZE):
        for x in range(FIELD_SIZE):
            #for player 1
            #water
            if field1[y][x] == 0:
                if shots2[y][x] != 0:
                    ansi_print(10 + x*2, 9 + y, "~", color=RED)
                else:
                    ansi_print(10 + x*2, 9 + y, "~", color=BLUE)
            else:
                #print destroyed ship
                if shots2[y][x] != 0:
                    ansi_print(10 + x*2, 9 + y, "*", color=RED, bold=True)
                #print undestroyed ship
                else:
                    ansi_print(10 + x*2, 9 + y, "*", color=GREEN, bold=True)

            #for player 2
            #display only the squares which were shoot
            if shots1[y][x] != 0:
                #water
                if field2[y][x] == 0:
                    ansi_print(50 + x*2, 9 + y, "~", color=RED)
                #destroyed ship
                else:
                    ansi_print(50 + x*2, 9 + y, "*", color=RED, bold=True)
            #unknown field
            else:
                ansi_print(50 + x*2, 9 + y, "~", color=BLUE)

msg = ""
err = ""
clear_screen()
display()

#player 1 placing ships
cursor_x, cursor_y = 0, 0
ship = 0
counter = 0
while True:
    msg = "Place your ships!"
    clear_screen()
    display(message=msg, error=err)

    ship_h = len(SHIP_TYPE[ship])
    ship_w = len(SHIP_TYPE[ship][0])
    #draw ship
    for y in range(ship_h):
        for x in range(ship_w):
            if SHIP_TYPE[ship][y][x] == 0:
                ansi_print(10 + (cursor_x + x)*2, 9 + cursor_y + y, "~", color=BLUE)
            else:
                ansi_print(10 + (cursor_x + x)*2, 9 + cursor_y + y, "*", color=GREEN)

    pressed = get_key()
    if pressed == ARROW_R and cursor_x < FIELD_SIZE - ship_w:
        cursor_x += 1
    elif pressed == ARROW_L and cursor_x > 0:
        cursor_x -= 1
    elif pressed == ARROW_U and cursor_y > 0:
        cursor_y -= 1
    elif pressed == ARROW_D and cursor_y < FIELD_SIZE - ship_h:
        cursor_y += 1
    elif pressed == SPACE:
        #check if position is valid
        valid = True
        for y in range(ship_h+2):
            for x in range(ship_w+2):
                if cursor_y - 1 + y > 0 and cursor_y - 1 + y < FIELD_SIZE-1 and cursor_x - 1 + x > 0 and cursor_x - 1 + x < FIELD_SIZE-1:
                    if field1[cursor_y - 1 + y][cursor_x - 1 + x] != 0:
                        valid = False
        #put ship into the field
        if valid:
            err = ""
            for y in range(ship_h):
                for x in range(ship_w):
                    if SHIP_TYPE[ship][y][x] == 1:
                        field1[cursor_y + y][cursor_x + x] = 1
            counter += 1
            if counter == SHIP_COUNT[ship]:
                ship += 1
                counter = 0
            if ship == len(SHIP_TYPE):
                break
            cursor_x, cursor_y = 0, 0
        else:
            err = "Invalid position!"

#player 2 placing ships
ship = 0
counter = 0
while True:
    ship_h = len(SHIP_TYPE[ship])
    ship_w = len(SHIP_TYPE[ship][0])
    cursor_x = random.randrange(FIELD_SIZE + 1 - ship_w)
    cursor_y = random.randrange(FIELD_SIZE + 1 - ship_h)

    #check if position is valid
    valid = True
    for y in range(ship_h+2):
        for x in range(ship_w+2):
            if cursor_y - 1 + y > 0 and cursor_y - 1 + y < FIELD_SIZE-1 and cursor_x - 1 + x > 0 and cursor_x - 1 + x < FIELD_SIZE-1:
                if field2[cursor_y - 1 + y][cursor_x - 1 + x] != 0:
                    valid = False
    #put ship into the field
    if valid:
        for y in range(ship_h):
            for x in range(ship_w):
                if SHIP_TYPE[ship][y][x] == 1:
                    field2[cursor_y + y][cursor_x + x] = 1
        counter += 1
        if counter == SHIP_COUNT[ship]:
            ship += 1
            counter = 0
        if ship == len(SHIP_TYPE):
            break

msg = ""

#shooting
while True:
    cursor_x, cursor_y = 0, 0
    while True:
        #player 1's part
        msg = "It's Player 1's turn!"
        clear_screen()
        display(message=msg, error=err)

        #print the red crosshair
        ansi_print(50 + cursor_x*2 - 1, 9 + cursor_y, "[+]", color=RED)

        pressed = get_key()
        if pressed == ARROW_R and cursor_x < FIELD_SIZE - 1:
            cursor_x += 1
        elif pressed == ARROW_L and cursor_x > 0:
            cursor_x -= 1
        elif pressed == ARROW_U and cursor_y > 0:
            cursor_y -= 1
        elif pressed == ARROW_D and cursor_y < FIELD_SIZE - 1:
            cursor_y += 1
        elif pressed == SPACE:
            if shots1[cursor_y][cursor_x] == 0:
                err = ""
                #make cool sound
                ansi_print(0, 0, "\a")

                if field2[cursor_y][cursor_x] != 0:
                    shots1[cursor_y][cursor_x] = 2

                    clear_screen()
                    display(message=msg, error=err)
                    ansi_print(0, 0, "\a\a\a")
                    time.sleep(1)
                    hits1 += 1
                else:
                    shots1[cursor_y][cursor_x] = 1
                break
            else:
                err = "This square was already hit!"

    if hits1 == MAX_HITS:
        break

    #player 2's part
    msg = "It's Player 2's turn!"
    clear_screen()
    display(message=msg, error=err)
    time.sleep(.5)

    cursor_x, cursor_y = 0, 0

    #generate random destination which has not been hit already
    dest_x = random.randrange(FIELD_SIZE)
    dest_y = random.randrange(FIELD_SIZE)
    while shots2[dest_y][dest_x] != 0:
        dest_x = random.randrange(FIELD_SIZE)
        dest_y = random.randrange(FIELD_SIZE)

    ansi_print(10 + cursor_x*2 - 1, 9 + cursor_y, "[+]", color=RED)
    #move cursor hoizontally
    for i in range(dest_x):
        cursor_x += 1

        time.sleep(.3)
        clear_screen()
        display(message=msg, error=err)

        #print the red crosshair
        ansi_print(10 + cursor_x*2 - 1, 9 + cursor_y, "[+]", color=RED)
    #move cursor vertically
    for i in range(dest_y):
        cursor_y += 1

        time.sleep(.3)
        clear_screen()
        display(message=msg, error=err)

        #print the red crosshair
        ansi_print(10 + cursor_x*2 - 1, 9 + cursor_y, "[+]", color=RED)

    time.sleep(.5)

    #make badass sound
    ansi_print(0, 0, "\a")

    if field1[cursor_y][cursor_x] != 0:
        shots2[cursor_y][cursor_x] = 2

        ansi_print(0, 0, "\a\a\a")
        hits2 += 1
    else:
        shots2[cursor_y][cursor_x] = 1

    clear_screen()
    display(message=msg, error=err)
    time.sleep(1)


    if hits2 == MAX_HITS:
        break

    time.sleep(.5)

clear_screen()
display()
if hits1 == MAX_HITS:
    ansi_print(35, 13, "YOU WON!", color=GREEN, bold=True)
if hits2 == MAX_HITS:
    ansi_print(34, 13, "YOU LOST!", color=RED, bold=True)

#end
ansi_print(0,30,"")
