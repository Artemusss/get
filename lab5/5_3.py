import RPi.GPIO as GPIO
import time as tm

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

dac = [8, 11, 7, 1, 0, 5, 12, 6]
leds = [2, 3, 4, 17, 27, 22, 10, 9]
comp = 14
troyka = 13

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(leds, GPIO.OUT)
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
        if val2 == 1:
            k -= 2**i
    return k
    
def vol(val):
    val = int(val / 256 * 10)
    arr = [0] * 8
    for i in range(val - 1):
        arr[i] = 1
    return arr


try:
    while True:
        i = adc()
        if i:
            val_vol = vol(i)
            GPIO.output(leds, val_vol)
            print(int(i / 256 * 10))
            print(i * 3.3 / 256)
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()