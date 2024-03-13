import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(21, GPIO.OUT)

GPIO.setup(20, GPIO.IN)

GPIO.output(21, GPIO.input(20))