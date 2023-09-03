#!/usr/bin/env python3
"""
Module for sending messages to a device.
"""

import json
import telepot
from datetime import datetime, timedelta
import logging
import os
import re


def read_config():  # Load config
    """Open and load the config"""
    try:
        with open('/etc/birdconfig/bird_messenger_secrets.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error('ERROR: Cannot find config file for message_sender.py module')


# Create a Telegram bot
secrets = read_config()
bot = telepot.Bot(secrets['API'])


def send_single_message(message):
    bot.sendMessage(secrets['USER_ID'], message)


def send_motion_capture(image):
    file = open(image, 'rb')
    bot.sendPhoto(secrets['USER_ID'],
                  file,
                  caption=f'Movement spotted at the birdfeeder at: {datetime.now().strftime("%d-%m-%Y %H:%M:%S.%f")}')


def send_summary(log_location, staging_location, database):
    """ Send a daily summary with statistics and the most accurate image of a bird """

    log_date = datetime.now().strftime("%d-%m-%Y")
    logfile = os.path.join(log_location, (log_date + '.log'))
    target_date = (datetime.now() - timedelta(days=1)).strftime("%d-%m-%Y")

    try:
        with open(logfile, 'r') as infile:
            log_content = infile.read()
            pictures_amount = re.search(r"Staging (\d+) images", log_content)
            birds_amount = re.search(r"Identified (\d+) birds", log_content)
            avg = re.search(r"Average accuracy for birds= (\d{1,3}.\d+)", log_content)

            header = f'Report {target_date}\n'
            image_stat = f'Images taken: {pictures_amount.group(1)}\nBirds: {birds_amount.group(1)}\nAverage accuracy: {avg.group(1)}%'
            bot.sendMessage(secrets['USER_ID'], header + image_stat)
            logging.info('\t\tSummary sent')

            if int(birds_amount.group(1)) >= 1:
                try:
                    db_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
                    best_img_query = f"SELECT image_name FROM Image WHERE classification LIKE 'Bird' AND date = '{db_date}' ORDER BY accuracy_class DESC LIMIT 1;"
                    select_cursor = database.cursor()
                    select_cursor.execute(best_img_query)
                    select_result = select_cursor.fetchone()

                    staging_location = staging_location + '/Bird'
                    file = open(os.path.join(staging_location, select_result[0]), 'rb')
                    bot.sendPhoto(secrets['USER_ID'], file, caption=f'Most accurate image taken on {log_date}')
                    logging.info('\t\tImage with highest accuracy sent as part of the summary')
                except FileNotFoundError:
                    logging.error('ERROR: Cannot fetch image from disk for daily summary')
                except TypeError:
                    logging.error('ERROR: Cannot fetch image from database for daily summary')

    except FileNotFoundError:
        logging.error('ERROR: Cannot find log file of the day to make summary')


if __name__ == '__main__':
    print('sending a test message')
    # send_single_message('Testing 123')

    # print('Send test image')
    # send_motion_capture('')

    print('Send test summary')
    send_summary('/logs')
