import picamera , sys

camera = picamera.PiCamera()
camera.resolution=(224,224)
camera.start_preview()