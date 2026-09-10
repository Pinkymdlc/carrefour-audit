import streamlit as st
import pandas as pd
import requests
import re

st.set_page_config(page_title="Auditor Carrefour")

st.title("Auditor Carrefour")

texto = st.text_area(
    "Pega aquí Modelo y URL",
    height=300
)

def limpiar_modelo(modelo):

    return modelo.split(".")[0].upper()


def analizar_url(modelo, url):

    try:

        respuesta = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=30
        )

        html = respuesta.text.upper()

        modelo_base = limpiar_modelo(modelo)

        if modelo_base in html:
            posicion = "Encontrado"
        else:
            posicion = "No encontrado"

        seller = "Desconocido"
        carrefour = "No"

        if "VENDIDO POR CARREFOUR" in html:
            seller = "Carrefour"
            carrefour = "Sí"

        elif "MIHOGARDIGITAL" in html:
            seller = "Mihogardigital"

        elif "DROITEK" in html:
            seller = "Droitek"

        elif "VAYAELECTRO" in html:
            seller = "VayaElectro"

        elif "YOU GET" in html:
            seller = "You Get"

        return posicion, seller, carrefour

    except Exception as e:

        return f"ERROR: {e}", "", ""


if st.button("Procesar"):

    lineas = [x.strip() for x in texto.splitlines() if x.strip()]

    datos = []

    for linea in lineas:

        partes = linea.split()

        if len(partes) < 2:
            continue

        modelo = partes[0]
        url = partes[1]

        posicion, seller, carrefour = analizar_url(
            modelo,
            url
        )

        datos.append({
            "MODELO": modelo,
            "URL": url,
            "POSICION": posicion,
            "SELLER": seller,
            "CARREFOUR": carrefour
        })

    if len(datos) == 0:

        st.error("No se encontraron registros")

    else:

        df = pd.DataFrame(datos)

        st.success(
            f"{len(df)} registros procesados"
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        csv = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="Descargar CSV",
            data=csv,
            file_name="resultado.csv",
            mime="text/csv"
        )
