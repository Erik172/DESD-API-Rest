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

def process_files(upload_files):
    global models
    global result_id

    if len(models) == 0:
        st.warning("Debes seleccionar al menos un modelo", icon="⚠️")
        return

    if not result_id:
        result_id = f'auditoria_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}'
    else:
        result_id = result_id.lower().replace(" ", "_")

    models = [model.lower() for model in models]

    if len(upload_files) == 0:
        st.warning("Debes subir al menos un archivo", icon="⚠️")

    progress_bar = st.progress(0, text=f"Procesando archivos {0}/{len(upload_files)}")

    st.success(f"Los resultados se guardarán con el identificador: **{result_id}**")
    st.info(f"Total de archivos a procesar: **{len(upload_files)}**")
    st.info(f"Modelos seleccionados: **{', '.join(models)}**")

    for file in upload_files:
        progress_bar.progress(upload_files.index(file) / len(upload_files), f"Procesando archivos {upload_files.index(file) + 1}/{len(upload_files)}")
        url = 'http://localhost:5000/desd'
        files = {'file': file}
        response = requests.post(url, files=files, data={'model_names': models, 'result_id': result_id})
        # st.write(response.json())
        if len(upload_files) < 3:
            display_multi_metrics(response.json())
        #FIXME: Crear un mecanismo para borrar los csv generados
        create_csv = requests.get(f"http://localhost:5000/export/{result_id}")
        resultados_id_sidebar.caption(result_id)
        total_documentos.write(f"Total de imagenes/paginas procesadas: **{create_csv.json()['total']}**")
        download.markdown(f"Descargar resultados: [CSV](http://localhost:5000{create_csv.json()['url']})")

    progress_bar.progress(100, "Procesamiento de archivos completado")
    st.toast("Procesamiento de archivos completado", icon="🎈")

    with st.sidebar:
        if st.button("Limpiar", help="Limpiar los archivos procesados", use_container_width=True):
            delete = requests.delete(f"http://localhost:5000/export/{result_id}")
            st.toast(delete.json()["status"], icon="🗑️")
            st.caching.clear_cache()
            st.experimental_rerun()

if st.button("Procesar", help="Procesar las imágenes y archivos PDF subidos", use_container_width=True):
    if uploaded_file:
        with st.sidebar:
            resultados_id_sidebar = st.empty()
            total_documentos = st.empty()
            download = st.empty()
        process_files(uploaded_file)
