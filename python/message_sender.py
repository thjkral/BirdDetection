#!/usr/bin/env python3
"""
Module for sending messages to a device.
"""

import json
import telepot
from datetime import datetime


def read_config():  # Load config
    """Open and load the config"""
    with open('/etc/birdconfig/bird_messenger_secrets.json', 'r') as f:
        return json.load(f)


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


def send_summary():
    pass


if __name__ == '__main__':
    print('sending a test message')
    #send_single_message('Testing 123')

    print('Send test image')
    send_motion_capture('/home/tom/Pictures/11-07-2022_23-00-27.jpg')