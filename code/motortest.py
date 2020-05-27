import gpiozero as gz

motor = Motor(11,13)

motor.forward()
time.sleep(1)
motor.stop()
