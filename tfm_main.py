import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pprint import pprint
from scipy.stats import linregress
import sys

import methods as mt
import plots
import textwrap
import tfm_methods as tmt

#########################################################################################
#
# Variables
#
#########################################################################################
# Create statistics df from csv
csv_name = "forms-habits-lectura-compartit-bak-20260428.csv"

# Verbosity
verbose, plots = tmt.parse_arguments()

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
# 1. First Data Inspection
# =======================================================================================
# Import df from csv
df = pd.read_csv(csv_name)

if verbose:
    print("\n=======================================================================================\nIncome Dataframe Info\n=======================================================================================")
    print(f"Dataframe dimensions (rows, cols): {df.shape}")
    print(f"First 5 lines of the dataframe: \n{df.head()}")
    print(f"\nCheck no null values:")
    print(df.info())
    print(f"\nCheck no nulls values per column:")
    print(df.isnull().sum())

# =======================================================================================
# 2. Rename columns
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

# Ahora creamos un df más limpio solo con esas variables
df_lectura = df[
    [
        "p4_temps_lectura",
        "p5_llibres",
        "p6_pag",
        "p7_lectura_actual",
        "p10_visites_biblioteca",
        "p16_lectura_obligatoria",
    ]
].copy()

if verbose:
    print("\n=======================================================================================\nReduced Dataframe\n=======================================================================================")
    print(f"Dataframe dimensions (rows, cols): {df_lectura.shape}")
    print(f"First 5 lines of the dataframe: \n{df_lectura.head()}")

# =======================================================================================
# 3. Composed variables books * pages --> pages / year
# =======================================================================================
# Recode P5 to mean number of books
map_llibres = {
    "0 llibres o còmics.": 0,
    "1-2 llibres o còmics.": 1.5,
    "3-5 llibres o còmics.": 4,
    "6-10 llibres o còmics.": 8,
    "11-15 llibres o còmics.": 13,
    "Més de 15 llibres o còmics": 18
}

df_lectura["p5_num"] = df_lectura["p5_llibres"].map(map_llibres)

# Recode P6 to mean number of pages
map_pagines = {
    "1-99 pàgines.": 50,
    "100-299 pàgines.": 200,
    "300-599 pàgines.": 450,
    "Més de 600 pàgines": 700
}

df_lectura["p6_num"] = df_lectura["p6_pag"].map(map_pagines)

# Create Composed variable p5 * p6 = total aproximado de páginas leídas al año
df_lectura["p5_6_pagines_num"] = (
    df_lectura["p5_num"] * df_lectura["p6_num"]
)
# If p5 = 0 books -> p5_6 = 0
df_lectura.loc[
    df_lectura["p5_num"] == 0,
    "p5_6_pagines_num"
] = 0

# Replace Nan for 0
df_lectura["p5_6_pagines_num"] = df_lectura["p5_6_pagines_num"].fillna(0)


# =======================================================================================
# 4. Discretize composed variable into categories
# =======================================================================================
# Categorize
bins = [-1, 0, 500, 1000, 3000, 4000, float("inf")]
labels = ["0", "1-500", "501-1000", "1001-3000", "3001-4000", ">4000"]

# df_lectura["p5_6_pagines"] = df_lectura["p5_6_pagines_num"].apply(tmt.categorize_pags)
df_lectura["p5_6_pagines"] = pd.cut(
    df_lectura["p5_6_pagines_num"],
    bins=bins,
    labels=labels
)

# Check result
if verbose:
    print("\n=======================================================================================\nComposed Variable\n=======================================================================================")
    print("Check first 20 rows:")
    print(
        df_lectura[
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

# =======================================================================================
# 5. Thematic
# =======================================================================================
# Remap thematic
map_thematic = {
    1: 3,
    2: 2,
    3: 1
}

columnes_generes = {
    "fantastica": "Marca ordenadament els 3 gèneres literaris que més llegeixes per oci. [Novel·la fantàstica.]",
    "romantica": "Marca ordenadament els 3 gèneres literaris que més llegeixes per oci. [Novel·la romàntica.]",
    "terror": "Marca ordenadament els 3 gèneres literaris que més llegeixes per oci. [Novel·la de terror.]",
    "negra": "Marca ordenadament els 3 gèneres literaris que més llegeixes per oci. [Novel·la negra.]",
    "historica": "Marca ordenadament els 3 gèneres literaris que més llegeixes per oci. [Novel·la històrica.]",
    "ciencia_ficcio": "Marca ordenadament els 3 gèneres literaris que més llegeixes per oci. [Ciència ficció.]",
    "comic": "Marca ordenadament els 3 gèneres literaris que més llegeixes per oci. [Còmic.]",
    "classics": "Marca ordenadament els 3 gèneres literaris que més llegeixes per oci. [Clàssics.]",
    "poesia": "Marca ordenadament els 3 gèneres literaris que més llegeixes per oci. [Poesia.]",
    "assaig": "Marca ordenadament els 3 gèneres literaris que més llegeixes per oci. [Assaig (Filosofia, divulgació científica, etc.)]",
    "teatre": "Marca ordenadament els 3 gèneres literaris que més llegeixes per oci. [Teatre.]"
}

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

print(resultats_df)

freq = resultats_df["puntuacio_total"]

if len(plots) > 0 and 1 in plots:
    plt.figure(1)

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
    plt.show()

# =======================================================================================
# 6. Estatistics
# =======================================================================================
# p5_6_pagines_num
# ==========================================
print(f'\n=======================================================================================\nEstatistics from p5_6_pagines_num variable:\n=======================================================================================')
print(df_lectura["p5_6_pagines_num"].describe())

# =======================================================================================
# 6. Plot descriptive histograms
# =======================================================================================
# p4_temps_lectura
# ==========================================
if len(plots) > 0 and 2 in plots:
    plt.figure(2)
    sort = [
        "0 minuts.",
        "Menys de 30 minuts a la setmana.",
        "Entre 30 minuts i 1 hora a la setmana.",
        "Entre 1 i 2 hores a la setmana.",
        "Entre 2 i 3 hores a la setmana.",
        "3 hores o més a la setmana."
    ]

    tmt.plot_descriptive_hists(
        df=df_lectura,
        var="p4_temps_lectura",
        title="Distribució del temps promig dedicat a la lectura de llibres o còmics per oci a la setmana",
        xlabel="",
        ylabel="Freqüència",
        sort=sort
    )

# p5_llibres
# ==========================================
if len(plots) > 0 and 3 in plots:
    plt.figure(3)

    tmt.plot_descriptive_hists(
        df=df_lectura,
        var="p5_llibres",
        title="Distribució nombre de llibres o còmics llegits per oci en l'últim any",
        xlabel="Nombre de llibres o còmics llegits per oci en l'últim any",
        ylabel="Freqüència"
    )

# p5_6_pagines
# ==========================================
if len(plots) > 0 and 4 in plots:
    plt.figure(4)

    tmt.plot_descriptive_hists(
        df=df_lectura,
        var="p5_6_pagines",
        title="Distribució nombre de pàgines estimades llegides aquest any (llibre o còmic) per oci",
        xlabel="Pàgines estimades llegides anualment",
        ylabel="Freqüència"
    )

# p7_lectura_actual
# ==========================================
if 5 in plots: 
    plt.figure(5)
    tmt.plot_descriptive_hists(
        df=df_lectura,
        var="p7_lectura_actual",
        title="Distribució alumnes que estan llegint actualment un llibre o còmic per oci",
        xlabel="",
        ylabel="Freqüència"
    )

# p16_lectura_obligatoria
# ==========================================
if len(plots) > 0 and 6 in plots:
    plt.figure(6)
    sort = [
        "No en llegeixo cap.",
        "En llegeixo poques o molt poques.",
        "En llegeixo aproximadament la meitat.",
        "Les llegeixo gairebé totes.",
    "Les llegeixo totes."
    ]

    tmt.plot_descriptive_hists(
        df=df_lectura,
        var="p16_lectura_obligatoria",
        title="Distribució alumnes que llegeixen les lectures obligatòries de l’escola",
        xlabel="",
        ylabel="Freqüència",
        sort=sort
    )

# p10_visites_biblioteca
# ==========================================
if len(plots) > 0 and 7 in plots:
    plt.figure(7)
    sort = [
        "0 cops.",
        "1-2 cops.",
        "3-5 cops.",
        "6-10 cops.",
        "Més de 10 cops."
    ]

    tmt.plot_descriptive_hists(
        df=df_lectura,
        var="p10_visites_biblioteca",
        title="Distribució nombre de visites a la biblioteca per llegir o agafar llibres o còmics en préstec en l'últim any per oci",
        xlabel="",
        ylabel="Freqüència",
        sort=sort
    )


# ==========================================
# Crear histograma y capturar datos
if len(plots) > 0 and 8 in plots:
    plt.figure(8)
    counts, bins, patches = plt.hist(df_lectura["p5_6_pagines_num"], bins=12)

    plt.title("Histograma del nombre de pàgines estimades llegides anualment (llibre o còmic) per oci")
    plt.xlabel("Pàgines estimades llegides anualment")
    plt.ylabel("Freqüència")

    # Añadir valores encima de cada barra
    for count, patch in zip(counts, patches):
    plt.text(
        patch.get_x() + patch.get_width() / 2,
        count,
        int(count),
        ha='center',
        va='bottom'
    )

plt.show()

#########################################################################################
#
# / Main Operations
#
#########################################################################################

# Per tal d’obtenir una mesura més precisa del volum anual de lectura per oci, es va construir una variable composta a partir del nombre aproximat de llibres llegits durant els últims 12 mesos i del nombre mitjà de pàgines d’aquests llibres. Per fer-ho, es va assignar a cada categoria ordinal un valor representatiu corresponent al punt mig de cada interval, i posteriorment es va calcular una estimació del total de pàgines llegides anualment.