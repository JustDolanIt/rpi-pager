#!/usr/bin/python3

from Interfac import interface
from PagerServer import pagerServer
from Cleaner import cleaner
from time import sleep
import asyncore
import os

device = "eth0"

ipWork = os.popen("ifconfig "+device+" | grep 'inet addr' | awk -F: '{print $2}' | awk '{print $1}'").read()[:-1] # Deleting \n at the end of output

iface = interface()

iface.newMail(ipWork)
sleep(1)

server = pagerServer((ipWork,25),None,iface)

asyncore.loop()
