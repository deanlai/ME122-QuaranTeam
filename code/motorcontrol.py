# motorcontrol.py -- controls motors for ME122 robot arm using gpiozero and
# curses libraries

import gpiozero as gz
import curses

# Constants
BASE_HI, BASE_LOW = 11, 13 
ELBOW1_HI, ELBOW1_LOW = 19, 20
ELBOW2_HI, ELBOW2_LOW = 13, 16
CLAW_HI, CLAW_LOW = 5, 6

# Functions
def setupCurses():
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)
    return screen

def closeCurses():
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()

def setupMotors():
    base = gz.Motor(BASE_HI, BASE_LOW)
    elbow1 = gz.Motor(ELBOW1_HI, ELBOW1_LOW)
    elbow2 = gz.Motor(ELBOW2_HI, ELBOW2_LOW)
    claw = gz.Motor(CLAW_HI, CLAW_LOW)
    return base, elbow1, elbow2, claw

def dummySetupMotors():
    return DummyMotor(), DummyMotor(), DummyMotor(), DummyMotor()

class DummyMotor():

    def __init__(self):
        pass

    def forward(self):
        return 0

    def backward(self):
        return 0


screen = setupCurses()
base, elbow1, elbow2, claw = setupMotors()

try:
    while True:
        char = screen.getch()
        if char == ord('q'):
            break
        elif char == ord('a'):
            base.forward()
            print('base --> left')

        elif char == ord('d'):
            base.backward()
            print('base --> right')

        elif char == ord('s'):
            elbow1.forward()
            print('elbow1 --> down')

        elif char == ord('w'):
            base.backward()
            print('elbow1 --> up')

        elif char == ord('k'):
            base.forward()
            print('elbow2 --> down')

        elif char == ord('i'):
            base.backward()
            print('elbow2 --> up')

        elif char == ord('j'):
            base.forward()
            print('claw --> open')

        elif char == ord('l'):
            base.backward()
            print('claw --> close')

finally:
    closeCurses()

