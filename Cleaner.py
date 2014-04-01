import RPi.GPIO as gpio

def cleaner():
    gpio.cleanup()
    print ("--> GPIO cleared")
