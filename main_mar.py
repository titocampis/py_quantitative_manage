import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pprint import pprint
from scipy.stats import linregress
import sys

import methods as mt
import plots

#########################################################################################
#
# Variables
#
#########################################################################################
# Create statistics df from csv
csv_name = "dades.csv"
group_var = "Mar"
statistics_vars = ["Pre-T", "Pre-D", "Pre-I", "Pre-V", "Post-T", "Post-D", "Post-I", "Post-V", "Pre-Son", "Post-Son"]

# Checks / prints
check_df = False
check_dict = False

# Export
# # Full csv
export_full_csv = False
export_full_csv_name = "estadisticas_completas.csv"

# # Grouped csv
export_groups_csv = False
export_groups_csv_vars = ['Stat', 'Pre-D', 'Post-D']

# Regression
make_regression = True
step_by_step_regression = False

# First figure
start_fig = 1

#########################################################################################
#
# / Variables
#
#########################################################################################

#########################################################################################
#
# Main Operations
#
#########################################################################################
# Import df from csv
df = pd.read_csv(csv_name)

# Create statistics dictionary
full_stats_dict = mt.create_complete_stats_dict(df, group_var, statistics_vars)

# Check statistics dictionary
if check_dict: 
    full_stats_dict_cleaned = mt.clean_np_dictionary(full_stats_dict)
    pprint(full_stats_dict_cleaned, sort_dicts=True, width=80)

# Convert dictionary to a df
full_stats_df = mt.dict_to_tidy_df(full_stats_dict)

# Check df
if check_df: 
    pprint(full_stats_df, sort_dicts=True, width=80)
    # pprint(full_stats_df[full_stats_df["Stat"] == "std"][["Group","Pre-Son", "Post-Son"]], sort_dicts=True, width=80)
    # pprint(full_stats_df[["Group", "Stat", "Pre-Son", "Post-Son"]], sort_dicts=True, width=80)
    # print(df[df["Mar"]==0]["Pre-T"])

# Export df to csv
if export_full_csv: full_stats_df.to_csv(export_full_csv_name, index=False)

# Export df_grouped to csv's
if export_groups_csv: mt.select_and_export_df(full_stats_df, export_groups_csv_vars)

#########################################################################################
#
# / Main Operations
#
#########################################################################################

#########################################################################################
#
# Regression
#
#########################################################################################
if make_regression:
    mt.calc_regression(df, "Post-D", "Post-Son", step_by_step_regression, start_fig)
    start_fig += 1

#########################################################################################
#
# / Regression
#
#########################################################################################

#########################################################################################
#
# Plots
#
#########################################################################################
# Which plot
which_plot = int(sys.argv[1]) # 1, 2, 3, 4 ...

# Variables
groups = list(dict.fromkeys(full_stats_df["Group"]))
axis_x = np.arange(1, len(groups) + 1, 1)

# Plots
if which_plot == 1:
    plots.plot_double_boxplot(axis_x, groups, group_var, "Pre-T", "Post-T", df, full_stats_df, start_fig)
    plots.plot_double_boxplot(axis_x, groups, group_var, "Pre-D", "Post-D", df, full_stats_df, start_fig + 1)
    plots.plot_double_boxplot(axis_x, groups, group_var, "Pre-I", "Post-I", df, full_stats_df, start_fig + 2)
    plots.plot_double_boxplot(axis_x, groups, group_var, "Pre-V", "Post-V", df, full_stats_df, start_fig + 3)
    plots.plot_double_boxplot(axis_x, groups, group_var, "Pre-Son", "Post-Son", df, full_stats_df, start_fig + 4)

elif which_plot == 2:
    plots.plot_superboxplot(group_var, df, full_stats_df, start_fig)

else:
    print("Nothing to plot.")

# If anything to plot:
if which_plot != None or which_plot != 0:
    plt.show()

#########################################################################################
#
# / Plots
#
#########################################################################################
