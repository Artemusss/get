import RPi.GPIO as GPIO
import time as t

GPIO.setmode(GPIO.BCM)

GPIO.setup(21, GPIO.OUT)

for i in range(1000):
    GPIO.output(21, 1)
    t.sleep(10)
    GPIO.output(21, 0)
GPIO.output(21, 0)