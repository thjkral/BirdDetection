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


def rename_move(file, path, img_type, output_folder):
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
    new_path = os.path.join(output_folder, img_type, str(time_stamp)) + '_' + Path(file).stem + "_" + img_type + "_.jpg"

    os.rename(full_path, new_path)
    return new_path


def write(file, accuracy, img_type, database):
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
            f"VALUES ('{fileName}', MD5(CONCAT(image_name,timestamp)), '{img_type}', {accuracy}, '{dt_c}', '{date}', '{time}');"

    cursor = database.cursor()
    cursor.execute(query)
    database.commit()

    cursor.close()


def save(cache_location, staging_location, database_connector):
    """ Classify and save cached images """

    # Define some values for statistics
    no_of_birds = 0
    no_of_undef = 0
    no_of_rejects = 0
    acc_bird = []
    acc_rejects = []
    avg_accuracy_bird = 0
    avg_accuracy_rejects = 0

    cache = os.listdir(cache_location)
    for image in cache:
        # Classify the image
        classify_results = classifier.classify_image(os.path.join(cache_location, image))
        img_type = classify_results[0]
        accuracy = classify_results[1]

        # Save the image to staging and database
        renamed_moved_image = rename_move(image, cache_location, img_type, staging_location)
        write(renamed_moved_image, accuracy, img_type, database_connector)

        # Add to statistics
        if img_type == 'Bird':
            no_of_birds += 1
            acc_bird.append(accuracy)
        elif img_type == 'False':
            no_of_rejects += 1
            acc_rejects.append(accuracy)
        elif img_type == 'undef':
            no_of_undef += 1
        else:
            logging.warning('The model returned an unknown category!')

    if no_of_birds >= 1:
        avg_accuracy_bird = round((sum(acc_bird)/len(acc_bird)), 2)
    if no_of_rejects >= 1:
        avg_accuracy_rejects = round((sum(acc_rejects)/len(acc_rejects)), 2)

    logging.info(f'\t\tIdentified {no_of_birds} birds and rejected {no_of_rejects} images')
    logging.info(f'\t\tCould not correctly identify {no_of_undef} images.')
    logging.info(f'\t\tAverage accuracy for birds= {avg_accuracy_bird}')
    logging.info(f'\t\tAverage accuracy for rejects= {avg_accuracy_rejects}')


