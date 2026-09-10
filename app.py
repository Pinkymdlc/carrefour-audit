import streamlit as st
import pandas as pd
from io import StringIO

st.title("Auditor Carrefour")

st.write(
    "Copia las columnas desde Excel y pégalas aquí."
)

datos = st.text_area(
    "Pegar tabla",
    height=300
)

if st.button("Cargar datos"):

    if datos:

        df = pd.read_csv(
            StringIO(datos),
            sep="\t"
        )

        st.success("Datos cargados")

        st.dataframe(df)

    else:
        st.warning("Pega primero una tabla")
