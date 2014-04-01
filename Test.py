#!/usr/bin/python3

from newScreen import Screen
from time import sleep
from Cleaner import cleaner


scr = Screen()
scr.message('a')
sleep(2)
scr.clear()
cleaner()
