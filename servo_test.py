# Simple test for micro servo
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)
p = GPIO.PWM(22, 50)

p.start(7.5)

def SetAngle(angle):
	duty = float(angle) / 18 + 2.5
	p.ChangeDutyCycle(duty)
	time.sleep(0.5)
	

try:
    while True:

        for i in range(3):
            SetAngle(0)
            SetAngle (180)

        time.sleep(3)

except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()






