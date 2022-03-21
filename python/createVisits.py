#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 13:23:00 2022

@author: tom
"""


import mysql.connector
import datetime

import databaseConnector

db = databaseConnector.makeConnection()

def getCurrentId():
    ''' Gets the next ID from the Visit table '''
    
    idQuery = 'SELECT MAX(id) FROM Visit;'
    idCursor = db.cursor()
    idCursor.execute(idQuery)
    
    highestId = idCursor.fetchone()
    print(highestId)
    
    if highestId[0] == None:
        return 1
    else:
        highestId = int(highestId[0])
        return highestId + 1



def makeVisit(visitList):
    ''' Makes a new visit and writes it to the database. Should be called before updating the image! '''

    arrival = visitList[0][1]
    departure = visitList[-1][1]    
    visit_len = (departure - arrival).total_seconds()
    visit_len = int(visit_len)
    
    insertQuery = f"INSERT INTO Visit (id, arrival, departure, visit_len) VALUES ('{currentId}','{arrival}','{departure}','{visit_len}');"
    insertCursor = db.cursor()
    insertCursor.execute(insertQuery)
    db.commit()
    insertCursor.close()
    


def updateImageInfo(row_id):
    ''' Assigns a visit ID to the images grouped as a visit. '''
    
    print(f"Updating image {row_id[0]} with visit_id {currentId}")
    
    updateQuery = f"UPDATE Image SET visit_id='{currentId}' WHERE id='{row_id[0]}'"
    updateCursor = db.cursor()
    updateCursor.execute(updateQuery)
    db.commit()
    
    updateCursor.close()


currentId = getCurrentId() # Get the next ID

# Select all images that are not assigned a visit
selectQuery = 'SELECT id, capture_day FROM Image WHERE visit_id IS NULL ORDER BY capture_day ASC;'
selectCursor = db.cursor()
selectCursor.execute(selectQuery)
selectResult = selectCursor.fetchall()

# List for visit
visitList = []
 
for i, elem in enumerate(selectResult):
    
    
    if (i < (len(selectResult)-1)):
        
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
            
    else:
        timeOne = selectResult[i][1]
        timeTwo = selectResult[i-1][1]
        
        diff = timeOne - timeTwo
        diff = diff.total_seconds()
        
        if diff <= 20.0:
            visitList.append(selectResult[i])
            
            makeVisit(visitList)
            
            for j in visitList:
                updateImageInfo(j)
        else:
            currentId += 1
            visitList = []
            visitList.append(selectResult[i])
            
            makeVisit(visitList)
            
            for j in visitList:
                updateImageInfo(j)
        


db.close() # Close the database connection








