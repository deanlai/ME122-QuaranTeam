import gpiozero as gz
import time

motor = gz.Motor(11,13)

motor.forward()
time.sleep(1)
motor.stop()
