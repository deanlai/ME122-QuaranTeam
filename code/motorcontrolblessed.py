# motorcontrol.py -- controls motors for ME122 robot arm using gpiozero and

import gpiozero as gz
from blessed import Terminal

# Constants
BASE_HI, BASE_LOW = 11, 13 
ELBOW1_HI, ELBOW1_LOW = 19, 20
ELBOW2_HI, ELBOW2_LOW = 27, 16
CLAW_HI, CLAW_LOW = 5, 6

# Classes
# Functions
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
        print('forward')

    def backward(self):
        print('backward')

    def stop(self):
        pass

def runMotors(key, motors, motorKeys):
    for motor in motors:
        if key in  motorKeys[motor]:
            if motorKeys[motor][key] == 1:
                motor.forward()
            else:
                motor.backward()

def stopMotors(motors):
    for motor in motors:
        motor.stop()
    print('stop')


term = Terminal()
base, elbow1, elbow2, claw = setupMotors()
motors = [base, elbow1, elbow2, claw]
motorKeys = {base: {'a': 1, 'd': 0},
             elbow1: {'w': 1, 's': 0},
             elbow2: {'i': 1, 'k': 0},
             claw: {'j': 1, 'l': 0}}


print(f"{term.home}{term.moccasin_on_gray25}{term.clear}")
print(f"{term.move_down(2)}{term.moccasin_on_gray25}")

with term.cbreak():
    val = ''
    while val.lower() != 'q':
        val = term.inkey(timeout=0)
        if val != '':
            if val != 't':
                print(f"You pressed {val}")
                runMotors(val, motors, motorKeys)
            else:
                stopMotors(motors)
    print(f"Closing...{term.normal}")
