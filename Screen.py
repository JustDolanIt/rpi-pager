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
 
from Symbols import getCode
import RPi.GPIO as GPIO
from time import sleep

# Screen works in 4-bit mode, so some commands from datasheet may be unusable
# 0 installed on unused pins, so you shouldn't worry about commands that are for 8-bit mode

class Screen:

    def __init__(self, pin_adress=7, pin_e=8, pins_db=[18,23,24,25], lines_4=True):
        
        # Setting primary data
        self.pin_adress=pin_adress
        self.pin_e=pin_e
        self.pins_db=pins_db

        # Setting working mode and pins in their mode
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_e, GPIO.OUT)
        GPIO.setup(self.pin_adress, GPIO.OUT)
        for pin in self.pins_db:
            GPIO.setup(pin, GPIO.OUT)

        # Now here we setting properties, connected with lines
        self.sym_per_line=20
        self.lines=4
        self.row_adresses=[0x0,0x40,0x14,0x54]

        if lines_4 is False: # 2 line display mode
            self.sym_per_line=16
            self.lines=2
            self.row_adresses=[0x0,0x40]

        # Setting current line parameter
        self.cur_line=1

        # Clearing display, just in case
        self.finalSetup()
        
    # __init__ END

#---------------------------------

    def finalSetup(self):
    # Initiate start sequence for normal working mode of module. Lookup in datasheet
    
        # Wait, 1st step
        sleep(0.001)
        
        # Now just make steps that written in datasheet, 2nd step
        GPIO.output(self.pin_adress, False)

        GPIO.output(self.pins_db[0], False)
        GPIO.output(self.pins_db[1], False)
        GPIO.output(self.pins_db[2], True)
        GPIO.output(self.pins_db[3], True)
        # Sending first set
        GPIO.output(self.pin_e, True)
        GPIO.output(self.pin_e, False)
        # Wait, 3rd step
        sleep(0.001)
        # Send second part (all data already set on GPIO), 4th step
        GPIO.output(self.pin_e, True)
        GPIO.output(self.pin_e, False)
        # Wait moar, 5th step
        sleep(0.001)
        # Send again, 6th step
        GPIO.output(self.pin_e, True)
        GPIO.output(self.pin_e, False)
        # Wait... again, 7th step
        sleep(0.001)
        # Change lowest bit to 0, 8th step
        GPIO.output(self.pins_db[0], False)
        GPIO.output(self.pins_db[1], False)
        GPIO.output(self.pins_db[2], True)
        GPIO.output(self.pins_db[3], False)
        # Aaaand... wait, 9th stap
        sleep(0.001)
        # Atlast - set parameters
        # -> Page of symbols
        # First part the same, so send
        GPIO.output(self.pin_e, True)
        GPIO.output(self.pin_e, False)
        # Second differs
        GPIO.output(self.pins_db[0], True)
        GPIO.output(self.pins_db[1], False)
        GPIO.output(self.pins_db[2], False)
        GPIO.output(self.pins_db[3], False)
        # Sending
        GPIO.output(self.pin_e, True)
        GPIO.output(self.pin_e, False)
        # Wait 40 ms
        sleep(0.001)
        # -> Turn off display
        # First part
        GPIO.output(self.pins_db[0], False)
        GPIO.output(self.pins_db[1], False)
        GPIO.output(self.pins_db[2], False)
        GPIO.output(self.pins_db[3], False)
        # Sending
        GPIO.output(self.pin_e, True)
        GPIO.output(self.pin_e, False)
        # Second part
        GPIO.output(self.pins_db[0], True)
        GPIO.output(self.pins_db[1], False)
        GPIO.output(self.pins_db[2], False)
        GPIO.output(self.pins_db[3], False)
        # Sending
        GPIO.output(self.pin_e, True)
        GPIO.output(self.pin_e, False)
        # Wait 40 ms
        sleep(0.001)
        # -> Clear display
        # First part
        GPIO.output(self.pins_db[0], False)
        GPIO.output(self.pins_db[1], False)
        GPIO.output(self.pins_db[2], False)
        GPIO.output(self.pins_db[3], False)
        # Sending
        GPIO.output(self.pin_e, True)
        GPIO.output(self.pin_e, False)
        # Second part
        GPIO.output(self.pins_db[0], False)
        GPIO.output(self.pins_db[1], False)
        GPIO.output(self.pins_db[2], False)
        GPIO.output(self.pins_db[3], True)
        # Sending
        GPIO.output(self.pin_e, True)
        GPIO.output(self.pin_e, False)
        # Wait 40 ms
        sleep(0.001)
        # -> Set input mode
        # First part
        GPIO.output(self.pins_db[0], False)
        GPIO.output(self.pins_db[1], False)
        GPIO.output(self.pins_db[2], False)
        GPIO.output(self.pins_db[3], False)
        # Sending
        GPIO.output(self.pin_e, True)
        GPIO.output(self.pin_e, False)
        # Second part
        GPIO.output(self.pins_db[0], False)
        GPIO.output(self.pins_db[1], True) 
        GPIO.output(self.pins_db[2], True) 
        GPIO.output(self.pins_db[3], False)
        # Sending
        GPIO.output(self.pin_e, True)
        GPIO.output(self.pin_e, False)
        # Wait 40 ms
        sleep(0.001)
    
        # finalSetup END

#---------------------------------

    def cmd(self, data, char_mode=True):
    # Send command. 'char_mode' parameter is for command - if 1, then address will be 1, which means read/write command of char. Otherwise - send real command


        # Making data in 8bit format without 'b' at the beggining
            # int->bin->delete b in created string->8 bit command (theoreticly 4 first bits wouln't mean anything, because it isn't connected)

        data=bin(data)[2:].zfill(8)  

        # Sending data is going in 2 steps - last 4 (7,6,5,4) bits, then first 4 (3,2,1,0)
        # Applying is going with Enable pin jump (0->1->0)
        
        
        # Set working mode, as said before in header of command
        GPIO.output(self.pin_adress, char_mode)

        # !First part:
        
        # Reseting data on data pins
        for pin in self.pins_db:
            GPIO.output(pin, False)

        # Kinda tricky: we take range(4)=[0,1,2,3] -> highest 4 bits in 'data'. Then, we send data in reversed array of pins ([::-1] - reversing array), by number of right pin. So we will set it as it required in datasheet of display. Nasty one
        
        for i in range(4):
            if data[i]=="1":
                GPIO.output(self.pins_db[i], True)

        # Sending first part

        GPIO.output(self.pin_e, True)
        GPIO.output(self.pin_e, False)

        # !Second part

        # Reseting data on data pins
        for pin in self.pins_db:
            GPIO.output(pin, False)

        # Now new trick, but easier after previous one: idea nearly same, but in pins number we take 4, because range(4,8)=[4,5,6,7]. So by this we take right bits, but not right legs if just use it so. Really wicked method

        for i in range(4,8):  
            if data[i] == "1":  
                GPIO.output(self.pins_db[i-4], True)  
            
        # Sending second part

        GPIO.output(self.pin_e, True)
        GPIO.output(self.pin_e, False)

        #Sleep because it requires time to do job
        sleep(0.001)
        
    # cmd END

#---------------------------------

    def newLine(self):
    # Send data on new line
    
        # Idea is - you should add 1 as 8'th bit, so for this you add 1000.0000 -> 0x80. By this you will make command to move your carrier to the point you need, which actually is new string

        # If already maximum lines used, go to first. Else - to next
        if self.cur_line == self.lines:
            self.cur_line=1
        else:
            self.cur_line=self.cur_line+1

        self.cmd(0x80+self.row_adresses[self.cur_line-1],False)

    # newLine END

#---------------------------------

    def clear(self):
    # Clear screen
        
        # Read datasheet for your command
        self.cmd(0x1,False)

        # Back to first line
        self.cur_line=1

    # clear END

#---------------------------------

    def message(self, text):
    # Send text message on screen
    
        # This commans uses 'symbols' dictionary to send data. It is ASCII-compatible, but for russian and special symbols need to use that one module.
        # This method has one trick - if in text has '\n' OR string is more then length of display, then send it to new string. But it has strange way of adress, so it takes it takes special fields of object. More about it you may read in __init__

        # For start - let's split string by needed size and full lines
        text=text.split('\n')
        splitedText=[]
        
        # Thx stackoverflow for this method of spliting!
        for lin in text:
            tempArr = [ lin[i:i+self.sym_per_line] for i in range(0,len(lin),self.sym_per_line) ]
            for elem in tempArr:
                splitedText.append(elem)

        # Now after every part - print it
        for partedLine in splitedText:
            for c in partedLine:
                self.cmd(getCode(c))
            self.newLine()

    # message END
