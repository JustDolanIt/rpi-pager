#!/usr/bin/python3

from Interfac import interface
from PagerServer import pagerServer
from Cleaner import cleaner
from time import sleep
import RPi.GPIO as GPIO
import subprocess
import asyncore

ipWork = subprocess.getoutput("hostname -I")[:-1] # Don't need space at the end

GPIO.setwarnings(False)

iface = interface()

iface.newMail(ipWork)
sleep(1)

server = pagerServer((ipWork,25),None,iface)

asyncore.loop()
