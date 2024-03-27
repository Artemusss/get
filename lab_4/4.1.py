import RPi.GPIO as GPIO

def decimal2binary(value):
 
    return [int(bit) for bit in format(value, 'b').zfill(8)]



dac = [8, 11, 7, 1, 0, 5, 12, 6]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

try:
    while True:
        num = input("Enter a number in range from 1 to 255: ")
        try:
            num = int(num)
            if 0 <= num <= 255:
                GPIO.output(dac, decimal2binary(num))
                vlt = float(num) / 256.0 * 3.3
                print(f"Output voltage approximately equal {vlt:.4} volt")
            else:
                if num < 0:
                    print("You should input number above 0")
                elif num > 255:
                    print("You sould input number below 255")
        except Exception:
            if num == "q":
                break
            print("You should enter a number not a text")
finally:
    GPIO.output(dac,0)
    GPIO.cleanup()
    print("end")

