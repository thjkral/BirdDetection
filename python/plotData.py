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
from sklearn import preprocessing


# Connect to the database and retrieve the visits as dataframe
db = databaseConnector.makeConnection()
query = 'SELECT arrival, departure, visit_len FROM Visit ORDER BY arrival;'
df = pd.read_sql(query, db)
db.close()



'''Plot average visit frequency per month'''

# Count the amount of visits for every month
months = list(df['arrival'].dt.month)
occ = list(map(months.count, range(1,13)))

# Normalize the data
mmin, mmax = min(occ), max(occ)
for i, val in enumerate(occ):
    occ[i] = (val-mmin) / (mmax-mmin)

# Make a new dataframe with name of months and frequency
monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
df_m = pd.DataFrame()
df_m['Month'] = monthNames
df_m['Frequency'] = occ


# Plot a barchart for the months
plt.figure(figsize=(20,10))
plt.bar(df_m['Month'], df_m['Frequency'], color='red')
plt.title('Average frequency of visits per month', fontsize=40)
plt.xlabel('Month', fontsize=20)
plt.ylabel('Frequency', fontsize=20)
plt.xticks(fontsize=15)
plt.savefig('/home/tom/Projects/Bird Detection/python/plots/VisitFrequencyMonth.png')



'''Plot average visit frequency per hour'''

# Count the amount of visits per hour
hours = list(df['arrival'].dt.hour)
freq = list(map(hours.count, range(1,25)))

# Normalize the data
hmin, hmax = min(freq), max(freq)
for i, val in enumerate(freq):
    freq[i] = (val-hmin) / (hmax-hmin)

# Make a new dataframe with hours and frequency
hoursInADay = list(range(1,25))
df_h = pd.DataFrame()
df_h['Hour'] = hoursInADay
df_h['Frequency'] = freq


# Plot a barchart for the hours
plt.figure(figsize=(20,10))
plt.bar(df_h['Hour'], df_h['Frequency'])
plt.title('Average frequency of visits per hour', fontsize=40)
plt.xlabel('Hour', fontsize=20)
plt.ylabel('Frequency', fontsize=20)
plt.xticks(hoursInADay, fontsize=15)
plt.savefig('/home/tom/Projects/Bird Detection/python/plots/VisitFrequencyHour.png')



'''Plotting visiting hours per month'''

# New dataframe to have the average frequency per hour for every month
columnNames = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
empty_row = list([0]*24)

df_comb = pd.DataFrame(columns=columnNames)
for i in range(1,13): #For every month
    month_df = df.loc[df['arrival'].dt.month==i]
    
    if month_df.empty: # In the case of month without visits
        df_len = len(df_comb)
        df_comb.loc[df_len] = empty_row
    else:
        new_row = []
        for h in range(1,25): # For every hour
            hour_df = month_df.loc[month_df['arrival'].dt.hour==h]
            
            if hour_df.empty:
                new_row.append(0)
            else:
                new_row.append(len(hour_df))
                
        df_len = len(df_comb)
        df_comb.loc[df_len] = new_row
                
# Normalize the data
x = df_comb.values
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
df_norm = pd.DataFrame(x_scaled, columns=columnNames, index=monthNames, dtype='float')

# Make a heatmap
plt.figure(figsize=(20,10))
sb.heatmap(df_norm, cmap='Greens', linewidths=1, linecolor='lightgrey')
plt.xticks(rotation=0, size=20)
plt.yticks(rotation=0, size=20)
plt.xlabel('Hours of the day', size=30)
plt.ylabel('Months', size=30)
plt.title('Frequency of visits per hour for every month', size=40)
plt.savefig('/home/tom/Projects/Bird Detection/python/plots/heatmap.png')
plt.show()




