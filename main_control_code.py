#import RPi.GPIO as GPIO
import time
import numpy
import keyboard
import servo
import Ultrasonic
import requests, json
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
global hx
global p
global sleep_time
global start_deg
depth1 = 0
depth2 = 0
url = 'http://ec2-3-34-187-76.ap-northeast-2.compute.amazonaws.com:8080'

#Functions

def send_height(h1, h2):
    api = url+'/bin/amount'
    data ={'bin_name':'first_bin', 'plastic_amount' : int(h2),'paper_amount':int(h1)}
    headers={'Content-Type':'application/json'}
    response = requests.post(api,headers=headers, data= json.dumps(data))

def send_phonenumber(number):
    api = url+'/bin/point'
    data ={'phone_number':str(number)}
    headers={'Content-Type':'application/json'}
    response = requests.post(api,headers=headers, data= json.dumps(data))

# Load Cell function
# return True/False
# True : No inner water
# False : There is some water, process it first
def check_load_cell():
    return example.get_weight(hx)

def init_keras():
    np.set_printoptions(suppress=True)
    model = tensorflow.keras.models.load_model('keras_model.h5')
    return model

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
                stream.seek(0)
                stream.truncate()
                max_idx = 0
                max_prob = 0
                print("Prediction result : "+str(prediction))
                tmp_list = prediction.tolist()
                for i in range(0,5):
                    if tmp_list[0][i] > max_prob:
                        max_prob = tmp_list[0][i]
                        max_idx= i
                
                #code just for presentation
                if max_idx != 4:
                    camera.start_preview()
                    time.sleep(2)
                    camera.stop_preview()

                return max_idx
            
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
    


model = init_keras()
p,sleep_time,start_deg = servo.init_servo()
# main
if __name__ == "__main__":
    send_count = 0
    Ultrasonic.ultra_init()
    while 1:
        try:
            time.sleep(2)

            send_count = send_count+1
            print("send count : "+str(send_count))
            if send_count == 3:
                # update value of ultra and gps info,
                # and send info to server
                (d1, d2) = Ultrasonic.get_distance()
                send_height(d1,d2)
                send_count = 0
            #
            classify_result = tensor_flow(model)
            print("classify index : " + str(classify_result))

            #background
            if classify_result == 4:
                continue

            # Plastic  
            elif classify_result == 0:
                servo.to_left(p,sleep_time,start_deg)

            # Paper
            elif classify_result == 2 :
                servo.to_right(p,sleep_time,start_deg)

            else:
                do_empty_gui()
                time.sleep(3)
                continue
            # Point Accumlate
            phone_number = point_add_gui()
            send_phonenumber(phone_number)
            print("received phone number : ",phone_number)
        
        except KeyboardInterrupt:
            print("keyboard interrupt")
            servo.p.stop()
            servo.GPIO.cleanup()
            break
           