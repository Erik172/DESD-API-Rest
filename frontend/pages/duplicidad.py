from streamlit_cookies_controller import CookieController
import streamlit as st
import threading
import requests
import time

controller = CookieController()

st.logo("https://procesosyservicios.net.co/wp-content/uploads/2019/10/LETRA-GRIS.png")

st.title("DuDe (Duplicate Detection) Detección de duplicados 2️⃣")
st.caption("V2.0 - Estable, con alta precisión 📊")

uploaded_file = st.file_uploader("Subir Archivos", type=["jpg", "jpeg", "png", "tif", "tiff", "pdf"], accept_multiple_files=True)

def work_status(result_id):
    url = f"http://localhost:5000/v2/status/{result_id}"
    response = requests.get(url)
    return response

def process_uploaded_images(uploaded_file):
    random_id = requests.get("http://localhost:5000/v2/generate_id").json()["random_id"]
    controller.set("dude_result_id", random_id)
    st.success(f"Identificador de resultados: **{random_id}**", icon="📄")
    st.info(f"Procesando **{len(uploaded_file)}** archivos... 🔄")
        
    url = 'http://localhost:5000/v2/dude'
    files = [('files', (file.name, file, file.type)) for file in uploaded_file]
    threading.Thread(target=requests.post, args=(url,), kwargs={"files": files, "data": {"result_id": str(random_id)}}).start()
    st.caption("Procesando archivos...")
    time.sleep(3)


if st.button("Buscar Duplicados", help="Presiona el botón para procesar los archivos cargados", use_container_width=True):
    if uploaded_file:
        process_uploaded_images(uploaded_file)

if controller.get("dude_result_id"):
    st.subheader(f"Estado de ({controller.get('dude_result_id')})")
    porcentaje = st.empty()
    files_process = st.empty()
    data = st.empty()
    error_count = 0
    download_partial = st.empty()
    while True:
        status = work_status(controller.get("dude_result_id"))
        if status.status_code == 200:
            status = status.json()
            if status["status"] == "in_progress":
                porcentaje.progress(float(status["percentage"]) / 100.0, f'{round(status["percentage"], 1)}% - {status["files_processed"]} / {status["total_files"]} completados')
                files_process.info(f"Procesando archivos...   {status['files_processed']} de {status['total_files']} completados")
            else:
                download_partial.empty()
                porcentaje.progress(1.0, "100% completado")
                files_process.success("Procesamiento completado")
                break
        elif status.status_code == 404:
            controller.remove("dude_result_id")
            break

        else:
            files_process.error("Error al obtener los resultados")
            st.rerun()
            break

    try:
        st.info(f'Total de archivos procesados: {status["total_files"]}')

        if st.download_button(
            label="Descargar resultados completos en CSV",
            data=requests.get(f"http://localhost:5000/v2/export/{controller.get('dude_result_id')}").content,
            file_name=f"{controller.get('dude_result_id')}.csv",
            mime="text/csv",
            help="Descargar los resultados completos en formato CSV",
            use_container_width=True
        ):
            st.toast("Descargando resultados...", icon="📥")
            requests.delete(f"http://localhost:5000/v2/export/{controller.get('dude_result_id')}")
    except:
        pass

    if st.button("Limpiar", help="Eliminar resultados previos", use_container_width=True):
        controller.remove("dude_result_id")
        st.rerun()