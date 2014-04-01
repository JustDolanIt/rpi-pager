#!/usr/bin/python3

# LCD           RPi             Meaning
# --------------------------------------------------------------
# 01  <------>  GPIO-GND<--->   GND
# 02  <------>  GPIO-5V <--->   Vcc(5V0/3V3) 
# 03  <------>  GPIO-GND<--->   Brightness (may be controlled)
# 04  <------>  GPIO-14 <--->   Adress (data)
# 05  <------>  GPIO-GND<--->   Read/Write -> 0 (Read only)
# 06  <------>  GPIO-15 <--->   E (Enable)
# 07
# 08
# 09
# 10
# 11  <------>  GPIO-23 <--->   DB4 (lowest for 4bit mode)
# 12  <------>  GPIO-24 <--->   DB5
# 13  <------>  GPIO-25 <--->   DB6
# 14  <------>  GPIO-08 <--->   DB7 (highest for 4bit mode)
# 15  <------>  GPIO-5V <--->   LED power
# 16  <------>  GPIO-GND<--->   LED GND

from Symbols import getCode
from Splitter import splitLine
from time import sleep

import RPi.GPIO as GPIO

class Screen:

    def __init__(self, pin_a0=14, pin_e=15, pins_db=[8,25,24,23]):
        
        self.pin_a0=pin_a0
        self.pin_e=pin_e
        self.pins_db=pins_db
  
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_e, GPIO.OUT)
        GPIO.setup(self.pin_a0, GPIO.OUT)
        for pin in self.pins_db:
            GPIO.setup(pin, GPIO.OUT)

        self.sym_per_line=20
        self.lines=4
        self.row_adresses=[0x0,0x40,0x14,0x54]
        self.cur_line=1

        # Parameters setting. Biggest problem in this shit
        self.cmd(0x33) 
        self.cmd(0x32)
        self.cmd(0x28)
        self.cmd(0x0C)
        self.cmd(0x06)
        self.clear()

    def cmd(self, bits, char_mode=False):  
        """ Send command to LCD """  
  
        sleep(0.001) 

        bits=bin(bits)[2:].zfill(8)  

        GPIO.output(self.pin_a0, char_mode)  
  
        for pin in self.pins_db:  
            GPIO.output(pin, False)  
  
        for i in range(4):  
            if bits[i] == "1":  
                GPIO.output(self.pins_db[i], True)  
  
        GPIO.output(self.pin_e, True)  
        GPIO.output(self.pin_e, False)  
  
        for pin in self.pins_db:  
            GPIO.output(pin, False)  

        for i in range(4,8):  
            if bits[i] == "1":  
                GPIO.output(self.pins_db[i-4], True)  
  
  
        GPIO.output(self.pin_e, True)  
        GPIO.output(self.pin_e, False)  

    def clear(self):  

        self.cmd(0x01)
        self.cur_line=1

    def newLine(self):
        
        if self.cur_line == self.lines:
            self.cur_line=1
        else:
            self.cur_line=self.cur_line+1

        self.cmd(0x80+self.row_adresses[self.cur_line-1])

    def message(self, text):
        
        splittedText=splitLine(text,20)
        for line in splittedText:
            for char in line:
                self.cmd(getCode(char),True)
            self.newLine()
