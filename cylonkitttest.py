#!/usr/bin/env python3

# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18
global_brightness=0.2

# The number of NeoPixels
num_pixels = 60

# For cylon / kitt
width=6
start=10
length=40
delay=0.07
sidered=10
centrered=255

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=global_brightness, auto_write=False,
                           pixel_order=ORDER)

def cylonup(side, center, delay, start, end, width):
    st = start
    end = start-width+end
    for  i in range(st,end):
        # leading edge
        pixels[i+1]=(side,0,0)
        # main eye
        pixels[i]=(center,0,0)
        dim=0.5
        #trailing tail
        for tail in range (i-1, i-(width-2),-1):
            if (tail>0):
                pixels[tail]=(int(side/(dim*2)),0,0)
            dim+=1
            
        # clear the end of the tail
        pixels[i-(width-1)]=(0,0,0)

        pixels.show()
        time.sleep(delay)

def cylondown(side, center, delay, start, end, width):
    st = start
    end = start-width+end
    for  i in range(end, st, -1):
        # leading edge
        pixels[i-1]=(side,0,0)
        # main eye
        pixels[i]=(center,0,0)
        dim=0.5
        #trailing tail
        for tail in range (i+1, i+(width+2)):
            if (tail>0):
                pixels[tail]=(int(side/(dim*2)),0,0)
            dim+=1
            
        # clear the end of the tail
        pixels[i-(width+1)]=(0,0,0)

        pixels.show()
        time.sleep(delay)

def white(start, length):
    for i in range(start,start+length): 
       pixels[i]=(255,255,255)
    pixels.show()

def clear():
    pixels.fill((0,0,0))


def whitepulse(updown=3):
    if (updown==3):
        whitepulse(1)
        whitepulse(2)
    else:
        if (updown==1):
            start=0
            end=255
            step=2
        if (updown==2):
            start=255
            end=0 
            step=-2   
        for bright in range(start, end, step):
           pixels.fill((bright,bright,bright))
           pixels.show()
           time.sleep(delay/2)

def splitin(side, center, delay, start, length, pulsewidth):
    leftstart = start
    leftend = (start+length)/2
    rightstart = start+length
    rightend = leftend
    
    left = 0
    right = rightstart
    while left <= leftend+width:
#        print("left: ",left, "right: ", right)
        if (left<=leftend):
            # leading edge
            pixels[left+1]=(side,0,0)
            pixels[right-1]=(side,0,0)
            # main eye
            pixels[left]=(center,0,0)
            pixels[right]=(center,0,0)
            dim=0.5
            #trailing tail
            for tail in range (left-1, left-(pulsewidth+2)):
                if (tail>leftstart and tail<rightend):
                    pixels[tail]=(int(side/(dim*2)),0,0)
                dim+=1
            for tail in range (right+1, right+(pulsewidth+2)):
                if (tail>leftstart and tail<rightend):
                    pixels[tail]=(int(side/(dim*2)),0,0)
                dim+=1
            
        # clear the end of the tail
        pixels[left-(pulsewidth-1)]=(0,0,0)
        pixels[right+(pulsewidth+1)]=(0,0,0)

        pixels.show()
        time.sleep(delay)
        
        left+=1
        right-=1   
    
def splitout(side, center, delay, start, length, pulsewidth):
    leftend = start
    leftstart = (start+length)/2
    rightend = start+length
    rightstart = leftend
    
    left = leftstart
    right = rightstart
    while left <= leftend:
#        print("left: ",left, "right: ", right)
        # leading edge
        pixels[left-1]=(side,0,0)
        pixels[right+1]=(side,0,0)
        # main eye
        pixels[left]=(center,0,0)
        pixels[right]=(center,0,0)
        dim=0.5
        #trailing tail
        for tail in range (left+1, left+(pulsewidth+2)):
            if (tail>leftstart and tail<rightend):
                pixels[tail]=(int(side/(dim*2)),0,0)
            dim+=1
        for tail in range (right-1, right-(pulsewidth+2)):
            if (tail>leftstart and tail<rightend):
                pixels[tail]=(int(side/(dim*2)),0,0)
            dim+=1
            
        # clear the end of the tail
        pixels[left+(pulsewidth+1)]=(0,0,0)
        pixels[right-(pulsewidth-1)]=(0,0,0)

        pixels.show()
        time.sleep(delay)
        
        left-=1
        right+=1   
    

while True:
    whitepulse(3)
    time.sleep(0.5)
    cylonup(sidered,centrered,delay,start,length, width)
    time.sleep(delay)
    cylondown(sidered,centrered,delay,start,length, width)
    time.sleep(delay)
    splitin(sidered,centrered,delay,start,length, width)
    time.sleep(delay)
#    splitout(sidered,centrered,delay,start,length, width)
#    time.sleep(delay)
#    clear()


