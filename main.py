import datetime
import logging
import os
import sys

import AccuracyStatistics as accStats
import numpy as np
import ReadFromFile as read
import pandas as pd

# LOGGING
root_path = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(filename=root_path + '/Logs/run.log', level=logging.DEBUG)
# Logging Levels:
# CRITICAL
# ERROR
# WARNING
# INFO
# DEBUG

t = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
logging.info('{0} START: Starting data analysis.'.format(t))

srs_file = root_path + '\Data\SRSstats.csv'
load_of_interest = 'M80 Ball'

load_list = pd.read_csv(srs_file, delimiter=',', header=0, names=['Load', 'Shot Num', 'x', 'y']).Load.unique()

df = pd.read_csv(srs_file, delimiter=',', header=0, names=['Load', 'Shot Num', 'x', 'y'])
df = df.loc[df.Load == load_of_interest]

M80 = accStats.LoadStats(df)
# accStats.plot_shots(M80.xy)

print('M80 Ball in a SRS-A1 has a 90% hit probability of ' + str(np.round(M80.accuracy[1], 2)) +
      ' MOA with a measured max spread of ' + str(np.round(M80.max_spread[0] / 1.0471996, 2)) + ' MOA.')

print(accStats.moa_to_inches(1, 100))
print(accStats.moa_to_mrad(1))
print(accStats.mrad_to_moa(0.1))
print(M80.poi_shift)

t = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
logging.info('{0} END: Target Destroyed.'.format(t))
