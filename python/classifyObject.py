#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 16:34:03 2022

@author: tom
"""

from lobe import ImageModel

def classify(filePath):
    
    
    model = ImageModel.load('/home/tom/Projects/Bird Detection/models/Birds_vs_Rest-TFLite_97acc')    
    result = model.predict_from_file(filePath)
    
    # Return top prediction
    prediction = result.labels[0][0]
    accuracy = round((result.labels[0][1] * 100), 2)
    
    return prediction, accuracy

    
