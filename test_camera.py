import picamera , sys
import time

camera = picamera.PiCamera()
camera.resolution=(224,224)
camera.start_preview()
time.sleep(1000)