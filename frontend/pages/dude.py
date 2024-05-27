from datetime import datetime
import requests
import streamlit as st

st.set_page_config(
    page_title="DuDe (Duplicate Detection)",
    page_icon="2️⃣",
    layout="centered",
    initial_sidebar_state="auto"
)

st.title("DuDe (Duplicate Detection) Detección de duplicados 2️⃣")
st.warning("En construcción... 🚧")

work_id = st.text_input("Identificador de trabajo", placeholder=f"Identificador de trabajo (Opcional)")

show_image = st.checkbox("Mostrar imagenes", value=False)
uploaded_file = st.file_uploader("Upload image(s)", type=["jpg", "jpeg", "png", "tif", "tiff"], accept_multiple_files=True)


def process_uploaded_images(uploaded_file, folder_name: str = "dude", show_image: bool = False):
    if len(uploaded_file) < 2:
        st.error("Debes cargar al menos dos imágenes")
        
    else:
        st.info(f"Tiempo estimado de procesamiento: {(((len(uploaded_file) * 2.2) * 2) / 60):.2f} minutos")
        with st.spinner(f"subiendo {len(uploaded_file)} imágenes..."):
            bar_progress = st.progress(0, text="Subiendo archivos...")
            url = f"http://localhost:5000/dude/{folder_name}"
            for file in uploaded_file:
                bar_progress.progress(uploaded_file.index(file) / len(uploaded_file), f"Subiendo {uploaded_file.index(file) + 1}/{len(uploaded_file)} archivos...")     
                response = requests.post(url, files={"file": file})
                st.toast(response.json()["message"], icon="🎈")
            bar_progress.progress(100, "Subida de archivos completada 🎈")
        
        with st.spinner("Buscando duplicados..."):
            url = f"http://localhost:5000/dude/{folder_name}"
            response = requests.get(url).json()

            if response:
                st.write(response)
            else:
                st.error("No se encontraron duplicados")

        delete = requests.delete(url)
        st.toast(delete.json()["message"], icon="☁️")

        if response.get('duplicates'):
            duplicates = response.get('duplicates')
            st.warning(f":warning: {len(duplicates)} archivos con duplicados encontrados")
            for key, value in duplicates.items():
                with st.expander(f"Archivo: {key}"):
                    st.write(f'Numero de duplicados: {len(value)}')
                    for i, duplicate in enumerate(value):
                        st.write(f'{i + 1}. {duplicate}')

        else:
            st.success("No se encontraron duplicados", icon="✅")

def main():
    global work_id
    if not work_id:
        work_id = f"dude_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    if st.button("Buscar Duplicados", help="Presiona el botón para procesar los archivos cargados", use_container_width=True):
        if uploaded_file:
            process_uploaded_images(uploaded_file, work_id)

if __name__ == "__main__":
    main()