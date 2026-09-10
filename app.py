import streamlit as st
import pandas as pd
import re

st.title("Auditor Carrefour")

texto = st.text_area(
    "Pega aquí el contenido de Excel",
    height=300
)

if st.button("Procesar"):

    lineas = texto.splitlines()

    datos = []

    for linea in lineas:

        partes = linea.split(" ", 1)

        if len(partes) < 2:
            continue

        modelo = partes[0].strip()
        url = partes[1].strip()

datos.append({
    "MODELO": modelo,
    "URL": url,
    "POSICION": "",
    "SELLER": "",
    "CARREFOUR": ""
})

    df = pd.DataFrame(datos)

    st.dataframe(df)
