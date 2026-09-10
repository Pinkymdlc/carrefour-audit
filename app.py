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

    st.write("Número de líneas:", len(lineas))

    datos = []

    for linea in lineas:

        datos.append({
            "LINEA": linea
        })

    df = pd.DataFrame(datos)

    st.dataframe(df)
