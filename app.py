import streamlit as st
import pandas as pd
import requests

st.title("Auditor Carrefour")

texto = st.text_area(
    "Pega aquí el contenido de Excel",
    height=300
)


def buscar_producto(modelo, url):

    try:

        respuesta = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=20
        )

        html = respuesta.text.upper()

        modelo_base = modelo.split(".")[0].upper()

        if modelo_base in html:
            posicion = "Encontrado"
        else:
            posicion = "No encontrado"

        seller = ""

        if "VENDIDO POR CARREFOUR" in html:
            seller = "Carrefour"
            carrefour = "Sí"
        else:
            seller = "Marketplace"
            carrefour = "No"

        return posicion, seller, carrefour

    except Exception as e:

        return str(e), "", ""


if st.button("Procesar"):

    lineas = [x.strip() for x in texto.splitlines() if x.strip()]

    datos = []

    for linea in lineas:

        partes = linea.split()

        if len(partes) < 2:
            continue

        modelo = partes[0]
        url = partes[1]

        posicion, seller, carrefour = buscar_producto(
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

    if len(datos) > 0:

        df = pd.DataFrame(datos)

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

    else:

        st.error(
            "No se encontraron registros"
        )
