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
        connection = connect(host='####',
                                database='birdDatabase',
                                user='####',
                                password='####')
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

        