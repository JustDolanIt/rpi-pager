#!/usr/bin/python3

# Interface for work with screen and buttons after new mail

from newScreen import lcd
from time import sleep
from Splitter import splitLine
import RPi.GPIO as GPIO

class interface:
  def __init__(self,pin_a0=14,pin_e=15,pins_db=[8,25,24,23],pin_diode=7,pin_button=11):
    self.lcd = lcd(pin_a0,pin_e,pins_db)
    self.diode = pin_diode
    GPIO.setup(self.diode, GPIO.OUT)
    self.button = pin_button
    GPIO.setup(self.button, GPIO.IN)

  def newMail(self,message):
    GPIO.output(self.diode, True)
    while GPIO.input(self.button) == False:
      sleep(0.2)
    GPIO.output(self.diode, False)

    splittedText=splitLine(message,20)
    partedSpTxt = [splittedText[i:i+4] for i in range(0,len(splittedText),4)]
    for part in partedSpTxt:
      for line in part:
        self.lcd.message(line)
      sleep(0.5)
      while GPIO.input(self.button) == False:
        sleep(0.2)
      self.lcd.clear()
      sleep(0.1)
