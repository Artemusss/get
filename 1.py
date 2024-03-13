import RPi.GPIO as GPIO
import time as tm

leds = [2, 3, 4, 17, 27, 22, 10, 9]

GPIO.setmode(GPIO.BCM)

GPIO.setup(leds, GPIO.OUT)
for i in range(3):
    for j in leds:
        GPIO.output(j, 1)
        tm.sleep(0.2)
        GPIO.output(j, 0)
GPIO.output(leds, 0)
GPIO.cleanup()