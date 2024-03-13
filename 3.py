import RPi.GPIO as GPIO
import time as tm

leds = [2, 3, 4, 17, 27, 22, 10, 9]
aux = [21, 20, 26, 16, 19, 25, 23, 24]

GPIO.setmode(GPIO.BCM)

GPIO.setup(leds, GPIO.OUT)
GPIO.setup(aux, GPIO.IN)

GPIO.output(4, 1)
while True:
    for i in range(len(leds)):
        GPIO.output(leds[i], GPIO.input(aux[i]))
        tm.sleep(0.02)