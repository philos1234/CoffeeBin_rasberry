#import RPi.GPIO as GPIO
import time
import numpy
import keyboard
import servo
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
import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import picamera
import io

#for gui
app = QApplication(sys.argv)

#Variables
global model
global hx
global p
global sleep_time
global start_deg
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

def init_keras():
    global model
    np.set_printoptions(suppress=True)
    model = tensorflow.keras.models.load_model('keras_model.h5')

# Classify the cup using TensorFlow Lite
# return True/False
# True : Plastic
# False : Paper
def tensor_flow(model):
    with picamera.PiCamera(resolution=(224, 224), framerate=35) as camera:
        try:  
            stream = io.BytesIO()
            for _ in camera.capture_continuous(
                stream, format='jpeg', use_video_port=True):

                
                data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
                stream.seek(0)
                image = Image.open(stream).convert('RGB').resize((224, 224),
                                                                Image.ANTIALIAS)

                #resize the image to a 224x224 with the same strategy as in TM2:
                #resizing the image to be at least 224x224 and then cropping from the center
                size = (224, 224)
                image = ImageOps.fit(image, size, Image.ANTIALIAS)

                #turn the image into a numpy array
                image_array = np.asarray(image)

                # display the resized image
                #image.show()

                # Normalize the image
                normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

                # Load the image into the array
                data[0] = normalized_image_array

                # run the inference
                prediction = model.predict(data)
                #print(prediction)
                stream.seek(0)
                stream.truncate()
                #time.sleep(3)
                max_idx = 0
                max_prob = 0
                for i in range(0,4):
                    if prediction[i] > max_prob:
                        max_prob = prediction[i]
                        max_idx= i
                return i
        finally:
            pass


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
    #hx = example.init_hx711()
    
    p,sleep_time,start_deg = servo.init_servo()
    Ultrasonic.ultra_init()
    #gps.gps_init()
    #ret,prob = classify_picamera.main()
    #classify_result = tensor_flow()
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

            #gram = check_load_cell()
            #print("gram : ",gram,"g")
            #if gram < 3:
            #    continue
            #elif gram > 30 :
            #    do_empty_gui()
            #    time.sleep(3)
            #    continue

            #
            classify_result = tensor_flow(model)
            print("classify index : " + classify_result)
            print("here")
            time.sleep(2)
            continue

            if classify_result == True:
                servo.to_left(p,sleep_time,start_deg)

            else :
                servo.to_right(p,sleep_time,start_deg)

            # Point Accumlate
            phone_number = point_add_gui()
            print("received phone number : ",phone_number)
        
        except KeyboardInterrupt:
            print("keyboard interrupt")

            # servo.p.stop()
            # servo.GPIO.cleanup()
            break
           