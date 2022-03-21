#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 13:24:21 2022

@author: tom
"""

import databaseConnector
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sb


# Connect to the database and retrieve the visits as dataframe
db = databaseConnector.makeConnection()
query = 'SELECT arrival, departure, visit_len FROM Visit ORDER BY arrival;'
df = pd.read_sql(query, db)
db.close()

#print(result_df['day'].min(), result_df['day'].max())
#df['day'] = df['day'].astype('datetime64')
months = list(df['arrival'].dt.month)

# Count the occurences per month and normalize this data
occ = list(map(months.count, range(1,13)))
mmin, mmax = min(occ), max(occ)
for i, val in enumerate(occ):
    occ[i] = (val-mmin) / (mmax-mmin)


# Make a new dataframe with name of months and frequency
monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
df_m = pd.DataFrame()
df_m['Month'] = monthNames
df_m['Frequency'] = occ

'''
# Plot a barchart for the months
plt.figure(figsize=(20,10))
plt.bar(df_m['Month'], df_m['Frequency'], color='red')
plt.title('Average frequency of visits per month', fontsize=40)
plt.xlabel('Month', fontsize=20)
plt.ylabel('Frequency', fontsize=20)
plt.xticks(fontsize=15)
plt.savefig('/home/tom/Projects/Bird Detection/python/plots/VisitFrequency.png')
'''



hours = list(df['arrival'].dt.hour)
freq = list(map(hours.count, range(1,25)))
hmin, hmax = min(freq), max(freq)
for i, val in enumerate(freq):
    freq[i] = (val-hmin) / (hmax-hmin)

hoursInADay = list(range(1,25))
df_h = pd.DataFrame()
df_h['Hour'] = hoursInADay
df_h['Frequency'] = freq

'''
# Plot a barchart for the hours
plt.figure(figsize=(20,10))
plt.bar(df_h['Hour'], df_h['Frequency'])
plt.title('Average frequency of visits per hour', fontsize=40)
plt.xlabel('Hour', fontsize=20)
plt.ylabel('Frequency', fontsize=20)
plt.xticks(hoursInADay, fontsize=15)
plt.savefig('/home/tom/Projects/Bird Detection/python/plots/VisitFrequencyHour.png')
'''

sb.heatmap(df_h)



