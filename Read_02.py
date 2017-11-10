#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Patrick Brockmann for LSCE (UMR8212)

# Usage: ./Read_01.py /dir1/dir2/DATA4LSCE image.png

#======================================================
import datetime
import pandas as pd
import sys

inputDir = sys.argv[1]
outputFile = sys.argv[2]

#======================================================
# Read files as DataFrame
dates = [datetime.date.today() + datetime.timedelta(days=i) for i in range(-6, 1, 1)]

df = pd.DataFrame()
for date in dates:
    fileIn = inputDir + "/GIF_" + date.strftime("%Y%m%d") + "_FIDAS_0109.0a"
    print "Reading ", fileIn
    try:
    	df = df.append(pd.read_csv(fileIn, sep='\t'))
    except:
	continue

df = df.rename(columns=lambda x: x.strip())            # remove leading space

df['date'] = pd.to_datetime(df['date     time'], format='%Y-%m-%d %H:%M:%S')    # first column is 'date time'


df = df.set_index('date')
df = df.sort_index()
df = df.drop_duplicates()

df_resampled = df.resample('1T').mean()

#======================================================
# Colors
# from https://github.com/mbostock/d3/wiki/Ordinal-Scales\n",
#colors = ["#1f77b4","#ff7f0e","#2ca02c","#d62728","#9467bd","#8c564b","#e377c2","#7f7f7f","#bcbd22","#17bec"]
colors = ["#8c564b","#1f77b4","#2ca02c","#d62728","#9467bd","#e377c2","#7f7f7f","#bcbd22","#17bec"]

#======================================================
# Matplotlib

import numpy as np
import matplotlib

# If not from a notebook
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, HourLocator, MinuteLocator, DateFormatter

matplotlib.rcParams['font.family'] = 'DejaVu Sans'


# In[18]:

fig, ax = plt.subplots(figsize=(10,6))

#for i,var in enumerate(['PM-total', 'PM10', 'PM4', 'PM2.5', 'PM1']):
for i,var in enumerate(['PM10', 'PM2.5']):
    plt.plot(df_resampled.index.to_pydatetime(), df_resampled[var], linewidth=1, label=var, color=colors[i])
    
#ax.xaxis.set_major_locator(HourLocator())
ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d     '))
ax.xaxis.set_major_locator(DayLocator(interval=1))

#ax.xaxis.set_minor_formatter(DateFormatter('%H'))
ax.xaxis.set_minor_locator(HourLocator(interval=6))
ax.xaxis.set_minor_formatter(DateFormatter('%H'))

x = ax.get_xlim()
ax.set_xlim([np.floor(x[0]), np.ceil(x[1])])
y = ax.get_ylim()
#ax.set_ylim([0, y[1]])
ax.set_ylim([0, 100])

ax.tick_params(axis='x', direction='in', top='on', which='both')

xplace = np.ceil(x[1])+0.1
ax.axhline(y=80, color='red', linewidth=2, linestyle='dashed')
ax.text(xplace, 80, "Seuil d'alerte PM10", ha='left', fontsize=8, style='italic', bbox=dict(facecolor='red'))

ax.axhline(y=50, color='orange', linewidth=2, linestyle='dashed')
ax.text(xplace, 50, "Seuil d'information PM10", ha='left', fontsize=8, style='italic', bbox=dict(facecolor='orange'))

plt.legend(loc=2, bbox_to_anchor=(1.0, 1.0), edgecolor='black', borderpad=0.8)
plt.title("LSCE FIDAS")
#plt.xlabel('Time')
plt.ylabel(u'Concentration μg/m3')
plt.grid(color='gray', axis='both', which='both', linestyle='dotted')

labels = ax.get_xmajorticklabels()
plt.setp(labels, rotation=70, fontsize=10)
labels = ax.get_xminorticklabels()
plt.setp(labels, fontsize=8)

startDate = int(np.floor(x[0])%2)
for i in np.arange(startDate, len(dates), 2):
    #print dates[i]
    plt.axvspan(dates[i], dates[i]+datetime.timedelta(days=1), color='gray', alpha=0.1)

plt.savefig(outputFile, bbox_inches='tight', dpi=100)

plt.show()

plt.close()

print outputFile, "created"

#======================================================
