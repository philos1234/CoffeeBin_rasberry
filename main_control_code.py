#import RPi.GPIO as GPIO
import time
import numpy
import keyboard
# import servo
# import UltraSonic
# import gps
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import uic,QtGui,QtCore
from PyQt5.QtCore import *
import get_phone_number as phone
import error
import example



#for gui
app = QApplication(sys.argv)

#Variables
send_count = 0
depth1 = 0
depth2 = 0

#Functions




# Load Cell function
# return True/False
# True : No inner water
# False : There is some water, process it first
def check_load_cell():
    return False

# Classify the cup using TensorFlow Lite
# return True/False
# True : Plastic
# False : Paper
def tensor_flow():
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
    #servo.servo_init()
    #UltraSonic.ultra_init()
    #gps.gps_init()
    
   
   
    while 1:
        try:
            time.sleep(2)

            # send_count = send_count+1
            # if send_count == 10:
            #     # update value of ultra and gps info,
            #     # and send info to server
            #     (d1, d2) = UltraSonic.get_distance()
            #
            #     send_count = 0
            #
            if check_load_cell() == True :
                do_empty_gui()
                time.sleep(3)
                continue


            #
            # classify_result = tensor_flow()

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
           