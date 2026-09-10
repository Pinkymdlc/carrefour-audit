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

        if "http" not in linea:
            continue

        modelo = re.search(
            r"([A-Z0-9]+(?:\.[A-Z0-9]+)?)",
            linea
        )

        url = re.search(
            r"https?://[^\s]+",
            linea
        )

        if modelo and url:

            resultados.append({
                "MODELO": modelo.group(1),
                "URL": url.group(0),
                "POSICION": "Pendiente",
                "SELLER": "Pendiente",
                "CARREFOUR": "Pendiente"
            })

    if len(resultados) == 0:

        st.error(
            "No se han encontrado modelos y URLs."
        )

    else:

        df = pd.DataFrame(resultados)

        st.success(
            f"{len(df)} referencias encontradas"
        )

        st.dataframe(df)

        csv = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "Descargar CSV",
            csv,
            "resultado.csv",
            "text/csv"
        )
