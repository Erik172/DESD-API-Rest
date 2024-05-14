from datetime import datetime
import requests
import streamlit as st

st.set_page_config(
    page_title="DuDe (Duplicate Detection)",
    page_icon="2️⃣",
    layout="centered",
    initial_sidebar_state="auto"
)

st.warning("En Desarrollo ⚠️")
st.title("DuDe (Duplicate Detection) Detección de duplicados 2️⃣")
    
show_image = st.checkbox("Mostrar imagenes", value=False)
uploaded_file = st.file_uploader("Upload image(s)", type=["jpg", "jpeg", "png", "tif", "tiff"], accept_multiple_files=True)


def process_uploaded_images(uploaded_file, show_image):
    if len(uploaded_file) < 2:
        st.error("Debes cargar al menos dos imágenes")
        
    else:
        with st.spinner(f"subiendo {len(uploaded_file)} imágenes..."):
            bar_progress = st.progress(0, text="Subiendo...")
            url = "http://localhost:5000/dude/v1/dude"
            for file in uploaded_file:
                bar_progress.progress(uploaded_file.index(file) / len(uploaded_file), f"Subiendo {uploaded_file.index(file) + 1}/{len(uploaded_file)}")
                response = requests.post(url, files={"file": file})
                st.toast(response.json()["message"], icon="🎈")
            bar_progress.progress(100, "Subiendo completado")
        
        with st.spinner("Buscando duplicados..."):
            url = "http://localhost:5000/dude/v1/dude"
            response = requests.get(url).json()

            if response:
                st.write(response)
            else:
                st.error("No se encontraron duplicados")

        delete = requests.delete(url)
        st.toast(delete.json()["message"], icon="☁️")

        if response.get('duplicates'):
            duplicates = response.get('duplicates')
            st.warning(f":warning: {len(duplicates)} duplicados encontrados")
            for key, value in duplicates.items():
                st.write(f"Archivo: {key}")
                for file in value:
                    st.write(f"Duplicado: {file}")

        else:
            st.success("No se encontraron duplicados", icon="✅")

def main():
    if st.button("Buscar Duplicados", help="Presiona el botón para procesar los archivos cargados", use_container_width=True):
        if uploaded_file:
            process_uploaded_images(uploaded_file, show_image)

if __name__ == "__main__":
    main()