#!/usr/bin/python  
# Solenoid test 
import RPi.GPIO as GPIO  
import time  

GPIO.setmode(GPIO.BCM)  
  
S_pin = 22;
  

GPIO.setup(S_pin, GPIO.OUT)   
GPIO.output(S_pin, GPIO.LOW)  
  
# time to sleep between operations in the main loop  
  
SleepTime = 0.06  
  
def ring_pattern(BeatTime):
    GPIO.output(S_pin, GPIO.HIGH)  
    time.sleep(SleepTime);   
    GPIO.output(S_pin, GPIO.LOW)
    time.sleep(BeatTime);

#while(1):  
#	try:  
ring_pattern(.25) 
ring_pattern(.1)
ring_pattern(.1)
ring_pattern(.25) 
ring_pattern(.5)
ring_pattern(.3)
ring_pattern(.25)
  #print ("Good bye!");
  #GPIO.cleanup()
  
# End program cleanly with keyboard  
#	except KeyboardInterrupt:  
#  		print(" Quit")  
#  		GPIO.cleanup()  
GPIO.cleanup()
