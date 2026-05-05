import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pprint import pprint
from scipy.stats import linregress
import sys

import methods as mt
import plots

vals_1 = [
    0.55, 0.52, 0.55, 0.58, 0.6,
    0.69, 0.57, 0.53, 0.59, 0.62,
    0.59, 0.56, 0.64, 0.6, 0.65,
    0.61, 0.5, 0.55, 0.58, 0.67
]

vals_2 = [
    0.75, 0.82, 0.88, 0.79, 0.85,
    0.8, 0.77, 0.83, 0.81, 0.83,
    0.78, 0.7, 0.74, 0.76, 0.81,
    0.79, 0.7, 0.72, 0.75, 0.86
]

vals_3 = [
    0.75, 0.72, 0.85, 0.68, 0.6,
    0.89, 0.77, 0.53, 0.81, 0.65,
    0.85, 0.6, 0.81, 0.86, 0.81,
    0.8, 0.6, 0.6, 0.97, 0.91
]

vals_4 = [
    0.7, 0.72, 0.8, 0.79, 0.79,
    0.72, 0.77, 0.7, 0.71, 0.83,
    0.78, 0.65, 0.7, 0.79, 0.81,
    0.79, 0.65, 0.7, 0.77, 0.72
]

# Fig 1
plt.figure(1)

# Boxplot Full vars no mar
plt.boxplot(
    [vals_1],
    positions=[2],
    widths=0.25,
    patch_artist=True,
    boxprops=dict(facecolor='red', alpha=0.5),
    medianprops=dict(color='darkred')
)

plt.boxplot(
    [vals_2],
    widths=0.25,
    positions=[1],
    patch_artist=True,
    boxprops=dict(facecolor='lightgreen', alpha=0.5),
    medianprops=dict(color='green')
)

# plt.xticks(pos_pre + 0.075, groups)
plt.ylabel("AUC")
plt.xlabel("Grup")
plt.title(f"Boxplots AUC detecció estimuls globals")
plt.grid(True)
plt.xticks([1, 2], ['P', 'N'])
# plt.yticks(np.arange(2, 20, 1))

# Fig 1
plt.figure(2)

# Boxplot Full vars no mar
plt.boxplot(
    [vals_3],
    positions=[2],
    widths=0.25,
    patch_artist=True,
    boxprops=dict(facecolor='red', alpha=0.5),
    medianprops=dict(color='darkred')
)

plt.boxplot(
    [vals_4],
    widths=0.25,
    positions=[1],
    patch_artist=True,
    boxprops=dict(facecolor='lightgreen', alpha=0.5),
    medianprops=dict(color='green')
)

# plt.xticks(pos_pre + 0.075, groups)
plt.ylabel("AUC")
plt.xlabel("Grup")
plt.title(f"Boxplots AUC detecció estimuls individuals")
plt.grid(True)
plt.xticks([1, 2], ['P', 'N'])
# plt.yticks(np.arange(2, 20, 1))

# plt.legend(handles=[blue_patch, green_patch, pre_mean_plot, no_mar_mean_plot, mar_mean_plot])
plt.show()