#import RPi.GPIO as GPIO
import time
import numpy
import keyboard
#import servo
import Ultrasonic
# import gps
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import uic,QtGui,QtCore
from PyQt5.QtCore import *
import get_phone_number as phone
import error
import example
from examples.lite.examples.image_classification.raspberry_pi import classify_picamera

#for gui
app = QApplication(sys.argv)

#Variables
global hx
send_count = 0
depth1 = 0
depth2 = 0

#Functions


# Load Cell function
# return True/False
# True : No inner water
# False : There is some water, process it first
def check_load_cell():
    return example.get_weight(hx)

# Classify the cup using TensorFlow Lite
# return True/False
# True : Plastic
# False : Paper
def tensor_flow():
    ret = classify_picamera.main()
    if ret == 0:
        return False
    else:
        return True

def point_add_gui()->str: # 입력한 전화번호를 리턴
    myWindow = phone.PhoneWindow()
    myWindow.show()
    app.exec_()
    return myWindow.result_number

def do_empty_gui():
    myWindow = error.ErrorWindow()
    myWindow.show()
    app.exec_()
    


# main
if __name__ == "__main__":
    hx = example.init_hx711()
    #servo.servo_init()
    Ultrasonic.ultra_init()
    #gps.gps_init()


    while 1:
        try:
            time.sleep(2)

            send_count = send_count+1
            if send_count == 10:
                # update value of ultra and gps info,
                # and send info to server
                (d1, d2) = Ultrasonic.get_distance()
                print("distance : ",d1,d2)
                send_count = 0

            gram = check_load_cell()
            print("gram : ",gram,"g")
            if gram < 3:
                continue
            elif gram > 20 :
                do_empty_gui()
                time.sleep(3)
                continue

            #
            classify_result = tensor_flow()
            print("classfiy result : ",classify_result)
            # if classify_result == True:
            #     servo.to_left()
            #
            # else :
            #     servo.to_right()

            # Point Accumlate
            phone_number = point_add_gui()
            print("received phone number : ",phone_number)
        
        except KeyboardInterrupt:
            print("keyboard interrupt")
            # servo.p.stop()
            # servo.GPIO.cleanup()
            break
           