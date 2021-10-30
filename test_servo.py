import RPi.GPIO as GPIO
import time
import keyboard
import numpy

start_deg = 7.125

def to_left():
    i = start_deg
    while i>=start_deg-1.95:
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

def to_right():
    i = start_deg
    while i<=start_deg+1.825:
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


pin = 13 # PWM pin num 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
p = GPIO.PWM(pin, 50)
p.start(0)
p.ChangeDutyCycle(start_deg)
time.sleep(2)
sleep_time = 0.02

try:
    while True:
        a = int(input())
        if a == 1:
            to_left()
        else:
            to_right()

except KeyboardInterrupt:
    p.stop()

GPIO.cleanup()