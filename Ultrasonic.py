import RPi.GPIO as GPIO
import time

print("HC-SR04 Start")

def ultra_init():
    GPIO.setmode(GPIO.BCM)
    #Ultra 1
    # Pin 16 : 23(Trig)
    GPIO.setup(23, GPIO.OUT)
    # Pin 15 : 22(Echo)
    GPIO.setup(22, GPIO.IN)

    #Ultra 2
    # Pin 13 : 27(Trig)
    GPIO.setup(27, GPIO.OUT)
    # Pin 11 : 17(Echo)
    GPIO.setup(17, GPIO.IN)

def get_distance():
    try:
        while True:
            GPIO.output(23, False)
            time.sleep(0.5)

            GPIO.output(23, True)
            time.sleep(0.00001)
            GPIO.output(23, False)

            while GPIO.input(22) == 0:
                start = time.time()

            while GPIO.input(22) == 1:
                stop = time.time()

            time_interval = stop - start
            distance1 = time_interval * 17000
            distance1 = round(distance1, 2)

            GPIO.output(27, False)
            time.sleep(0.5)

            GPIO.output(27, True)
            time.sleep(0.00001)
            GPIO.output(27, False)

            while GPIO.input(17) == 0:
                start = time.time()

            while GPIO.input(17) == 1:
                stop = time.time()

            time_interval = stop - start
            distance2 = time_interval * 17000
            distance2 = round(distance2, 2)

            return distance1,distance2

    except KeyboardInterrupt:
        GPIO.cleanup()
        print("HC-SR04 End")