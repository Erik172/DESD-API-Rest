from concurrent.futures import ThreadPoolExecutor, as_completed
from components import display_multi_metrics
from datetime import datetime
import streamlit as st
import requests

st.set_page_config(
    page_title="Auditoría",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="auto"
)

st.title("Auditoría 🔍")

result_id = st.text_input("Identificador para guardar los resultados", placeholder=f"Identificador para guardar los resultados (Optional)")

models = st.multiselect(
    "Selecciona los modelos a utilizar",
    ["Inclinacion", "Rotacion", "Corte_informacion"],
    ["Rotacion"]
)

uploaded_file = st.file_uploader("Subir Archivos", type=["jpg", "jpeg", "png", "tif", "tiff", "pdf"], accept_multiple_files=True)

def process_single_file(file, models, result_id):
    url = 'http://localhost:5000/v1/desd'
    files = {'file': file}
    response = requests.post(url, files=files, data={'models': models, 'result_id': result_id})
    create_csv = requests.get(f"http://localhost:5000/v1/export/{result_id}")
    csv_url = f"http://localhost:5000{create_csv.json()['url']}"
    return response.json(), csv_url

def process_files(upload_files):
    global models
    global result_id

    if not result_id:
        result_id = f'auditoria_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}'

    models = [model.lower() for model in models]

    if len(upload_files) == 0:
        st.warning("Debes subir al menos un archivo", icon="⚠️")
        return

    progress_bar = st.progress(0, text=f"Procesando archivos {0}/{len(upload_files)}")

    st.success(f"Los resultados se guardarán con el identificador: **{result_id}**")
    st.info(f"Total de archivos a procesar: **{len(upload_files)}**")
    st.info(f"Modelos seleccionados: **{', '.join(models)}**")

    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_file = {executor.submit(process_single_file, file, models, result_id): file for file in upload_files}
        for i, future in enumerate(as_completed(future_to_file)):
            file = future_to_file[future]
            try:
                data, csv_url = future.result()
                results.append((data, csv_url))
                progress_bar.progress((i + 1) / len(upload_files), f"Procesando archivos {i + 1}/{len(upload_files)}")
            except Exception as exc:
                st.error(f"{file.name} generated an exception: {exc}")

    for data, csv_url in results:
        if len(upload_files) < 3:
            display_multi_metrics(data)
        download.markdown(f"Descargar resultados: [CSV]({csv_url})")

    progress_bar.progress(100, "Procesamiento de archivos completado")
    st.toast("Procesamiento de archivos completado", icon="🎈")

if st.button("Procesar", help="Procesar las imágenes y archivos PDF subidos", use_container_width=True):
    if uploaded_file:
        with st.sidebar:
            st.caption(result_id)
            download = st.empty()
        process_files(uploaded_file)