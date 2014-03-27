#!/usr/bin/env python2.7
#! ~*~ coding: utf-8 ~*~

import Screen
from time import sleep
import RPi.GPIO as GPIO

scr = Screen.Screen()
"""
scr.message("FIRE!")
sleep(2)
scr.clear()
"""
scr.message('a')
GPIO.cleanup()
