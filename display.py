#!/usr/bin/env python2.7  
#! ~*~ coding: utf-8 ~*~

# LCD           RPi             Meaning
# --------------------------------------------------------------
# 01  <------>  GPIO-06 <--->   GND
# 02  <------>  GPIO-02 <--->   Vcc(5V0/3V3) 
# 03  <------>  GPIO-06 <--->   Brightness (may be controlled)
# 04  <------>  GPIO-26 <--->   Adress (data)
# 05  <------>  GPIO-06 <--->   Read/Write -> 0 (Read only)
# 06  <------>  GPIO-24 <--->   E (Enable)
# 07
# 08
# 09
# 10
# 11  <------>  GPIO-22 <--->   DB4 (lowest for 4bit mode)
# 12  <------>  GPIO-18 <--->   DB5
# 13  <------>  GPIO-16 <--->   DB6
# 14  <------>  GPIO-12 <--->   DB7 (highest for 4bit mode)
# 15    +5V             <--->   LED power
# 16  <------>  GPIO-06 <--->   LED GND
  
import RPi.GPIO as GPIO  
from time import sleep  

class HD:  
  
    def __init__(self, pin_rs=7, pin_e=8, pins_db=[25, 24, 23, 18]):  
  
        self.pin_rs=pin_rs  
        self.pin_e=pin_e  
        self.pins_db=pins_db  
  
        GPIO.setmode(GPIO.BCM)  
        GPIO.setup(self.pin_e, GPIO.OUT)  
        GPIO.setup(self.pin_rs, GPIO.OUT)  
        for pin in self.pins_db:  
            GPIO.setup(pin, GPIO.OUT)  
  
        self.clear()  
  
    def clear(self):  
        """ Blank / Reset LCD """  
  
        self.cmd(0x33) # $33 8-bit mode  
        self.cmd(0x32) # $32 8-bit mode  
        self.cmd(0x28) # $28 8-bit mode  
        self.cmd(0x0C) # $0C 8-bit mode  
        self.cmd(0x06) # $06 8-bit mode  
        self.cmd(0x01) # $01 8-bit mode  
  
    def cmd(self, bits, char_mode=False):  
        """ Send command to LCD """  
  
        sleep(0.001) 

        bits=bin(bits)[2:].zfill(8)  

        GPIO.output(self.pin_rs, char_mode)  
  
        for pin in self.pins_db:  
            GPIO.output(pin, False)  
  
        for i in range(4):  
            if bits[i] == "1":  
                GPIO.output(self.pins_db[::-1][i], True)  
  
        GPIO.output(self.pin_e, True)  
        GPIO.output(self.pin_e, False)  
  
        for pin in self.pins_db:  
            GPIO.output(pin, False)  

        for i in range(4,8):  
            if bits[i] == "1":  
                GPIO.output(self.pins_db[::-1][i-4], True)  
  
  
        GPIO.output(self.pin_e, True)  
        GPIO.output(self.pin_e, False)  

  
    def message(self, text):  
        """ Send string to LCD. Newline wraps to second line"""  
  
        for char in text:  
            if char == '\n':  
                self.cmd(0xC0) # next line  
            else:  
                self.cmd(ord(char),True)  
  
if __name__ == '__main__':  
  
    lcd = HD()  
    lcd.message('abcdefG')
    lcd.clear()
    GPIO.cleanup()
