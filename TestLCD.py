#!/usr/bin/python3

from newScreen import lcd
from time import sleep
from Cleaner import cleaner


scr = lcd()
scr.clear()
scr.message('Проверка\nTest')
cleaner()
