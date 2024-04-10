import RPi.GPIO as GPIO
import time as tm

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
troyka = 13

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def decimal2binary(value):
 
    return [int(bit) for bit in format(value, 'b').zfill(8)]

def adc():
    k = 0
    for i in range(7, -1, -1):
        k += 2**i
        val1 = decimal2binary(k)
        GPIO.output(dac, val1)
        val2 = GPIO.input(comp)
        tm.sleep(0.1)
        if val2 == 0:
            k -= 2**i
    return k


try:
    while True:
        i = adc()
        vlt = i * 3.3 / 256.0
        if i:
            print("digital value:", i)
            print("voltage value:", vlt)
            print("////////////////////////////")
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()