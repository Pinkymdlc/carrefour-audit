import streamlit as st
import pandas as pd

st.title("Auditor Carrefour")

texto = st.text_area(
    "Pega aquí el contenido de Excel",
    height=300
)

if st.button("Procesar"):

    lineas = [x.strip() for x in texto.splitlines() if x.strip()]

    datos = []

    for linea in lineas:

        partes = linea.split()

        if len(partes) < 2:
            continue

        modelo = partes[0]
        url = partes[1]

        datos.append({
            "MODELO": modelo,
            "URL": url,
            "POSICION": "",
            "SELLER": "",
            "CARREFOUR": ""
        })

    if datos:
        df = pd.DataFrame(datos)
        st.dataframe(df)
    else:
        st.error("No se encontraron registros")
