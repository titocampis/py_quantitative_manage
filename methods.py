import numpy as np
import pandas as pd
from pprint import pprint
from scipy.stats import linregress
import plots

#########################################################################################
#
# Methods
#
#########################################################################################

def clean_np_dictionary(d:dict):
    """
    Cleans np dictionaries
    """
    if not isinstance(d, dict):
        return d

    cleaned = {}
    for key, value in d.items():
        if isinstance(value, dict):
            cleaned[key] = clean_np_dictionary(value)
        elif isinstance(value, (np.float64, float)):
            cleaned[key] = float(value)
        elif isinstance(value, (np.int64, int)):
            cleaned[key] = int(value)
        else:
            cleaned[key] = value
    return cleaned

def calc_stats(list_elems:list, print:bool=None):
    """
    Calculates basic stadistics from a list of elements and returns it as a dictionary
    """
    only_stats_dict = {
        "mean": round(list_elems.mean(), 2),
        "var": round(list_elems.var(), 2),
        "std": round(list_elems.std(), 2),
        "min": round(list_elems.min(), 2),
        "Q1": round(list_elems.quantile(0.25), 2),
        "Q2": round(list_elems.quantile(0.50), 2),
        "Q3": round(list_elems.quantile(0.75), 2),
        "max": round(list_elems.max(), 2),
        "cv (%)": round(100 * list_elems.std() / list_elems.mean(), 2)
    }

    if print:
        pprint(only_stats_dict, sort_dicts=True, width=80)

    return only_stats_dict

def create_complete_stats_dict(df: pd.DataFrame, groups_varname:str, variables: list):
    """
    Creates a superdictionary with the statistics nested into the groups, and the groups nested into
    the variables
    """
    full_stats_dict = {}
    
    # Get all groups
    groups = list(dict.fromkeys(df[groups_varname]))

    # Get stats for each specified variable
    for var in variables:
        if var not in df.columns:
            print(f"[WARNING]: Variable <<{var}>> not on the dataframe. Skipping.")
            continue

        full_stats_dict[var] = {}

        # Get stats for each specified group
        for group in groups:
            # Filter by group and variable
            series = df[df[groups_varname] == group][var]
            full_stats_dict[var][group] = calc_stats(series)

    return full_stats_dict
    # { 
    #    "Var1": 
    #           {
    #                 "Group1": 
    #                           {
    #                               "mean": 1,
    #                               "std": 0.5,
    #                                ...
    #                           },
    #                 "Group2": 
    #                           {
    #                               "mean": 1,
    #                               "std": 0.5,
    #                               ...
    #                           }
    #                 ...
    #         },

    #    "Var2": 
    #           {
    #                 "Group1": 
    #                           {
    #                               "mean": 1,
    #                               "std": 0.5,
    #                                ...
    #                           },
    #                 "Group2": 
    #                           {
    #                               "mean": 1,
    #                               "std": 0.5,
    #                               ...
    #                           }
    #                 ...
    #           }
    #           ...
    # }

def dict_to_tidy_df(full_stats_dict:dict):
    """
    Converts a dictionary: dict[Var][Group][Stat] 
    Into a pandas.df: Group | Stat | Var1 | Var2 | ...
    """
    # List of dictionaries for each row
    rows = []

    # Iterate the full dictionary
    for var_name, groups_dict in full_stats_dict.items():
        # For each group (A,B,C,D,...) 
        for group_name, stats in groups_dict.items():
            # For each stat (mean, std, min, max,...)
            for stat_name, value in stats.items():
                # Append the dictionary to the list 
                rows.append({
                    'Group': group_name,
                    'Stat': stat_name,
                    'Variable': var_name,
                    'Value': value
                })

    # Create a dataframe from the list of dictionaries
    df_long = pd.DataFrame(rows)

    # Pivot to define rowed data into rows (A,B,C,D - mean,std,min,...), columns (Pre-D, Post-D, ...), and values (0.5, 2.7, ...)
    df_wide = df_long.pivot_table(index=['Group', 'Stat'], columns='Variable', values='Value')

    # Clean and reset index
    df_wide = df_wide.reset_index()
    df_wide.columns.name = None

    return df_wide

def select_and_export_df(full_stats_df:pd.DataFrame, desired_vars:list):
    """
    Selects vars from a full stats df and converts it into csv
    """
    # Get all groups
    groups = list(dict.fromkeys(full_stats_df["Group"]))

    for group in groups:
        df_gruped = full_stats_df[full_stats_df["Group"] == f"{group}"]

        # Make a subset with desired columns
        df_gruped_subset = df_gruped[desired_vars]

        # Export df to csv
        df_gruped_subset.to_csv(f"exported_csvs/{group}_PreD_PostD.csv", index=False)


def calc_regression(df, var_x, var_y, start_fig, step_by_step=None):
    # Easy way
    cov = df[var_x].cov(df[var_y])
    corr = df[var_x].corr(df[var_y])
    slope, intercept, r_value, p_value, std_err = linregress(df[var_x], df[var_y])
    print("Linear Regression\n--------------")
    print(f"Covariance:                {round(cov, 2)}")
    print(f"Correlation Coefficient:   {round(corr, 2)}\n")
    if intercept > 0: print(f"y = {slope}·x + {intercept}\n")
    else: print(f"y = {slope}·x + {intercept}\n")
    plots.plot_regression(df, var_x, var_y, slope, intercept, start_fig)

    # Calculated table
    if step_by_step:
        stats_var_x = calc_stats(df[var_x])
        stats_var_y = calc_stats(df[var_y])
        mean_var_x = stats_var_x["mean"]
        mean_var_y = stats_var_y["mean"]

        var_x_less_m = [round(x - float(mean_var_x), 2) for x in list(df[var_x])]
        var_y_less_m = [round(x - float(mean_var_y), 2) for x in list(df[var_y])]
        
        covariance_list = [round(var_x_less_m[i] * var_y_less_m[i], 2) for i in range(len(var_y_less_m))]

        covariance = sum(covariance_list) / (len(var_y_less_m) - 1)
        correlation = covariance / (stats_var_x["std"] * stats_var_y["std"])

        print(f"Covariance calculated:                {round(covariance, 2)}")
        print(f"Correlation Coefficient calculated:   {round(correlation, 2)}\n")

#########################################################################################
#
# / Methods
#
#########################################################################################