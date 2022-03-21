#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 20:57:37 2022

@author: tom
"""


import os
import numpy as np
import tensorflow as tf
assert tf.__version__.startswith('2')
import matplotlib.pyplot as plt
import tensorflow.lite as tflite
import cv2
import numpy as np

# Load TFLite model and allocate tensors.
interpreter = tflite.Interpreter(model_path='/home/tom/Projects/Bird Detection/models/Birds_vs_Rest-TFLite_97acc/saved_model.tflite')

#allocate the tensors
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


image_path='/home/tom/Pictures/vogel.jpg'
img = cv2.imread(image_path)
img = cv2.resize(img,(300,300))

#Preprocess the image to required size and cast
input_shape = input_details[0]['shape']
input_tensor= np.array(np.expand_dims(img,0))


input_index = interpreter.get_input_details()[0]["index"]
interpreter.set_tensor(input_index, input_tensor)
interpreter.invoke()
output_details = interpreter.get_output_details()

output_data = interpreter.get_tensor(output_details[0]['index'])
pred = np.squeeze(output_data)

highest_pred_loc = np.argmax(pred)

bird_name = class_ind[highest_pred_loc]
print(f"It's a wild {bird_name}! So cute.")

