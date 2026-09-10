import streamlit as st
import pandas as pd
from io import StringIO
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Auditor Carrefour")

st.title("Auditor Carrefour")

datos = st.text_area(
    "Pega aquí la tabla copiada desde Excel",
    height=300
)

def limpiar_modelo(modelo):
    return str(modelo).split(".")[0].upper()

def buscar_producto(modelo, url):

    try:

        pagina = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=20
        )

        html = pagina.text.upper()

        modelo_base = limpiar_modelo(modelo)

        posicion = "No encontrado"

        if modelo_base in html:
            posicion = "Encontrado"

        vendedor = "No encontrado"
        carrefour = "No"

        if "VENDIDO POR CARREFOUR" in html:
            vendedor = "Carrefour"
            carrefour = "Sí"

        return posicion, vendedor, carrefour

    except Exception as e:
        return str(e), "", ""

if st.button("Procesar"):

    if not datos.strip():

        st.warning("Pega primero una tabla")

    else:

        try:

            df = pd.read_csv(
                StringIO(datos),
                sep="\t"
            )

            resultados = []

            for _, fila in df.iterrows():

                modelo = fila["ARTÍCULO"]
                url = fila["URL"]

                posicion, vendedor, carrefour = buscar_producto(
                    modelo,
                    url
                )

                resultados.append(
                    {
                        "MODELO": modelo,
                        "URL": url,
                        "POSICION": posicion,
                        "SELLER": vendedor,
                        "CARREFOUR": carrefour
                    }
                )

            resultado_df = pd.DataFrame(resultados)

            st.success("Proceso terminado")

            st.dataframe(resultado_df)

            csv = resultado_df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                "Descargar CSV",
                csv,
                "resultado.csv",
                "text/csv"
            )

        except Exception as e:

            st.error(str(e))
