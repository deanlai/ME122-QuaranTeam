# motorcontrol.py -- controls motors for ME122 robot arm using gpiozero and

import gpiozero as gz
from blessed import Terminal

# Constants
BASE_HI, BASE_LOW = 11, 13 
ELBOW1_HI, ELBOW1_LOW = 19, 20
ELBOW2_HI, ELBOW2_LOW = 27, 16
CLAW_HI, CLAW_LOW = 5, 6

# Functions
def setupMotors():
    base = gz.Motor(BASE_HI, BASE_LOW, pwm=True)
    elbow1 = gz.Motor(ELBOW1_HI, ELBOW1_LOW, pwm=True)
    elbow2 = gz.Motor(ELBOW2_HI, ELBOW2_LOW, pwm=True)
    claw = gz.Motor(CLAW_HI, CLAW_LOW, pwm=True)
    return base, elbow1, elbow2, claw

def dummySetupMotors():
    return DummyMotor(), DummyMotor(), DummyMotor(), DummyMotor()

def runMotors(key, motors, motorKeys):
    print(f"You pressed {key}. ", end="")
    for motor in motors:
        if key in motorKeys[motor]:
            if motorKeys[motor][key] == 0:
                printMotorControlString(key, motorKeys, motor, 0)
                motor.forward(speed=.25)
            elif motorKeys[motor][key] == 1:
                printMotorControlString(key, motorKeys, motor, 1)
                motor.backward(speed=.25)
    print("")


def printMotorControlString(key, motorKeys, motor, direction):
    print(f"{motorKeys[motor]['name']} --> {motorKeys[motor]['directions'][direction]}", end="")


def stopMotors(motors):
    for motor in motors:
        motor.stop()
    print('stop')

def showProgramGreeting():
    print(f"{term.home}{term.moccasin_on_gray25}{term.clear}")
    print(term.gray25_on_moccasin(term.center('QUARANTEAM ARM CONTROL')))
    print(term.gray25_on_moccasin(term.center('Press WASD and IJKL to control arm, T to stop motors')))
    print(term.gray25_on_moccasin(term.center('Press Q to quit')))
    print(f"{term.move_down(2)}{term.moccasin_on_gray25}")

# Classes
class DummyMotor():

    def __init__(self):
        pass

    def forward(self, speed):
        pass

    def backward(self, speed):
        pass

    def stop(self):
        pass


base, elbow1, elbow2, claw = dummySetupMotors()
motors = [base, elbow1, elbow2, claw]
motorKeys = {base: {'a': 0, 'd': 1, 'name': 'base', 'directions': ['left', 'right']},
             elbow1: {'w': 0, 's': 1, 'name': 'elbow1', 'directions': ['up', 'down']},
             elbow2: {'i': 0, 'k': 1, 'name': 'elbow2', 'directions': ['up', 'down']},
             claw: {'j': 0, 'l': 1, 'name': "claw", 'directions': ['open', 'closed']}}

term = Terminal()
showProgramGreeting()

with term.cbreak():
    val = ''
    while val.lower() != 'q':
        val = term.inkey(timeout=0)
        if val != '':
            if val != 't':
                runMotors(val, motors, motorKeys)
            else:
                stopMotors(motors)
    print(f"Closing...{term.normal}")
