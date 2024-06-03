from pdf2image import convert_from_bytes
import streamlit as st
import pandas as pd
import requests
import os

st.set_page_config(
    page_title="Auditoría",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="auto"
)

st.title("Auditoría 🔍")


models = st.multiselect(
    "Selecciona los modelos a utilizar",
    ["TilDe", "RoDe", "CuDe"],
    ["RoDe"]
)

uploaded_file = st.file_uploader("Subir Archivos", type=["jpg", "jpeg", "png", "tif", "tiff", "pdf"], accept_multiple_files=True)

def process_files(upload_files):
    global models
    # cambiar todos los nombres a lowercase
    models = [model.lower() for model in models]

    if len(upload_files) == 0:
        st.warning("Debes subir al menos un archivo", icon="⚠️")

    for file in upload_files:
        url = 'http://localhost:5000/desd'
        files = {'file': file}
        response = requests.post(url, files=files, data={'model_names': models})
        st.write(response.json())

if st.button("Procesar", help="Procesar las imagenes y archivos PDF subidos", use_container_width=True):
    if uploaded_file:
        process_files(uploaded_file)