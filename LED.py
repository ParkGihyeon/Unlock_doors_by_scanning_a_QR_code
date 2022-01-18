import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT) # yellow
GPIO.setup(21,GPIO.OUT) # red
GPIO.setup(24,GPIO.OUT) # green


def compare_start():
        GPIO.output(18, True)

def compare_end():
        GPIO.output(18, False)

def compare_true():
        GPIO.output(24,True)
        time.sleep(2)
        GPIO.output(24,False)

def compare_false():
        GPIO.output(21,True)
        time.sleep(2)
        GPIO.output(21,False)