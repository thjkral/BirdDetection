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


def read_config():  # Load config
    """Open and load the config"""
    try:
        with open('/etc/birdconfig/birdconfig.json', 'r') as f:
            print('Config file loaded')
            return json.load(f)
    except Error as e:
        print(e)


pipeline_config = read_config()


# Parse commandline options
parser = argparse.ArgumentParser(
    prog='Bird detection pipeline',
    description='Save and identify images from my birdfeeder')

parser.add_argument('-s', '--save', action='store_true', help='Save cached images in cache to the database')
parser.add_argument('-i', '--identify', action='store_true', help='Identify new images with NN model')
parser.add_argument('-v', '--visits', action='store_true', help='Subdivide new images in visits')
parser.add_argument('-r', '--recap', action='store_true', help='Send daily summaries of the process')
parser.add_argument('-a', '--all', action='store_true', help='Run the entire pipeline')
parser.add_argument('-l', '--log', action='store_true', help='Create log file')

args = parser.parse_args()


if len(sys.argv) == 1:  # quit if no arguments are provided
    parser.print_help()
    sys.exit()
else:  # execute program if arguments are passed

    # Set up logging
    if args.log:
        logging.basicConfig(filename=pipeline_config['application']['logfile_location']
                            + str(datetime.now().strftime("%d-%m-%Y_%H:%M:%S"))
                            + '.log'
                            , level=logging.INFO
                            , format='%(asctime)s:%(msecs)03d | %(message)s'
                            , datefmt='%H:%M:%S')

        logging.info('START RUN - Arguments: %s', args)

    def connect_to_database():  # Open database connection
        """Open the connection to the database"""
        try:
            connection = connect(host=pipeline_config['database']['host'],
                                 database=pipeline_config['database']['database'],
                                 user=pipeline_config['database']['user'],
                                 password=pipeline_config['database']['password'])
            print('Database connection made')
            if args.log: logging.info('Database connection made')
            return connection

        except Error as e:
            print(e)
            if args.log: logging.ERROR(e)


    db = connect_to_database()

    if args.save or args.all:  # Start saving photos to the database
        print('Moving images from cache to staging')

        photo_cache = os.listdir(pipeline_config['application']['cache_folder'])
        print(f'Staging {len(photo_cache)} photos')
        for picture in photo_cache:
            saveImage.save(picture,
                           pipeline_config['application']['cache_folder'],
                           pipeline_config['application']['staging_folder'],
                           db)

    if args.identify or args.all:
        print('Identifying images is not yet implemented')
        # TODO: calculate predictions

    if args.visits or args.all:  # Calculate visits
        print('Calculating and assigning visits.')
        createVisits.calculate(db)

    if args.recap or args.all:  # Send summarizing recap messages
        print('Sending a summary is not yet implemented')
        # TODO: sending of a recap to a device
