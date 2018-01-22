import datetime
import logging
import os

import matplotlib.pyplot as plt
import numpy as np
from numpy import nanmax, argmax, unravel_index
from scipy.spatial.distance import pdist, squareform
from scipy import stats

# LOGGING
root_path = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(filename=root_path + '/Logs/run.log', level=logging.DEBUG)
# Logging Levels:
# CRITICAL
# ERROR
# WARNING
# INFO
# DEBUG


class LoadStats:
    def __init__(self, dataframe):
        self.load = dataframe.Load.unique()[0]
        self.dataframe = dataframe
        self.xy_raw = np.array(dataframe.x), np.array(dataframe.y)
        self.center_of_mass = center_of_mass(self.xy_raw[0], self.xy_raw[1])
        self.xy = xy_adjusted(self.xy_raw[0], self.xy_raw[1])
        self.radius = radius(self.xy_raw[0], self.xy_raw[1])
        self.radius_stats = shot_stats(self.radius)
        self.x_stats = shot_stats(self.xy[0])
        self.y_stats = shot_stats(self.xy[1])
        self.max_spread = max_spread(self.xy_raw[0], self.xy_raw[1])
        self.accuracy = inches_to_moa(2 * self.radius_stats[0], 100), inches_to_moa(2 * self.radius_stats[2], 100)
        self.poi_shift = inches_to_moa(self.center_of_mass[0], 100), inches_to_moa(self.center_of_mass[1], 100)


def shot_stats(values):
    avg = np.percentile(values, 50)
    std = np.std(values)
    P90 = np.percentile(values, 90)
    max_diff = np.sort(values)[-1] - np.sort(values)[0]
    return avg, std, P90, max_diff


def xy_adjusted(x, y):
    com = center_of_mass(x, y)
    x_adj = x - com[0]
    y_adj = y - com[1]
    return x_adj, y_adj


def max_spread(x, y):
    shots = list()
    for i in range(0, len(x)):
        shots.append([x[i], y[i]])

    shots = np.array(shots)
    D = pdist(shots)
    D = squareform(D)
    N, [I_row, I_col] = nanmax(D), unravel_index(argmax(D), D.shape)
    return N, [I_row, I_col]


def radius(x, y):
    x_adj, y_adj = xy_adjusted(x, y)
    r = np.sqrt(x_adj**2 + y_adj**2)
    return r


def center_of_mass(x, y):
    return np.average(x), np.average(y)


def histogram(radius):
    max_dist = 3
    shot_bins = max_dist * 10

    freq, bins = np.histogram(radius, shot_bins)
    mode = np.max(freq)

    plt.hist(radius, bins=shot_bins)
    plt.axis([0, max_dist, 0, mode])
    plt.xlabel('Radius from Point of Aim, r (inches)')
    plt.ylabel('Number of Shots')
    plt.show()


def plot_shots(xy_adjusted):
    plt.scatter(xy_adjusted[0], xy_adjusted[1])
    plt.axis([-2, 2, -2, 2])
    plt.xlabel('Horizontal Distance, x (inches)')
    plt.ylabel('Veritcal Distance, y (inches)')
    plt.grid(which='both')
    plt.grid(which='minor', alpha=0.2)
    plt.grid(which='major', alpha=0.5)
    plt.show()


def moa_to_inches(moa, yards):
    return np.tan(moa * np.pi / (180 * 60)) * yards * 36


def inches_to_moa(inches, yards):
    return np.tan((inches / 36) / yards) * 180 * 60 / np.pi


def moa_to_mrad(moa):
    return moa * np.pi / (180 * 60) * 1000


def mrad_to_moa(mrad):
    return mrad / 1000 * (180 * 60) / np.pi