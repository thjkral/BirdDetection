#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 16:44:42 2022

@author: tom
"""


import mysql.connector
import os
import datetime
import time

import databaseConnector


def renameAndMove(filePath):
    
    #change the filename to a timestamp
    creationDate = os.path.getmtime(filePath)
    creationTime = time.ctime(creationDate)
    
    t_obj = time.strptime(creationTime)
    timeStamp = time.strftime("%d-%m-%Y_%H-%M-%S", t_obj)
    newPath = os.path.join('/home/tom/Pictures/tmp/', str(timeStamp)) + ".jpg"
    
    os.rename(filePath, newPath)
    return newPath


def write(filePath, accuracy):
    '''Writes a file to the database'''
    
    # Start database connection
    db = databaseConnector.makeConnection()
    
    # Get the filename
    fileName = os.path.basename(filePath)
    
    # Get the creation date and convert to datetime
    path = os.path.join(filePath, filePath)
    c_time = os.path.getmtime(path)
    dt_c = datetime.datetime.fromtimestamp(c_time)
    
    # Round the accuracy
    round(accuracy, 2)
    
    query = f"INSERT INTO Image (image_name, capture_day, accuracy) VALUES ('{fileName}', '{dt_c}', {accuracy});"
    
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    
    cursor.close()
    db.close()

def save(filePath, accuracy):
    '''Performs all save operations'''
    newPath = renameAndMove(filePath)
    write(newPath, accuracy)


    

