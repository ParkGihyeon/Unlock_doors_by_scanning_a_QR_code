import RPi.GPIO as GPIO
import QR_Scanner
import time


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(19, GPIO.IN)

while True:
    if GPIO.input(19) == 1:
        QR_Scanner.end = False
        QR_Scanner.start()
        time.sleep(1)
