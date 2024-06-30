from streamlit_cookies_controller import CookieController
from datetime import datetime
import streamlit as st
import requests
import threading
import time

controller = CookieController()

st.set_page_config(
    page_title="DuDe (Duplicate Detection)",
    page_icon="2️⃣",
    layout="centered",
    initial_sidebar_state="auto"
)

st.logo("https://procesosyservicios.net.co/wp-content/uploads/2019/10/LETRA-GRIS.png")

# st.warning("🚧 Pagina en actualizacion a V2 🚧")
st.title("DuDe (Duplicate Detection) Detección de duplicados 2️⃣")
st.caption("V1.0 - Estable, con alta precisión 📊")

st.warning("⚠️ **Advertencia:** No cambiar, cerrar o recargar la página mientras se procesan los archivos. ⚠️")
uploaded_file = st.file_uploader("Subir Archivos", type=["jpg", "jpeg", "png", "tif", "tiff", "pdf"], accept_multiple_files=True)


def process_uploaded_images(uploaded_file):
    random_id = requests.get("http://localhost:5000/v2/generate_id").json()["random_id"]
    st.success(f"Identificador de resultados: **{random_id}**", icon="📄")
    st.info(f"Procesando **{len(uploaded_file)}** archivos... 🔄")

    with st.spinner(f"subiendo {len(uploaded_file)} imágenes..."):
        bar_progress = st.progress(0, text="Subiendo archivos...")
        url = f"http://localhost:5000/v1/dude/{random_id}"
        for file in uploaded_file:
            bar_progress.progress(uploaded_file.index(file) / len(uploaded_file), f"Subiendo {uploaded_file.index(file) + 1}/{len(uploaded_file)} archivos...")     
            response = requests.post(url, files={"file": file})
            st.toast(response.json()["message"], icon="🎈")
        bar_progress.progress(100, "Subida de archivos completada 🎈")
        
    with st.spinner("Buscando duplicados..."):
        start_time = datetime.now()
        url = f"http://localhost:5000/v1/dude/{random_id}"
        response = requests.get(url).json()
        end_time = datetime.now()
        elapsed_time = end_time - start_time
        elapsed_seconds = elapsed_time.total_seconds()
        if elapsed_seconds <= 60:
            st.success(f"Tiempo transcurrido: {elapsed_seconds} segundos")
        elif elapsed_seconds <= 3600:
            elapsed_minutes = elapsed_seconds / 60
            st.success(f"Tiempo transcurrido: {elapsed_minutes} minutos")
        else:
            elapsed_hours = elapsed_seconds / 3600
            st.success(f"Tiempo transcurrido: {elapsed_hours} horas")

    delete = requests.delete(url)
    st.toast(delete.json()["message"], icon="☁️")
    if response.get('duplicados'):
        duplicates = response.get('duplicados')
        st.warning(f":warning: {len(duplicates)} archivos con duplicados encontrados")
        for key, value in duplicates.items():
            with st.expander(f"Archivo: {key}"):
                st.write(f'Numero de duplicados: {len(value)}')
                for i, duplicate in enumerate(value):
                    st.write(f'{i + 1}. {duplicate}')

    else:
        st.success("No se encontraron duplicados", icon="✅")

    with st.sidebar:
        url = f"http://localhost:5000/v1/export/{random_id}"
        response = requests.get(url)
        if int(response.json()['total']) > 0:
            st.caption(response.json()['resultado_id'])
            st.write(f'Total de archivos duplicados: {response.json()["total"]}')
            st.markdown(f"Descargar resultados [CSV](http://localhost:5000{response.json()['url']})")

        if st.button("Limpiar resultados", help="Presiona el botón para limpiar los resultados", use_container_width=True):
            delete = requests.delete(url)
            st.toast(delete.json()["status"], icon="🧹")
            st.clear_cache()
            st.experimental_rerun()

def main():
    if st.button("Buscar Duplicados", help="Presiona el botón para procesar los archivos cargados", use_container_width=True):
        if uploaded_file:
            process_uploaded_images(uploaded_file)

if __name__ == "__main__":
    main()