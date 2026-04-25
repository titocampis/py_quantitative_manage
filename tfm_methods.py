import argparse
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pprint import pprint
from scipy.stats import linregress
import plots
import textwrap

#########################################################################################
#
# Methods
#
#########################################################################################
def parse_arguments():
    """
    Parse command line arguments
    """

    # 1. Crete the parser
    parser = argparse.ArgumentParser(description="Parse command line arguments for the TFM project")

    # 2. Add -v argument for verbosity
    # action="store_true" hace que si el flag existe, valga True, y si no, False
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbosity")

    # 3. Parseamos los argumentos
    args = parser.parse_args()

    # 4. Asignamos a tu variable
    return args.verbose

def plot_descriptive_hists(df:pd.DataFrame, var:str, title:str, xlabel:str, ylabel:str, sort:list=None):
    """
    Plot descriptive histograms for the TFM project
    """
    if sort is not None:
        df[var] = pd.Categorical(
            df[var],
            categories=sort,
            ordered=True
        )

    # Plot frequency of categories
    freq = df[var].value_counts().sort_index()
    freq.index = [textwrap.fill(label, 15) for label in freq.index]
    ax = freq.plot(kind="bar")

    # Show freq values
    total = freq.sum()
    for i, v in enumerate(freq):
        ax.text(i, v, f"{v} alumnes | {(v/total)*100:.1f}%", ha="center", va="bottom")
        # ax.text(i, v, f"{(v/total)*100:.1f}%", ha="center", va="bottom")

    # Edit text
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha="center")
    plt.xlabel(xlabel)

    # plt.show()


#########################################################################################
#
# / Methods
#
#########################################################################################