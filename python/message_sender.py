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


def send_summary(staging_location, database):
    """ Send a daily summary with statistics and the most accurate image of a bird """
    target_date = (datetime.now() - timedelta(days=1)).strftime("%d-%m-%Y")

    try:
        db_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        daily_count_query = f"""SELECT bird_amount, false_amount, undef_amount 
                                FROM Image_statistics WHERE date_day = '{db_date}';"""
        count_cursor = database.cursor()
        count_cursor.execute(daily_count_query)
        count_result = count_cursor.fetchone()

        (bird_count, false_count, undef_count) = count_result

        header = f'Report {target_date}\n'
        image_stat = f"Images taken: {sum(count_result)}\nBirds: {bird_count}\nFalse positives: {false_count}\nUndefined: {undef_count}"
        bot.sendMessage(secrets['USER_ID'], header + image_stat)

        logging.info('\t\tSummary sent')

        if int(bird_count) >= 1:
            try:
                best_img_query = f"SELECT image_name FROM Image WHERE classification LIKE 'Bird' AND date = '{db_date}' ORDER BY accuracy_class DESC LIMIT 1;"
                select_cursor = database.cursor()
                select_cursor.execute(best_img_query)
                select_result = select_cursor.fetchone()

                staging_location = staging_location + '/Bird'
                file = open(os.path.join(staging_location, select_result[0]), 'rb')
                bot.sendPhoto(secrets['USER_ID'], file, caption=f'Most accurate image taken on {target_date}')
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
