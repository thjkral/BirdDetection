#!/usr/bin/env python3
"""
Module for sending messages to a device.
"""

import json
import network
import urequests
import statistics
import time


def read_config():  # Load config
    """Open and load the config"""
    with open('/etc/birdconfig/bird_messenger_secrets.json', 'r') as f:
        return json.load(f)


secrets = read_config()

# Set up WLAN connection
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.SSID, secrets.PASSWORD)
time.sleep(5)
print(wlan.isconnected())

def send_single_message(message):
    urequests.get(
        "https://api.telegram.org/bot"
        + secrets['API']
        + "/sendMessage?text="
        + message
        + "&chat_id="
        + secrets['USER_ID'])


def send_summary():
    pass


if __name__ == '__main__':
    print('sending a test message')
    send_single_message('Testing 123')