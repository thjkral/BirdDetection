#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 14:28:58 2022

@author: tom
"""

import flickrapi
import xml.etree.ElementTree as ET
import urllib.request
import os
import datetime



# open the .txt list of bird species and read them in as a list 
with open("/home/tom/Projects/Bird Detection/bird_species_small.txt") as birds_file:
    birds = [line.strip() for line in birds_file]

#get an api key and secret from flickr
api_key = u'b4a1c0168405aae7971233f352cac57a'
api_secret = u'65c263d43f48b13d'
flickr = flickrapi.FlickrAPI(api_key, api_secret)



for bird in birds:
    
    print(f'Fetching images for the {bird}')
    time_start = datetime.datetime.now()
    
    photos = flickr.walk(text=bird,
                        tag_mode='all',
                        tags=bird,
                        extras='url_c',
                        privacy_filters = 1,
                        per_page=500,         
                        sort='relevance')

    for i, photo in enumerate(photos):
        url = photo.get('url_c')
        #if an error occurs just keep moving
        try:
            if i > 1500:
                break
            else:
                TrainDirectory = f'/home/tom/ResearchData/birdberry/BirdSpeciesSmall/{bird}'
                #check if directory exists
                if not os.path.exists(TrainDirectory):
                    os.makedirs(TrainDirectory)
                #create file path    
                filepath = os.path.join(TrainDirectory, f'{i-9}.jpg')
                # Download image from the url and save it to '00001.jpg'
                urllib.request.urlretrieve(url, filepath)
        except:
            pass
    
    time_end = datetime.datetime.now()
    print(f'Duration of process: {time_end - time_start}')
    print('\n###########\n')



