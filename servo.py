# duty cycle available : 2~13
# 7로 두기.
import RPi.GPIO as GPIO
import time
import keyboard
import numpy

def to_left(p,sleep_time, start_deg):
    i = start_deg
    while i>=start_deg-2.75:
        p.ChangeDutyCycle(i)
        print("angle : ",i)
        time.sleep(sleep_time)
        i = i-0.125
    time.sleep(3)
    while i<=start_deg:
        p.ChangeDutyCycle(i)
        print("angle : ",i)
        time.sleep(sleep_time)
        i = i+0.125

def to_right(p,sleep_time,start_deg):
    i = start_deg
    while i<=start_deg+2.75:
        p.ChangeDutyCycle(i)
        print("angle : ",i)
        time.sleep(sleep_time)
        i = i+0.125
    time.sleep(3)
    while i>=start_deg:
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
    return p,0.07, 7.125
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