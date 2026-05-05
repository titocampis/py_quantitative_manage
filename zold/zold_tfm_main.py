import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pprint import pprint
from scipy.stats import linregress
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
    print("\n=======================================================================================\nIncome Dataframe Info\n=======================================================================================")
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
        ylabel="Freqüència",
        sort=sort
    )

    # Femení
    # =======================================================
    plot_it += 1
    plt.figure(plot_it)
    tmt.plot_descriptive_hists(
        df=df_fem,
        var="p4_temps_lectura",
        title="Distribució del temps promig dedicat per les noies a la lectura de llibres o còmics per oci a la setmana",
        xlabel="",
        ylabel="Freqüència",
        color="purple",
        sort=sort
    )


    # Masculí
    # =======================================================
    plot_it += 1
    plt.figure(plot_it)
    tmt.plot_descriptive_hists(
        df=df_mas,
        var="p4_temps_lectura",
        title="Distribució del temps promig dedicat pels nois a la lectura de llibres o còmics per oci a la setmana",
        xlabel="",
        ylabel="Freqüència",
        color="orange",
        sort=sort
    )

    # 3e
    # =======================================================
    plot_it += 1
    plt.figure(plot_it)
    tmt.plot_descriptive_hists(
        df=df_3e,
        var="p4_temps_lectura",
        title="Distribució del temps promig dedicat pels alumnes de 3r d'ESO a la lectura de llibres o còmics per oci a la setmana",
        xlabel="",
        ylabel="Freqüència",
        color="green",
        sort=sort
    )

    # 4e
    # =======================================================
    plot_it += 1
    plt.figure(plot_it)
    tmt.plot_descriptive_hists(
        df=df_4e,
        var="p4_temps_lectura",
        title="Distribució del temps promig dedicat pels alumnes de 4t d'ESO a la lectura de llibres o còmics per oci a la setmana",
        xlabel="",
        ylabel="Freqüència",
        color="orange",
        sort=sort
    )

    # 1b
    # =======================================================
    plot_it += 1
    plt.figure(plot_it)
    tmt.plot_descriptive_hists(
        df=df_1b,
        var="p4_temps_lectura",
        title="Distribució del temps promig dedicat pels alumnes de 1r de Batxillerat a la lectura de llibres o còmics per oci a la setmana",
        xlabel="",
        ylabel="Freqüència",
        color="blue",
        sort=sort
    )

    # 2b
    # =======================================================
    plot_it += 1
    plt.figure(plot_it)
    tmt.plot_descriptive_hists(
        df=df_2b,
        var="p4_temps_lectura",
        title="Distribució del temps promig dedicat pels alumnes de 2n de Batxillerat a la lectura de llibres o còmics per oci a la setmana",
        xlabel="",
        ylabel="Freqüència",
        color="red",
        sort=sort
    )


# =======================================================================================
# 3. Composed variables books * pages --> pages / year (p5_6_pagines)
# =======================================================================================
if len(tags) > 0 and 3 in tags:
    print("\n=======================================================================================\nPages per year\n=======================================================================================")
    # Recode P5 to mean number of books
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
    ######################################################################################
    # Categorize
    bins = [-1, 0, 500, 1000, 3000, 4000, float("inf")]
    labels = ["0", "1-500", "501-1000", "1001-3000", "3001-4000", ">4000"]

    # df["p5_6_pagines"] = df["p5_6_pagines_num"].apply(tmt.categorize_pags)
    df["p5_6_pagines"] = pd.cut(
        df["p5_6_pagines_num"],
        bins=bins,
        labels=labels
    )

    # Check result
    if verbose:
        print("\n=======================================================================================\nComposed Variable\n=======================================================================================")
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

    # Print estatistics
    print(f'\n=======================================================================================\nEstatistics from p5_6_pagines_num variable:\n=======================================================================================')
    print(df["p5_6_pagines_num"].describe())

    # Plot
    plot_it += 1
    plt.figure(plot_it)

    tmt.plot_descriptive_hists(
        df=df,
        var="p5_6_pagines",
        title="Distribució nombre de pàgines estimades llegides aquest any (llibre o còmic) per oci",
        xlabel="Pàgines estimades llegides anualment",
        ylabel="Freqüència"
    )

    # # Crear histograma y capturar datos
    # plot_it += 1
    # plt.figure(plot_it)
    # counts, bins, patches = plt.hist(df["p5_6_pagines_num"], bins=12)

    # plt.title("Histograma del nombre de pàgines estimades llegides anualment (llibre o còmic) per oci")
    # plt.xlabel("Pàgines estimades llegides anualment")
    # plt.ylabel("Freqüència")

    # # Añadir valores encima de cada barra
    # for count, patch in zip(counts, patches):
    #     plt.text(
    #         patch.get_x() + patch.get_width() / 2,
    #         count,
    #         int(count),
    #         ha='center',
    #         va='bottom'
    #     )


# =======================================================================================
# 4. p7_lectura_actual
# =======================================================================================
if len(tags) > 0 and 4 in tags: 
    plot_it += 1
    plt.figure(plot_it)
    tmt.plot_descriptive_hists(
        df=df,
        var="p7_lectura_actual",
        title="Distribució alumnes que estan llegint actualment un llibre o còmic per oci",
        xlabel="",
        ylabel="Freqüència"
    )

# =======================================================================================
# 5. p16_lectura_obligatoria
# =======================================================================================
# Grau de lectura
if len(tags) > 0 and 5 in tags:
    plot_it += 1
    plt.figure(plot_it)
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
        title="Distribució alumnes que llegeixen les lectures obligatòries de l’escola",
        xlabel="",
        ylabel="Freqüència",
        sort=sort
    )

# =======================================================================================
# 6. p10_visites_biblioteca
# =======================================================================================
if len(tags) > 0 and 6 in tags:
    plot_it += 1
    plt.figure(plot_it)
    sort = [
        "0 cops.",
        "1-2 cops.",
        "3-5 cops.",
        "6-10 cops.",
        "Més de 10 cops."
    ]

    tmt.plot_descriptive_hists(
        df=df,
        var="p10_visites_biblioteca",
        title="Distribució nombre de visites a la biblioteca per llegir o agafar llibres o còmics en préstec en l'últim any per oci",
        xlabel="",
        ylabel="Freqüència",
        sort=sort
    )


# =======================================================================================
# 7. Format de lectura
# =======================================================================================
if len(tags) > 0 and 7 in tags:
    # Clean df_lectors
    valores_excluir = [
        "digital (xarxes socials)",
        "en paper i en digital",
        "wattpad,webtoon"
    ]

    col = "Quin format de lectura utilitzes més habitualment per a la lectura de llibres o còmics per oci? "

    df_lectors = df_lectors[
        ~df_lectors[col].isin(valores_excluir)
    ]

    plot_it += 1
    plt.figure(plot_it)

    tmt.plot_descriptive_hists(
        df=df_lectors,
        var="Quin format de lectura utilitzes més habitualment per a la lectura de llibres o còmics per oci? ",
        title="Format de lectura més habitual per a la lectura de llibres o còmics per oci",
        xlabel="",
        ylabel="Freqüència"
    )


# =======================================================================================
# Pending tasks --> crossed analysis plots and basic statistics
# =======================================================================================
# Genero
# =======================================
# Tiempo de lectura ocio por genero histogram
# Stat Chicas que no leen nada vs chicos que no leen nada
# Stat Chicas que leen mas de 3 horas vs chicos que leen mas de 3 horas
# Numero de pàginas ocio por genero --> Boxplots
# Lectura obligatoria por genero
# Narrativa social de la lectura chicos vs chicas

# Curso
# =======================================
# Tiempo de lectura ocio por curso
# Stat personas que no leen nada por curso
# Stat personas que leen mas de 3 horas a la semana por curso
# Numero de pàginas ocio por curso --> Boxplots
# Lectura obligatoria por genero
# Narrativa social de la lectura por curso

# Itinerario academico
# =======================================
# Tiempo de lectura ocio por itinerario academico
# Stat personas que no leen nada social vs cient / tec
# Stat personas que leen mas de 3 horas a la semana social vs cient / tec
# Numero de pàginas ocio por curso --> Boxplots
# Lectura obligatoria por genero
# Narrativa social de la lectura segun el itinerario academico

# Lectores vs no lectores (categorias lectoras)
# =======================================
# Narrativa social de la lectura lectores vs no lectores
# Us de xarxes socials lectors vs no lectors
# Lectura obligatoria lectores vs no lectores


plt.show()
#########################################################################################
#
# / Main Operations
#
#########################################################################################

# Per tal d’obtenir una mesura més precisa del volum anual de lectura per oci, es va construir una variable composta a partir del nombre aproximat de llibres llegits durant els últims 12 mesos i del nombre mitjà de pàgines d’aquests llibres. Per fer-ho, es va assignar a cada categoria ordinal un valor representatiu corresponent al punt mig de cada interval, i posteriorment es va calcular una estimació del total de pàgines llegides anualment.