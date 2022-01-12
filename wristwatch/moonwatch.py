#!/usr/bin/env python

import os
import sys
import time
import math, datetime
import logging
from moon import moon
from lcd import LCD_1inch28 as hardware
from PIL import Image,ImageDraw,ImageFont

logging.basicConfig(level=logging.DEBUG)
pics = os.path.join(os.path.dirname(__file__),"pics")
fonts = os.path.join(os.path.dirname(__file__),"fonts")
FontZ = ImageFont.truetype(os.path.join(fonts, "ZakirahsHand.ttf"),14)

lm_image = Image.open(os.path.join(pics,'moon','lm.jpg'))
lm_image = lm_image.convert(mode ="1") #this is to prevent a value error in the tobitmap function
lm_image.save(os.path.join(pics,'moon','lm.bmp'))

# create display with hardware SPI:
disp = hardware.LCD_1inch28()
disp.Init()
disp.clear()




def test():
    image = Image.new("RGB", (disp.width, disp.height), "BLUE")
    draw = ImageDraw.Draw(image)
    draw.arc((116,116,124,124),0, 360, width=4, fill ="RED")
    disp.ShowImage(image)


def getBackground(now):
    pos = moon.position(now)
    phasename = moon.phase(pos)
    phasename = phasename.replace(' ','_')
    background = os.path.join(pics, 'moon', phasename+'.jpg')
    return background


def draw_face():
    background = os.path.join(pics,'LCD_1inch28_1.jpg')
    background = os.path.join(pics,'moon','First_Quarter.jpg')

    i=0
    ss=57
    while True:
      now = datetime.datetime.now()
      timestring = now.strftime("%H:%M:%S")
      t = timestring.split(":")
      h = int(t[0]) 
      m = int(t[1])
      s = int(t[2])
      sum = (h * 60 * 60) + (m * 60) + (s)

      if h == 0: # it's a new day.  Check the lunation
        background = getBackground(now)
        print(background)


      image1 = Image.open(background).resize((200,200))
      image = Image.new("RGB", (disp.width, disp.height), "BLACK")
      image.paste(image1, (20,20))
      draw = ImageDraw.Draw(image)

      draw_hour_hand(draw, sum / (12*60))
      draw_minute_hand(draw, m)
      draw_second_hand(draw, s)
      draw.arc((116,116,124,124),0, 360, width=4, fill ="YELLOW")

      draw.text((120, 145),"BartCo.", fill = "WHITE",font=FontZ)
      draw.text((120, 165), timestring, fill = "WHITE",font=FontZ)

      disp.ShowImage(image)


def draw_hour_hand(draw, m):
    m = (m+45)
    m = m%60
    draw_hand(draw, m, 80, "BLUE", 4)


def draw_minute_hand(draw, m):
    m = (m+45)%60
    draw_hand(draw, m, 100, "RED", 4)


def draw_second_hand(draw, m):
    m = (m+45)%60
    xy = get_coordinates(m,100)
    draw.bitmap(xy,lm_image )


def draw_hand(draw, m, length=100, colour="RED", width=6):
    coordinates = get_coordinates(m,length)
    x = coordinates[0]
    y = coordinates[1]
    #print(f"drawing a {colour} line {length} pixels long at minute {m}")
    draw.line([(120, 120), (int(x), int(y))], fill = colour, width = width)
    return [x,y]


def get_coordinates(m, length=100):
    theta = 360/60*m
    x = 120 + (math.cos(math.radians(theta)) * length)
    y = 120 + (math.sin(math.radians(theta)) * length)
    return [x,y]



if __name__ == '__main__':
    print('---- moonwatch -----')
    #test()
    draw_face()

    disp.module_exit()
    logging.info("quitting")

