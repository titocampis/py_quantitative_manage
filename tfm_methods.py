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

    # 1. Crear el parser
    parser = argparse.ArgumentParser(
        description="Parse command line arguments for the TFM project"
    )

    # 2. Argumento -v para verbosity
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbosity"
    )

    # 3. Argumento -t para recibir una lista de valores
    parser.add_argument(
        "-t",
        "--tags",
        type=lambda s: [int(x) for x in s.split(",")],
        default=[],  # si no se pasa -t, devuelve lista vacía
        help="Lista de valores separados por comas, ejemplo: -t 1,2,3,4"
    )

    # 4. Parsear argumentos
    args = parser.parse_args()

    # 5. Devolver lo que necesites
    return args.verbose, args.tags

def plot_descriptive_hists(df:pd.DataFrame, var:str, title:str, xlabel:str, ylabel:str, color:str=None, sort:list=None):
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
    freq_raw = df[var].value_counts().sort_index()
    freq_pct = df[var].value_counts(normalize=True).sort_index() * 100
    freq_raw.index = [textwrap.fill(label, 15) for label in freq_raw.index]
    freq_pct.index = [textwrap.fill(label, 15) for label in freq_pct.index]
    ax = freq_pct.plot(kind="bar")

    # print(freq_raw)
    # print(freq_pct)

    # Show freq values
    total = freq_raw.sum()
    for i, v in enumerate(freq_pct):
        ax.text(i, v, f"{v:.1f}% (n={int((v/100)*total)})", ha="center", va="bottom")

    # Edit text
    if color: 
        ax = freq_pct.plot(kind="bar", color=color)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha="center")
    plt.xlabel(xlabel)

    # plt.show()

def plot_descriptive_combined_hists2(df_1:pd.DataFrame, df_2:pd.DataFrame, var:str, groups:list, title:str, xlabel:str, ylabel:str, colors:list=None, sort:list=None):
    """
    Plot 2 descriptive histograms in the same plot for the TFM project
    """
    if sort is not None:
        df_1[var] = pd.Categorical(
            df_1[var],
            categories=sort,
            ordered=True
        )
        df_2[var] = pd.Categorical(
            df_2[var],
            categories=sort,
            ordered=True
        )

    # Plot frequency of categories
    freq = pd.concat({
        groups[0]: df_1[var].value_counts(normalize=True).sort_index() * 100,
        groups[1]: df_2[var].value_counts(normalize=True).sort_index() * 100
    }, axis=1).fillna(0)

    freq.index = [textwrap.fill(label, 15) for label in freq.index]

    ax = freq.plot(kind="bar", color=colors)

    # Show freq values
    for i in range(len(freq.index)):
        for j, col in enumerate(freq.columns):
            v = freq.iloc[i, j]

            if v > 0:
                total_group = freq[col].sum()  # 👈 clave

                ax.text(
                    i + j*0.25 - 0.125,
                    v,
                    f"{v:.1f}",
                    ha="center",
                    va="bottom"
                )

    # Edit text
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.xticks(rotation=45, ha="center")

     # plt.show()


def plot_descriptive_combined_hists4(df_1:pd.DataFrame, df_2:pd.DataFrame, df_3:pd.DataFrame, df_4:pd.DataFrame, var:str, groups:list, title:str, xlabel:str, ylabel:str, colors:list=None, sort:list=None):
    """
    Plot 4 descriptive histograms in the same plot for the TFM project
    """
    # -----------------------------
    # Ordenar categorías si existe sort
    # -----------------------------
    if sort is not None:
        for df in [df_1, df_2, df_3, df_4]:
            df[var] = pd.Categorical(
                df[var],
                categories=sort,
                ordered=True
            )

    # -----------------------------
    # Frecuencias normalizadas (%)
    # -----------------------------
    freq = pd.concat({
        groups[0]: df_1[var].value_counts(normalize=True).sort_index() * 100,
        groups[1]: df_2[var].value_counts(normalize=True).sort_index() * 100,
        groups[2]: df_3[var].value_counts(normalize=True).sort_index() * 100,
        groups[3]: df_4[var].value_counts(normalize=True).sort_index() * 100
    }, axis=1).fillna(0)

    # -----------------------------
    # Formato eje X
    # -----------------------------
    freq.index = [textwrap.fill(str(label), 15) for label in freq.index]

    # -----------------------------
    # Plot
    # -----------------------------
    ax = freq.plot(kind="bar", color=colors)

    # -----------------------------
    # Etiquetas centradas (FIX IMPORTANTE)
    # -----------------------------
    for p in ax.patches:
        height = p.get_height()

        if height > 0:
            ax.text(
                p.get_x() + p.get_width() / 2,
                height,
                f"{height:.1f}",
                ha="center",
                va="bottom",
                fontsize=9
            )

    # -----------------------------
    # Estética final
    # -----------------------------
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.xticks(rotation=45, ha="center")

#########################################################################################
#
# / Methods
#
#########################################################################################