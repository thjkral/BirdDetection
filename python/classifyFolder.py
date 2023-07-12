#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 11:31:04 2022

@author: tom
"""

import sys
import os

import classifyObject
import saveImage


#List all files in the directories
dataDirectory = sys.argv[1]
files = os.listdir(dataDirectory)

for file in files:
    
    wholePath = os.path.join(dataDirectory, file)
    
    prediction, accuracy = classifyObject.classify(wholePath)
    
    if prediction == 'Bird':
        saveImage.save(wholePath, accuracy)
        print(f'Vogel gespot! Met {accuracy}% zekerheid')
    else:
        saveImage.saveFalsePicture(wholePath)
        print(f'Geen vogel gezien. Ik ben {accuracy}% zeker')