import datetime
import logging
import os

import numpy as np
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


def shot_data(file, load=None):
    t = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    logging.info('{0} INFO: Reading {1} file.'.format(t, file))

    try:
        df = pd.read_csv(file, delimiter=',', header=0, names=['Load', 'Shot Num', 'x', 'y'])
    except Exception:
        t = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        logging.error('{0} ERROR: Error reading {1} file.'.format(t, file))
        raise ValueError

    if load is None:
        return df
    else:
        return df.loc[df.Load == load]


