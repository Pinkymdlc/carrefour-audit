import streamlit as st
import pandas as pd
 
st.title("Auditor Carrefour")
 
archivo = st.file_uploader(
"Sube el Excel",
type=["xlsx"]
)
 
if archivo:
df = pd.read_excel(archivo)
 
st.write("Datos cargados")
 
st.dataframe(df)
 
if st.button("Procesar"):
df["POSICION"] = ""
df["SELLER"] = ""
df["CARREFOUR"] = ""
 
st.dataframe(df)
