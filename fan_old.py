import RPi.GPIO as GPIO
import time
import os
import sys, signal

def konec(sig, frame):
    GPIO.cleanup()
    print("Program zastaven")
    sys.exit(0)

pwmPin = 23
zastavit = True
stop_temp = 45
start_temp = 60
max_temp = 120
freq = 25000

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pwmPin, GPIO.OUT, initial=False)

if zastavit:
    dc = 0
    dc0 = 0
else:
    dc = 20
    dc0 = 20

fan = GPIO.PWM(pwmPin, freq)
fan.start(dc)
print("ventilator inicializovan, " + str(dc) + "%")

signal.signal(signal.SIGTERM, konec)
try:
    while True:
        temp = int(os.popen("vcgencmd measure_temp").readline().replace("temp=", "").replace("'C\n", "")[:-2])
        #print(temp)
        if zastavit:
            if temp <= stop_temp:
                dc = 0
        if temp > stop_temp and temp < start_temp and dc0 != 0:
            dc = 20
        if temp >= start_temp and temp <= max_temp:
            if dc0 == 0:
                dc = 20
                print("zmena (rozdil: " + str(abs(dc - dc0)) + "%) (rychlost: " + str(dc) + "%) (teplota: " + str(temp) + "°C)")
                dc0 = dc
                fan.ChangeDutyCycle(dc)
                time.sleep(0.5)
                continue
            else:
                dc = 20 + (temp - start_temp) * (80/(max_temp-start_temp))
        if temp > max_temp:
            dc = 100
        if abs(dc - dc0) > 10:
            print("zmena (rozdil: " + str(abs(dc - dc0)) + "%) (rychlost: " + str(dc) + "%) (teplota: " + str(temp) + "°C)")
            dc0 = dc
            fan.ChangeDutyCycle(dc)
        print("temp = " + str(temp) + ", DC = " + str(dc))
        time.sleep(1)
except:
    GPIO.cleanup()
    print("Konec programu")
