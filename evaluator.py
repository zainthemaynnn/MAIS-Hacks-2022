
from tensorflow import keras
import cv2
import tensorflow as tf
import numpy as np
model = keras.models.load_model('models/fishySucks5.h5')

img = cv2.imread('testing images/basstest.jpg')
resize = tf.image.resize(img, (256,256))

x = model.predict(np.expand_dims(resize/255, 0))

max = -1
i = 1
for j, n in enumerate(x[0]):
    if n > max:
        i = j
        max = n

fish = ["bass", "black crappie", "catfish", "salmon", "roundgoby", "suckerfish", "sunfish", "trout"]

print(fish[i])