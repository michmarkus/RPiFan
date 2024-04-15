#!/usr/bin/env python
# coding=utf-8

import RPi.GPIO as GPIO
import time
import os
import sys, signal

pin = 0    # Set pin of blue wire (PWM)
zastavit = True
stop_temp = 40
start_temp = 50
max_temp = 80
min_dc = 10
step = 10
freq = 25000    # PWM specification, adjust if needed

def konec(sig, frame):
    GPIO.cleanup()
    print("Program zastaven")
    sys.exit(0)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT, initial=False)

if zastavit:
    dc = 0
    dc0 = 0
else:
    dc = min_dc
    dc0 = min_dc

fan = GPIO.PWM(pin, freq)
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
            dc = min_dc + (temp - stop_temp) * ((100-min_dc)/(max_temp-stop_temp))
            #dc = (dc // step) * step
        if temp >= start_temp and temp <= max_temp:
            dc = min_dc + (temp - stop_temp) * ((100-min_dc)/(max_temp-stop_temp))
            #dc = (dc // step) * step
            if dc0 == 0:
                print("zmena (rozdil: " + str(abs(dc - dc0)) + "%) (rychlost: " + str(dc) + "%) (teplota: " + str(temp) + "°C)")
                dc0 = dc
                fan.ChangeDutyCycle(dc)
                time.sleep(0.5)
                continue
        if temp > max_temp:
            dc = 100
        if abs(dc - dc0) >= step:
            print("zmena (rozdil: " + str(abs(dc - dc0)) + "%) (rychlost: " + str(dc) + "%) (teplota: " + str(temp) + "°C)")
            dc0 = dc
            fan.ChangeDutyCycle(dc)
        print("temp = " + str(temp) + ", DC = " + str(dc))
        time.sleep(1)
except:
    GPIO.cleanup()
    print("Konec programu")
