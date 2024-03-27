import RPi.GPIO as GPIO
import time as tm

def decimal2binary(value):
 
    return [int(bit) for bit in format(value, 'b').zfill(8)]



dac = [8, 11, 7, 1, 0, 5, 12, 6]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

flag = 0
x = 0

try:
    p = float(input("Enter singal period: "))

    while True:
        GPIO.output(dac, decimal2binary(x))

        print(f"current voltage {(x / 255 * 3.3):.4}")
        
        if x == 0:
            flag = 1
        elif x == 255:
            flag = 0

        if flag == 1:
            x += 1
        else:
            x -= 1
        
        tm.sleep(p / 512)
except ValueError:
    print("Wrong period")

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
    print("end")