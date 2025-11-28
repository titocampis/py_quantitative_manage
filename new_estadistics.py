import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pprint import pprint

#########################################################################################
#
# Methods
#
#########################################################################################

def clean_np_dictionary(d: dict):
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

def calc_stats(list_elems: list):
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


#########################################################################################
#
# / Methods
#
#########################################################################################

#########################################################################################
#
# Main Program
#
#########################################################################################
# Import df from csv
df = pd.read_csv("dades.csv")

# Create statistics dictionary
full_stats_dict = create_complete_stats_dict(df, "Act", ["Pre-T", "Pre-D", "Pre-I", "Pre-V", "Post-T", "Post-D", "Post-I", "Post-V", "Pre-Son", "Post-Son"])

# Convert dictionary to a df
full_stats_df = dict_to_tidy_df(full_stats_dict)

# Export df to csv
# full_stats_df.to_csv("estadisticas_completas.csv", index=False)

# To test
# full_stats_dict_cleaned = clean_np_dictionary(full_stats_dict)
# pprint(full_stats_dict_cleaned, sort_dicts=True, width=80)
# print(full_stats_df)

# Export df_grouped to csv's
select_and_export_df(full_stats_df, ['Stat', 'Pre-D', 'Post-D'])

#########################################################################################
#
# / Main Program
#
#########################################################################################

#########################################################################################
#
# Plots
#
#########################################################################################
which_plot = 3 # 1, 2 or 3
axis_x = [1, 2, 3, 4]
groups = list(dict.fromkeys(full_stats_df["Group"]))

# First plot
# ---------------------------
if which_plot == 1:
    # Figure 1
    plt.figure(1)
    plt.title(f"Valors Estadístics de la variable Depressió recollida prèviament (Pre-D)")
    plt.xlabel("Grup")
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

    # Figure 2
    plt.figure(2)
    plt.title(f"Valors Estadístics de la variable Depressió recollida posteriorment (Post-D)")
    plt.xlabel("Grup")
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

# 2 Plot
# ---------------------------
elif which_plot == 2:
    # Figure 3
    plt.figure(3)
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

    # Figure 4

    # Calculate dif
    dif_mean = np.array(list(full_stats_df[full_stats_df["Stat"] == "mean"]["Pre-D"])) - np.array(list(full_stats_df[full_stats_df["Stat"] == "mean"]["Post-D"]))
    dif_q3 = np.array(list(full_stats_df[full_stats_df["Stat"] == "Q3"]["Pre-D"])) - np.array(list(full_stats_df[full_stats_df["Stat"] == "Q3"]["Post-D"]))
    dif_q2 = np.array(list(full_stats_df[full_stats_df["Stat"] == "Q2"]["Pre-D"])) - np.array(list(full_stats_df[full_stats_df["Stat"] == "Q2"]["Post-D"]))
    dif_q1 = np.array(list(full_stats_df[full_stats_df["Stat"] == "Q1"]["Pre-D"])) - np.array(list(full_stats_df[full_stats_df["Stat"] == "Q1"]["Post-D"]))

    plt.figure(4)
    plt.title(f"Diferència d'estadístics (PRE-POST) de la variable Depressió ")
    plt.xlabel("Grup")
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

    # Figure 5
    plt.figure(5)
    plt.title(f"Desviació típica (σ) de la variable depressió")
    plt.xlabel("Grup")
    plt.ylabel("σ")

    labels = groups
    plt.plot(axis_x, list(full_stats_df[full_stats_df["Stat"] == "std"]["Pre-D"]), marker='o', color='red', label="Pre-D", linestyle='--')
    plt.plot(axis_x, list(full_stats_df[full_stats_df["Stat"] == "std"]["Post-D"]), marker='o', color='green', label="Post-D", linestyle='--')
    plt.xticks(axis_x, labels)

    plt.yticks(np.arange(0.8, 2.2, 0.1))
    plt.grid(True)
    plt.legend()

# 3 Plot
# ---------------------------
elif which_plot == 3:
    # Figure 6
    # Positions for the boxes
    pos_pre = np.arange(1, 5)
    pos_post = pos_pre + 0.08

    # Boxplot Pre-D
    plt.boxplot(
        [df[df["Act"]==g]["Pre-D"] for g in groups],
        positions=pos_pre,
        widths=0.25,
        patch_artist=True,
        boxprops=dict(facecolor='red', alpha=0.5),
        medianprops=dict(color='darkred')
    )

    # Boxplot Post-D
    plt.boxplot(
        [df[df["Act"]==g]["Post-D"] for g in groups],
        positions=pos_post,
        widths=0.25,
        patch_artist=True,
        boxprops=dict(facecolor='lightgreen', alpha=0.5),
        medianprops=dict(color='green')
    )

    # Plot means
    plt.plot(
        pos_pre,
        list(full_stats_df[full_stats_df["Stat"] == "mean"]["Pre-D"]),
        marker='x', color='red', linestyle='--', label='Mitjana Pre-D'
    )

    plt.plot(
        pos_post,
        list(full_stats_df[full_stats_df["Stat"] == "mean"]["Post-D"]),
        marker='x', color='green', linestyle='--', label='Mitjana Post-D'
    )

    plt.xticks(pos_pre + 0.075, groups)
    plt.ylabel("Valor")
    plt.xlabel("Grup")
    plt.title("Boxplots Pre-D i Post-D")
    plt.legend()
    plt.grid(True)
    plt.yticks(np.arange(6, 21, 1))

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
