# Kinetic Courier
# as of 12/21/2019

import RPi.GPIO as GPIO  # for solenoid and reset button
import time 
import datetime
import board
import random
import neopixel
import pigpio  # for servo
from Adafruit_IO import Client, RequestError, Data

AIO_USER = '********'
AIO_KEY = '***********************************'
aio = Client(AIO_USER,AIO_KEY)

# Add Adafruit.io feed name here
weather_feed = "kinetic-courier.weather"
dinner_feed = "kinetic-courier.dinnerbell"
ISS_feed = "kinetic-courier.iss-overhead"
reminder_feed = "kinetic-courier.reminder"
garage_feed = "garagedoor"  # garagedoor feed is in Default Group

# Set feed so it actually continues - set in program, DO NOT CHANGE 
do_continue = {"weather":0,"dinner":0,"reminder":0,"iss-overhead":0,"garage":0}

# Quiet Time: no alert actions will take place
quiet_start = 21			# quiet time starts at this hour, using 24hr style
quiet_end = 9				# quiet time ends at this hour

# DO NOT CHANGE program variable default that follows: quiet_state
quiet_state = False	# Program toggles to indicate if alerts will activate ("True") or be quiet ("False")


# Setup solenoid
GPIO.setmode(GPIO.BCM)  
S_pin = 22;
GPIO.setup(S_pin, GPIO.OUT)   
GPIO.output(S_pin, GPIO.LOW)

# Setup NeoPixels
pixel_pin = board.D18
num_pixels = 16
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.5, auto_write=False,
                           pixel_order=ORDER)

# Setup servo
servos = 23 

# Setup reset button
GPIO.setmode(GPIO.BCM)  
reset_pin = 17;

def reset_callback(channel):
    global do_continue
    # specify each feed(s) you want reset
    do_continue["weather"] = 0
    do_continue["garage"] = 0
   
GPIO.setup(reset_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(reset_pin,GPIO.FALLING,callback=reset_callback,bouncetime=200)

# Setup variables

# Colors
gold = (255, 215, 0)
mauve =  (178, 132, 190)
pink = (255, 145, 175)
purple = (180, 0, 255)
lt_purple = (255, 51, 255)
cyan = (0, 255, 255) 
yellow = (255, 150, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
OFF = (0, 0, 0)


def start_up():
    for i in range(4):
        Larson(cyan)

    # NeoPixels on
    AllPixels(gold)
    # trigger servo
    flag_wave()
    time.sleep(0.5)
    shave_ring()
    time.sleep(2)
    AllPixels(OFF)

def quiet_time():
    #global quiet_start	# start time for quiet	
    #global quiet_end	# end time for quiet
    global quiet_state	# quiet True/False
	
    now = datetime.datetime.now()
    t = now.hour	# will be in 24hr format
		
    if quiet_state is False:
        if t >= quiet_start:
           quiet_state = True

        if quiet_state is True and t <= 12:
           if t >= quiet_end:
              quiet_state = False 

    return(quiet_state)

# NeoPixel routines
def AllPixels(color):
    pixels.fill(color)
    pixels.show()

# nightrider (AKA Larson Scanner) adapted from :
# Feiticeir0's Blog
# http://blog.whatgeek.com.pt/2015/04/raspberry-pi-and-adafruits-neopixel-stick/
# This is tuned to the round shape of the KC base
# The NeoPixels light up on each side, starting near the buttons
# They meet in the middle (servo), and then light up in reverse
def Larson(color, wait_ms=70):
        """ Knight raider kitt scanner """
        for i in range(int(num_pixels/2)):
                pixels[i] = color
                rev_i =(int((num_pixels) -(i+1)))
                pixels[rev_i] =  color
                pixels.show()
                time.sleep(wait_ms/1000.0)
                pixels[i] = (0,0,0)
                pixels[rev_i] = (0,0,0)
        # reverse the direction
        for j in range(int(num_pixels/2),1,-1):
                pixels[j] = color
                rev_j = (num_pixels - j)
                pixels[rev_j] = color
                pixels.show()
                time.sleep(wait_ms/1000.0)
                pixels[j] = (0,0,0)
                pixels[rev_j] = (0,0,0)

def SnowSparkle():
    pixels.fill((0, 0, 0))
    pixels.show()

    one_pixel = random.randrange(0, num_pixels)
    pixels[one_pixel] = (255, 255, 255)
    pixels.show()
    SparkleDelay = .1
    SpeedDelay =  random.uniform(0, .5)
    time.sleep(SparkleDelay)
    pixels[one_pixel] = (10,10,10)
    pixels.show()
    time.sleep(SpeedDelay)

    time.sleep(10)

def Breathe(fade_color):
    pixels.fill((0, 0, 0))
    pixels.show()
    
    # fade up and down
    for i in range(10,255):  # range must be integer
        if fade_color == "RED":
            pixels.fill((i,0,0))
            pixels.show() 
            time.sleep(.005)
        if fade_color == "GREEN":
            pixels.fill((0,i,0))
            pixels.show() 
            time.sleep(.005)
        if fade_color == "BLUE":
            pixels.fill((0,0,i))
            pixels.show() 
            time.sleep(.005)

    time.sleep(.5)

    for i in range(255,10,-1):
        if fade_color == "RED":
            pixels.fill((i,0,0))
            pixels.show() 
            time.sleep(.005)
        if fade_color == "GREEN":
            pixels.fill((0,i,0))
            pixels.show() 
            time.sleep(.005)
        if fade_color == "BLUE":
            pixels.fill((0,0,i))
            pixels.show() 
            time.sleep(.005)
    
    pixels.fill((0, 0, 0))
    pixels.show()

# Solenoid routines
def ring_pattern(BeatTime):
    GPIO.output(S_pin, GPIO.HIGH)  
    time.sleep(0.06)
    GPIO.output(S_pin, GPIO.LOW)
    time.sleep(BeatTime);

def shave_ring():
    ring_pattern(.25) 
    ring_pattern(.1)
    ring_pattern(.1)
    ring_pattern(.25) 
    ring_pattern(.5)
    ring_pattern(.3)
    ring_pattern(.25)

def ring_times(i):
    for j in range(i):
        ring_pattern(.5)

# Servo routines
def flag_wave():
  pi = pigpio.pi() # connect to Pi

  if not pi.connected:
     exit()

  #pulsewidth can only set between 500-2500
  for i in range(3):

        pi.set_servo_pulsewidth(servos, 500) #0 degree
        #print("Servo {} {} micro pulses".format(servos, 500))
        time.sleep(0.5)
        #pi.set_servo_pulsewidth(servos, 1500) #90 degree
        #print("Servo {} {} micro pulses".format(servos, 1500))
        #time.sleep(1)
        pi.set_servo_pulsewidth(servos, 2500) #180 degree
        #print("Servo {} {} micro pulses".format(servos, 2500))
        time.sleep(0.5)
       # pi.set_servo_pulsewidth(servos, 500)
       # print("Servo {} {} micro pulses".format(servos, 1000))
       # time.sleep(1)

  pi.set_servo_pulsewidth(servos, 500) #0 degree
  #print("Servo {} {} micro pulses".format(servos, 500))
  time.sleep(0.7)

  # switch all servos off
  pi.set_servo_pulsewidth(servos, 0);
  pi.stop()

def flag_90_deg():
  pi = pigpio.pi() # connect to Pi

  if not pi.connected:
     exit()

  pi.set_servo_pulsewidth(servos, 1500) #90 degree
  #print("Servo {} {} micro pulses".format(servos, 1500))
  time.sleep(3)

  pi.set_servo_pulsewidth(servos, 500) #0 degree
  #print("Servo {} {} micro pulses".format(servos, 500))
  time.sleep(0.7)


  # switch all servos off
  pi.set_servo_pulsewidth(servos, 0);
  pi.stop()

  

def get_feeds():
     global weather_feed
     global garage_feed
     global ISS_feed
     if quiet_time():
        return
     # Alert for weather
     current_feed = weather_feed
     wfeed=(run_api(current_feed))
     
     # Alert for rain in next day's forecast
     if wfeed == "rain":
        # NeoPixels on 
        AllPixels(blue)
        ring_times(3)
        # trigger servo
        flag_wave()
        # NeoPixels off
        time.sleep(2)
        AllPixels(OFF)
        do_continue["weather"] = 1
        
     # Alert for garage door
     current_feed = garage_feed
     gfeed=(run_api(current_feed))

     if gfeed == "OPEN":
        AllPixels(green)
        ring_times(3)
        # trigger servo
        flag_90_deg()
        # NeoPixels off
        time.sleep(2)
        AllPixels(OFF)
        do_continue["garage"] = 1

     if gfeed == "SHUT":
        # print("SHUT Received")
        do_continue["garage"] = 0  # Reset an OPEN when "SHUT" is received

     # alert for ISS Overhead
     current_feed = ISS_feed
     Ifeed=(run_api(current_feed))
     
     if Ifeed == "ISS_Overhead":
        AllPixels(purple)
        ring_times(3)
        # trigger servo
        flag_90_deg()
        # NeoPixels off
        time.sleep(2)
        AllPixels(OFF)

def continue_neopixels():
    # NeoPixels for these feeds until you press reset button
    if do_continue["weather"] == 1:  
       for i in range(3):
           Breathe("BLUE")
    if do_continue["garage"] == 1:  
       for i in range(3):
           Breathe("GREEN")

def run_api(check_feed):
     rec_not_found ="404 Not Found"   # used by receive.next
     try:    
        feed_data = aio.receive_next(check_feed).value
        return(feed_data)
     except RequestError as e: 
        # can't iterate over e, so convert to string
        e_string = str(e)
        if  rec_not_found in e_string:  # an expected result
            pass
        else:
            print(e)   # unexpected error

# start-up routine
if quiet_time ():
    pass
else:
    start_up()

try: 
    while True:
        get_feeds()
        continue_neopixels()
        time.sleep(10)
except KeyboardInterrupt:
    GPIO.cleanup()
    print(" ")
    print("End Program")


