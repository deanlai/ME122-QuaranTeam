# motorcontrol.py -- controls motors for ME122 robot arm using gpiozero and
# curses libraries

import gpiozero as gz
import curses

while True:
    // TODO: check for button presses

    // Move motors


def turnMotor(direction):
    if direction == "right":
        // TODO: turn right
    else:
        // TODO: turn left

class RobotArm:
    def __init__(self, base, firstElbow, secondElbow, claw):
        self.base = base
        self.firstElbow = firstElbow
        self.secondElbow = secondElbow
        self.claw = claw

    def pivotJoint(self, joint):
        if direction == "right":
            self.base.forward()
        elif direction == "left":
            self.base.backward()

    def pivotFirstElbow(self, direction):
        if direction == "up":
            self.firstElbow.forward()
        elif direction == "down":
            self.firstElbow.backward()

