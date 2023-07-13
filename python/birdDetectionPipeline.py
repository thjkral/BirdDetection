"""
Starting point for the pipeline that runs every night. It has two main functions:
1) Add cached photos to the database
2) Calculate and group photos into visits
"""

# Import libraries
from mysql.connector import connect, Error
import os
import json

# Import Python scripts
import saveImage
import createVisits


# Load config
def read_config():
    """Open and load the config"""
    try:
        with open('/etc/birdconfig/birdconfig.json', 'r') as f:
            print('Config file loaded')
            return json.load(f)
    except Error as e:
        print(e)


pipeline_config = read_config()


# Open database connection
def connect_to_database():
    """Open the connection to the database"""
    try:
        connection = connect(host=pipeline_config['database']['host'],
                             database=pipeline_config['database']['database'],
                             user=pipeline_config['database']['user'],
                             password=pipeline_config['database']['password'])
        print('Database connection made')
        return connection

    except Error as e:
        print(e)


db = connect_to_database()

# Start saving photos to the database
photo_cache = os.listdir(pipeline_config['application']['cache_folder'])
print(f'Staging {len(photo_cache)} photos')
for picture in photo_cache:
    saveImage.save(picture,
                   pipeline_config['application']['cache_folder'],
                   pipeline_config['application']['staging_folder'],
                   db)

# Calculate visits
createVisits.calculate(db)

# TODO: calculate predictions
