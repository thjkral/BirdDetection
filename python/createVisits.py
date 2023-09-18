#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Creates visits by comparing timestamps of photos.
"""

import hashlib
import logging
from mysql.connector import connect, Error


def makeVisit(visitList, database):
    """ Makes a new visit and writes it to the database. Should be called before updating the image! """

    arrival = visitList[0][1]
    if arrival == visitList[-1][1]:  # visit is one picture so no time difference
        visit_len = 1
        visit_id = computeMD5hash((arrival.strftime("%Y-%m-%d %H:%M:%S")) +
                                  str(visit_len))
        insert_query = f"INSERT INTO Visit (visit_id, arrival, visit_len) " \
                      f"VALUES ('{visit_id}','{arrival}','{visit_len}');"
    else:
        departure = visitList[-1][1]
        visit_len = int((departure - arrival).total_seconds())
        visit_id = computeMD5hash((arrival.strftime("%Y-%m-%d %H:%M:%S")) +
                                  str(visit_len))
        insert_query = f"INSERT INTO Visit (visit_id, arrival, departure, visit_len) " \
                      f"VALUES ('{visit_id}','{arrival}','{departure}','{visit_len}');"

    insert_cursor = database.cursor()

    try:
        insert_cursor.execute(insert_query)
        database.commit()
    except Error as e:
        logging.error(f'ERROR: Adding visit to database failed. Arrival at: {arrival}\n{e}')
    finally:
        insert_cursor.close()

    return visit_id


def updateImageInfo(row, visit_id, database):
    """ Assigns a visit ID to the images grouped as a visit. """

    print(f"Updating image {row[0]} with visit_id {visit_id}")

    updateQuery = f"UPDATE Image SET visit_id='{visit_id}' WHERE image_id='{row[0]}'"

    try:
        updateCursor = database.cursor()
        updateCursor.execute(updateQuery)
        database.commit()
    except Error as e:
        logging.error(f'ERROR: updating image failed. Image ID = {row[0]}')
    finally:
        updateCursor.close()


def computeMD5hash(my_string):
    """ Takes a string and return a hashkey """
    m = hashlib.md5()
    m.update(my_string.encode('utf-8'))
    return m.hexdigest()


def calculate(database):
    """
    Takes unassigned photos and groups them into visits. When photos are made within 20 seconds of each other,
    this counts as one visit. These are updated with the same visit ID.
    """

    # Select all images that are not assigned a visit
    select_query = """SELECT image_id, timestamp FROM Image 
                      WHERE visit_id IS NULL AND classification = 'Bird' 
                      ORDER BY timestamp ASC;"""
    select_cursor = database.cursor()
    select_cursor.execute(select_query)
    select_result = select_cursor.fetchall()

    # List for visit
    visit_list = []

    for i, elem in enumerate(select_result):

        if i < (len(select_result) - 1):  # checks if current photo is the last or not

            time_one = select_result[i][1]
            time_two = select_result[i + 1][1]

            diff = time_two - time_one
            diff = diff.total_seconds()  # difference between images in seconds

            if diff <= 20.0:  # if there is 20 seconds or less between pictures, it belongs to the same visit.
                visit_list.append(select_result[i])
            else:  # A new visit occurs with more than 20 seconds between pictures. In this case update the database and start a new visit.
                visit_list.append(select_result[i])

                created_visit = makeVisit(visit_list, database)  # Adds a new entry to the Visit table.

                for j in visit_list:  # Update the Photo table for grouped images.
                    updateImageInfo(j, created_visit, database)

                visit_list = []  # Reset the grouping

        else:
            time_one = select_result[i][1]
            time_two = select_result[i - 1][1]

            diff = time_one - time_two
            diff = diff.total_seconds()

            if diff <= 20.0:
                visit_list.append(select_result[i])

                created_visit = makeVisit(visit_list, database)  # Adds a new entry to the Visit table.

                for j in visit_list:
                    updateImageInfo(j, created_visit, database)

            else:
                visit_list = []  # Reset the grouping
                visit_list.append(select_result[i])

                created_visit = makeVisit(visit_list, database)  # Adds a new entry to the Visit table.

                for j in visit_list:
                    updateImageInfo(j, created_visit, database)
