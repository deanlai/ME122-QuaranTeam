# ME122 Quaranteam spring '20 group project
# motorcontrol.py -- controls motors for a raspi robot arm from the terminal 
# using gpiozero and blessed libraries

import gpiozero as gz
from blessed import Terminal

# Pin setup for motors
BASE_HI, BASE_LOW = 11, 13 
ELBOW1_HI, ELBOW1_LOW = 27, 16
ELBOW2_HI, ELBOW2_LOW = 19, 20
CLAW_HI, CLAW_LOW = 5, 6

# Speed tuning for each motor
BASE_SPEED = 0.5
ELBOW1_SPEED = 0.5
ELBOW2_SPEED = 0.5
CLAW_SPEED = 0.5

# ----------FUNCTIONS----------
def setupMotors():
    # Sets up gpiozero Motor objects for pins specified in Pin setup
    base = gz.Motor(BASE_HI, BASE_LOW, pwm=True)
    elbow1 = gz.Motor(ELBOW1_HI, ELBOW1_LOW, pwm=True)
    elbow2 = gz.Motor(ELBOW2_HI, ELBOW2_LOW, pwm=True)
    claw = gz.Motor(CLAW_HI, CLAW_LOW, pwm=True)
    return base, elbow1, elbow2, claw

def setupDummyMotors():
    # Sets up dummy motors for testing code on a non-raspi device
    return DummyMotor(), DummyMotor(), DummyMotor(), DummyMotor()

def runMotors(key, motors, motorKeys):
    # Runs a motor as specified by which key was pressed
    # EX: If 'A' is pressed, search for which motor 'A' is associated with
    #     and run that motor in the direction specified by 'A'. Also print the
    #     action to the terminal for feedback to user.
    # See motorKeys dictionary below to see how motors are defined
    for motor in motors:
        if key in motorKeys[motor]:
            if motorKeys[motor][key] == 0:
                printMotorControlString(motorKeys, motor, 0)
                motor.forward(speed=motorKeys[motor]['speed'])
            elif motorKeys[motor][key] == 1:
                printMotorControlString(motorKeys, motor, 1)
                motor.backward(speed=motorKeys[motor]['speed'])

def stopMotors(motors):
    # Stop all motors from moving. This is used because we cannot detect a
    # key release event to stop a motor.
    for motor in motors:
        motor.stop()
    print(term.center('Stop all motors'))

def printMotorControlString(motorKeys, motor, direction):
    # Prints the motor control string as specified by motor object passed in
    # EX: if printMotorcontrolString(motorKeys, base, 1) is called, this will
    #     print "base --> right"
    motorString = f"{motorKeys[motor]['name']} --> {motorKeys[motor]['directions'][direction]}"
    print(term.center(motorString))

def printNewCommandString(key):
    # Prints what key was pressed for user feedback
    print(term.clear_eos)
    commandString = f"You pressed {key}"
    print(term.center(commandString))

def resetTerminalLine():
    # Resets terminal print position for subsequent prints
    print(f"{term.home}{term.move_down(5)}")

def showProgramGreeting():
    # Displays the program greeting explaining how to use the program
    print(f"{term.home}{term.moccasin_on_gray25}{term.clear}")
    print(term.gray25_on_moccasin(term.center('QUARANTEAM ARM CONTROL')))
    print(term.gray25_on_moccasin(term.center('Press WASD and IJKL to control arm, T to stop motors')))
    print(term.gray25_on_moccasin(term.center('Press Q to quit')))
    print(f"{term.move_down(1)}{term.moccasin_on_gray25}")

def closeTerminal():
    # Resets the terminal to reenable normal terminal functionality before 
    # closing the program.
    print(term.clear_eos)
    closeString = f"Closing...{term.normal}"
    print(term.gray25_on_moccasin(term.center(closeString)))
    term.move_down()

class DummyMotor():
    # Dummy motor class used to test code without a raspi
    def __init__(self):
        pass
    def forward(self, speed):
        pass
    def backward(self, speed):
        pass
    def stop(self):
        pass

# ----------MOTOR SETUP----------
# Note: swap setupMotors() <--> setupDummyMotors() if running on or off a raspi
base, elbow1, elbow2, claw = setupMotors()
motors = [base, elbow1, elbow2, claw]

# motorKeys: sets up motor parameters for driving motors and printing actions
# to the terminal window. Each motor has 5 key:value pairs -->
#   1. direction 0 key (ex: 'a')
#   2. direction 1 key (ex: 'b')
#   3. name            (ex: 'base')
#   4. directions      (ex: 'left' and 'right')
#   5. speed           (ex: BASE_SPEED, or 0.5 [defined from 0 to 1])
#
#   note:Swap 1 and 0 for motor keys to swap motor/joint movement direction
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

# ----------TERMINAL SETUP----------
term = Terminal()
showProgramGreeting()

# ----------MAIN CONTROL LOOP----------
with term.cbreak():
    key = ''

    # continuously loops until user presses 'Q'
    while key.lower() != 'q':
        key = term.inkey(timeout=0).lower()

        # if user pressed a key
        if key != '':
            # print what the user pressed
            printNewCommandString(key)

            # if the user did not press 'T' run the appropriate motor, 
            # otherwise stop all motors.
            if key != 't':
                runMotors(key, motors, motorKeys)
            else:
                stopMotors(motors)
            resetTerminalLine()

    # Close program and reset the terminal
    printNewCommandString('q')
    closeTerminal()
