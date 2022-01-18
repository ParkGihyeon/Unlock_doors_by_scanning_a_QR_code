import RPi.GPIO as GPIO
import time


def mortor():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(13, GPIO.OUT)
    p = GPIO.PWM(13, 50)  # 50hz - 2s
    p.start(1)

    print("모터 작동")
    p.ChangeDutyCycle(12.5)
    time.sleep(2)

