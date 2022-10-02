import tensorflow as tf
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
import keras
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
from keras.preprocessing.image import ImageDataGenerator

gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)


train_datagen = ImageDataGenerator(rescale=1./255,
                                   horizontal_flip=True,
                                   vertical_flip=True
                                   )
test_datagen = ImageDataGenerator(rescale=1./255,
                                  )

training_set = train_datagen.flow_from_directory('seperated_data/train',
                                       target_size=(256,256),
                                                batch_size=64,
                                     class_mode='categorical',
                                            )

validation_set = test_datagen.flow_from_directory('seperated_data/val',
                                        target_size=(256,256),
                                                 batch_size=64,
                                      class_mode='categorical',
                                               shuffle = False,
                                           )

from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D

# create the base pre-trained model
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(256, 256, 3))

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(512, activation='relu')(x)
predictions = Dense(9, activation='softmax')(x)

# this is the model we will train
model = Model(inputs=base_model.input, outputs=predictions)

# first: train only the top layers (which were randomly initialized)
# i.e. freeze all convolutional InceptionV3 layers
for layer in base_model.layers:
    layer.trainable = False

# compile the model (should be done *after* setting layers to non-trainable)
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0015), loss='categorical_crossentropy',metrics=['accuracy'])

model.summary()



hist = model.fit(training_set,
                    steps_per_epoch=len(training_set),
                    epochs=20,
                    validation_data=validation_set,
                    validation_steps = len(validation_set),
                    callbacks=[
                     tf.keras.callbacks.ReduceLROnPlateau(),
                     tf.keras.callbacks.EarlyStopping(patience=3)
                 ])
model.save(os.path.join('models','fishySucks.tflite'))
fig = plt.figure()
plt.plot(hist.history['loss'], color='teal', label='loss')
plt.plot(hist.history['val_loss'], color='orange', label='val_loss')
fig.suptitle('Loss', fontsize=20)
plt.legend(loc="upper left")
plt.show()

