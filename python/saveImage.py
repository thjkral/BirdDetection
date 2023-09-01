#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Saves cached photos to a staging area and renames the files in the process.
"""

import os
import datetime
import time
import logging
from pathlib import Path

import classifier


def rename_move(file, path, output_folder):
    """
    Rename the cached files to their time stamp
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
    new_path = os.path.join(output_folder, str(time_stamp)) + '_' + Path(file).stem + "_bird.jpg"

    os.rename(full_path, new_path)
    return new_path


def write(file, accuracy, type, database):
    """Writes a file to the database"""

    # Get the filename
    fileName = os.path.basename(file)

    # Get the creation date and convert to datetime
    path = os.path.join(file, file)
    c_time = os.path.getmtime(path)
    dt_c = datetime.datetime.fromtimestamp(c_time)
    date = dt_c.date()
    time = dt_c.time()

    query = f"INSERT INTO Image (image_name, image_id, classification, accuracy_class, timestamp, date, time) " \
            f"VALUES ('{fileName}', MD5(CONCAT(image_name,timestamp)), '{type}', {accuracy}, '{dt_c}', '{date}', '{time}');"

    cursor = database.cursor()
    cursor.execute(query)
    database.commit()

    cursor.close()


def reject_image(file, path, output_location):
    """ Put non-bird pictures in a seperate folder """

    old_path = os.path.join(path, file)
    new_path = os.path.join(output_location, file)
    os.rename(old_path, new_path)
    return new_path


def save(cache_location, staging_location, rejects_location, database_connector):
    """ Classify and save cached images """

    # Define some values for statistics
    no_of_birds = 0
    no_of_rejects = 0
    acc_bird = []
    acc_rejects = []
    avg_accuracy_bird = 0
    avg_accuracy_rejects = 0

    cache = os.listdir(cache_location)
    for image in cache:

        classify_results = classifier.classify_image(os.path.join(cache_location, image))
        img_type = classify_results[0]
        accuracy = classify_results[1]

        if classify_results[0] == 'Bird':  # Only save if the image is of a bird
            renamed_moved_image = rename_move(image, cache_location, staging_location)
            write(renamed_moved_image, accuracy, img_type, database_connector)
            no_of_birds += 1
            acc_bird.append(accuracy)
        else:  # Non-bird pictures are saved elsewhere
            renamed_moved_image = reject_image(image, cache_location, rejects_location)
            write(renamed_moved_image, accuracy, img_type, database_connector)
            no_of_rejects += 1
            acc_rejects.append(accuracy)

    if no_of_birds >= 1:
        avg_accuracy_bird = round((sum(acc_bird)/len(acc_bird)), 2)
    if no_of_rejects >= 1:
        avg_accuracy_rejects = round((sum(acc_rejects)/len(acc_rejects)), 2)

    logging.info(f'\t\tIdentified {no_of_birds} birds and rejected {no_of_rejects} images')
    logging.info(f'\t\tAverage accuracy for birds= {avg_accuracy_bird}')
    logging.info(f'\t\tAverage accuracy for rejects= {avg_accuracy_rejects}')

