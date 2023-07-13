#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Saves cached photos to a staging area and renames the files in the process.
"""

import mysql.connector
import os
import datetime
import time

import databaseConnector


def rename_move(file, path, output_folder):
    """Rename the cached files to their time stamp
        file: name of the file that needs to be moved and renamed
        path: the filepath leading to the file
        output_folder: the location where the file needs to be moved to
    """
    full_path = os.path.join(path, file)

    # change the filename to a timestamp
    creation_date = os.path.getmtime(full_path)
    creation_time = time.ctime(creation_date)

    t_obj = time.strptime(creation_time)
    time_stamp = time.strftime("%d-%m-%Y_%H-%M-%S", t_obj)
    new_path = os.path.join(output_folder, str(time_stamp)) + ".jpg"

    os.rename(full_path, new_path)
    return new_path


def write(file, database):
    """Writes a file to the database"""

    # Get the filename
    fileName = os.path.basename(file)

    # Get the creation date and convert to datetime
    path = os.path.join(file, file)
    c_time = os.path.getmtime(path)
    dt_c = datetime.datetime.fromtimestamp(c_time)

    query = f"INSERT INTO Photo (photo_name, timestamp, photo_id) " \
            f"VALUES ('{fileName}', '{dt_c}', MD5(CONCAT(photo_name,timestamp)));"

    cursor = database.cursor()
    cursor.execute(query)
    database.commit()

    cursor.close()


def save(image_name, image_path, staging_location, database_connector):
    """Performs all save operations"""
    renamed_moved_image = rename_move(image_name, image_path, staging_location)
    write(renamed_moved_image, database_connector)
