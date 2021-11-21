import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import picamera
import io
import time

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
#model = tensorflow.keras.models.load_model('./examples/lite/examples/image_classification/raspberry_pi/keras_model.h5')
#model = tensorflow.keras.models.load_model('./keras_model.h5')
# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.

with picamera.PiCamera(resolution=(2592, 1944), framerate=35) as camera:
    camera.start_preview()
    # camera.brightness=65
    # time.sleep(4)
    model = tensorflow.keras.models.load_model('keras_model.h5')
    print("load completed")
    try:  
      stream = io.BytesIO()
      for _ in camera.capture_continuous(
          stream, format='jpeg', use_video_port=True):

        
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        stream.seek(0)
        image = Image.open(stream).convert('RGB').resize((2592, 1944),
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
        print(prediction)
        tmp_list = prediction.tolist()
        camera.annotate_text = 'plastic : %.2fplastic_holder: %.2f\npaper:  %.2f paper_cup: %.2f\nbackground: %.2f' % (tmp_list[0][0],tmp_list[0][1],
        tmp_list[0][2],tmp_list[0][3],tmp_list[0][4])
        camera.annotate_text_size = 20
        stream.seek(0)
        stream.truncate()

        
        time.sleep(1)

    finally:
      camera.stop_preview()
