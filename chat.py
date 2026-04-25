# ==============================
# 1. PRIMERA INSPECCIÓN
# ==============================

print(df.shape)          # filas, columnas
print(df.head())
print(df.info())
print(df.isnull().sum())


# ==============================
# 2. RENOMBRAR COLUMNAS (MUY RECOMENDABLE)
# ==============================

# No trabajes con nombres larguísimos de Google Forms.
# Pon nombres cortos y claros.

df = df.rename(columns={
    "Quant temps a la setmana dediques, de mitjana, a la lectura de llibres o còmics per oci? (Ja sigui en format físic o digital).": "p4_temps_lectura",
    "Quants llibres o còmics t’has llegit aproximadament en els últims 12 mesos per oci? (Ja sigui en format físic o digital)": "p5_llibres",
    "En cas que la resposta hagi estat diferent de 0 llibres o còmics, quantes pàgines, de mitjana, tenien aproximadament aquests llibres o còmics?": "p6_pag",
    "Actualment estàs llegint algun llibre o còmic per oci?": "p7_lectura_actual",
    "Quants cops aproximadament has visitat una biblioteca per llegir o agafar llibres en préstec en els últims 12 mesos per oci?": "p10_visites_biblioteca",
    "En quin grau llegeixes les lectures obligatòries de l’escola?": "p16_lectura_obligatoria",
})


# ==============================
# 3. RECODIFICAR P5 (LIBROS)
# ==============================

map_libros = {
    "0 llibres o còmics.": 0,
    "1-2 llibres o còmics.": 1.5,
    "3-5 llibres o còmics.": 4,
    "6-10 llibres o còmics.": 8,
    "11-15 llibres o còmics.": 13,
    "Més de 15 llibres o còmics": 18
}

df["p5_libros_num"] = df["p5_libros"].map(map_libros)


# ==============================
# 4. RECODIFICAR P6 (PÁGINAS)
# ==============================

map_paginas = {
    "1-99 pàgines.": 50,
    "100-299 pàgines.": 200,
    "300-599 pàgines.": 450,
    "Més de 600 pàgines": 700
}

df["p6_paginas_num"] = df["p6_paginas"].map(map_paginas)


# ==============================
# 5. CREAR VARIABLE:
# PÁGINAS TOTALES ANUALES
# ==============================

# Si libros = 0 → páginas totales = 0

df["paginas_totales_anuales"] = (
    df["p5_libros_num"] * df["p6_paginas_num"]
)

df.loc[df["p5_libros_num"] == 0, "paginas_totales_anuales"] = 0


# ==============================
# 6. COMPROBAR RESULTADO
# ==============================

print(
    df[
        [
            "p5_libros",
            "p5_libros_num",
            "p6_paginas",
            "p6_paginas_num",
            "paginas_totales_anuales"
        ]
    ].head(20)
)


# ==============================
# 7. DESCRIPTIVOS BÁSICOS
# ==============================

print(df["paginas_totales_anuales"].describe())


# ==============================
# 8. CREAR NIVELES ORDINALES (6 NIVELES)
# ==============================

def categorizar_lectura(x):
    if x == 0:
        return 1
    elif x <= 500:
        return 2
    elif x <= 1500:
        return 3
    elif x <= 3000:
        return 4
    elif x <= 6000:
        return 5
    else:
        return 6

df["nivel_volumen_lector"] = df["paginas_totales_anuales"].apply(categorizar_lectura)


# ==============================
# 9. FRECUENCIAS
# ==============================

print(
    df["nivel_volumen_lector"]
    .value_counts()
    .sort_index()
)


# ==============================
# 10. YA PUEDES HACER CORRELACIONES
# ==============================

# aquí empieza lo interesante
```
