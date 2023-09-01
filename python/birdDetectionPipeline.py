#!/usr/bin/env python3
"""
Starting point for the pipeline that runs every night. It has four main functions:
1) Add cached photos to the database
2) Identify birds on pictures
3) Calculate and group photos into visits
4) Send a daily summary
"""

# Import libraries
from mysql.connector import connect, Error
import os
import json
import argparse
import sys
import logging
from datetime import datetime

# Import Python scripts
import saveImage
import createVisits
import message_sender


def read_config():  # Load config
    """Open and load the config"""
    try:
        with open('/etc/birdconfig/birdconfig.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error("Can't find config file at main pipeline level")


pipeline_config = read_config()

# Parse commandline options
parser = argparse.ArgumentParser(
    prog='Bird detection pipeline',
    description='Save and identify images from my birdfeeder')

parser.add_argument('-s', '--save', action='store_true', help='Save cached images in cache to the database')
parser.add_argument('-v', '--visits', action='store_true', help='Subdivide new images in visits')
parser.add_argument('-r', '--recap', action='store_true', help='Send daily summaries of the process')
parser.add_argument('-a', '--all', action='store_true', help='Run the entire pipeline')

args = parser.parse_args()

if len(sys.argv) == 1:  # quit if no arguments are provided
    parser.print_help()
    sys.exit()
else:  # execute program if arguments are passed

    # Set up logging
    logfile = pipeline_config['application']['logfile_location'] + str(datetime.now().strftime("%d-%m-%Y")) + '.log'
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s:%(msecs)03d | %(message)s',
                        datefmt='%H:%M:%S',
                        handlers=[
                            logging.FileHandler(logfile),
                            logging.StreamHandler(sys.stdout)
                        ])

    logging.info('START RUN - Arguments: %s', args)


    def connect_to_database():  # Open database connection
        """Open the connection to the database"""
        try:
            connection = connect(host=pipeline_config['database']['host'],
                                 database=pipeline_config['database']['database'],
                                 user=pipeline_config['database']['user'],
                                 password=pipeline_config['database']['password'])
            logging.info('Database connection made')
            return connection

        except Error as e:
            logging.error('Database connection could not be made', e)


    db = connect_to_database()

    if args.save or args.all:  # Start saving photos to the database
        logging.info('Moving images from cache to staging')

        photo_cache = os.listdir(pipeline_config['application']['cache_folder'])

        if len(photo_cache) > 0:
            logging.info(f'\t\tStaging {len(photo_cache)} images')

            saveImage.save(pipeline_config['application']['cache_folder'],
                           pipeline_config['application']['staging_folder'],
                           pipeline_config['application']['rejects_folder'],
                           db)
        else:
            logging.info(f'\t\tNo images to stage')

    if args.visits or args.all:  # Calculate visits
        logging.info('Calculating and assigning visits.')
        createVisits.calculate(db)

    if args.recap or args.all:  # Send summarizing recap messages
        logging.info('Sending a summary to Telegram')
        message_sender.send_summary(pipeline_config['application']['logfile_location'],
                                    pipeline_config['application']['staging_folder'],
                                    db)
        # TODO: sending of a recap to a device
