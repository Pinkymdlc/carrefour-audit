import streamlit as st
import pandas as pd
import re

st.title("Auditor Carrefour")

texto = st.text_area(
    "Pega aquí el contenido de Excel",
    height=300
)

if st.button("Procesar"):

    resultados = []

    lineas = texto.splitlines()

    for linea in lineas:

        st.write(linea)

        if "http" not in linea:
            continue

        resultados.append({
            "LINEA": linea
        })

    if len(resultados) > 0:
        st.dataframe(pd.DataFrame(resultados))
