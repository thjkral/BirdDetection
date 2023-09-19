#!/usr/bin/env python3
"""
Functions for checking the system
"""

import os
import sys
import psutil
import logging
import message_sender


def staging_folders(staging_folder):
    """ Checks if the mandatory staging folders exist on the system """
    staging_dirs = ['Bird', 'False', 'undef']
    for d in staging_dirs:
        if not os.path.isdir(os.path.join(staging_folder, d)):
            os.makedirs(os.path.join(staging_folder, d))
            logging.info(f'Mandatory staging folder created: {d}')
        else:
            logging.info(f'Mandatory staging folder {d} exists')


def empty_cache(cache_folder):
    """ Checks if there are any cached images to process """
    file_list = os.listdir(cache_folder)
    if len(file_list) == 0:
        logging.error('No images in cache. Aborting')
        message_sender.send_single_message('No cached images to process today')
        sys.exit(0)


def available_disk_size():
    """ Checks if enough disk size is available. Issues warning when usable disk runs out """
    logging.info('Monitoring available disk space')
    disk = psutil.disk_usage('/')  # use entire disk
    percentage_used = (disk.free / disk.total) * 100
    logging.info(f'\t\tDisk is used for {round(percentage_used, 2)}%')

    if 80 <= percentage_used < 95:  # issue warning when disk usage is between 80 and 95 percent
        message_sender.send_single_message('WARNING: disk space is used for 85% or more!')
        logging.warning('\t\tDisk is used for 85% or more')
    elif percentage_used >= 95:  # issue warning when disk usage is above 95 percent
        message_sender.send_single_message('CRITICAL: 5% of disk space remaining!')
        logging.critical('\t\tDisk is almost full')
    else:
        logging.info('\t\tDisk usage at acceptable levels')
