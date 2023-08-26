#!/usr/bin/env python3
"""
Module for sending messages to a device.
"""

import json
import telepot


def read_config():  # Load config
    """Open and load the config"""
    with open('/etc/birdconfig/bird_messenger_secrets.json', 'r') as f:
        return json.load(f)


# Create a Telegram bot
secrets = read_config()
bot = telepot.Bot(secrets['API'])

def send_single_message(message):
    bot.sendMessage(secrets['USER_ID'], message)


def send_summary():
    pass


if __name__ == '__main__':
    print('sending a test message')
    #send_single_message('Testing 123')