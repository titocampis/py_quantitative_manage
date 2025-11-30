import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pprint import pprint
import sys
from scipy.stats import linregress

#########################################################################################
#
# Plots
#
#########################################################################################
def plot_1(axis_x, groups, group_var, full_stats_df, start_fig):
    # Fig 1
    plt.figure(start_fig)
    plt.title(f"Valors Estadístics de la variable Depressió recollida prèviament (Pre-D)")
    plt.xlabel(group_var)
    plt.ylabel("Valors Estadístics")

    labels = groups
    plt.plot(axis_x, list(full_stats_df[full_stats_df["Stat"] == "Q3"]["Pre-D"]), marker='o', color='orange', label="Q3", linestyle='--')
    plt.plot(axis_x, list(full_stats_df[full_stats_df["Stat"] == "mean"]["Pre-D"]), marker='o', color='r', label="Mitjana", linestyle='--')
    plt.plot(axis_x, list(full_stats_df[full_stats_df["Stat"] == "Q2"]["Pre-D"]), marker='o', color='b', label="Q2", linestyle='--')
    plt.plot(axis_x, list(full_stats_df[full_stats_df["Stat"] == "Q1"]["Pre-D"]), marker='o', color='g', label="Q1", linestyle='--')
    plt.xticks(axis_x, labels)

    plt.yticks(np.arange(9, 18.5, 0.5))
    plt.grid(True)
    plt.legend()

    # Fig 2
    plt.figure(start_fig + 1)
    plt.title(f"Valors Estadístics de la variable Depressió recollida posteriorment (Post-D)")
    plt.xlabel(group_var)
    plt.ylabel("Valors Estadístics")

    labels = groups
    plt.plot(axis_x, list(full_stats_df[full_stats_df["Stat"] == "Q3"]["Post-D"]), marker='o', color='orange', label="Q3", linestyle='--')
    plt.plot(axis_x, list(full_stats_df[full_stats_df["Stat"] == "mean"]["Post-D"]), marker='o', color='r', label="Mitjana", linestyle='--')
    plt.plot(axis_x, list(full_stats_df[full_stats_df["Stat"] == "Q2"]["Post-D"]), marker='o', color='b', label="Q2", linestyle='--')
    plt.plot(axis_x, list(full_stats_df[full_stats_df["Stat"] == "Q1"]["Post-D"]), marker='o', color='g', label="Q1", linestyle='--')
    plt.xticks(axis_x, labels)

    plt.yticks(np.arange(7, 16.5, 0.5))
    plt.grid(True)
    plt.legend()

def plot_2(axis_x, groups, group_var, full_stats_df, start_fig):
    # Fig 1
    plt.figure(start_fig)
    plt.title(f"Mitjana (x̄) de la variable Depressió")
    plt.xlabel("Grup")
    plt.ylabel("x̄")

    labels = groups
    plt.plot(axis_x, list(full_stats_df[full_stats_df["Stat"] == "mean"]["Pre-D"]), marker='o', color='red', label="Pre-D", linestyle='--')
    plt.plot(axis_x,list(full_stats_df[full_stats_df["Stat"] == "mean"]["Post-D"]), marker='o', color='green', label="Post-D", linestyle='--')
    plt.xticks(axis_x, labels)

    plt.yticks(np.arange(8, 17, 0.5))
    plt.grid(True)
    plt.legend()

    # Fig 2
    plt.figure(start_fig + 1)

    # Calculate dif
    dif_mean = np.array(list(full_stats_df[full_stats_df["Stat"] == "mean"]["Pre-D"])) - np.array(list(full_stats_df[full_stats_df["Stat"] == "mean"]["Post-D"]))
    dif_q3 = np.array(list(full_stats_df[full_stats_df["Stat"] == "Q3"]["Pre-D"])) - np.array(list(full_stats_df[full_stats_df["Stat"] == "Q3"]["Post-D"]))
    dif_q2 = np.array(list(full_stats_df[full_stats_df["Stat"] == "Q2"]["Pre-D"])) - np.array(list(full_stats_df[full_stats_df["Stat"] == "Q2"]["Post-D"]))
    dif_q1 = np.array(list(full_stats_df[full_stats_df["Stat"] == "Q1"]["Pre-D"])) - np.array(list(full_stats_df[full_stats_df["Stat"] == "Q1"]["Post-D"]))

    plt.title(f"Diferència d'estadístics (PRE-POST) de la variable Depressió ")
    plt.xlabel(group_var)
    plt.ylabel("Valor")

    labels = groups
    plt.plot(axis_x, dif_q3, marker='o', color='orange', label="Q3", linestyle='--')
    plt.plot(axis_x, dif_mean, marker='o', color='r', label="Mitjana", linestyle='--')
    plt.plot(axis_x, dif_q2, marker='o', color='b', label="Q2", linestyle='--')
    plt.plot(axis_x, dif_q1, marker='o', color='g', label="Q1", linestyle='--')
    plt.xticks(axis_x, labels)

    plt.yticks(np.arange(0, 9.5, 0.5))
    plt.grid(True)
    plt.legend()

    # Fig 3
    plt.figure(start_fig + 2)
    plt.title(f"Desviació típica (σ) de la variable depressió")
    plt.xlabel(group_var)
    plt.ylabel("σ")

    labels = groups
    plt.plot(axis_x, list(full_stats_df[full_stats_df["Stat"] == "std"]["Pre-D"]), marker='o', color='red', label="Pre-D", linestyle='--')
    plt.plot(axis_x, list(full_stats_df[full_stats_df["Stat"] == "std"]["Post-D"]), marker='o', color='green', label="Post-D", linestyle='--')
    plt.xticks(axis_x, labels)

    plt.yticks(np.arange(0.8, 2.2, 0.1))
    plt.grid(True)
    plt.legend()

def plot_regression(df, var_x, var_y, slope, intercept, start_fig):
    # Fig 1
    plt.figure(start_fig)

    # Calc regression
    y = slope * df[var_x] + intercept

    plt.title(f"Gràfic de dispersió")
    plt.xlabel(var_x)
    plt.ylabel(var_y)

    plt.plot(list(df[var_x]), list(df[var_y]), marker='o', color='red', linestyle='')
    plt.plot(list(df[var_x]), list(y), color='blue', label=f'Recta regressió lineal: y={slope:.2f}x+{intercept:.2f}', linestyle="-")

    # plt.yticks(np.arange(0, 11, 1))
    # plt.xticks(np.arange(0, 21, 1))
    plt.grid(True)
    plt.legend()


def plot_double_boxplot(axis_x, groups, group_var, var_1, var_2, df, full_stats_df, start_fig):
    # Fig 1
    plt.figure(start_fig)

    # Positions for the boxes
    pos_pre = axis_x
    pos_post = pos_pre + 0.08

    # Boxplot Pre-D
    plt.boxplot(
        [df[df[group_var]==g][var_1] for g in groups],
        positions=pos_pre,
        widths=0.25,
        patch_artist=True,
        boxprops=dict(facecolor='red', alpha=0.5),
        medianprops=dict(color='darkred')
    )

    # # Boxplot Post-D
    plt.boxplot(
        [df[df[group_var]==g][var_2] for g in groups],
        positions=pos_post,
        widths=0.25,
        patch_artist=True,
        boxprops=dict(facecolor='lightgreen', alpha=0.5),
        medianprops=dict(color='green')
    )

    # Plot means
    mean_plot_var_1, = plt.plot(
        pos_pre,
        list(full_stats_df[full_stats_df["Stat"] == "mean"][var_1]),
        marker='x', color='red', linestyle='--', label=f'Mitjana {var_1}'
    )

    mean_plot_var_2, = plt.plot(
        pos_post,
        list(full_stats_df[full_stats_df["Stat"] == "mean"][var_2]),
        marker='x', color='green', linestyle='--', label=f'Mitjana {var_2}'
    )

    plt.xticks(pos_pre + 0.075, groups)
    plt.ylabel("Valor")
    plt.xlabel(group_var)
    plt.title(f"Boxplots {var_1} i {var_2}")
    plt.grid(True)
    # plt.yticks(np.arange(6, 21, 1))

    red_patch = mpatches.Patch(color='red', alpha=0.5, label=var_1)
    green_patch = mpatches.Patch(color='lightgreen', alpha=0.5, label=var_2)
    plt.legend(handles=[red_patch, green_patch, mean_plot_var_1, mean_plot_var_2])

def plot_superboxplot(group_var, df, full_stats_df, start_fig):
    # Fig 1
    plt.figure(start_fig)

    # Positions for the boxes
    pos_pre = np.arange(1, 6, 1)
    pos_post = pos_pre + 0.08
    groups = ["Post-T", "Post-D", "Post-I", "Post-V", "Post-Son"]
    groups_means = ["Pre-T", "Pre-D", "Pre-I", "Pre-V", "Pre-Son"]

    # Boxplot Full vars no mar
    plt.boxplot(
        [df[df[group_var]==0][g] for g in groups],
        positions=pos_pre,
        widths=0.25,
        patch_artist=True,
        boxprops=dict(facecolor='lightblue', alpha=0.5),
        medianprops=dict(color='blue')
    )

    # Boxplot Full vars Mar
    plt.boxplot(
        [df[df[group_var]==1][g] for g in groups],
        positions=pos_post,
        widths=0.25,
        patch_artist=True,
        boxprops=dict(facecolor='lightgreen', alpha=0.5),
        medianprops=dict(color='green')
    )

    # Plot means
    mean_plot, = plt.plot(
        pos_pre,
        list(full_stats_df[(full_stats_df["Stat"] == "mean")][groups_means]
            .iloc[0].tolist()),
        marker='x',
        color='red',
        linestyle='',
        label='Mitjana Pre mostra completa'
    )

    plt.xticks(pos_pre + 0.075, groups)
    plt.ylabel("Valor")
    plt.xlabel("Variables")
    plt.title(f"Boxplots No Mar / Mar")
    plt.grid(True)
    # plt.yticks(np.arange(6, 21, 1))
    blue_patch = mpatches.Patch(color='lightblue', alpha=0.5, label='No Mar')
    green_patch = mpatches.Patch(color='lightgreen', alpha=0.5, label='Mar')

    plt.legend(handles=[blue_patch, green_patch, mean_plot])


#########################################################################################
#
# / Plots
#
#########################################################################################
