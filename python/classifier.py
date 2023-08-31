#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Methods for identifying images of entire folders of images
"""

from lobe import ImageModel
import json
import os
import logging

"""Open and load the config"""
try:
    with open('/etc/birdconfig/birdconfig.json', 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    logging.error("Can't find config file at classifier.py module")

cnn_model = ImageModel.load(config['prediction_model']['path'])


def classify_image(file_path):
    result = cnn_model.predict_from_file(file_path)

    # Return top prediction
    prediction = result.labels[0][0]
    accuracy = round((result.labels[0][1] * 100), 2)

    return prediction, accuracy


def classify_directory(dir_path, model):
    result_list = []

    for file in os.listdir(dir_path):
        cnn_model = ImageModel.load(model)
        result = cnn_model.predict_from_file(os.path.join(dir_path, file))

        # Return top prediction
        prediction = result.labels[0][0]
        accuracy = round((result.labels[0][1] * 100), 2)
        result_tuple = (file, prediction, accuracy)
        result_list.append(result_tuple)

    return result_list


if __name__ == '__main__':  # for testing models or the module
    print('Testing model or classify module')

    # img_result = classify_image('', model)
    # print(img_result)

    # print('\n\nPredicting from dir')
    # dir_results = classify_directory('', model)
    # print(dir_results)
