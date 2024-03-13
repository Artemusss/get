import RPi.GPIO as GPIO
import time as tm

dac = [8, 11, 7, 1, 0, 5, 12, 6]

num = [1, 1, 1, 1, 1, 1, 1, 1]

GPIO.setmode(GPIO.BCM)

GPIO.setup(dac, GPIO.OUT)

num = [1, 1, 1, 1, 1, 1, 1, 1]

GPIO.output(dac, num)

tm.sleep(10)

GPIO.output(dac, 0)

GPIO.cleanup()