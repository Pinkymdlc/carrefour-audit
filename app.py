import streamlit as st
import pandas as pd
import re
from playwright.sync_api import sync_playwright

st.set_page_config(page_title="Auditor Carrefour")

st.title("Auditor Carrefour")

texto = st.text_area(
    "Pega MODELO y URL",
    height=300
)


def limpiar_modelo(modelo):
    return modelo.split(".")[0].upper()


def analizar_url(modelo, url):

    modelo_base = limpiar_modelo(modelo)

    try:

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=True
            )

            page = browser.new_page()

            page.goto(
                url,
                timeout=60000
            )

            page.wait_for_timeout(5000)

            html = page.content().upper()

            browser.close()

            if modelo_base in html:
                posicion = "ENCONTRADO"
            else:
                posicion = "NO ENCONTRADO"

            if "VENDIDO POR CARREFOUR" in html:
                seller = "Carrefour"
                carrefour = "Sí"
            else:
                seller = "Marketplace"
                carrefour = "No"

            return posicion, seller, carrefour

    except Exception as e:

        return f"ERROR {e}", "", ""


if st.button("Procesar"):

    lineas = [
        x.strip()
        for x in texto.splitlines()
        if x.strip()
    ]

    datos = []

    for linea in lineas:

        partes = linea.split()

        if len(partes) < 2:
            continue

        modelo = partes[0]

        url = ""

        for parte in partes:

            if parte.startswith("http"):
                url = parte
                break

        if not url:
            continue

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

    if datos:

        df = pd.DataFrame(datos)

        st.dataframe(
            df,
            use_container_width=True
        )

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
