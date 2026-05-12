import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pprint import pprint
from scipy.stats import chi2_contingency
from scipy.stats import spearmanr
import sys

import methods as mt
import textwrap
import tfm_methods as tmt

#########################################################################################
#
# Variables
#
#########################################################################################
# Create statistics df from csv
csv_name = "forms-habits-lectura-compartit.csv"

# Verbosity
verbose, tags = tmt.parse_arguments()

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

# =======================================================================================
# First Data Inspection
# =======================================================================================
# Import df from csv
df = pd.read_csv(csv_name)

# Ad id column
df["id"] = range(1, len(df) + 1)

# Print df data
if verbose:
    print("========================================================================================\nCheck Dataset\n========================================================================================")
    print(f"Dataframe dimensions (rows, cols): {df.shape}")
    print(f"First 5 lines of the dataframe: \n{df.head()}")
    # print(f"\nCheck no null values:")
    # print(df.info())
    # print(f"\nCheck no nulls values per column:")
    # print(df.isnull().sum())

# =======================================================================================
# Rename some important columns
# =======================================================================================
df = df.rename(columns={
    "Quant temps a la setmana dediques, de mitjana, a la lectura de llibres o còmics per oci? (Ja sigui en format físic o digital).": "p4_temps_lectura",
    "Quants llibres o còmics t’has llegit aproximadament en els últims 12 mesos per oci? (Ja sigui en format físic o digital)": "p5_llibres",
    "En cas que la resposta hagi estat diferent de 0 llibres o còmics, quantes pàgines, de mitjana, tenien aproximadament aquests llibres o còmics?": "p6_pag",
    "Actualment estàs llegint algun llibre o còmic per oci?": "p7_lectura_actual",
    "Quants cops aproximadament has visitat una biblioteca per llegir o agafar llibres en préstec en els últims 12 mesos per oci?": "p10_visites_biblioteca",
    "En quin grau llegeixes les lectures obligatòries de l’escola?": "p16_lectura_obligatoria", 
    "Quin format de lectura utilitzes més habitualment per a la lectura de llibres o còmics per oci? ": "format",
    "Quan llegeixes, com acostumen a ser les teves sessions de lectura?" : "sessions",
    "Marca ordenadament els 3 gèneres literaris que més llegeixes per oci. [Novel·la fantàstica.]": "Novel·la fantàstica",
    "Marca ordenadament els 3 gèneres literaris que més llegeixes per oci. [Novel·la romàntica.]": "Novel·la romàntica",
    "Marca ordenadament els 3 gèneres literaris que més llegeixes per oci. [Novel·la de terror.]": "Novel·la de terror",
    "Marca ordenadament els 3 gèneres literaris que més llegeixes per oci. [Novel·la negra.]": "Novel·la negra",
    "Marca ordenadament els 3 gèneres literaris que més llegeixes per oci. [Novel·la històrica.]": "Novel·la històrica",
    "Marca ordenadament els 3 gèneres literaris que més llegeixes per oci. [Ciència ficció.]": "Ciència ficció",
    "Marca ordenadament els 3 gèneres literaris que més llegeixes per oci. [Còmic.]": "Còmic",
    "Marca ordenadament els 3 gèneres literaris que més llegeixes per oci. [Clàssics.]": "Clàssics",
    "Marca ordenadament els 3 gèneres literaris que més llegeixes per oci. [Poesia.]": "Poesia",
    "Marca ordenadament els 3 gèneres literaris que més llegeixes per oci. [Assaig (Filosofia, divulgació científica, etc.)]": "Assaig",
    "Marca ordenadament els 3 gèneres literaris que més llegeixes per oci. [Teatre.]": "Teatre"
})

# =======================================================================================
# Sorting, maps and Spearman ready variables
# =======================================================================================
# Maps
# =======================================================

# Generic sorts and maps
# ===
sort_gust = [
    "Gens.",
    "Poc.",
    "Regular.",
    "Bastant.",
    "Molt."
]

map_gust_sp = {
    "Gens.": 0,
    "Poc.": 1,
    "Regular.": 2,
    "Bastant.": 3,
    "Molt.": 4    
}

sort_acords = [
    "Molt en desacord.",
    "Poc d'acord,",
    "Parcialment d'acord.",
    "Bastant d'acord.",
    "Molt d'acord."
]

map_acord_sp = {
    "Molt en desacord.": 0,
    "Poc d'acord,": 1,
    "Parcialment d'acord.": 2,
    "Bastant d'acord.": 3,
    "Molt d'acord.": 4
}

sort_freq = [
    "Mai.",
    "Gairebé mai.",
    "Algunes vegades.",
    "Sovint.",
    "Molt sovint."
]

map_freq_sp = {
    "Mai.": 0,
    "Gairebé mai.": 1,
    "Algunes vegades.": 2,
    "Sovint.": 3,
    "Molt sovint.": 4
}

# Temps de lectura setmanal
# ===
sort_temps = [
    "0 minuts.",
    "Menys de 30 minuts a la setmana.",
    "Entre 30 minuts i 1 hora a la setmana.",
    "Entre 1 i 2 hores a la setmana.",
    "Entre 2 i 3 hores a la setmana.",
    "3 hores o més a la setmana."
]

map_temps_sp = {
    "0 minuts.": 0,
    "Menys de 30 minuts a la setmana.": 1,
    "Entre 30 minuts i 1 hora a la setmana.": 2,
    "Entre 1 i 2 hores a la setmana.": 3,
    "Entre 2 i 3 hores a la setmana.": 4,
    "3 hores o més a la setmana.": 5
}

# Llibres 12 mesos
# ===
sort_llibres = [
    "0 llibres o còmics.",
    "1-2 llibres o còmics.",
    "3-5 llibres o còmics.",
    "6-10 llibres o còmics.",
    "11-15 llibres o còmics.",
    "Més de 15 llibres o còmics"
]

map_llibres_num = {
    "0 llibres o còmics.": 0,
    "1-2 llibres o còmics.": 1.5,
    "3-5 llibres o còmics.": 4,
    "6-10 llibres o còmics.": 8,
    "11-15 llibres o còmics.": 13,
    "Més de 15 llibres o còmics": 18
}

map_llibres_sp = {
    "0 llibres o còmics.": 0,
    "1-2 llibres o còmics.": 1,
    "3-5 llibres o còmics.": 2,
    "6-10 llibres o còmics.": 3,
    "11-15 llibres o còmics.": 4,
    "Més de 15 llibres o còmics": 5
}

# Pàgines anuals
# ===
map_pagines_sp = {
    "0": 0,
    "1-300": 1,
    "301-800": 2,
    "801-2000": 3,
    "2001-4000": 4,
    ">4000": 5
}

map_pagines_num = {
    "1-99 pàgines.": 50,
    "100-299 pàgines.": 200,
    "300-599 pàgines.": 450,
    "Més de 600 pàgines": 700
}

# Classificació lectora
# ===
map_class_sp =  {
    "No lector / Lector molt ocasional": 0,
    "Lector ocasional": 1,
    "Lector habitual": 2
}

# Sessions de lectura
# ===
sort_sessions = [
    "Llegeixo gairebé sempre en estones molt curtes (menys de 15 minuts).",
    "Llegeixo sobretot en estones curtes (15–30 minuts).",
    "Combino estones curtes (15–30 minuts) i mitjanes (30–60 minuts).",
    "Llegeixo habitualment en sessions mitjanes (30-60 minuts) i llargues (més d’1 hora seguida).",
    "Depèn molt del moment (no tinc un patró clar)."
]

map_sessions_sp = {
    "Llegeixo gairebé sempre en estones molt curtes (menys de 15 minuts).": 0,
    "Llegeixo sobretot en estones curtes (15–30 minuts).": 1,
    "Combino estones curtes (15–30 minuts) i mitjanes (30–60 minuts).": 2,
    "Llegeixo habitualment en sessions mitjanes (30-60 minuts) i llargues (més d’1 hora seguida).": 3
}

sort_distraccions_inv = [
    "No miro mai les xarxes socials mentre llegeixo",
    "Cada 2 hores aprox.",
    "Cada hora aprox.",
    "Cada 30 minuts aprox.",
    "Cada 15 minuts aprox.",
    "Cada 5 minuts aprox."
]

map_distraccions_inv_sp = {
    "Cada 5 minuts aprox.": 5,
    "Cada 15 minuts aprox.": 4,
    "Cada 30 minuts aprox.": 3,
    "Cada hora aprox.": 2,
    "Cada 2 hores aprox.": 1,
    "No miro mai les xarxes socials mentre llegeixo": 0
}

# Biblioteca
# ===
sort_visites_biblioteca_anual = [
    "0 cops.",
    "1-2 cops.",
    "3-5 cops.",
    "6-10 cops.",
    "Més de 10 cops."
]

map_visites_biblioteca_anual_sp = {
    "0 cops.": 0,
    "1-2 cops.": 1,
    "3-5 cops.": 2,
    "6-10 cops.": 3,
    "Més de 10 cops.": 4
}

# Lectura obligatoria
# ===
sort_lectura_obligatoria = [
    "No en llegeixo cap.",
    "En llegeixo poques o molt poques.",
    "En llegeixo aproximadament la meitat.",
    "Les llegeixo gairebé totes.",
    "Les llegeixo totes."
]

map_lectura_obligatoria_sp = {
    "No en llegeixo cap.": 0,
    "En llegeixo poques o molt poques.": 1,
    "En llegeixo aproximadament la meitat.": 2,
    "Les llegeixo gairebé totes.": 3,
    "Les llegeixo totes.": 4    
}

# Narrativa social adolescent sobre la lectura
# ===
sort_afirmacio = [
    "La lectura no m'agrada gens o em sembla avorrida.",
    "No m’agrada gaire la lectura o no em resulta interessant.",
    "La lectura m’és indiferent.",
    "La lectura em sembla interessant i una activitat agradable.",
    "La lectura em sembla molt interessant i una activitat molt positiva."
]

map_afirmacio_sp = {
    "La lectura no m'agrada gens o em sembla avorrida.": 0,
    "No m’agrada gaire la lectura o no em resulta interessant.": 1,
    "La lectura m’és indiferent.": 2,
    "La lectura em sembla interessant i una activitat agradable.": 3,
    "La lectura em sembla molt interessant i una activitat molt positiva.": 4
}

sort_com_es_veu = [
    "Una activitat avorrida o poc interessant.",
    "Una activitat normal, sense cap etiqueta especial.",
    "Una activitat positiva o interessant."
]

map_com_es_veu_sp = {
    "Una activitat avorrida o poc interessant.": 0,
    "Una activitat normal, sense cap etiqueta especial.": 1,
    "Una activitat positiva o interessant.": 2
}

# TRIC
# ===
sort_tric = [
    "0 minuts al dia.",
    "Menys de 30 minuts al dia.",
    "Entre 30 minuts i 1 hora al dia.",
    "Entre 1 i 2 hores al dia.",
    "Entre 2 i 3 hores al dia.",
    "3 hores o més al dia."
]

map_tric_sp = {
    "0 minuts al dia.": 0,
    "Menys de 30 minuts al dia.": 1,
    "Entre 30 minuts i 1 hora al dia.": 2,
    "Entre 1 i 2 hores al dia.": 3,
    "Entre 2 i 3 hores al dia.": 4,
    "3 hores o més al dia": 5
}

# Entorn familiar pro-lector
# ===
sort_estudis_familiars = [
    "Educació Primaria.",
    "Educació Secundària.",
    "Batxillerat o Cicles Formatius de Grau Mitjà o Superior.",
    "Estudis Universitaris.",
]

map_estudis_familiars_sp = {
    "Educació Primaria.": 0,
    "Educació Secundària.": 1,
    "Batxillerat o Cicles Formatius de Grau Mitjà o Superior.": 2,
    "Estudis Universitaris.": 3,
}

sort_num_llibres = [
    "0 llibres",
    "Entre 1 i 10 llibres.",
    "Entre 11 i 25 llibres.",
    "Entre 26 i 100 llibres.",
    "Entre 101 i 200 llibres.",
    "Més de 200 llibres."
]

map_num_llibres_sp = {
    "0 llibres": 0,
    "Entre 1 i 10 llibres.": 1,
    "Entre 11 i 25 llibres.": 2,
    "Entre 26 i 100 llibres.": 3,
    "Entre 101 i 200 llibres.": 4,
    "Més de 200 llibres.": 5
}

# =======================================================================================
# Create the Spearman ready variables
# =======================================================================================
# Temps de lectura setmanal
# ===
df["p4_temps_lectura_sp"] = df["p4_temps_lectura"].map(map_temps_sp)

# Llibres 12 mesos
# ===
df["p5_llibres_sp"] = df["p5_llibres"].map(map_llibres_sp)

# =======================================================================================
# Save poltergeists
# =======================================================================================
df = tmt.save_poltergeists(df, verbose=verbose)

# =======================================================================================
# Clean dataset and ensure consistency
# =======================================================================================
df = tmt.clean_reading_dataset_and_consistency(df, verbose=verbose)

# =======================================================================================
# Create subdataframes of readers, no readers, gender, curs
# =======================================================================================
readers_mask = (
    (df["p5_llibres"] != "0 llibres o còmics.") &
    (df["p4_temps_lectura"] != "0 minuts.") &
    (df["sessions"] != "No llegeixo per oci.") &
    (df["format"] != "No llegeixo per oci.")
)

df_readers = df[readers_mask].copy()
df_no_readers = df[~readers_mask].copy()

# df_fem = df[df["Gènere"] == "Femení."].copy()
# df_mas = df[df["Gènere"] == "Masculí."].copy()

if verbose:
    show_list = ["id", "Gènere", "Curs", "p4_temps_lectura", "p5_llibres", "format", "sessions"]
    print("\n========================================================================================\nReaders DF\n========================================================================================")
    print(f"Dataframe dimensions (rows, cols): {df_readers.shape}")
    print(f"First 5 lines of the dataframe: \n{df_readers[show_list].head(12)}")
    print("\n========================================================================================\nNo Readers DF\n========================================================================================")
    print(f"Dataframe dimensions (rows, cols): {df_no_readers.shape}")
    print(f"First 5 lines of the dataframe: \n{df_no_readers[show_list].head(12)}")

# =======================================================================================
# 1. Característiques Generals de la mostra
# =======================================================================================
if len(tags) > 0 and 1 in tags:
    print("\n=======================================================================================\nCaracterístiques Generals de la Mostra\n=======================================================================================")
    
    # Boys & girls
    # =======================================================
    tmt.plot_descriptive_hists(
        df=df.copy(),
        var="Gènere",
        title="Distribució de l'alumnat segons el gènere",
        xlabel="",
        ylabel="Percentatge d'alumnes"
    )

    # Cursos
    # =======================================================
    tmt.plot_descriptive_hists(
        df=df.copy(),
        var="Curs",
        title="Distribució de l'alumnat segons el curs",
        xlabel="",
        ylabel="Percentatge d'alumnes"
    )

    # Itinerari (només si estàs cursant Batxillerat)
    # =======================================================
    tmt.plot_descriptive_hists(
        df=df.copy(),
        var="Itinerari (només si estàs cursant Batxillerat)",
        title="Distribució de l'alumnat segons l'itinerari (només Batxillerat)",
        xlabel="",
        ylabel="Percentatge d'alumnes"
    )

# =======================================================================================
# 2. Temps de lectura setmanal i llibres llegits en els últims 12 mesos per oci per grups
# =======================================================================================
if len(tags) > 0 and 2 in tags:
    print("\n=======================================================================================\nTemps de lectura setmanal i llibres llegits en els últims 12 mesos per oci per grups\n=======================================================================================")
    # print(df[df["Gènere"] == "Prefereixo no respondre."])
    tmt.spearman_analysis(
        df.copy(),
        "p4_temps_lectura_sp",
        "p5_llibres_sp",
        "Spearman: temps de lectura vs llibres llegits"
    )

    tmt.chi_square_analysis(
        df[df["Gènere"] != "Prefereixo no respondre."].copy(),
        "Gènere",
        "p4_temps_lectura",
        "Chi-cuadrat: gènere normatiu vs temps de lectura"
    )

    tmt.chi_square_analysis(
        df[df["Gènere"] != "Prefereixo no respondre."].copy(),
        "Gènere",
        "p5_llibres",
        "Chi-cuadrat: gènere normatiu vs llibres llegits"
    )

    # Llibres llegits en els últims 12 mesos per oci per grups
    # =======================================================
    # General
    # ===
    tmt.plot_descriptive_hists(
        df=df.copy(),
        var="p4_temps_lectura",
        title="Distribució de l'alumnat segons el temps promig de lectura setmanal per oci",
        xlabel="",
        ylabel="Percentatge d'alumnes",
        sort=sort_temps
    )
    
    # Boys vs girls
    # ===
    tmt.plot_descriptive_combined_hists(
        df[df["Gènere"] == "Femení."].copy(),
        df[df["Gènere"] == "Masculí."].copy(),
        groups=["Noies", "Nois"],
        var="p4_temps_lectura",
        title="Distribució de l'alumnat segons el temps promig de lectura setmanal per oci per gènere",
        xlabel="",
        ylabel="Percentatge d'alumnes (%)",
        colors=["purple", "orange"],
        sort=sort_temps
    )

    # Groups
    # ===
    tmt.plot_descriptive_combined_hists(
        df[df["Curs"] == "3r d'ESO."].copy(),
        df[df["Curs"] == "4t d'ESO."].copy(),
        df[df["Curs"] == "1r de Batxillerat."].copy(),
        df[df["Curs"] == "2n de Batxillerat."].copy(),
        groups=["3r d'ESO", "4t d'ESO", "1r de Batxillerat", "2n de Batxillerat"],
        var="p4_temps_lectura",
        title="Distribució de l'alumnat segons el temps promig de lectura setmanal per oci per curs",
        xlabel="",
        ylabel="Percentatge d'alumnes (%)",
        colors=["blue", "orange", "green", "red"],
        sort=sort_temps
    )

    # Ciencies Socials vs Tecnologia i Ciencia
    # ===
    tmt.plot_descriptive_combined_hists(
        df[df["Itinerari (només si estàs cursant Batxillerat)"] == "Ciències Socials."].copy(),
        df[df["Itinerari (només si estàs cursant Batxillerat)"] == "Ciències i Tecnologia."].copy(),
        groups=["Ciències Socials", "Ciències i Tecnologia"],
        var="p4_temps_lectura",
        title="Distribució de l'alumnat segons el temps promig de lectura setmanal per oci per itinerari",
        xlabel="",
        ylabel="Percentatge d'alumnes (%)",
        colors=["red", "green"],
        sort=sort_temps
    )

    # Llibres llegits en els últims 12 mesos per oci per grups
    # =======================================================
    # General
    # ===
    tmt.plot_descriptive_hists(
        df=df.copy(),
        var="p5_llibres",
        title="Distribució de l'alumnat segons els llibres llegits per oci en els últims 12 mesos",
        xlabel="",
        ylabel="Percentatge d'alumnes",
        sort=sort_llibres
    )
    
    # Boys vs girls
    # =======================================================
    tmt.plot_descriptive_combined_hists(
        df[df["Gènere"] == "Femení."].copy(),
        df[df["Gènere"] == "Masculí."].copy(),
        groups=["Noies", "Nois"],
        var="p5_llibres",
        title="Distribució de l'alumnat segons els llibres llegits per oci en els últims 12 mesos per gènere",
        xlabel="",
        ylabel="Percentatge d'alumnes (%)",
        colors=["purple", "orange"],
        sort=sort_llibres
    )

    # Groups
    # =======================================================
    tmt.plot_descriptive_combined_hists(
        df[df["Curs"] == "3r d'ESO."].copy(),
        df[df["Curs"] == "4t d'ESO."],
        df[df["Curs"] == "1r de Batxillerat."],
        df[df["Curs"] == "2n de Batxillerat."],
        groups=["3r d'ESO", "4t d'ESO", "1r de Batxillerat", "2n de Batxillerat"],
        var="p5_llibres",
        title="Distribució de l'alumnat segons els llibres llegits per oci en els últims 12 mesos per curs",
        xlabel="",
        ylabel="Percentatge d'alumnes (%)",
        colors=["blue", "orange", "green", "red"],
        sort=sort_llibres
    )

    # Ciencies Socials vs Tecnologia i Ciencia
    # =======================================================
    tmt.plot_descriptive_combined_hists(
        df[df["Itinerari (només si estàs cursant Batxillerat)"] == "Ciències Socials."],
        df[df["Itinerari (només si estàs cursant Batxillerat)"] == "Ciències i Tecnologia."],
        groups=["Ciències Socials", "Ciències i Tecnologia"],
        var="p5_llibres",
        title="Distribució de l'alumnat segons els llibres llegits per oci en els últims 12 mesos per itinerari",
        xlabel="",
        ylabel="Percentatge d'alumnes (%)",
        colors=["red", "green"],
        sort=sort_llibres
    )

# =======================================================================================
# 3. Composed variables books * pages --> pages / year (p5_6_pagines)
# =======================================================================================
# Recode P5 to mean number of books
# =======================================================
df["p5_num"] = df["p5_llibres"].map(map_llibres_num)
df["p6_num"] = df["p6_pag"].map(map_pagines_num)

# Create Composed variable p5 * p6 = total aproximado de páginas leídas al año
df["p5_6_pagines_num"] = (
    df["p5_num"] * df["p6_num"]
)

# If p5 = 0 books -> p5_6 = 0
df.loc[
    df["p5_num"] == 0,
    "p5_6_pagines_num"
] = 0

# Replace Nan for 0
df["p5_6_pagines_num"] = df["p5_6_pagines_num"].fillna(0)

# Discretize composed variable into categories
# =======================================================
# Categorize
bins = [-1, 0, 300, 800, 2000, 4000, float("inf")]
labels = ["0", "1-300", "301-800", "801-2000", "2001-4000", ">4000"]

# df["p5_6_pagines"] = df["p5_6_pagines_num"].apply(tmt.categorize_pags)
df["p5_6_pagines"] = pd.cut(
    df["p5_6_pagines_num"],
    bins=bins,
    labels=labels
)

# Aplicar mapa
df["p5_6_pagines_sp"] = df["p5_6_pagines"].map(map_pagines_sp)

# Check result
if len(tags) > 0 and 3 in tags:
    print("\n=======================================================================================\nPages per year: Estatistics\n=======================================================================================")
    # Correlations
    tmt.spearman_analysis(
        df.copy(),
        "p4_temps_lectura_sp",
        "p5_6_pagines_sp",
        "Spearman: temps de lectura vs pàgines llegides"
    )
    tmt.spearman_analysis(
        df.copy(),
        "p5_num",
        "p5_6_pagines_num",
        "Spearman: llibres llegits vs pàgines llegides"
    )

if verbose:
    print("Check first 20 rows of number of pages per year:")
    print(
        df[
            [
                "id",
                "p5_llibres",
                "p6_pag",
                "p5_num",
                "p6_num",
                "p5_6_pagines_num",
                "p5_6_pagines",
            ]
        ].head(20)
    )
if len(tags) > 0 and 3 in tags:
    print("\n========================== General ===========================")
    print(df["p5_6_pagines_num"].describe())
    print("\n============================ Sexe ============================")
    print("------------- Femení -------------")
    print(df[df["Gènere"] == "Femení."]["p5_6_pagines_num"].describe())
    print("------------- Masculí -------------")
    print(df[df["Gènere"] == "Masculí."]["p5_6_pagines_num"].describe())
    print("\n============================ Curs ============================")
    print("------------- 3r d'ESO -------------")
    print(df[df["Curs"] == "3r d'ESO."]["p5_6_pagines_num"].describe())
    print("------------- 4t d'ESO -------------")
    print(df[df["Curs"] == "4t d'ESO."]["p5_6_pagines_num"].describe())
    print("------------- 1r de Batxillerat -------------")
    print(df[df["Curs"] == "1r de Batxillerat."]["p5_6_pagines_num"].describe())
    print("------------- 2n de Batxillerat -------------")
    print(df[df["Curs"] == "2n de Batxillerat."]["p5_6_pagines_num"].describe())

    # # Plot
    # tmt.plot_descriptive_hists(
    #     df=df,
    #     var="p5_6_pagines",
    #     title="Distribució nombre de pàgines estimades llegides aquest any (llibre o còmic) per oci",
    #     xlabel="Pàgines estimades llegides anualment",
    #     ylabel="Percentatge d'alumnes",
    # )
    
    # # Plot
    # tmt.plot_descriptive_combined_hists(
    #     df[df["Gènere"] == "Masculí."].copy(),
    #     df[df["Gènere"] == "Femení."].copy(),
    #     sort=["0", "1-300", "301-800", "801-2000", "2001-4000", ">4000"],
    #     groups=["Nois", "Noies"],
    #     var="p5_6_pagines",
    #     title="Distribució nombre de pàgines estimades llegides aquest any (llibre o còmic) per oci per gènere",
    #     xlabel="Pàgines estimades llegides anualment",
    #     ylabel="Percentatge d'alumnes (%)",
    #     colors=["orange", "purple"]
    # )

    # # Plot
    # tmt.plot_descriptive_combined_hists(
    #     df[df["Curs"] == "3r d'ESO."].copy(),
    #     df[df["Curs"] == "4t d'ESO."].copy(),
    #     df[df["Curs"] == "1r de Batxillerat."].copy(),
    #     df[df["Curs"] == "2n de Batxillerat."].copy(),
    #     sort=["0", "1-300", "301-800", "801-2000", "2001-4000", ">4000"],
    #     groups=["3r d'ESO", "4t d'ESO", "1r de Batxillerat", "2n de Batxillerat"],
    #     var="p5_6_pagines",
    #     title="Distribució nombre de pàgines estimades llegides aquest any (llibre o còmic) per oci per curs",
    #     xlabel="Pàgines estimades llegides anualment",
    #     ylabel="Percentatge d'alumnes (%)",
    #     colors=["blue", "orange", "green", "red"]
    # )

    # Plot 
    plt.figure()
    df["p5_6_pagines_num"].plot(kind="box", showmeans=True)

    plt.title("Boxplot nombre de pàgines en els últims 12 mesos")
    plt.suptitle("")  # elimina el título automático de pandas
    plt.ylabel("Pàgines")
    plt.xlabel("")
    plt.grid(True)

    # # Plot 
    # plt.figure()
    # df["p5_6_pagines_num"].plot(kind="box", showmeans=True, showfliers=False)

    # plt.title("Boxplot nombre de pàgines en els últims 12 mesos (sense outliers)")
    # plt.suptitle("")  # elimina el título automático de pandas
    # plt.ylabel("Pàgines")
    # plt.xlabel("")
    # plt.grid(True)

    # Plot
    df_filtrat = df[df["Gènere"] != "Prefereixo no respondre."]
    df_filtrat.boxplot(column="p5_6_pagines_num", by="Gènere", showmeans=True)

    plt.title("Boxplot nombre de pàgines en els últims 12 mesos per gènere")
    plt.suptitle("")  # elimina el título automático de pandas
    plt.ylabel("Pàgines")
    plt.xlabel("")

    # # Plot
    # df_filtrat.boxplot(column="p5_6_pagines_num", by="Gènere", showmeans=True, showfliers=False)

    # plt.title("Boxplot nombre de pàgines en els últims 12 mesos per gènere (sense outliers)")
    # plt.suptitle("")  # elimina el título automático de pandas
    # plt.ylabel("Pàgines")
    # plt.xlabel("")

    # Plot
    orden = ["3r d'ESO.", "4t d'ESO.", "1r de Batxillerat.", "2n de Batxillerat."]
    df["Curs"] = pd.Categorical(df["Curs"], categories=orden, ordered=True)
    df.boxplot(column="p5_6_pagines_num", by="Curs", showmeans=True)

    plt.title("Boxplot nombre de pàgines en els últims 12 mesos per curs")
    plt.suptitle("")  # elimina el título automático de pandas
    plt.ylabel("Pàgines")
    plt.xlabel("")
    # plt.yscale("log")
    # plt.ylim(1, df["p5_6_pagines_num"].max())

    # # Plot
    # orden = ["3r d'ESO.", "4t d'ESO.", "1r de Batxillerat.", "2n de Batxillerat."]
    # # df["Curs"] = pd.Categorical(df["Curs"], categories=orden, ordered=True)
    # df.boxplot(column="p5_6_pagines_num", by="Curs", showmeans=True, showfliers=False)

    # plt.title("Boxplot nombre de pàgines en els últims 12 mesos per curs (sense outliers)")
    # plt.suptitle("")  # elimina el título automático de pandas
    # plt.ylabel("Pàgines")
    # plt.xlabel("")
    # # plt.yscale("log")
    # # plt.ylim(1, df["p5_6_pagines_num"].max())

# =======================================================================================
# 4. Classificació lectora
# =======================================================================================

# ---
df_readers["p4_temps_lectura_sp"] = df_readers["p4_temps_lectura"].map(map_temps_sp)
df_readers["p5_llibres_sp"] = df_readers["p5_llibres"].map(map_llibres_sp)

# Add column clasificació_lectora
# =======================================================
df = tmt.classify_reader(df)


# Calculate new correlation with classificació_lectora
df["p5_6_pagines_sp"] = df["p5_6_pagines"].map(map_pagines_sp)
df["classificacio_lectora_sp"] = df["classificacio_lectora"].map(map_class_sp)

if len(tags) > 0 and 4 in tags:
    print("\n=======================================================================================\nReading Classification \n=======================================================================================")
    # Correlations
    tmt.spearman_analysis(
        df.copy(),
        "p4_temps_lectura_sp",
        "classificacio_lectora_sp",
        "Spearman: temps de lectura vs classificació lectora"
    )

    tmt.spearman_analysis(
        df.copy(),
        "p5_llibres_sp",
        "classificacio_lectora_sp",
        "Spearman: llibres llegides vs classificació lectora"
    )

    tmt.spearman_analysis(
        df.copy(),
        "p5_6_pagines_sp",
        "classificacio_lectora_sp",
        "Spearman: pàgines llegides vs classificació lectora"
    )

    if verbose:
        print(df[["p5_6_pagines", "p5_6_pagines_sp", "p4_temps_lectura", "p4_temps_lectura_sp", "p5_llibres", "p5_llibres_sp"]].head(30))
    # Se observa una Correlació positiva fuerte entre el tiempo de lectura y el número de páginas leídas (ρ = 0.714), lo que indica coherencia entre ambas dimensiones del hábito lector. Esta relación justifica la construcción de una variable compuesta que integre frecuencia e intensidad de lectura.
    
    # Prints
    sort = [
        "No lector / Lector molt ocasional",
        "Lector ocasional",
        "Lector habitual"
    ]

    # General
    # =======================================================
    tmt.plot_descriptive_hists(
        df=df,
        var="classificacio_lectora",
        title="Classificació de l'alumnat segons l'hàbit lector per oci",
        xlabel="",
        ylabel="Percentatge d'alumnes",
        sort=sort
    )

    # print(df[df["classificacio_lectora"] == "Lector ocasional"][["p4_temps_lectura", "p5_6_pagines_num"]].to_string())
    # print(df[df["p4_temps_lectura"] == "0 minuts."][["p5_llibres","p5_6_pagines_num"]].to_string())
    
    # Boys vs girls
    # =======================================================
    tmt.plot_descriptive_combined_hists(
        df[df["Gènere"] == "Femení."].copy(),
        df[df["Gènere"] == "Masculí."].copy(),
        groups=["Noies", "Nois"],
        var="classificacio_lectora",
        title="Classificació de l'alumnat segons l'hàbit lector per oci per gènere",
        xlabel="",
        ylabel="Percentatge d'alumnes (%)",
        colors=["purple", "orange"],
        sort=sort
    )

    # Groups
    # =======================================================
    tmt.plot_descriptive_combined_hists(
        df[df["Curs"] == "3r d'ESO."].copy(),
        df[df["Curs"] == "4t d'ESO."].copy(),
        df[df["Curs"] == "1r de Batxillerat."].copy(),
        df[df["Curs"] == "2n de Batxillerat."].copy(),
        groups=["3r d'ESO", "4t d'ESO", "1r de Batxillerat", "2n de Batxillerat"],
        var="classificacio_lectora",
        title="Classificació de l'alumnat segons l'hàbit lector per oci per curs",
        xlabel="",
        ylabel="Percentatge d'alumnes (%)",
        colors=["blue", "orange", "green", "red"],
        sort=sort
    )

    # # Ciencies Socials vs Tecnologia i Ciencia
    # # =======================================================
    # tmt.plot_descriptive_combined_hists(
    #     df[df["Itinerari (només si estàs cursant Batxillerat)"] == "Ciències Socials."].copy(),
    #     df[df["Itinerari (només si estàs cursant Batxillerat)"] == "Ciències i Tecnologia."].copy(),
    #     groups=["Ciències Socials", "Ciències i Tecnologia"],
    #     var="classificacio_lectora",
    #     title="Distribució de l'alumnat segons el seu hàbit lector per oci per itinerari",
    #     xlabel="",
    #     ylabel="Percentatge d'alumnes (%)",
    #     colors=["red", "green"],
    #     sort=sort
    # )

# =======================================================================================
# 5. Thematic & Format
# =======================================================================================
if len(tags) > 0 and 5 in tags:
    print("\n=======================================================================================\nThematic & Format\n=======================================================================================")
    # Select df
    df_thematic = df.copy()
    
    # Remap thematic and calculate scores for all, girls and boys
    # =======================================================
    map_thematic = {
        1: 3,
        2: 2,
        3: 1
    }

    # print(list(df))

    columnes_generes = [
        "Novel·la fantàstica",
        "Novel·la romàntica",
        "Novel·la de terror",
        "Novel·la negra",
        "Novel·la històrica",
        "Ciència ficció",
        "Còmic",
        "Clàssics",
        "Poesia",
        "Assaig",
        "Teatre"
    ]

    readers_resultats_all = tmt.compute_thematic_scores(df_readers, columnes_generes, map_thematic)
    readers_resultats_girls = tmt.compute_thematic_scores(df_readers[df_readers["Gènere"] == "Femení."], columnes_generes, map_thematic)
    readers_resultats_boys = tmt.compute_thematic_scores(df_readers[df_readers["Gènere"] == "Masculí."], columnes_generes, map_thematic)
    all_resultats_all = tmt.compute_thematic_scores(df, columnes_generes, map_thematic)
    all_resultats_girls = tmt.compute_thematic_scores(df[df["Gènere"] == "Femení."], columnes_generes, map_thematic)
    all_resultats_boys = tmt.compute_thematic_scores(df[df["Gènere"] == "Masculí."], columnes_generes, map_thematic)

    if verbose:
        print("Thematics results for ALL ------------------------------------------------------")
        print(all_resultats_all)
        print("\nThematics results for ALL GIRLS ------------------------------------------------------")
        print(all_resultats_girls)
        print("\nThematics results for ALL BOYS ------------------------------------------------------")
        print(all_resultats_boys)
        print("\nThematics results for READERS ------------------------------------------------------")
        print(readers_resultats_all)
        print("\nThematics results for READERS GIRLS ------------------------------------------------------")
        print(readers_resultats_girls)
        print("\nThematics results for READERS BOYS ------------------------------------------------------")
        print(readers_resultats_boys)

    # Plots
    # =======================================================
    results = {
        # "Tots": all_resultats_all,
        # "Noies": all_resultats_girls,
        # "Nois": all_resultats_boys,
        "Rànking de les temàtiques preferides per a la lectura per oci": readers_resultats_all,
        "Rànking de les temàtiques preferides per a la lectura per oci entre les noies": readers_resultats_girls,
        "Rànking de les temàtiques preferides per a la lectura per oci entre els nois": readers_resultats_boys
    }

    tmt.plot_thematic_individual(results)

    # Formats de lectura
    # =======================================================
    df_to_use = df_readers.copy()
    
    # Clean df_readers
    valores_excluir = [
        "digital (xarxes socials)",
        "en paper i en digital",
        "No llegeixo per oci.",
        "no llegeixo pero oci",
    ]

    col = "format"
    mask = df_to_use[col] == "wattpad,webtoon"
    # print(mask.sum())  # número de coincidencias

    df_to_use.loc[mask, col] = "Digital (llibre Web o PDF en dispositiu electrònic)."

    df_to_use = df_to_use[
        ~df_to_use[col].isin(valores_excluir)
    ]

    tmt.plot_descriptive_hists(
        df=df_to_use,
        var="format",
        title="Format de lectura més habitual per a la lectura de llibres o còmics per oci",
        xlabel="",
        ylabel="Percentatge d'alumnes",
    )

# =======================================================================================
# 6. sessions (Com acostumen a ser les sessions de lectura)
# =======================================================================================
df["sessions_sp"] = df["sessions"].map(map_sessions_sp)
df["distraccions"] = df[
    "Amb quina freqüència consultes xarxes socials habitualment mentre llegeixes?"
].map(map_distraccions_inv_sp)

df["doble_tasca"] = df[
    "Quan llegeixes, acostumes a fer-ho amb música, vídeos o pòdcasts de fons?"
].map(map_freq_sp)

df_readers["doble_tasca"] = df_readers[
    "Quan llegeixes, acostumes a fer-ho amb música, vídeos o pòdcasts de fons?"
].map(map_freq_sp)

if len(tags) > 0 and 6 in tags:
    print("\n=======================================================================================\nSessions de lectura \n=======================================================================================")
    # Correlations
    tmt.spearman_analysis(
        df.copy(),
        "sessions_sp",
        "p4_temps_lectura_sp",
        "Spearman: sessions de lectura vs temps de lectura"
    )

    tmt.spearman_analysis(
        df.copy(),
        "sessions_sp",
        "p5_llibres_sp",
        "Spearman: sessions de lectura vs nombre de llibres anuals llegits"
    )

    tmt.spearman_analysis(
        df.copy(),
        "distraccions",
        "p4_temps_lectura_sp",
        "Spearman: freqüència de distraccions vs temps de lectura"
    )

    tmt.spearman_analysis(
        df.copy(),
        "distraccions",
        "p5_llibres_sp",
        "Spearman: freqüència de distraccions vs nombre de llibres anuals llegits"
    )

    tmt.spearman_analysis(
        df.copy(),
        "doble_tasca",
        "p4_temps_lectura_sp",
        "Spearman: freqüència de doble tasca vs temps de lectura"
    )

    tmt.spearman_analysis(
        df.copy(),
        "doble_tasca",
        "p5_llibres_sp",
        "Spearman: freqüència de doble tasca vs nombre de llibres anuals llegits"
    )

    tmt.spearman_analysis(
        df_readers.copy(),
        "doble_tasca",
        "p4_temps_lectura_sp",
        "Spearman: freqüència de doble tasca vs temps de lectura (only readers)"
    )

    tmt.spearman_analysis(
        df_readers.copy(),
        "doble_tasca",
        "p5_llibres_sp",
        "Spearman: freqüència de doble tasca vs nombre de llibres anuals llegits (only readers)"
    )

    # Plots sessions ------------------
    tmt.plot_descriptive_hists(
        df=df_readers.copy(),
        var="sessions",
        title="Distribució de l'alumnat segons les sessions de lectura per oci",
        xlabel="",
        ylabel="Percentatge d'alumnes (%)",
        sort=sort_sessions
    )

    tmt.plot_descriptive_combined_hists(
        df[df["classificacio_lectora"] == "No lector / Lector molt ocasional"].copy(),
        df[df["classificacio_lectora"] == "Lector ocasional"].copy(),
        df[df["classificacio_lectora"] == "Lector habitual"].copy(),
        groups=["No lector / Lector molt ocasional", "Lector ocasional", "Lector habitual"],
        var="sessions",
        title="Distribució de l'alumnat segons les sessions de lectura per oci i classificació lectora",
        xlabel="",
        ylabel="Percentatge d'alumnes (%)",
        colors=["blue", "orange", "green"],
        sort=sort_sessions
    )

    # Plots Doble Tasca ------------------
    tmt.plot_descriptive_hists(
        df=df_readers.copy(),
        var="Quan llegeixes, acostumes a fer-ho amb música, vídeos o pòdcasts de fons?",
        title="Freqüència de lectura amb música, vídeos o pòdcasts de fons",
        xlabel="",
        ylabel="Percentatge d'alumnes",
        sort=sort_freq
    )

    tmt.plot_descriptive_combined_hists(
        df[df["classificacio_lectora"] == "No lector / Lector molt ocasional"].copy(),
        df[df["classificacio_lectora"] == "Lector ocasional"].copy(),
        df[df["classificacio_lectora"] == "Lector habitual"].copy(),
        groups=["No lector / Lector molt ocasional", "Lector ocasional", "Lector habitual"],
        var="Quan llegeixes, acostumes a fer-ho amb música, vídeos o pòdcasts de fons?",
        title="Freqüència de lectura amb música, vídeos o pòdcasts de fons i classificació lectora",
        xlabel="",
        ylabel="Percentatge d'alumnes (%)",
        colors=["blue", "orange", "green"],
        sort=sort_freq   
    )

    # Plots Distraccions ------------------
    tmt.plot_descriptive_hists(
        df=df,
        var="Amb quina freqüència consultes xarxes socials habitualment mentre llegeixes?",
        title="Distribució de l'alumnat segons la freqüència de consulta x.socials mentre llegeixen",
        xlabel="",
        ylabel="Percentatge d'alumnes",
        sort=sort_distraccions_inv
    )

    tmt.plot_descriptive_combined_hists(
        df[df["classificacio_lectora"] == "No lector / Lector molt ocasional"].copy(),
        df[df["classificacio_lectora"] == "Lector ocasional"].copy(),
        df[df["classificacio_lectora"] == "Lector habitual"].copy(),
        groups=["No lector / Lector molt ocasional", "Lector ocasional", "Lector habitual"],
        var="Amb quina freqüència consultes xarxes socials habitualment mentre llegeixes?",
        title="Distribució de l'alumnat segons la freqüència de consulta de x.socials mentre llegeixen i classificació lectora",
        xlabel="",
        ylabel="Percentatge d'alumnes (%)",
        colors=["blue", "orange", "green"],
        sort=sort_distraccions_inv
    )

# =======================================================================================
# 7. p10_visites_biblioteca
# =======================================================================================
df["biblioteca_infancia_sp"] = df["Durant la teva infància i adolescència, amb quina freqüència aproximadament has anat a la biblioteca amb els teus pares o tutors legals a llegir o agafar llibres en préstec?"].map(map_freq_sp)
if len(tags) > 0 and 7 in tags:
    print("\n=======================================================================================\nVisites Biblioteca \n=======================================================================================")

    df["p10_visites_biblioteca_anual_sp"] = df["p10_visites_biblioteca"].map(map_visites_biblioteca_anual_sp)

    tmt.spearman_analysis(
        df.copy(),
        "p10_visites_biblioteca_anual_sp",
        "p4_temps_lectura_sp",
        "Spearman: visites biblioteca anual vs temps de lectura"
    )

    tmt.spearman_analysis(
        df.copy(),
        "p10_visites_biblioteca_anual_sp",
        "p5_llibres_sp",
        "Spearman: visites biblioteca anual vs llibres llegits"
    )

    tmt.spearman_analysis(
        df.copy(),
        "biblioteca_infancia_sp",
        "p4_temps_lectura_sp",
        "Spearman: freqüència d'anar a la biblioteca amb els pares vs temps de lectura setmanal"
    )

    tmt.spearman_analysis(
        df.copy(),
        "biblioteca_infancia_sp",
        "p5_llibres_sp",
        "Spearman: freqüència d'anar a la biblioteca amb els pares vs nombre de llibres anuals llegits"
    )

    tmt.plot_descriptive_hists(
        df=df.copy(),
        var="p10_visites_biblioteca",
        title="Distribució de l'alumnat segons les visites a la biblioteca en l'últim any per oci",
        xlabel="",
        ylabel="Percentatge d'alumnes (%)",
        sort=sort_visites_biblioteca_anual
    )

    tmt.plot_descriptive_combined_hists(
        df[df["classificacio_lectora"] == "No lector / Lector molt ocasional"].copy(),
        df[df["classificacio_lectora"] == "Lector ocasional"].copy(),
        df[df["classificacio_lectora"] == "Lector habitual"].copy(),
        groups=["No lector / Lector molt ocasional", "Lector ocasional", "Lector habitual"],
        var="p10_visites_biblioteca",
        title="Distribució de l'alumnat segons les visites a la biblioteca en l'últim any per oci i classificació lectora",
        xlabel="",
        ylabel="Percentatge d'alumnes (%)",
        colors=["blue", "orange", "green"],
        sort = sort_visites_biblioteca_anual
    )


# =======================================================================================
# 8. p16_lectura_obligatoria
# =======================================================================================
df["p16_lectura_obligatoria_sp"] = df["p16_lectura_obligatoria"].map(map_lectura_obligatoria_sp)
df["gust_lectura_obligatoria_sp"] = df["T’agraden les lectures obligatòries de l’escola? "].map(map_gust_sp)
df["llegiria_mes_lectura_obligatoria_sp"] = df["Fins a quin punt estàs d'acord amb la següent afirmació: llegiria més lectures obligatòries de l'escola si s'adaptessin més als meus gustos."].map(map_acord_sp)

if len(tags) > 0 and 8 in tags:
    print("\n=======================================================================================\nLectures Obligatòries\n=======================================================================================")
    # Correlations
    tmt.spearman_analysis(
        df.copy(),
        "gust_lectura_obligatoria_sp",
        "p16_lectura_obligatoria_sp",
        "Spearman: gust per la lectura obligatòria vs grau de lectura obligatòria"
    )

    tmt.spearman_analysis(
        df.copy(),
        "p16_lectura_obligatoria_sp",
        "p5_llibres_sp",
        "Spearman: grau de lectura obligatòria vs nombre de llibres anuals llegits"
    )

    tmt.spearman_analysis(
        df.copy(),
        "gust_lectura_obligatoria_sp",
        "p5_llibres_sp",
        "Spearman: gust per la lectura obligatòria vs nombre de llibres anuals llegits"
    )

    tmt.spearman_analysis(
        df.copy(),
        "llegiria_mes_lectura_obligatoria_sp",
        "p5_llibres_sp",
        "Spearman: percepció de que llegiria més lectures obligatòries si s'adaptessin més als seus gustos vs nombre de llibres anuals llegits"
    )

    tmt.spearman_analysis(
        df.copy(),
        "p16_lectura_obligatoria_sp",
        "p4_temps_lectura_sp",
        "Spearman: grau de lectura obligatòria vs temps de lectura"
    )

    tmt.spearman_analysis(
        df.copy(),
        "gust_lectura_obligatoria_sp",
        "p4_temps_lectura_sp",
        "Spearman: gust per la lectura obligatòria vs temps de lectura"
    )

    tmt.spearman_analysis(
        df.copy(),
        "llegiria_mes_lectura_obligatoria_sp",
        "p4_temps_lectura_sp",
        "Spearman: percepció de que llegiria més lectures obligatòries si s'adaptessin més als seus gustos vs temps de lectura"
    )

    sort = [
        "No en llegeixo cap.",
        "En llegeixo poques o molt poques.",
        "En llegeixo aproximadament la meitat.",
        "Les llegeixo gairebé totes.",
        "Les llegeixo totes."
    ]

    tmt.plot_descriptive_hists(
        df=df,
        var="p16_lectura_obligatoria",
        title="Distribució de l'alumnat segons el grau de lectura de les lectures obligatòries de l’escola",
        xlabel="",
        ylabel="Percentatge d'alumnes (%)",
        sort=sort
    )

    tmt.plot_descriptive_hists(
        df=df,
        var="T’agraden les lectures obligatòries de l’escola? ",
        title="Distribució de l'alumnat segons el gust per les lectures obligatòries de l’escola",
        xlabel="",
        ylabel="Percentatge d'alumnes (%)",
        sort=sort_gust
    )

    tmt.plot_descriptive_hists(
        df=df,
        var="Fins a quin punt estàs d'acord amb la següent afirmació: des que utilitzo eines d’IA generativa (ChatGPT, Gemini, Copilot, Claude, etc.), he reduït la lectura de les lectures obligatòries de l’escola. ",
        title="Distribució de l'alumnat segons reducció de lectures obligatòries per IA generativa",
        xlabel="",
        ylabel="Percentatge d'alumnes (%)",
        sort=sort_acords
    )

    tmt.plot_descriptive_hists(
        df=df,
        var="Amb quina freqüència utilitzes resums d’internet o eines digitals (com IA generativa) per consultar el contingut de les lectures obligatòries de l’escola?",
        title="Distribució de l'alumnat segons l'ús de resums d’internet o IA generativa",
        xlabel="",
        ylabel="Percentatge d'alumnes (%)",
        sort=sort_freq
    )

    tmt.plot_descriptive_hists(
        df=df,
        var="Fins a quin punt estàs d'acord amb la següent afirmació: llegiria més lectures obligatòries de l'escola si s'adaptessin més als meus gustos.",
        title="Percepció que llegirien més les lectures obligatòries si s'adaptessin més als seus gustos",
        xlabel="",
        ylabel="Percentatge d'alumnes (%)",
        sort=sort_acords
    )

    tmt.plot_descriptive_combined_hists(
        df[df["classificacio_lectora"] == "No lector / Lector molt ocasional"].copy(),
        df[df["classificacio_lectora"] == "Lector ocasional"].copy(),
        df[df["classificacio_lectora"] == "Lector habitual"].copy(),
        var="T’agraden les lectures obligatòries de l’escola? ",
        groups=["No lector / Lector molt ocasional", "Lector ocasional", "Lector habitual"],
        title="Distribució de l'alumnat segons el gust per les lectures obligatòries de l’escola per classificació lectora",
        xlabel="",
        ylabel="Percentatge d'alumnes (%)",
        colors=["purple", "orange", "green"],
        sort=sort_gust
    )

    tmt.plot_descriptive_combined_hists(
        df[df["classificacio_lectora"] == "No lector / Lector molt ocasional"].copy(),
        df[df["classificacio_lectora"] == "Lector ocasional"].copy(),
        df[df["classificacio_lectora"] == "Lector habitual"].copy(),
        var="p16_lectura_obligatoria",
        groups=["No lector / Lector molt ocasional", "Lector ocasional", "Lector habitual"],
        title="Distribució de l'alumnat que llegeix les lectures obligatòries de l’escola per classificació lectora",
        xlabel="",
        ylabel="Percentatge d'alumnes (%)",
        colors=["purple", "orange", "green"],
        sort=sort
    )

    tmt.plot_descriptive_combined_hists(
        df[df["classificacio_lectora"] == "No lector / Lector molt ocasional"].copy(),
        df[df["classificacio_lectora"] == "Lector ocasional"].copy(),
        df[df["classificacio_lectora"] == "Lector habitual"].copy(),
        var="Fins a quin punt estàs d'acord amb la següent afirmació: llegiria més lectures obligatòries de l'escola si s'adaptessin més als meus gustos.",
        groups=["No lector / Lector molt ocasional", "Lector ocasional", "Lector habitual"],
        title="Distribució de l'alumnat que llegirien més les lectures obligatòries de l'escola si s'adaptessin més als seus gustos per classificació lectora",
        xlabel="",
        ylabel="Percentatge d'alumnes (%)",
        colors=["purple", "orange", "green"],
        sort=sort_acords
    )
    
# =======================================================================================
# 9. Narrativa social adolescent sobre la lectura
# =======================================================================================
df["percepcio_social_lectura_sp"] = df["Amb quina de les següents afirmacions t’identifiques més?"].map(map_afirmacio_sp)
df["percepcio_individual_lectura_sp"] = df["En general, creus que llegir per oci entre els nois i noies de la teva edat és vist com:"].map(map_com_es_veu_sp)
df["compartir_sp"] = df["Comparteixes opinions de lectura sobre llibres o còmics que has llegit o estàs llegint amb altres persones? (Amics, família, companys de classe, companys d’activitats extraescolars, etc.)."].map(map_freq_sp)

# Grau de lectura
if len(tags) > 0 and 9 in tags:
    print("\n=======================================================================================\nNarrativa Social\n=======================================================================================")
    # Correlacions
    tmt.spearman_analysis(
        df.copy(),
        "percepcio_social_lectura_sp",
        "p4_temps_lectura_sp",
        "Spearman: percepció social sobre la lectura vs temps de lectura"
    )
    
    tmt.spearman_analysis(
        df.copy(),
        "percepcio_social_lectura_sp",
        "p5_llibres_sp",
        "Spearman: percepció social sobre la lectura vs nombre de llibres anuals llegits"
    )

    tmt.spearman_analysis(
        df.copy(),
        "percepcio_individual_lectura_sp",
        "p4_temps_lectura_sp",
        "Spearman: percepció individual sobre la lectura vs temps de lectura"
    )

    tmt.spearman_analysis(
        df.copy(),
        "percepcio_individual_lectura_sp",
        "p5_llibres_sp",
        "Spearman: percepció individual sobre la lectura vs nombre de llibres anuals llegits"
    )

    tmt.spearman_analysis(
        df.copy(),
        "compartir_sp",
        "p4_temps_lectura_sp",
        "Spearman: freqüència de compartir opinions de lectura vs temps de lectura"
    )

    tmt.spearman_analysis(
        df.copy(),
        "compartir_sp",
        "p5_llibres_sp",
        "Spearman: freqüència de compartir opinions de lectura vs nombre de llibres anuals llegits"
    )

    # fig, axs = plt.subplots(1, 2, figsize=(18, 12))
    # axs = axs.flatten()
    tmt.plot_descriptive_hists(
    df=df,
    var='Amb quina de les següents afirmacions t’identifiques més?',
    title="Distribució de l'alumnat segons la seva percepció sobre l'activitat de llegit per oci",
    xlabel="",
    ylabel="Percentatge d'alumnes",
    sort=sort_afirmacio
    )   

    tmt.plot_descriptive_hists(
    df=df,
    var='En general, creus que llegir per oci entre els nois i noies de la teva edat és vist com:',
    title="Distribució segons la percepció sobre com es veu la lectura per oci entre adolescents",
    xlabel="",
    ylabel="Percentatge d'alumnes",
    sort=sort_com_es_veu,
    color="green"
    ) 

    tmt.plot_descriptive_hists(
    df=df,
    var="Fins a quin punt estàs d'acord amb la següent afirmació: si els meus amics o companys de classe llegissin habitualment i parlessin sovint de llibres o còmics, jo també llegiria més.",
    title="Distribució segons la percepció que llegirien més si compartissin més opions de lectura",
    xlabel="",
    ylabel="Percentatge d'alumnes",
    sort=sort_acords
    )

    tmt.plot_descriptive_hists(
    df=df,
    var="Comparteixes opinions de lectura sobre llibres o còmics que has llegit o estàs llegint amb altres persones? (Amics, família, companys de classe, companys d’activitats extraescolars, etc.).",
    title="Distribució de l'alumnat segons freqüència amb que es comparteixen opinions de lectura",
    xlabel="",
    ylabel="Percentatge d'alumnes",
    sort=sort_freq
    )


# =======================================================================================
# 10. TRIC
# =======================================================================================
df["consumir_contingut_sp"] = df["Veus o escoltes continguts audiovisuals relacionats amb literatura, llibres o còmics per oci?"].map(map_freq_sp)
df["tecnos"] = df["Quant temps al dia dediques, de mitjana, a l’ús de dispositius digitals per a l’oci? (Mòbil, Ordinador, Tablet, Televisió, Smart-watch, etc.)."].map(map_tric_sp)
df["xarxes"] = df["Quant temps al dia dediques, de mitjana, a utilitzar xarxes socials o veure contingut audiovisual ràpid? (Instagram, TikTok, WhatsApp, X, Telegram, Facebook, Shorts de YouTube)."].map(map_tric_sp)
df["plataformes_streaming"] = df[
    "Quant temps al dia dediques, de mitjana, a veure o sentir contingut audiovisual en Plataformes com Netflix, YouTube, Twitch, Canals de Televisió, Amazon Prime, Spotify, Movistar +, DAZN? (Ja sigui en format vídeo gravat, vídeo en streaming o pòdcast)"
].map(map_tric_sp)

df["videojocs"] = df[
    "Quant temps al dia dediques, de mitjana, a jugar a videojocs. (Ja sigui en PlayStation, Xbox, PC, mòbil, Nintendo Switch, Nintendo DS, etc.)."
].map(map_tric_sp)


if len(tags) > 0 and 10 in tags:
    print("\n=======================================================================================\nTRIC\n=======================================================================================")
    tmt.spearman_analysis(
        df.copy(),
        "consumir_contingut_sp",
        "p4_temps_lectura_sp",
        "Spearman: consum de contingut audiovisual vs temps de lectura"
    )

    tmt.spearman_analysis(
        df.copy(),
        "consumir_contingut_sp",
        "p5_llibres_sp",
        "Spearman: consum de contingut audiovisual vs nombre de llibres anuals llegits"
    )

    tmt.spearman_analysis(
        df.copy(),
        "tecnos",
        "p4_temps_lectura_sp",
        "Spearman: temps dedicat a l’ús de dispositius digitals per a l’oci vs temps de lectura"
    )

    tmt.spearman_analysis(
        df.copy(),
        "tecnos",
        "p5_llibres_sp",
        "Spearman: temps dedicat a l’ús de dispositius digitals per a l’oci vs nombre de llibres anuals llegits"
    )

    tmt.spearman_analysis(
        df.copy(),
        "xarxes",
        "p4_temps_lectura_sp",
        "Spearman: temps dedicat a l’ús de xarxes socials vs temps de lectura"
    )

    tmt.spearman_analysis(
        df.copy(),
        "xarxes",
        "p5_llibres_sp",
        "Spearman: temps dedicat a l’ús de xarxes socials vs nombre de llibres anuals llegits"
    )

    tmt.spearman_analysis(
        df.copy(),
        "plataformes_streaming",
        "p4_temps_lectura_sp",
        "Spearman: temps dedicat a veure contingut en plataformes de streaming vs temps de lectura"
    )

    tmt.spearman_analysis(
        df.copy(),
        "plataformes_streaming",
        "p5_llibres_sp",
        "Spearman: temps dedicat a veure contingut en plataformes de streaming vs nombre de llibres anuals llegits"
    )

    tmt.spearman_analysis(
        df.copy(),
        "videojocs",
        "p4_temps_lectura_sp",
        "Spearman: temps dedicat a jugar a videojocs vs temps de lectura"
    )

    tmt.spearman_analysis(
        df.copy(),
        "videojocs",
        "p5_llibres_sp",
        "Spearman: temps dedicat a jugar a videojocs vs nombre de llibres anuals llegits"
    )

    # Plots Xarxes socials ------------------
    tmt.plot_descriptive_hists(
        df=df,
        var="Quant temps al dia dediques, de mitjana, a utilitzar xarxes socials o veure contingut audiovisual ràpid? (Instagram, TikTok, WhatsApp, X, Telegram, Facebook, Shorts de YouTube).",
        title="Distribució de l'alumnat segons el temps diari dedicat a xarxes socials o contingut audiovisual ràpid",
        xlabel="",
        ylabel="Percentatge d'alumnes",
        sort=sort_tric
    )

    tmt.plot_descriptive_combined_hists(
        df[df["classificacio_lectora"] == "No lector / Lector molt ocasional"].copy(),
        df[df["classificacio_lectora"] == "Lector ocasional"].copy(),
        df[df["classificacio_lectora"] == "Lector habitual"].copy(),
        groups=["No lector / Lector molt ocasional", "Lector ocasional", "Lector habitual"],
        var="Quant temps al dia dediques, de mitjana, a utilitzar xarxes socials o veure contingut audiovisual ràpid? (Instagram, TikTok, WhatsApp, X, Telegram, Facebook, Shorts de YouTube).",
        title="Distribució de l'alumnat segons temps diari dedicat a x.socials o contingut audiovisual ràpid per class. lectora",
        xlabel="",
        ylabel="Percentatge d'alumnes (%)",
        colors=["blue", "orange", "green"],
        sort=sort_tric
    )

    # Plots Contingut Audioviual Lectura ------------------
    # fig, axs = plt.subplots(2, 1, figsize=(18, 6))
    tmt.plot_descriptive_hists(
        df=df,
        var="Veus o escoltes continguts audiovisuals relacionats amb literatura, llibres o còmics per oci?",
        title="Freqüència de consum de contingut audiovisual sobre literatura, llibres o còmics",
        xlabel="",
        ylabel="Percentatge d'alumnes",
        sort=sort_freq
    )

    tmt.plot_descriptive_combined_hists(
        df[df["classificacio_lectora"] == "No lector / Lector molt ocasional"].copy(),
        df[df["classificacio_lectora"] == "Lector ocasional"].copy(),
        df[df["classificacio_lectora"] == "Lector habitual"].copy(),
        groups=["No lector / Lector molt ocasional", "Lector ocasional", "Lector habitual"],
        var="Veus o escoltes continguts audiovisuals relacionats amb literatura, llibres o còmics per oci?",
        title="Freqüència de consum de contingut audiovisual sobre literatura, llibres o còmics segons classificació lectora",
        xlabel="",
        ylabel="Percentatge d'alumnes (%)",
        colors=["blue", "orange", "green"],
        sort=sort_freq
    )

    # Plots llegiria més si.... ------------------
    tmt.plot_descriptive_hists(
    df=df_readers,
    var="Fins a quin punt estàs d'acord amb la següent afirmació: llegiria més llibres o còmics si dediqués menys temps a les xarxes socials i plataformes de videos curts? . (Instagram, TikTok, WhatsApp, X, Telegram, Facebook, Shorts de YouTube).",
    title="Percepció que llegirien més si dediquessin menys temps a x.socials i plat. de videos curts",
    xlabel="",
    ylabel="Percentatge d'alumnes",
    sort=sort_acords
    )

    tmt.plot_descriptive_hists(
    df=df_readers,
    var="Fins a quin punt estàs d'acord amb la següent afirmació: llegiria més llibres o còmics si dediqués menys temps a videojocs (PlayStation, PC, mòbil, etc.) i/o plataformes de contingut audiovisual.  (Netflix, YouTube, Twitch, canals de televisió, Amazon Prime, HBO, Disney +, Movistar +, DAZN).",
    title="Percepció que llegirien més si dediquessin menys temps a vjocs i cont. audiovisual",
    xlabel="",
    ylabel="Percentatge d'alumnes",
    color="orange",
    sort=sort_acords
    )

# =======================================================================================
# 11. Altres activitats
# =======================================================================================
df["estudi_sp"] = df["Quant temps al dia dediques, de mitjana, a l’estudi i la realització de tasques acadèmiques fora de l’horari escolar? (Exàmens, deures, treballs, etc.)"].map(map_tric_sp)

df["cultura_sp"] = df["Quant temps al dia dediques, de mitjana, a realitzar activitats relacionades amb la cultura fora de l’horari escolar? (Música, dansa, teatre, pintura, escriptura, visites a museus, etc.)."].map(map_tric_sp)

df["sport_sp"] = df["Quant temps al dia dediques, de mitjana, a la pràctica d’esport fora de l’horari escolar? (Futbol, bàsquet, atletisme, ciclisme, natació, ioga, gym, senderisme, tenis, pàdel, ping-pong, etc.)."].map(map_tric_sp)

df["hangout_sp"] = df["Quant temps al dia dediques, de mitjana, a quedar amb amics / amigues o parella sentimental fora de l’horari escolar?"].map(map_tric_sp)

if len(tags) > 0 and 11 in tags:
    print("\n=======================================================================================\nAltres Activitats\n=======================================================================================")
    tmt.spearman_analysis(
        df.copy(),
        "estudi_sp",
        "p4_temps_lectura_sp",
        "Spearman: temps dedicat a l’estudi vs temps de lectura"
    )

    tmt.spearman_analysis(
        df.copy(),
        "estudi_sp",
        "p5_llibres_sp",
        "Spearman: temps dedicat a l’estudi vs nombre de llibres anuals llegits"
    )

    tmt.spearman_analysis(
        df.copy(),
        "cultura_sp",
        "p4_temps_lectura_sp",
        "Spearman: temps dedicat a activitats culturals vs temps de lectura"
    )

    tmt.spearman_analysis(
        df.copy(),
        "cultura_sp",
        "p5_llibres_sp",
        "Spearman: temps dedicat a activitats culturals vs nombre de llibres anuals llegits"
    )

    tmt.spearman_analysis(
        df.copy(),
        "sport_sp",
        "p4_temps_lectura_sp",
        "Spearman: temps dedicat a la pràctica d’esport vs temps de lectura"
    )

    tmt.spearman_analysis(
        df.copy(),
        "sport_sp",
        "p5_llibres_sp",
        "Spearman: temps dedicat a la pràctica d’esport vs nombre de llibres anuals llegits"
    )

    tmt.spearman_analysis(
        df.copy(),
        "hangout_sp",
        "p4_temps_lectura_sp",
        "Spearman: temps dedicat a quedar amb amics / amigues o parella sentimental vs temps de lectura"
    )

    tmt.spearman_analysis(
        df.copy(),
        "hangout_sp",
        "p5_llibres_sp",
        "Spearman: temps dedicat a quedar amb amics / amigues o parella sentimental vs nombre de llibres anuals llegits"
    )

    # Plots Cultura ------------------
    tmt.plot_descriptive_combined_hists(
        df[df["classificacio_lectora"] == "No lector / Lector molt ocasional"].copy(),
        df[df["classificacio_lectora"] == "Lector ocasional"].copy(),
        df[df["classificacio_lectora"] == "Lector habitual"].copy(),
        groups=["No lector / Lector molt ocasional", "Lector ocasional", "Lector habitual"],
        var="Quant temps al dia dediques, de mitjana, a realitzar activitats relacionades amb la cultura fora de l’horari escolar? (Música, dansa, teatre, pintura, escriptura, visites a museus, etc.).",
        title="Distribució de l'alumnat segons temps dedicat a activitats culturals fora de l’horari escolar per class. lectora",
        xlabel="",
        ylabel="Percentatge d'alumnes (%)",
        colors=["blue", "orange", "green"],
        sort=sort_tric
    )

    # Plots Hangout ------------------
    tmt.plot_descriptive_combined_hists(
        df[df["classificacio_lectora"] == "No lector / Lector molt ocasional"].copy(),
        df[df["classificacio_lectora"] == "Lector ocasional"].copy(),
        df[df["classificacio_lectora"] == "Lector habitual"].copy(),
        groups=["No lector / Lector molt ocasional", "Lector ocasional", "Lector habitual"],
        var="Quant temps al dia dediques, de mitjana, a quedar amb amics / amigues o parella sentimental fora de l’horari escolar?",
        title="Distribució de l'alumnat segons temps dedicat a quedar amb amics o parella per class. lectora",
        xlabel="",
        ylabel="Percentatge d'alumnes (%)",
        colors=["blue", "orange", "green"],
        sort=sort_tric
    )

     # Plots llegiria més si.... ------------------
    tmt.plot_descriptive_hists(
    df=df_readers,
    var="Fins a quin punt estàs d'acord amb la següent afirmació: llegiria més llibres o còmics si tingués menys càrrega acadèmica fora d'horari escolar. (Exàmens, deures, treballs, etc.)",
    title="Percepció que llegirien més si tinguessin menys càrrega acadèmica fora d'horari escolar",
    xlabel="",
    ylabel="Percentatge d'alumnes",
    sort=sort_acords
    )

# =======================================================================================
# 12. Entorn familiar pro-lector
# =======================================================================================
df["estudis_familiars_sp"] = df["Quin és el nivell d’estudis més alt dels teus pares o tutors legals?"].map(map_estudis_familiars_sp)
df["vist_pares_lectura_sp"] = df["Durant la teva infància i adolescència, amb quina freqüència has vist als teus pares o tutors legals llegint llibres o còmics per oci?"].map(map_freq_sp)
df["parlat_pares_lectura_sp"] = df["Durant la teva infància i adolescència, amb quina freqüència has parlat amb els teus pares o tutors legals sobre literatura, llibres o còmics?"].map(map_freq_sp)
df["sessions_lectura_familiars_sp"] = df["Durant la teva infància i adolescència, amb quina freqüència heu realitzat sessions de lectura conjunta a casa?"].map(map_freq_sp)
df["normes_clares_tric_sp"] = df["Fins a quin punt estàs d'acord amb la següent afirmació: a casa meva hi ha normes clares sobre el temps que puc dedicar a les pantalles i dispositius digitals."].map(map_acord_sp)
df["num_llibres_sp"] = df["Quants llibres aproximadament heu tingut a casa durant la teva infància i adolescència?"].map(map_num_llibres_sp)

if len(tags) > 0 and 12 in tags:
    print("\n=======================================================================================\nEntorn Familiar Pro-Lector\n=======================================================================================")
    tmt.spearman_analysis(
        df.copy(),
        "estudis_familiars_sp",
        "p4_temps_lectura_sp",
        "Spearman: nivell d'estudis familiars vs temps de lectura setmanal"
    )

    tmt.spearman_analysis(
        df.copy(),
        "estudis_familiars_sp",
        "p5_llibres_sp",
        "Spearman: nivell d'estudis familiars vs nombre de llibres anuals llegits"
    )

    tmt.spearman_analysis(
        df.copy(),
        "vist_pares_lectura_sp",
        "p4_temps_lectura_sp",
        "Spearman: freqüència de veure els pares llegint vs temps de lectura setmanal"
    )

    tmt.spearman_analysis(
        df.copy(),
        "vist_pares_lectura_sp",
        "p5_llibres_sp",
        "Spearman: freqüència de veure els pares llegint vs nombre de llibres anuals llegits"
    )

    tmt.spearman_analysis(
        df.copy(),
        "parlat_pares_lectura_sp",
        "p4_temps_lectura_sp",
        "Spearman: freqüència de parlar amb els pares sobre lectura vs temps de lectura setmanal"
    )

    tmt.spearman_analysis(
        df.copy(),
        "parlat_pares_lectura_sp",
        "p5_llibres_sp",
        "Spearman: freqüència de parlar amb els pares sobre lectura vs nombre de llibres anuals llegits"
    )

    tmt.spearman_analysis(
        df.copy(),
        "sessions_lectura_familiars_sp",
        "p4_temps_lectura_sp",
        "Spearman: freqüència de sessions de lectura conjunta vs temps de lectura setmanal"
    )

    tmt.spearman_analysis(
        df.copy(),
        "sessions_lectura_familiars_sp",
        "p5_llibres_sp",
        "Spearman: freqüència de sessions de lectura conjunta vs nombre de llibres anuals llegits"
    )

    tmt.spearman_analysis(
        df.copy(),
        "normes_clares_tric_sp",
        "p4_temps_lectura_sp",
        "Spearman: percepció de normes clares sobre lectura vs temps de lectura setmanal"
    )

    tmt.spearman_analysis(
        df.copy(),
        "normes_clares_tric_sp",
        "p5_llibres_sp",
        "Spearman: percepció de normes clares sobre lectura vs nombre de llibres anuals llegits"
    )

    tmt.spearman_analysis(
        df.copy(),
        "num_llibres_sp",
        "p4_temps_lectura_sp",
        "Spearman: nombre de llibres anuals llegits vs temps de lectura setmanal"
    )

    tmt.spearman_analysis(
        df.copy(),
        "num_llibres_sp",
        "p5_llibres_sp",
        "Spearman: nombre de llibres anuals llegits vs nombre de llibres anuals llegits"
    )

    # Plot Num llibres biblioteca ------------------
    tmt.plot_descriptive_combined_hists(
        df[df["classificacio_lectora"] == "No lector / Lector molt ocasional"].copy(),
        df[df["classificacio_lectora"] == "Lector ocasional"].copy(),
        df[df["classificacio_lectora"] == "Lector habitual"].copy(),
        groups=["No lector / Lector molt ocasional", "Lector ocasional", "Lector habitual"],
        var="Quants llibres aproximadament heu tingut a casa durant la teva infància i adolescència?",
        title="Distribució de l'alumnat segons nombre aprox. de llibres que han tingut a casa per classificació lectora",
        xlabel="",
        ylabel="Percentatge d'alumnes (%)",
        colors=["blue", "orange", "green"],
        sort=sort_num_llibres
    )

    # Plot normes clares ------------------
    tmt.plot_descriptive_combined_hists(
        df[df["classificacio_lectora"] == "No lector / Lector molt ocasional"].copy(),
        df[df["classificacio_lectora"] == "Lector ocasional"].copy(),
        df[df["classificacio_lectora"] == "Lector habitual"].copy(),
        groups=["No lector / Lector molt ocasional", "Lector ocasional", "Lector habitual"],
        var="Fins a quin punt estàs d'acord amb la següent afirmació: a casa meva hi ha normes clares sobre el temps que puc dedicar a les pantalles i dispositius digitals.",
        title="Distribució de l'alumnat segons normes clares sobre el temps de pantalles i dispositius digitals per class. lectora",
        xlabel="",
        ylabel="Percentatge d'alumnes (%)",
        colors=["blue", "orange", "green"],
        sort=sort_acords
    )

    # Plot parlar pares literatura ------------------
    tmt.plot_descriptive_combined_hists(
        df[df["classificacio_lectora"] == "No lector / Lector molt ocasional"].copy(),
        df[df["classificacio_lectora"] == "Lector ocasional"].copy(),
        df[df["classificacio_lectora"] == "Lector habitual"].copy(),
        groups=["No lector / Lector molt ocasional", "Lector ocasional", "Lector habitual"],
        var="Durant la teva infància i adolescència, amb quina freqüència has parlat amb els teus pares o tutors legals sobre literatura, llibres o còmics?",
        title="Distribució de l'alumnat segons freqüència de compartir a casa opinions sobre literatura per class. lectora",
        xlabel="",
        ylabel="Percentatge d'alumnes (%)",
        colors=["blue", "orange", "green"],
        sort=sort_freq
    )

if tmt.ask_to_plot() == "y":
    plt.show()

#########################################################################################
#
# / Main Operations
#
#########################################################################################
