#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example script for the database connection

@author: tom
"""


from mysql.connector import connect, Error

def makeConnection():
    '''Open the connection to the database'''
    try:
        connection = connect(host='localhost',
                                database='birdDatabase',
                                user='root',
                                password='db')
        return connection
    
    except Error as e:
        print(e)
        
def call_add_image(image_name, capture_day, accuracy):
    ''' Calls the stored procedure to add new images to the database '''
    
    args = [image_name, capture_day, accuracy]
    db = makeConnection()
    
    try:
        cursor = db.cursor()
        cursor.callproc('add_image', args)
    except Error as e:
        print(e)
    finally:
        cursor.close()
        db.close()

def call_make_visit(currentId, arrival, departure, visit_len):
    '''Calls stored procedure to create a new visit entry in the database'''
    
    args = [currentId, arrival, departure, visit_len]
    db = makeConnection()
    
    try:
        cursor = db.cursor()
        cursor.callproc('make_visit', args)
    except Error as e:
        print(e)
    finally:
        cursor.close()
        db.close()



def call_update_image(currentId, rowId):
    '''Calls stored procedure to update images when a new visit entry is made'''
    
    args = [currentId, rowId]
    db = makeConnection()
    
    try:
        cursor = db.cursor()
        cursor.callproc('update_image', args)
    except Error as e:
        print(e)
    finally:
        cursor.close()
        db.close()


def call_get_uas_images():
    '''Calls stored procedure to get all images not assigned a visit ID'''
    
    db = makeConnection()
    
    try:
        cursor = db.cursor()
        results = cursor.callproc('get_uas_images')
        return results
    except Error as e:
        print(e)
    finally:
        cursor.close()
        db.close()



