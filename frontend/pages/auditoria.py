from pdf2image import convert_from_bytes
import streamlit as st
import pandas as pd
import requests
import os

from src import (
    procces_image_rode,
    procces_pdf2image_rode
)

st.set_page_config(
    page_title="Auditoría",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="auto"
)

st.title("Auditoría 🔍")
st.error(":warning: **¡Atención!** Esta pagina esta en desarrollo y puede no funcionar correctamente.")

models = st.multiselect(
    "Selecciona los modelos a utilizar",
    ["TilDe", "RoDe", "CuDe", "DuDe"],
    ["RoDe"]
)

filters = st.multiselect(
    "Selecciona los filtros a utilizar",
    ["Hoja de Control", "Hoja en Blanco"],
    ["Hoja de Control"]
)
    
show_image = st.checkbox("Mostrar Imagenes", value=False)

uploaded_file = st.file_uploader("Subir Imagenes", type=["jpg", "jpeg", "png", "tif", "tiff"], accept_multiple_files=True)
uploaded_pdf = st.file_uploader("Subir Archivos PDF", type=["pdf"], accept_multiple_files=True)

def process_images(upload_files):
    st.write(len(upload_files))
    if len(upload_files) == 0:
        st.warning("Debes subir al menos un archivo", icon="⚠️")
        
    if not models and not filters:
        st.warning("Debes seleccionar al menos un modelo o filtro", icon="⚠️")

    for file in upload_files:
        image = file.read()
        
        if "TilDe" in models:
            pass
        if "RoDe" in models:
            data, response = procces_image_rode(image, file.name)
            st.write(data)
            st.write(response)
        if "CuDe" in models:
            pass
        if "DuDe" in models:
            pass

def process_pdfs(upload_files):
    pass

if st.button("Procesar", help="Procesar las imagenes y archivos PDF subidos", use_container_width=True):
    if uploaded_file:
        process_images(uploaded_file)
    if uploaded_pdf:
        process_pdfs(uploaded_pdf)