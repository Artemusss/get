import RPi.GPIO as GPIO
import time as tm
import matplotlib.pyplot as plt

# Get voltage at comparator
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

# Convertation of int in arr of 8 bits
def decimal2binary(value):
 
    return [int(bit) for bit in format(value, 'b').zfill(8)]

# Displays val on led
def num2_dac_leds(val):
    sgn = decimal2binary(val)
    GPIO.output(dac, sgn)
    return sgn

GPIO.setmode(GPIO.BCM)

dac = [8, 11, 7, 1, 0, 5, 12, 6]
leds = [2, 3, 4, 17, 27, 22, 10, 9]
comp = 14
troyka = 13
bits = 8
levels = 2 ** bits
V_max = 3.3

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(comp, GPIO.IN)

GPIO.output(troyka, 0)

mas_vlt = []
mas_tm = []

try:
    start = tm.time()
    val = 0
    GPIO.output(troyka, 1)

    # Charge capcitor to 210 volt
    # Print and save voltage changes over time
    while(val < 210):
        val = adc()
        print("Current volts UP: {:3}".format(val / levels * V_max), "  NUM:", val)
        num2_dac_leds(val)
        mas_vlt.append(val / levels * V_max)
        mas_tm.append(tm.time() - start)
    
    # Discharging capcitor
    GPIO.output(troyka, 0)

    # Print and save voltage changes over time
    while(val > 64):
        val = adc()
        print("Current volts DOWN: {:3}".format(val / levels * V_max), "  NUM:", val)
        num2_dac_leds(val)
        mas_vlt.append(val / levels * V_max)
        mas_tm.append(tm.time() - start)
    
    end = tm.time()

    # Write parametrs in file
    with open("./settings.txt", "w") as f:
        f.write(str((end- start) / len(mas_vlt)))
        f.write(("\n"))
        f.write(str(V_max / 256))
    
    print(end -start, "seconds\n", len(mas_vlt) / (end - start), "\n", V_max / 256)
        
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.output(troyka, GPIO.LOW)
    GPIO.cleanup()

mas_tm_str = [str(item) for item in mas_tm]
mas_vlt_str = [str(item) for item in mas_vlt]

# Write values of experiments in file
with open("data.txt", "w") as f:
    f.write("\n".join(mas_vlt_str))

plt.plot(mas_tm, mas_vlt)
plt.show()
