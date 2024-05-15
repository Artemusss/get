import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import time

# Convertation of int in arr of 8 bits
def to_bin(n):
    s = bin(n)[2:].zfill(8)
    return list(map(int, s))

# Get voltage at comparator
def adc():
    k = 0
    for i in range(7, -1, -1):
        k += 2 ** i
        dac_val = to_bin(k)
        GPIO.output(dac, dac_val)
        time.sleep(0.005)
        cmp = GPIO.input(comp)
        if cmp == GPIO.HIGH:
            k -= 2 ** i
    return k

# Displays val on led
def num2_dac_leds(value):
    signal = to_bin(value)
    GPIO.output(dac, signal)
    return signal

dac = [8, 11, 7, 1, 0, 5, 12, 6]
leds = [2, 3, 4, 17, 27, 22, 10, 9]
comp = 14
troyka = 13
bits = len(dac)
levels = 2 ** bits
V_max = 3.3

GPIO.setmode(GPIO.BCM)

GPIO.setup(troyka, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)

GPIO.output(troyka, 0)

data_volts = []
data_times = []

try:
    val = 0
    GPIO.output(troyka, 1)
    start_time = time.time()

    # Charge capcitor to 207 volt
    # Print and save voltage changes over time
    while(val < 207):
        val = adc()
        print("Current volts UP: {:3}".format(val / levels * V_max), "  NUM:", val)
        num2_dac_leds(val)
        data_times.append(time.time() - start_time)
        data_volts.append(val / levels * V_max)

    discharge_start = len(data_volts)
    # Discharging capcitor
    GPIO.output(troyka, 0)

    # Print and save voltage changes over time
    while(val > 168):
        val = adc()
        print("Current volts DOWN: {:3}".format(val / levels * V_max), "  NUM:", val)
        num2_dac_leds(val)
        data_times.append(time.time() - start_time)
        data_volts.append(val / levels * V_max)

    end_time = time.time()

    # Write parametrs in file
    with open("./settings.txt", "w") as file:
        file.write(str((end_time - start_time) / len(data_volts)))
        file.write(("\n"))
        file.write(str(V_max / 256))

    # Print rhe duration, period of one measurement, average sampling step and quantization step
    print(end_time - start_time, " secs\n", len(data_volts) / (end_time - start_time), "\n", V_max / 256)

finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.output(troyka, GPIO.LOW)
    GPIO.cleanup()

# Write values of experiments in file
with open("data.txt", "w") as file:
    for i in range(discharge_start):
        print(f"Charging: {data_volts[i]}", file=file)
    for i in range(discharge_start, len(data_volts)):
        print(f"Discharging: {data_volts[i]}", file=file)

plt.plot(data_times, data_volts)
plt.show()
