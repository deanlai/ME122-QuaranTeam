# Short program to test keyboard control

from gpiozero import LED
from time import sleep

led = LED(17)

while True:
    input = raw_input("Type on or off to blink LED")
    if input == "on":
        led.on()
    elif input == "off":
        led(off)

