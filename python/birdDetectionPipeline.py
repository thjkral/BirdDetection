#!/usr/bin/env python3
"""
Starting point for the pipeline that runs every night. It has four main functions:
1) Add cached photos to the database
2) Identify birds on pictures
3) Calculate and group photos into visits - NEEDS ADJUSTMENT
4) Send a daily summary
"""

# Import libraries
from mysql.connector import connect, Error
import os
import json
import argparse
import sys
import logging
from datetime import datetime, timedelta

# Import Python scripts
import saveImage
import createVisits
import message_sender

# Open and load the config
try:
    with open('/etc/birdconfig/birdconfig.json', 'r') as f:
        pipeline_config = json.load(f)
except FileNotFoundError:
    logging.error("ERROR: Can't find config file at main pipeline level")
    sys.exit(0)

# Check if necessary staging folders are present
staging_dirs = ['Bird', 'False', 'undef']
for d in staging_dirs:
    if not os.path.isdir(os.path.join(pipeline_config['application']['staging_folder'], d)):
        os.makedirs(os.path.join(pipeline_config['application']['staging_folder'], d))

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
            logging.error('ERROR: Database connection could not be made', e)


    db = connect_to_database()

    if args.save or args.all:  # Start saving photos to the database
        logging.info('Moving images from cache to staging')

        photo_cache = os.listdir(pipeline_config['application']['cache_folder'])

        if len(photo_cache) > 0:
            logging.info(f'\t\tStaging {len(photo_cache)} images')

            saveImage.save(pipeline_config['application']['cache_folder'],
                           pipeline_config['application']['staging_folder'],
                           db)
        else:
            logging.info(f'\t\tNo images to stage')

    if args.visits or args.all:  # Calculate visits
        logging.info('Calculating and assigning visits not available yet.')
        # createVisits.calculate(db)

    if args.recap or args.all:  # Send summarizing recap messages
        logging.info('Preparing to send a summary to Telegram')

        db_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        logging.info(f'\t\tcalculating number of images taken on {db_date}')

        try:
            daily_count_query = f"""INSERT INTO Image_statistics(date_day, bird_amount, false_amount, undef_amount)    
                                    SELECT i.date, 
                                        SUM(CASE WHEN i.classification = 'Bird' THEN 1 ELSE 0 END) AS bird_count,
                                        SUM(CASE WHEN i.classification = 'False' THEN 1 ELSE 0 END) AS false_count, 
                                        SUM(CASE WHEN i.classification = 'undef' THEN 1 ELSE 0 END) AS undef_count 
                                        FROM birdDatabase.Image AS i WHERE date = '{db_date}';"""
            cursor = db.cursor()
            cursor.execute(daily_count_query)
            db.commit()
        except Error as e:
            logging.error(f'ERROR when calculating images taken: {e}')
        finally:
            cursor.close()

        logging.info(f'\t\tcalculating average accuracies')
        try:
            for i in ['Bird', 'False', 'undef']:
                average_query = f"""UPDATE Image_statistics SET {i}_average_accuracy = (
	                            SELECT IF(AVG(accuracy_class) IS NULL, 0, AVG(accuracy_class)) 
	                            FROM Image WHERE classification = '{i}' AND date = '{db_date}'
                                ) WHERE date_day = '{db_date}';"""
                cursor = db.cursor()
                cursor.execute(average_query)
                db.commit()
        except Error as e:
            logging.error(f'ERROR while calculating average accuracies for summary')
        finally:
            cursor.close()

        message_sender.send_summary(pipeline_config['application']['staging_folder'],
                                    db)
