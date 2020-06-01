# ME122 Quaranteam spring '20 group project
# motorcontrol.py -- controls motors for a raspi robot arm from the terminal 
# using gpiozero and blessed libraries

import gpiozero as gz
from blessed import Terminal
from time import sleep

# Pin setup
BASE_HI, BASE_LOW = 11, 13 
ELBOW1_HI, ELBOW1_LOW = 27, 16
ELBOW2_HI, ELBOW2_LOW = 19, 20
CLAW_HI, CLAW_LOW = 5, 6

# Time step and speed tuning for each joint
BASE_SPEED = 0.25
ELBOW1_SPEED = 0.25
ELBOW2_SPEED = 0.25
CLAW_SPEED = 0.25
TIME_STEP = 0.2


# Functions
def setupMotors():
    base = gz.Motor(BASE_HI, BASE_LOW, pwm=True)
    elbow1 = gz.Motor(ELBOW1_HI, ELBOW1_LOW, pwm=True)
    elbow2 = gz.Motor(ELBOW2_HI, ELBOW2_LOW, pwm=True)
    claw = gz.Motor(CLAW_HI, CLAW_LOW, pwm=True)
    return base, elbow1, elbow2, claw

def setupDummyMotors():
    return DummyMotor(), DummyMotor(), DummyMotor(), DummyMotor()

def runMotors(key, motors, motorKeys):
    for motor in motors:
        if key in motorKeys[motor]:
            if motorKeys[motor][key] == 0:
                printMotorControlString(motorKeys, motor, 0)
                motor.forward(speed=motorKeys[motor]['speed'])
                sleep(TIME_STEP)
                stopMotors()
            elif motorKeys[motor][key] == 1:
                printMotorControlString(motorKeys, motor, 1)
                motor.backward(speed=motorKeys[motor]['speed'])
                sleep(TIME_STEP)
                stopMotors()

def stopMotors(motors):
    for motor in motors:
        motor.stop()
    print(term.center('Stop all motors'))

def printMotorControlString(motorKeys, motor, direction):
    motorString = f"{motorKeys[motor]['name']} --> {motorKeys[motor]['directions'][direction]}"
    print(term.center(motorString))

def printNewCommandString(key):
    print(term.clear_eos)
    commandString = f"You pressed {key}"
    print(term.center(commandString))

def resetTerminalLine():
    print(f"{term.home}{term.move_down(5)}")

def showProgramGreeting():
    print(f"{term.home}{term.moccasin_on_gray25}{term.clear}")
    print(term.gray25_on_moccasin(term.center('QUARANTEAM ARM CONTROL')))
    print(term.gray25_on_moccasin(term.center('Press WASD and IJKL to control arm, T to stop motors')))
    print(term.gray25_on_moccasin(term.center('Press Q to quit')))
    print(f"{term.move_down(1)}{term.moccasin_on_gray25}")

def closeTerminal():
    print(term.clear_eos)
    closeString = f"Closing...{term.normal}"
    print(term.gray25_on_moccasin(term.center(closeString)))
    term.move_down()

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

# Motor setup
base, elbow1, elbow2, claw = setupDummyMotors()
motors = [base, elbow1, elbow2, claw]
# Swap 1 and 0 for motor keys to swap motor/joint movement direction
motorKeys = {base: {'a': 0, 'd': 1, 
            'name': 'base', 
            'directions': ['left', 'right'],
            'speed': BASE_SPEED},
            elbow1: {'w': 0, 's': 1, 
            'name': 'elbow1', 
            'directions': ['up', 'down'],
            'speed': ELBOW1_SPEED},
            elbow2: {'i': 0, 'k': 1, 
            'name': 'elbow2', 
            'directions': ['up', 'down'],
            'speed': ELBOW2_SPEED},
            claw: {'j': 0, 'l': 1, 
            'name': "claw", 
            'directions': ['open', 'closed'],
            'speed': CLAW_SPEED}}

# Terminal setup
term = Terminal()
showProgramGreeting()

# Where things actually happen
with term.cbreak():
    key = ''

    while key.lower() != 'q':
        key = term.inkey(timeout=0).lower()
        if key != '':
            printNewCommandString(key)
            if key != 't':
                runMotors(key, motors, motorKeys)
            else:
                stopMotors(motors)
            resetTerminalLine()

    printNewCommandString('q')
    closeTerminal()
