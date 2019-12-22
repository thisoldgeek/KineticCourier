# Simple test for NeoPixels on Raspberry Pi
# NOTE: NeoPixels running under Adafruit library
#       MUST be run with sudo (or under root)
import time
import board
import random
import neopixel
 
 
# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18
#pixel_pin = board.D12
 
# The number of NeoPixels
num_pixels = 16
 
# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False,
                           pixel_order=ORDER)
 
# Colors
gold = (255, 215, 0)
mauve =  (178, 132, 190)
pink = (255, 145, 175)
purple = (180, 0, 255)
lt_purple = (255, 51, 255)
brown = (150, 75, 0)
cyan = (0, 255, 255) 
yellow = (255, 150, 0)

# nightrider adapted from :
# Feiticeir0's Blog
# http://blog.whatgeek.com.pt/2015/04/raspberry-pi-and-adafruits-neopixel-stick/
# This is tuned to the round shape of the KC base
# The NeoPixels light up on each side, starting near the buttons
# They meet in the middle (servo), and then light up in reverse
def nightrider(color, wait_ms=70):
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
 
def dimColor (color):
        """ Color is an 32-bit int that merges the values into one """
        return (((color&0xff0000)/3)&0xff0000) + (((color&0x00ff00)/3)&0x00ff00) + (((color&0x0000ff)/3)&0x0000ff)
 

while True:
    # Comment this line out if you have RGBW/GRBW NeoPixels
    pixels.fill((255, 0, 0))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    # pixels.fill((255, 0, 0, 0))
    pixels.show()
    time.sleep(1)
 
    # Comment this line out if you have RGBW/GRBW NeoPixels
    pixels.fill((0, 255, 0))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    # pixels.fill((0, 255, 0, 0))
    pixels.show()
    time.sleep(1)
 
    # Comment this line out if you have RGBW/GRBW NeoPixels
    pixels.fill(yellow)
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    # pixels.fill((0, 0, 255, 0))
    pixels.show()
    time.sleep(1)

    nightrider(cyan)  # Blue theater chase
 
    
