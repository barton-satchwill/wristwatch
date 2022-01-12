#!/usr/bin/env python
import os
import sys
import time
import math, decimal, datetime
dec = decimal.Decimal
import logging
import spidev as SPI
#sys.path.append("..")

import lcd.baz
from lcd import LCD_1inch28 as hardware
from PIL import Image,ImageDraw,ImageFont

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 
logging.basicConfig(level=logging.DEBUG)
pics = os.path.join(os.path.dirname(__file__),"pics")
fonts = os.path.join(os.path.dirname(__file__),"fonts")
FontZ = ImageFont.truetype(os.path.join(fonts, "ZakirahsHand.ttf"),14)

# create display with hardware SPI:
disp = hardware.LCD_1inch28()
disp.Init()
disp.clear()




def test():
    image = Image.new("RGB", (disp.width, disp.height), "BLUE")
    draw = ImageDraw.Draw(image)
    draw.arc((116,116,124,124),0, 360, width=4, fill ="RED")
    disp.ShowImage(image)


def draw_face():
    background = os.path.join(pics,'LCD_1inch28_1.jpg')

    while True:
      now = datetime.datetime.now()
      timestring = now.strftime("%H:%M:%S")
      t = timestring.split(":")
      h = int(t[0]) 
      m = int(t[1])
      s = int(t[2])
      sum = (h * 60 * 60) + (m * 60) + (s)

      image = Image.open(background)
      draw = ImageDraw.Draw(image)

      draw_hour_hand(draw, sum / (12*60))
      draw_minute_hand(draw, m)
      draw_second_hand(draw, s)
      draw.arc((116,116,124,124),0, 360, width=4, fill ="YELLOW")

      draw.text((120, 145),"BartCo.", fill = "WHITE",font=FontZ)
      draw.text((120, 165), timestring, fill = "WHITE",font=FontZ)

      disp.ShowImage(image)
      time.sleep(1)


def draw_hour_hand(draw, m):
    m = (m+45)
    m = m%60
    draw_hand(draw, m, 80, "BLUE", 4)


def draw_minute_hand(draw, m):
    m = (m+45)%60
    draw_hand(draw, m, 100, "RED", 4)


def draw_second_hand(draw, m):
    m = (m+45)%60
    draw_hand(draw, m, 120, "YELLOW", 1)


def draw_hand(draw, m, length=100, colour="RED", width=6):
    theta = 360/60*m
    x = 120 + (math.cos(math.radians(theta)) * length)
    y = 120 + (math.sin(math.radians(theta)) * length)
    #print(f"drawing a {colour} line {length} pixels long at minute {m}")
    draw.line([(120, 120), (int(x), int(y))], fill = colour, width = width)



if __name__ == '__main__':
    print('---- wristwatch -----')
    #test()
    draw_face()

    disp.module_exit()
    logging.info("quitting")

