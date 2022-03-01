#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 11:15:55 2022

@author: tom
"""

from tflite_runtime.interpreter import Interpreter
from PIL import Image
import numpy as np
import time


def loadLabels(path):
    with open(path, 'r') as f:
        return [line.strip() for i, line in enumerate(f.readlines())]
    

def setInputTensor(interpreter, image):
    tensor_index = interpreter.get_input_details()[0]['index']
    input_tensor = interpreter.tensor(tensor_index)()[0]
    input_tensor[:, :] = image


def classifyImage(interpreter, image, top_k=1):
    '''
    Classify the image
    '''
    
    setInputTensor(interpreter, image)
    
    interpreter.invoke()
    output_details = interpreter.get_output_details()[0]
    output = np.squeeze(interpreter.get_tensor(output_details['index']))
    
    scale, zero_point = output_details['quantization']
    output = scale * (output - zero_point)
    
    ordered = np.argpartition(-output, top_k)
    return [(i, output[i]) for i in ordered[:top_k]][0]



def classify(filePath):
    '''
    Load the model
    '''
    
    model_path = "/home/tom/Projects/Bird Detection/models/Birds_vs_Rest-TFLite_97acc/saved_model.tflite"
    label_path = "/home/tom/Projects/Bird Detection/models/Birds_vs_Rest-TFLite_97acc/labels.txt"
    
    interpreter = Interpreter(model_path)
    
    interpreter.allocate_tensors()
    _, height, width, _ = interpreter.get_input_details()[0]['shape']
    
    # Loading image to be classified
    image = Image.open(filePath).resize((width, height))
    
    # Classify the image. Is it a bird or not?
    time1 = time.time()
    label_id, prob = classifyImage(interpreter, image)
    time2 = time.time()
    classification_time = np.round(time2 - time1, 3)
    print(f"Classification time: {classification_time} seconds")
    
    # Load labels
    labels = loadLabels(label_path)
    
    # Return classification
    classification_label = labels[label_id]
    return classification_label
















