from components import display_multi_metrics
from datetime import datetime
from streamlit_cookies_controller import CookieController
import streamlit as st
import requests
import aiohttp
import asyncio

st.set_page_config(
    page_title="Auditoría",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="auto"
)

controller = CookieController()

st.title("Auditoría 🔍")

models = st.multiselect(
    "Selecciona los modelos a utilizar",
    ["Inclinacion", "Rotacion", "Corte_informacion"],
    ["Rotacion"]
)

uploaded_file = st.file_uploader("Subir Archivos", type=["jpg", "jpeg", "png", "tif", "tiff", "pdf"], accept_multiple_files=True)

def work_status(result_id):
    url = f"http://localhost:5000/v1/desd/status/{result_id}"
    response = requests.get(url)
    return response

def process_files(upload_files):
    global models

    models = [model.lower() for model in models]

    if len(upload_files) == 0:
        st.warning("Debes subir al menos un archivo", icon="⚠️")
        return
    
    random_id = requests.get("http://localhost:5000/v1/generate_id").json()["random_id"]
    st.success(f"Identificador para guardar los resultados: **{random_id}**")
    controller.set("desd_result_id", random_id, expires=datetime.now().replace(hour=23, minute=59, second=59))

    st.info(f"Total de archivos a procesar: **{len(upload_files)}**")
    st.info(f"Modelos seleccionados: **{', '.join(models)}**")

    url = 'http://localhost:5000/v1/desd'
    files = [('files', (file.name, file, file.type)) for file in upload_files]
    requests.post(url, files=files, data={"models": models, "result_id": str(random_id)})

    porcentaje = st.empty()
    files_process = st.empty()
    data = st.empty()
    while True:
        status = work_status(controller.get("desd_result_id"))
        if status.status_code == 200:
            status = status.json()
            if status["status"] == "in_progress":
                files_process.info(f"Procesando archivos... {status['files_processed']} de {status['total_files']} completados")
                porcentaje.progress(float(status["percentage"]) / 100.0, f'{round(status["percentage"], 1)}%')
            else:
                files_process.success("Procesamiento completado")
                porcentaje.progress(1.0, "100% completado")
                break
        elif status.status_code == 404:
            files_process.error("No se encontraron resultados previos")
            break
        else:
            files_process.error("Error al obtener los resultados")
            break

        data.write(status)


if st.button("Procesar", help="Procesar las imágenes y archivos PDF subidos", use_container_width=True):
    if uploaded_file:
        with st.sidebar:
            download = st.empty()
        process_files(uploaded_file)

if controller.get("desd_result_id"):
    st.subheader(f"Resultados previos ({controller.get('desd_result_id')})")
    porcentaje = st.empty()
    files_process = st.empty()
    data = st.empty()
    while True:
        status = work_status(controller.get("desd_result_id"))
        if status.status_code == 200:
            status = status.json()
            if status["status"] == "in_progress":
                files_process.info(f"Procesando archivos... {status['files_processed']} de {status['total_files']} completados")
                porcentaje.progress(float(status["percentage"]) / 100.0, f'{round(status["percentage"], 1)}%')
            else:
                files_process.success("Procesamiento completado")
                porcentaje.progress(1.0, "100% completado")
                break
        elif status.status_code == 404:
            files_process.error("No se encontraron resultados previos")
            break
        else:
            files_process.error("Error al obtener los resultados")
            break

        data.write(status)

    if st.button("Limpiar", help="Eliminar resultados previos", use_container_width=True):
        controller.remove("desd_result_id")
        st.rerun()