import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pprint import pprint
from scipy.stats import linregress
import sys

import methods as mt
import seaborn as sns
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

# Iteration
plot_it = 0

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
if verbose:
    print("[Check]: Income Dataframe Info")
    print(f"Dataframe dimensions (rows, cols): {df.shape}")
    print(f"First 5 lines of the dataframe: \n{df.head()}")
    # print(f"\nCheck no null values:")
    # print(df.info())
    # print(f"\nCheck no nulls values per column:")
    # print(df.isnull().sum())

# =======================================================================================
# Rename some important columns
# =======================================================================================
# Primero renombramos columnas
df = df.rename(columns={
    "Quant temps a la setmana dediques, de mitjana, a la lectura de llibres o còmics per oci? (Ja sigui en format físic o digital).": "p4_temps_lectura",
    "Quants llibres o còmics t’has llegit aproximadament en els últims 12 mesos per oci? (Ja sigui en format físic o digital)": "p5_llibres",
    "En cas que la resposta hagi estat diferent de 0 llibres o còmics, quantes pàgines, de mitjana, tenien aproximadament aquests llibres o còmics?": "p6_pag",
    "Actualment estàs llegint algun llibre o còmic per oci?": "p7_lectura_actual",
    "Quants cops aproximadament has visitat una biblioteca per llegir o agafar llibres en préstec en els últims 12 mesos per oci?": "p10_visites_biblioteca",
    "En quin grau llegeixes les lectures obligatòries de l’escola?": "p16_lectura_obligatoria", 
})

# =======================================================================================
# Create subdataframes of readers, gender, curs
# =======================================================================================
df_lectors = df[
    (df["p5_llibres"] != "0 llibres o còmics.") &
    (df["p4_temps_lectura"] != "0 minuts.") &
    (df["Quan llegeixes, com acostumen a ser les teves sessions de lectura?"] != "No llegeixo per oci.") &
    (df["Quin format de lectura utilitzes més habitualment per a la lectura de llibres o còmics per oci? "] != "No llegeixo per oci.")
]

df_fem = df[df["Gènere"] == "Femení."].copy()
df_mas = df[df["Gènere"] == "Masculí."].copy()

df_3e = df[df["Curs"] == "3r d'ESO."].copy()
df_4e = df[df["Curs"] == "4t d'ESO."].copy()
df_1b = df[df["Curs"] == "1r de Batxillerat."].copy()
df_2b = df[df["Curs"] == "2n de Batxillerat."].copy()
df_soc = df[df["Itinerari (només si estàs cursant Batxillerat)"] == "Ciències Socials."].copy()
df_ct = df[df["Itinerari (només si estàs cursant Batxillerat)"] == "Ciències i Tecnologia."].copy()


# =======================================================================================
# 1. Thematic
# =======================================================================================
if len(tags) > 0 and 1 in tags:
    print("\n=======================================================================================\nThematic\n=======================================================================================")
    # Remap thematic
    map_thematic = {
        1: 3,
        2: 2,
        3: 1
    }

    columnes_generes = {
        "Novel·la fantàstica": "Marca ordenadament els 3 gèneres literaris que més llegeixes per oci. [Novel·la fantàstica.]",
        "Novel·la romàntica": "Marca ordenadament els 3 gèneres literaris que més llegeixes per oci. [Novel·la romàntica.]",
        "Novel·la de terror": "Marca ordenadament els 3 gèneres literaris que més llegeixes per oci. [Novel·la de terror.]",
        "Novel·la negra": "Marca ordenadament els 3 gèneres literaris que més llegeixes per oci. [Novel·la negra.]",
        "Novel·la històrica": "Marca ordenadament els 3 gèneres literaris que més llegeixes per oci. [Novel·la històrica.]",
        "Ciència ficció": "Marca ordenadament els 3 gèneres literaris que més llegeixes per oci. [Ciència ficció.]",
        "Còmic": "Marca ordenadament els 3 gèneres literaris que més llegeixes per oci. [Còmic.]",
        "Clàssics": "Marca ordenadament els 3 gèneres literaris que més llegeixes per oci. [Clàssics.]",
        "Poesia": "Marca ordenadament els 3 gèneres literaris que més llegeixes per oci. [Poesia.]",
        "Assaig": "Marca ordenadament els 3 gèneres literaris que més llegeixes per oci. [Assaig (Filosofia, divulgació científica, etc.)]",
        "Teatre": "Marca ordenadament els 3 gèneres literaris que més llegeixes per oci. [Teatre.]"
    }

    # Generics
    # =======================================================
    resultats = {}

    for nom, columna in columnes_generes.items():
        nova_col = f"{nom}_score"
        
        df[nova_col] = (
            pd.to_numeric(df[columna], errors="coerce")
            .map(map_thematic)
            .fillna(0)
        )
        
        resultats[nom] = df[nova_col].sum()

    resultats_df = pd.DataFrame.from_dict(
        resultats,
        orient="index",
        columns=["puntuacio_total"]
    ).sort_values("puntuacio_total", ascending=False)

    # print(resultats_df)

    freq = resultats_df["puntuacio_total"]

    # Plot
    plot_it += 1
    plt.figure(plot_it)

    # Opcional: partir textos llargs si uses noms més llargs després
    freq.index = [textwrap.fill(label, 15) for label in freq.index]

    ax = freq.plot(kind="bar")

    # Mostrar valors damunt de cada barra
    total = freq.sum()

    for i, v in enumerate(freq):
        ax.text(
            i,
            v,
            f"{int(v)} punts",
            ha="center",
            va="bottom"
        )

    # Editar text
    plt.title("Distribució de preferències dels gèneres literaris")
    plt.ylabel("Puntuació ponderada")
    plt.xlabel("Gèneres literaris")
    plt.xticks(rotation=45, ha="center")

    # Femení
    # =======================================================
    resultats_fem = {}

    for nom, columna in columnes_generes.items():
        nova_col = f"{nom}_score"
        
        df_fem[nova_col] = (
            pd.to_numeric(df_fem[columna], errors="coerce")
            .map(map_thematic)
            .fillna(0)
        )
        
        resultats_fem[nom] = df_fem[nova_col].sum()

    resultats_df_fem = pd.DataFrame.from_dict(
        resultats_fem,
        orient="index",
        columns=["puntuacio_total"]
    ).sort_values("puntuacio_total", ascending=False)

    freq = resultats_df_fem["puntuacio_total"]

    # Plot
    plot_it += 1
    plt.figure(plot_it)

    # Opcional: partir textos llargs si uses noms més llargs després
    freq.index = [textwrap.fill(label, 15) for label in freq.index]

    ax = freq.plot(kind="bar")

    # Mostrar valors damunt de cada barra
    total = freq.sum()

    for i, v in enumerate(freq):
        ax.text(
            i,
            v,
            f"{int(v)} punts",
            ha="center",
            va="bottom"
        )

    # Editar text
    ax = freq.plot(kind="bar", color="purple")
    plt.title("Distribució de preferències dels gèneres literaris per les noies")
    plt.ylabel("Puntuació ponderada")
    plt.xlabel("Gèneres literaris")
    plt.xticks(rotation=45, ha="center")

    # Masculí
    # =======================================================
    resultats_mas = {}

    for nom, columna in columnes_generes.items():
        nova_col = f"{nom}_score"
        
        df_mas[nova_col] = (
            pd.to_numeric(df_mas[columna], errors="coerce")
            .map(map_thematic)
            .fillna(0)
        )
        
        resultats_mas[nom] = df_mas[nova_col].sum()

    resultats_df_mas = pd.DataFrame.from_dict(
        resultats_mas,
        orient="index",
        columns=["puntuacio_total"]
    ).sort_values("puntuacio_total", ascending=False)

    freq = resultats_df_mas["puntuacio_total"]

    # Plot
    plot_it += 1
    plt.figure(plot_it)

    # Opcional: partir textos llargs si uses noms més llargs després
    freq.index = [textwrap.fill(label, 15) for label in freq.index]

    ax = freq.plot(kind="bar")

    # Mostrar valors damunt de cada barra
    total = freq.sum()

    for i, v in enumerate(freq):
        ax.text(
            i,
            v,
            f"{int(v)} punts",
            ha="center",
            va="bottom"
        )

    # Editar text
    # colores = ["red", "blue", "green", "orange", "purple"]
    ax = freq.plot(kind="bar", color="orange")
    plt.title("Distribució de preferències dels gèneres literaris pels nois")
    plt.ylabel("Puntuació ponderada")
    plt.xlabel("Gèneres literaris")
    plt.xticks(rotation=45, ha="center")

# =======================================================================================
# 2. p4_temps_lectura
# =======================================================================================
if len(tags) > 0 and 2 in tags:
    print(plot_it)
    print("\n=======================================================================================\nReading Time \n=======================================================================================")
    sort = [
        "0 minuts.",
        "Menys de 30 minuts a la setmana.",
        "Entre 30 minuts i 1 hora a la setmana.",
        "Entre 1 i 2 hores a la setmana.",
        "Entre 2 i 3 hores a la setmana.",
        "3 hores o més a la setmana."
    ]

    # General
    # =======================================================
    plot_it += 1
    plt.figure(plot_it)
    tmt.plot_descriptive_hists(
        df=df,
        var="p4_temps_lectura",
        title="Distribució del temps promig dedicat a la lectura de llibres o còmics per oci a la setmana",
        xlabel="",
        ylabel="Percentatge d'alumnes",
        sort=sort
    )
    
    # Boys vs girls
    # =======================================================
    # plot_it += 1
    plt.figure(plot_it)
    tmt.plot_descriptive_combined_hists2(
        df_1=df_fem,
        df_2=df_mas,
        groups=["Noies", "Nois"],
        var="p4_temps_lectura",
        title="Distribució del temps promig dedicat a la lectura de llibres o còmics per oci a la setmana per genere",
        xlabel="",
        ylabel="Percentatge d'alumnes (%)",
        colors=["purple", "orange"],
        sort=sort
    )

    # Groups
    # =======================================================
    # plot_it += 1
    plt.figure(plot_it)
    tmt.plot_descriptive_combined_hists4(
        df_1=df_3e,
        df_2=df_4e,
        df_3=df_1b,
        df_4=df_2b,
        groups=["3r d'ESO", "4t d'ESO", "1r de Batxillerat", "2n de Batxillerat"],
        var="p4_temps_lectura",
        title="Distribució del temps promig dedicat a la lectura de llibres o còmics per oci a la setmana per curs",
        xlabel="",
        ylabel="Percentatge d'alumnes (%)",
        colors=["blue", "orange", "green", "red"],
        sort=sort
    )

    # Ciencies Socials vs Tecnologia i Ciencia
    # =======================================================
    # plot_it += 1
    plt.figure(plot_it)
    tmt.plot_descriptive_combined_hists2(
        df_1=df_soc,
        df_2=df_ct,
        groups=["Ciències Socials", "Ciències i Tecnologia"],
        var="p4_temps_lectura",
        title="Distribució del temps promig dedicat a la lectura de llibres o còmics per oci a la setmana per itinerari",
        xlabel="",
        ylabel="Percentatge d'alumnes (%)",
        colors=["red", "green"],
        sort=sort
    )

# =======================================================================================
# 3. Composed variables books * pages --> pages / year (p5_6_pagines)
# =======================================================================================
if len(tags) > 0 and 3 in tags:
    print("\n=======================================================================================\nPages per year\n=======================================================================================")

    # Recode P5 to mean number of books
    # =======================================================
    map_llibres = {
        "0 llibres o còmics.": 0,
        "1-2 llibres o còmics.": 1.5,
        "3-5 llibres o còmics.": 4,
        "6-10 llibres o còmics.": 8,
        "11-15 llibres o còmics.": 13,
        "Més de 15 llibres o còmics": 18
    }

    df["p5_num"] = df["p5_llibres"].map(map_llibres)

    # Recode P6 to mean number of pages
    map_pagines = {
        "1-99 pàgines.": 50,
        "100-299 pàgines.": 200,
        "300-599 pàgines.": 450,
        "Més de 600 pàgines": 700
    }

    df["p6_num"] = df["p6_pag"].map(map_pagines)

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

    # Check result
    if verbose:
        print("[Check]: p5_6_pagines")
        print("Check first 20 rows:")
        print(
            df[
                [
                    "p5_llibres",
                    "p6_pag",
                    "p5_num",
                    "p6_num",
                    "p5_6_pagines_num",
                    "p5_6_pagines",
                ]
            ].head(20)
        )
        # print(df["p5_6_pagines_num"].to_string())

    print("\n------------ Estatistics from p5_6_pagines -------------")
    print("General ---")
    print(df["p5_6_pagines_num"].describe())
    print("Femení ---")
    print(df[df["Gènere"] == "Femení."]["p5_6_pagines_num"].describe())
    print("Masculí ---")
    print(df[df["Gènere"] == "Masculí."]["p5_6_pagines_num"].describe())
    print("3r d'ESO ---")
    print(df[df["Curs"] == "3r d'ESO."]["p5_6_pagines_num"].describe())
    print("4t d'ESO ---")
    print(df[df["Curs"] == "4t d'ESO."]["p5_6_pagines_num"].describe())
    print("1r de Batxillerat ---")
    print(df[df["Curs"] == "1r de Batxillerat."]["p5_6_pagines_num"].describe())
    print("2n de Batxillerat ---")
    print(df[df["Curs"] == "2n de Batxillerat."]["p5_6_pagines_num"].describe())

    # Plot
    plot_it += 1
    plt.figure(plot_it)

    tmt.plot_descriptive_hists(
        df=df,
        var="p5_6_pagines",
        title="Distribució nombre de pàgines estimades llegides aquest any (llibre o còmic) per oci",
        xlabel="Pàgines estimades llegides anualment",
        ylabel="Percentatge d'alumnes",
    )

    plot_it += 1
    plt.figure(plot_it)
    df["p5_6_pagines_num"].plot(kind="box", showmeans=True)

    plt.title("Boxplot de la distribució del nombre de pàgines estimades llegides anualment")
    plt.suptitle("")  # elimina el título automático de pandas
    plt.ylabel("Pàgines")
    plt.xlabel("")

    # plot_it += 1
    plt.figure(plot_it)
    df_filtrat = df[df["Gènere"] != "Prefereixo no respondre."]
    df_filtrat.boxplot(column="p5_6_pagines_num", by="Gènere", showmeans=True)

    plt.title("Distribució de pàgines llegides anualment per gènere")
    plt.suptitle("")  # elimina el título automático de pandas
    plt.ylabel("Pàgines")
    plt.xlabel("")

   # plot_it += 1
    plt.figure(plot_it)
    orden = ["3r d'ESO.", "4t d'ESO.", "1r de Batxillerat.", "2n de Batxillerat."]
    df["Curs"] = pd.Categorical(df["Curs"], categories=orden, ordered=True)
    df.boxplot(column="p5_6_pagines_num", by="Curs", showmeans=True)

    plt.title("Distribució de pàgines llegides anualment per curs")
    plt.suptitle("")  # elimina el título automático de pandas
    plt.ylabel("Pàgines")
    plt.xlabel("")

plt.show()
#########################################################################################
#
# / Main Operations
#
#########################################################################################

# Per tal d’obtenir una mesura més precisa del volum anual de lectura per oci, es va construir una variable composta a partir del nombre aproximat de llibres llegits durant els últims 12 mesos i del nombre mitjà de pàgines d’aquests llibres. Per fer-ho, es va assignar a cada categoria ordinal un valor representatiu corresponent al punt mig de cada interval, i posteriorment es va calcular una estimació del total de pàgines llegides anualment.