# duty cycle available : 2~13
# 7로 두기.
import RPi.GPIO as GPIO
import time
import keyboard
import numpy

def to_left(p,sleep_time):
    i = 7
    while i>=5.5:
        p.ChangeDutyCycle(i)
        print("angle : ",i)
        time.sleep(sleep_time)
        i = i-0.125
    while i<=7:
        p.ChangeDutyCycle(i)
        print("angle : ",i)
        time.sleep(sleep_time)
        i = i+0.125

def to_right(p,sleep_time):
    i = 7
    while i<=8.5:
        p.ChangeDutyCycle(i)
        print("angle : ",i)
        time.sleep(sleep_time)
        i = i+0.125
    while i>=7:
        p.ChangeDutyCycle(i)
        print("angle : ",i)
        time.sleep(sleep_time )
        i = i-0.125


def init_servo():
    pin = 13 # PWM pin num 18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    p = GPIO.PWM(pin, 50)
    p.start(0)
    p.ChangeDutyCycle(7)
    time.sleep(2)
    return p,0.1
#
# try:
#     while True:
#         a = int(input())
#         if a == 1:
#             to_left()
#         else:
#             to_right()
#
# except KeyboardInterrupt:
#     p.stop()
#
# GPIO.cleanup()