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

def clean_reading_dataset_and_consistency(df: pd.DataFrame, verbose: bool = False) -> pd.DataFrame:
    """
    Clean the reading dataset from noise
    """

    df = df.copy()

    if verbose:
        print(df[(df["Quan llegeixes, com acostumen a ser les teves sessions de lectura?"] == "No llegeixo per oci.") & (df["Quin format de lectura utilitzes més habitualment per a la lectura de llibres o còmics per oci? "] == "No llegeixo per oci.")][["p4_temps_lectura", "p5_llibres", "p6_pag"]].to_string(index=False))

    mask_p4 = (
        # (df["p5_llibres"] == "0 llibres o còmics.") |
        (df["Quan llegeixes, com acostumen a ser les teves sessions de lectura?"] == "No llegeixo per oci.") &
        (df["Quin format de lectura utilitzes més habitualment per a la lectura de llibres o còmics per oci? "] == "No llegeixo per oci.")
    )
    
    mask_p5 = (
        # (df["p4_temps_lectura"] == "0 minuts.") |
        (df["Quan llegeixes, com acostumen a ser les teves sessions de lectura?"] == "No llegeixo per oci.") &
        (df["Quin format de lectura utilitzes més habitualment per a la lectura de llibres o còmics per oci? "] == "No llegeixo per oci.")
    )

    df.loc[mask_p4, "p4_temps_lectura"] = "0 minuts."
    df.loc[mask_p5, "p5_llibres"] = "0 llibres o còmics."

    return df

def classify_reader(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    temps_baix = [
        "0 minuts.",
        # "Menys de 30 minuts a la setmana."
    ]

    temps_alt = [
        "Entre 1 i 2 hores a la setmana.",
        "Entre 2 i 3 hores a la setmana.",
        "3 hores o més a la setmana."
    ]

    # 1. NO LECTOR (prioridad máxima)
    cond_no = (
        (df["p4_temps_lectura"].isin(temps_baix)) |
        (df["p5_6_pagines_num"] <= 300)
    )

    # 2. HABITUAL (alta intensidad)
    cond_habitual = (
        (df["p4_temps_lectura"].isin(temps_alt)) &
        (df["p5_6_pagines_num"] >= 1200)
    )

    # 3. OCASIONAL (resto que no es nada de lo anterior)
    cond_ocasional = ~(cond_no | cond_habitual)

    df["classificacio_lectora"] = np.select(
        [cond_no, cond_habitual, cond_ocasional],
        ["No lector / Lector molt ocasional", "Lector habitual", "Lector ocasional"]
    )

    return df


def plot_descriptive_hists(df: pd.DataFrame, var: str, title: str, xlabel: str, ylabel: str, color: str = None, sort: list = None):
    """
    Plot descriptive histograms for the TFM project (one figure per plot)
    """

    if sort is not None:
        df[var] = pd.Categorical(df[var], categories=sort, ordered=True)

    freq = df[var].value_counts(normalize=True).sort_index() * 100

    freq.index = [textwrap.fill(label, 15) for label in freq.index]

    # Nueva figura independiente
    fig, ax = plt.subplots()

    freq.plot(kind="bar", ax=ax, color=color)

    n_total = len(df[var].dropna())

    for i, v in enumerate(freq):
        ax.text(i, v, f"{v:.1f}% (n={int(v * n_total / 100)})", ha="center", va="bottom")

    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    # plt.show()


def plot_descriptive_combined_hists2(df_1, df_2, var, groups, title, xlabel, ylabel, colors=None, sort=None):

    if sort is not None:
        df_1[var] = pd.Categorical(df_1[var], categories=sort, ordered=True)
        df_2[var] = pd.Categorical(df_2[var], categories=sort, ordered=True)

    freq_1 = df_1[var].value_counts(normalize=True).reindex(sort, fill_value=0) * 100
    freq_2 = df_2[var].value_counts(normalize=True).reindex(sort, fill_value=0) * 100

    freq = pd.concat({groups[0]: freq_1, groups[1]: freq_2}, axis=1).fillna(0)

    freq.index = [textwrap.fill(str(label), 15) for label in freq.index]

    # Independent figure
    fig, ax = plt.subplots()

    freq.plot(kind="bar", ax=ax, color=colors)

    for p in ax.patches:
        h = p.get_height()
        if h > 0:
            ax.text(p.get_x() + p.get_width()/2, h, f"{h:.1f}", ha="center")

    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    # plt.show()


def plot_descriptive_combined_hists4(
    df_1: pd.DataFrame,
    df_2: pd.DataFrame,
    df_3: pd.DataFrame,
    df_4: pd.DataFrame,
    var: str,
    groups: list,
    title: str,
    xlabel: str,
    ylabel: str,
    colors: list = None,
    sort: list = None
):
    """
    Plot 4 descriptive histograms in the same plot for the TFM project (one figure)
    """

    # -----------------------------
    # Ordenar categorías si existe sort
    # -----------------------------
    if sort is not None:
        for df in [df_1, df_2, df_3, df_4]:
            df[var] = pd.Categorical(df[var], categories=sort, ordered=True)

    # -----------------------------
    # Frecuencias normalizadas (%)
    # -----------------------------
    freq = pd.concat({
        groups[0]: df_1[var].value_counts(normalize=True).reindex(sort).fillna(0) * 100,
        groups[1]: df_2[var].value_counts(normalize=True).reindex(sort).fillna(0) * 100,
        groups[2]: df_3[var].value_counts(normalize=True).reindex(sort).fillna(0) * 100,
        groups[3]: df_4[var].value_counts(normalize=True).reindex(sort).fillna(0) * 100
    }, axis=1).fillna(0)

    # -----------------------------
    # Formato eje X
    # -----------------------------
    freq.index = [textwrap.fill(str(label), 15) for label in freq.index]

    # -----------------------------
    # FIGURA NUEVA (clave)
    # -----------------------------
    fig, ax = plt.subplots(figsize=(10, 5))

    freq.plot(kind="bar", ax=ax, color=colors)

    # -----------------------------
    # Etiquetas centradas
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
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    # plt.show()

#########################################################################################
#
# / Methods
#
#########################################################################################