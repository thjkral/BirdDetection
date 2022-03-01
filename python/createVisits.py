#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 13:23:00 2022

@author: tom
"""


import mysql.connector
import datetime

'''
Connect to the database with local credentials
'''
db = mysql.connector.connect(host='localhost',
                        database='birdDatabase',
                        user='root',
                        password='db')


def getCurrentId():
    '''
    Gets the next ID from the Visit table
    '''
    idQuery = 'SELECT MAX(id) FROM Visit;'
    idCursor = db.cursor()
    idCursor.execute(idQuery)
    
    highestId = idCursor.fetchone()
    highestId = int(highestId[0])
    return highestId + 1



def makeVisit(visitList):
    '''
    Makes a new visit and writes it to the database. Should be called before updating the image!
    '''
    arrival = visitList[0][1]
    departure = visitList[-1][1]    
    visit_len = (departure - arrival).total_seconds()
    visit_len = int(visit_len)
    day = arrival.date()
    
    insertQuery = f"INSERT INTO Visit (id, day, arrival, departure, visit_len) VALUES ('{currentId}','{day}','{arrival.time()}','{departure.time()}','{visit_len}');"
    insertCursor = db.cursor()
    insertCursor.execute(insertQuery)
    db.commit()
    insertCursor.close()
    


def updateImageInfo(row_id):
    '''
    Assigns a visit ID to the images grouped as a visit.
    '''
    updateQuery = f"UPDATE Images SET visit_id='{currentId}' WHERE id='{row_id[0]}'"
    updateCursor = db.cursor()
    updateCursor.execute(updateQuery)
     
    updateCursor.close()


currentId = getCurrentId() # Get the next ID

# Select all images that are not assigned a visit
selectQuery = 'SELECT id, capture_day FROM Images WHERE visit_id IS NULL ORDER BY capture_day ASC;'
selectCursor = db.cursor()
selectCursor.execute(selectQuery)
selectResult = selectCursor.fetchall()

# List for 
visitList = []
 
for i in range(len(selectResult)-1):
    timeOne = selectResult[i][1]
    timeTwo = selectResult[i+1][1]
    
    diff = timeTwo - timeOne
    diff = diff.total_seconds() # difference between images in seconds
    
    if diff <= 20.0: # if there is 20 seconds or less between pictures, it belongs to the same visit.
        visitList.append(selectResult[i])
    else: # A new visit occurs with more than 2 seconds betwee pictures. In this case update the database and start a new visit.
        visitList.append(selectResult[i])
        
        makeVisit(visitList) # Adds a new entry to the Visit table.
        
        for j in visitList: # Update the Image table for grouped images.
            updateImageInfo(j)
        
        visitList = [] # Reset the grouping
        currentId += 1 # Advance one ID


db.close() # Close the database connection








