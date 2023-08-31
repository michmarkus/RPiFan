import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

pin = int(input("Zadejte číslo pinu pro PWM: "))
freq = int(input("Zadejte regulační frekvenci: "))
GPIO.setup(pin, GPIO.OUT, initial=False)
fan = GPIO.PWM(pin, freq)

dc = 0
fan.start(dc)
while dc <= 100 and dc >= 0:
	fan.ChangeDutyCycle(dc)
	dc = int(input("Zadejte novou rychlost: "))
GPIO.cleanup()
