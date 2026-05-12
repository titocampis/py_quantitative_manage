import argparse
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pprint import pprint
import plots
from scipy.stats import chi2_contingency, spearmanr
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

def ask_to_plot():
    return input("¿Quieres ver los gráficos? (Y/n): ").lower()

def save_poltergeists(df: pd.DataFrame, verbose: bool = False) -> pd.DataFrame:
    """
    Save poltergeists in the dataset for later analysis
    """

    df = df.copy()

    if verbose:
        print("\n========================================================================================\nPoltergeists Saved\n========================================================================================")
        show_list = [
            "id",
            "p4_temps_lectura", 
            "p5_llibres", 
            "p6_pag", 
            "sessions", 
            "format"
        ]
        print("------------ Saved Poltergeist 1 (id=160)----------------\n > Incongruencia entre tiempo de lectura y número de libros leídos")
        print(df[df["id"] == 160][show_list].to_string(index=False)) # 2026/04/28 12:52:16 p. m. EEST

    # Poltergeist 1: Incongruencia entre tiempo de lectura y número de libros leídos
    df.loc[df["id"] == 160, "p4_temps_lectura"] = "Entre 30 minuts i 1 hora a la setmana."
    df.loc[df["id"] == 160, "p5_llibres"] = "3-5 llibres o còmics."
    df.loc[df["id"] == 160, "p6_pag"] = "100-299 pàgines."

    if verbose:
        print(df[df["id"] == 160][show_list].to_string(index=False))

    # Poltergeist 2: Incongruencia entre tiempo de lectura y número de libros leídos
    if verbose:
        print("\n------------ Saved Poltergeist 2 (id=104)----------------\n > Incongruencia entre tiempo de lectura y número de libros leídos")
        print(df[df["id"] == 104][show_list].to_string(index=False)) # 2026/04/27 11:38:51 a. m. EEST
    df.loc[df["id"] == 104, "p4_temps_lectura"] = "0 minuts."
    df.loc[df["id"] == 104, "p5_llibres"] = "0 llibres o còmics."

    if verbose:
        print(df[df["id"] == 104][show_list].to_string(index=False))

    # Poltergeist 3: Se ha olvidado poner las páginas leidas
    if verbose:
        print("\n------------ Saved Poltergeist 3 (id=138)----------------\n > Se ha olvidado poner las páginas leidas")
        print(df[df["id"] == 138][show_list].to_string(index=False)) # 2026/04/27 11:38:51 a. m. EEST
    df.loc[df["id"] == 138, "p6_pag"] = "100-299 pàgines."

    if verbose:
        print(df[df["id"] == 138][show_list].to_string(index=False)) # 2026/04/28 9:23:35 a. m. EEST

    # Poltergeist 4: Incongruencia entre tiempo de lectura y número de libros leídos
    if verbose:
        print("\n------------ Saved Poltergeist 4 (id=10)----------------\n > Incongruencia entre tiempo de lectura y número de libros leídos")
        print(df[df["id"] == 10][show_list].to_string(index=False)) # 2026/04/27 11:38:51 a. m. EEST
    df.loc[df["id"] == 10, "p6_pag"] = "1-99 pàgines."
    df.loc[df["id"] == 10, "p4_temps_lectura"] = "Menys de 30 minuts a la setmana."

    # Poltergeist 5: Incongruencia entre paginas y libros leidos + incongruencia tematica + tiempo y libros leidos
    if verbose:
        print("\n------------ Saved Poltergeist 5 (id=213)----------------\n > Incongruencia entre paginas y libros leidos + incongruencia tematica + tiempo y libros leidos")
        print(df[df["id"] == 213][show_list].to_string(index=False))
    df.loc[df["id"] == 213, "p4_temps_lectura"] = "0 minuts."

    # Poltergeist 6: Incongruencia entre tiempo de lectura y libros leidos
    if verbose:
        print("\n------------ Saved Poltergeist 6 (id=300)----------------\n > Incongruencia entre tiempo de lectura y número de libros leídos")
        print(df[df["id"] == 300][show_list].to_string(index=False))
    df.loc[df["id"] == 300, "p5_llibres"] = "3-5 llibres o còmics."

    # # Poltergeist X: Incongruencia entre tiempo de lectura y número de libros leídos (NO APLICADA, NO ES FILTRA)
    # if verbose:
    #     print("\n------------ Poltergeist 5 (id=105)----------------\n > Incongruencia entre tiempo de lectura y número de libros leídos")
    #     print(df[df["id"] == 105][show_list].to_string(index=False)) # 2026/04/27 11:38:51 a. m. EEST
    # df.loc[df["id"] == 105, "p4_temps_lectura"] = "Entre 30 minuts i 1 hora a la setmana."
    
    # Poltergeists perdidos:
    # - 191 - "2026/04/29 12:51:31 p. m. EEST"
    # - 263 - "2026/04/30 2:55:27 p. m. EEST"
    # - 252 - "2026/04/30 2:51:15 p. m. EEST"
    # - 52
    # - 58
    # - 74
    # - 6
    # - 29
    # - 103
    # - 143
    # - 298

    return df

def clean_reading_dataset_and_consistency(
    df: pd.DataFrame,
    verbose: bool = False
) -> pd.DataFrame:
    """
    Clean reading dataset and fix inconsistent answers.
    """

    df = df.copy()

    show_list = [
        "id",
        "p4_temps_lectura",
        "p5_llibres",
        "p6_pag",
        "sessions",
        "format"
    ]

    # =========================================================
    # BASE MASKS
    # =========================================================

    mask_no_lectura_oci = (
        (df["sessions"] == "No llegeixo per oci.") |
        (df["format"] == "No llegeixo per oci.")
    )

    temps_alts = [
        "Entre 30 minuts i 1 hora a la setmana.",
        "Entre 1 i 2 hores a la setmana.",
        "Entre 2 i 3 hores a la setmana.",
        "3 hores o més a la setmana."
    ]

    # NO APLICATS -> Pot ser que llegeixi poc una setaman habitual perque llegeix a l'estiu
    temps_baixos = [
        "0 minuts.",
        "Menys de 30 minuts a la setmana."
    ]
    
    llibres_alts = [
        "11-15 llibres o còmics.",
        "Més de 15 llibres o còmics"
    ]
    # -------------------------------------------------------------------------------------

    llibres_baixos = [
        "0 llibres o còmics.",
        "1-2 llibres o còmics."
    ]

    mask_incongruencia_temps_alts_llibres_baixos = (
        df["p4_temps_lectura"].isin(temps_alts) &
        df["p5_llibres"].isin(llibres_baixos)
    )

    # NO APLICADA -> Pot ser que llegeixi poc una setaman habitual perque llegeix a l'estiu
    mask_incongruencia_temps_baixos_llibres_alts = (
        df["p4_temps_lectura"].isin(temps_baixos) &
        df["p5_llibres"].isin(llibres_alts)
    )
    # -------------------------------------------------------------------------------------º

    # =========================================================
    # VERBOSE OUTPUT
    # =========================================================

    if verbose:

        print("\n========================================================================================")
        print("Filters to clean Dataset")
        print("========================================================================================")

        debug_filters = {
            "No lectura per oci però temps de lectura setmanal > 0": (
                mask_no_lectura_oci &
                (df["p4_temps_lectura"] != "0 minuts.")
            ),

            "No lectura per oci però llibres anuals > 0": (
                mask_no_lectura_oci &
                (df["p5_llibres"] != "0 llibres o còmics.")
            ),

            "Incongruencia temps alts i llibres baixos": (
                mask_incongruencia_temps_alts_llibres_baixos
            ), # NO APLICADA!!!
            "NO APLICAT!! --> Incongruencia temps baixos i llibres alts": (
                mask_incongruencia_temps_baixos_llibres_alts
            )
        }

        already_shown = pd.Series(False, index=df.index)

        for title, current_mask in debug_filters.items():

            # evitar duplicados entre bloques
            current_mask = current_mask & ~already_shown

            current_df = df[current_mask]

            print(f"\n{title} [{len(current_df)}] -----------------------------")

            if len(current_df) > 0:
                print(current_df[show_list].to_string(index=False))

            already_shown |= current_mask

    # =========================================================
    # CLEANING
    # =========================================================

    df.loc[mask_no_lectura_oci, "p4_temps_lectura"] = "0 minuts."
    df.loc[mask_no_lectura_oci, "p5_llibres"] = "0 llibres o còmics."

    df.loc[mask_incongruencia_temps_alts_llibres_baixos, "p4_temps_lectura"] = "0 minuts."
    # NO APLICAT -> Pot ser que llegeixi poc una setaman habitual perque llegeix a l'estiu
    # df.loc[mask_incongruencia_temps_baixos_llibres_alts, "p4_temps_lectura"] = "0 minuts.
    # -------------------------------------------------------------------------------------

    if verbose:
        print("\n========================================================================================")
        print("Unfiltered Inconsistencies")
        print("========================================================================================")
        print("\n------------ Numero de pag NaN pero no 0 minuts ----------------")
        print(df[(df["p6_pag"].isna()) & (df["p4_temps_lectura"] != "0 minuts.")][show_list].to_string(index=False))
        print("\n------------ Numero de pag NaN pero no 0 llibres ----------------")
        print(df[(df["p6_pag"].isna()) & (df["p5_llibres"] != "0 llibres o còmics.")][show_list].to_string(index=False))
        print("\n------------ Menys de 30 minuts i 0 llibres ----------------")
        print(df[(df["p4_temps_lectura"] == "Menys de 30 minuts a la setmana.") & (df["p5_llibres"] == "0 llibres o còmics.")][show_list].to_string(index=False))
        print("\n------------ Entre 30 minuts i 1 hora a la setmana i 0 llibres. ----------------")
        print(df[(df["p4_temps_lectura"] == "Entre 30 minuts i 1 hora a la setmana.") & (df["p5_llibres"] == "0 llibres o còmics.")][show_list].to_string(index=False))
        print("\n------------ Entre 1 i 2 hores a la setmana i 0 llibres. ----------------")
        print(df[(df["p4_temps_lectura"] == "Entre 1 i 2 hores a la setmana.") & (df["p5_llibres"] == "0 llibres o còmics.")][show_list].to_string(index=False))
        print("\n------------ Incongruencies llibres alts i temps baixos ----------------")
        print("* Beneficio de la duda, pot ser que llegeixi poc durant setmanes habituals perque llegeix a l'estiu")
        print(df[mask_incongruencia_temps_baixos_llibres_alts][show_list].to_string(index=False))

    return df

def classify_reader(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    temps_baix = [
        "0 minuts.",
        "Menys de 30 minuts a la setmana."
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
        [
            "No lector / Lector molt ocasional",
            "Lector habitual",
            "Lector ocasional"
        ],
        default="Sense classificar"
    )

    return df

def compute_thematic_scores(df, columnes_generes, map_thematic):

    resultats = {}

    for col in columnes_generes:

        puntuacio = (
            pd.to_numeric(df[col], errors="coerce")
            .map(map_thematic)
            .fillna(0)
            .sum()
        )

        resultats[col] = puntuacio

    resultats_df = (
        pd.DataFrame.from_dict(
            resultats,
            orient="index",
            columns=["puntuacio_total"]
        )
        .sort_values("puntuacio_total", ascending=False)
    )

    return resultats_df

def spearman_analysis(df, var1, var2, label=""):
    rho, p = spearmanr(df[var1], df[var2], nan_policy="omit")

    print(f"{label}")
    print(f"ρ = {rho:.3f}")
    print(f"p-value = {p:.5f}")
    print("--------------------------------------------------------")

    return rho, p

def chi_square_analysis(df, var1, var2, label=""):
    contingency = pd.crosstab(df[var1], df[var2])

    chi2, p, dof, expected = chi2_contingency(contingency)

    n = contingency.sum().sum()
    cramers_v = np.sqrt(chi2 / (n * (min(contingency.shape) - 1)))

    print(f"{label}")
    print(f"χ² = {chi2:.3f}")
    print(f"p-value = {p:.5f}")
    print(f"gl = {dof}")
    print(f"Cramér's V = {cramers_v:.3f}")
    print("--------------------------------------------------------")

    return chi2, p, dof, cramers_v

def plot_thematic_individual(results_dict):

    colors = {
        "Rànking de les temàtiques preferides per a la lectura per oci": "steelblue",
        "Rànking de les temàtiques preferides per a la lectura per oci entre les noies": "purple",
        "Rànking de les temàtiques preferides per a la lectura per oci entre els nois": "orange"
    }

    default_color = "steelblue"

    for title, df in results_dict.items():

        fig, ax = plt.subplots(figsize=(8, 5))

        freq = df["puntuacio_total"].copy()

        freq.index = [textwrap.fill(label, 15) for label in freq.index]

        color = colors.get(title, default_color)

        freq.plot(kind="bar", ax=ax, color=color)

        for i, v in enumerate(freq):
            ax.text(i, v, f"{int(v)}", ha="center", va="bottom")

        ax.set_title(title)
        ax.set_ylabel("Puntuació ponderada")
        ax.set_xlabel("Gèneres literaris")
        ax.tick_params(axis="x", rotation=45)

        plt.tight_layout()
        # plt.show()

def plot_descriptive_hists(df: pd.DataFrame, var: str, title: str, xlabel: str, ylabel: str, color: str = None, sort: list = None, ax=None):
    """
    Plot descriptive histograms for the TFM project (one figure per plot)
    """

    if sort is not None:
        df[var] = pd.Categorical(df[var], categories=sort, ordered=True)

    freq = df[var].value_counts(normalize=True).sort_index() * 100

    freq.index = [textwrap.fill(label, 15) for label in freq.index]

    # Nueva figura independiente solo si no le paso ax
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))

    freq.plot(kind="bar", ax=ax, color=color)

    n_total = len(df[var].dropna())

    for i, v in enumerate(freq):

        if pd.notna(v):

            ax.text(
                i,
                v,
                f"{v:.1f}% (n={int(v * n_total / 100)})",
                ha="center",
                va="bottom"
            )

    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    # plt.show()


def plot_descriptive_combined_hists(
    *dfs,
    var: str,
    groups: list,
    title: str,
    xlabel: str,
    ylabel: str,
    colors: list = None,
    sort: list = None,
    text: str = None,
    ax=None,
    figsize=(10, 5)
):
    """
    Plot combined descriptive histograms for multiple groups.

    Parameters
    ----------
    *dfs : pd.DataFrame
        DataFrames to compare.
    var : str
        Variable to plot.
    groups : list
        Names of each group.
    """

    # -----------------------------
    # Validación
    # -----------------------------
    if len(dfs) != len(groups):
        raise ValueError("len(dfs) must match len(groups)")

    # -----------------------------
    # Orden categorías
    # -----------------------------
    if sort is not None:
        dfs = [
            df.assign(
                **{
                    var: pd.Categorical(
                        df[var],
                        categories=sort,
                        ordered=True
                    )
                }
            )
            for df in dfs
        ]

    # -----------------------------
    # Frecuencias (%)
    # -----------------------------
    freq_dict = {}

    for df, group in zip(dfs, groups):

        if sort is not None:
            freq = (
                df[var]
                .value_counts(normalize=True)
                .reindex(sort, fill_value=0)
                * 100
            )
        else:
            freq = (
                df[var]
                .value_counts(normalize=True)
                * 100
            )

        freq_dict[group] = freq

    freq = pd.concat(freq_dict, axis=1).fillna(0)

    # -----------------------------
    # Wrap labels
    # -----------------------------
    freq.index = [
        textwrap.fill(str(label), 15)
        for label in freq.index
    ]

    # -----------------------------
    # Plot
    # -----------------------------
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    freq.plot(
        kind="bar",
        ax=ax,
        color=colors
    )

    # -----------------------------
    # Labels
    # -----------------------------
    for p in ax.patches:

        h = p.get_height()

        if h > 0:
            ax.text(
                p.get_x() + p.get_width() / 2,
                h,
                f"{h:.1f}",
                ha="center",
                va="bottom",
                fontsize=9
            )

    # -----------------------------
    # Estética
    # -----------------------------
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.tick_params(axis="x", rotation=45)
    
    if text is not None:
        ax.text(
            0.05,
            0.95,
            f"{text}",
            transform=ax.transAxes,
            verticalalignment='top'
    )

    plt.tight_layout()

#########################################################################################
#
# / Methods
#
#########################################################################################