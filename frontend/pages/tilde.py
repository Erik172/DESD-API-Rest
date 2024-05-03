from pdf2image import convert_from_bytes
from datetime import datetime
import streamlit as st
import pandas as pd
import os

from process_files import ImageProccesing
from display_metrics import single_model_metrics

st.set_page_config(
    page_title="TilDe (Tilted Detection)",
    page_icon="📐",
    layout="centered",
    initial_sidebar_state="auto"
)

st.title("TilDe (Tilted Detection) Detección de inclinación 📐")

version = "v1"

show_image = st.checkbox("Mostar imagen previa", value=False)
uploaded_file = st.file_uploader("Subir Imagenes", type=["jpg", "jpeg", "png", "tif", "tiff"], accept_multiple_files=True)
uploaded_pdf = st.file_uploader("Subir Archivos PDF", type=["pdf"], accept_multiple_files=True)

st.caption("Resultados de imagenes con problemas")
bad_placeholder = st.empty()

st.caption("Todos los resultados")
placeholder = st.empty()

bad_dataframe = pd.DataFrame(columns=["archivo", "predicción", "confianza", "tiempo(s)"])
dataframe = pd.DataFrame(columns=["archivo", "predicción", "confianza", "tiempo(s)"])

with st.container():
    bad_placeholder.dataframe(bad_dataframe)
    placeholder.dataframe(dataframe)   

def process_uploaded_images(uploaded_file, show_image, version="v1"):
    global dataframe
    global bad_dataframe

    with st.spinner(f'Procesando {len(uploaded_file)} imagenes...'):
        st.info(f"Procesando {len(uploaded_file)} imagenes...")
        st.info(f"Proceso incio a las {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        for file in uploaded_file:
            image = file.read()
            response = ImageProccesing("tilde").process_file(image, version)

            # cambiar nombres a español
            response['data'][0]['name'] = "inclinado" if response['data'][0]['name'] == "tilted" else "no inclinado"
            response['data'][1]['name'] = "inclinado" if response['data'][1]['name'] == "tilted" else "no inclinado"

            data = {
                    "archivo": [file.name],
                    "predicción": [response['data'][0]['name']],
                    "confianza": [response['data'][0]['confidence']],
                    "tiempo(s)": [response['time']],
                    "fecha": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            }

            st.caption(file.name)   

            if version == "v1":
                single_model_metrics(response)
                dataframe = pd.concat([dataframe, pd.DataFrame(data)], ignore_index=True)

                if response['data'][0]['name'] == "inclinado":
                    bad_dataframe = pd.concat([bad_dataframe, pd.DataFrame(data)], ignore_index=True)
                    st.error(f':warning: La imagen "**{file.name}**" está inclinada.')
            
            if show_image:
                st.image(image, use_column_width=True, caption="Uploaded Image")

            st.divider()

            placeholder.dataframe(dataframe)
            bad_placeholder.dataframe(bad_dataframe)

def process_pdf_file(uploaded_file, show_image, version="v1"):
    global dataframe
    global bad_dataframe

    with st.spinner(f"Procesando {len(uploaded_file)} archivos PDF..."):
        st.info(f"Procesando {len(uploaded_file)} archivos PDF...")
        st.info(f"Proceso incio a las {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        for pdf in uploaded_file:
            images = convert_from_bytes(pdf.read())
            for i, image in enumerate(images):
                image.save(f"temp/temp_{i}.jpg")
                image_path = f"temp/temp_{i}.jpg"

                with open(f"temp/temp_{i}.jpg", "rb") as image:
                    response = ImageProccesing("tilde").process_file(image, version)

                # cambiar nombres a español
                response['data'][0]['name'] = "inclinado" if response['data'][0]['name'] == "tilted" else "no inclinado"
                response['data'][1]['name'] = "inclinado" if response['data'][1]['name'] == "tilted" else "no inclinado"

                data = {
                    "archivo": [pdf.name],
                    "pagina": [f'Página {i + 1}'],
                    "predicción": [response['data'][0]['name']],
                    "confianza": [response['data'][0]['confidence'] * 100],
                    "tiempo(s)": [response['time']],
                    "fecha": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
                }

                st.caption(f"Página {i + 1} del PDF {pdf.name}")

                if version == "v1":
                    single_model_metrics(response)
                    dataframe = pd.concat([dataframe, pd.DataFrame(data)], ignore_index=True)

                    if response['data'][0]['name'] == "inclinado":
                        bad_dataframe = pd.concat([bad_dataframe, pd.DataFrame(data)], ignore_index=True)
                        st.error(f':warning: La **Página {i + 1}** en el PDF "**{pdf.name}**" está inclinada.')

                if show_image:
                    st.image(image_path, use_column_width=True, caption=f"Página {i + 1} del PDF {pdf.name}")
                
                try:
                    os.remove(f"temp/temp_{i}.jpg")
                except PermissionError:
                    print("PermissionError: Unable to delete the temporary file.")

                st.divider()
                bad_placeholder.dataframe(bad_dataframe)
                placeholder.dataframe(dataframe)

def main():
    if uploaded_file:
        process_uploaded_images(uploaded_file, show_image, version)
    if uploaded_pdf:
        process_pdf_file(uploaded_pdf, show_image, version)

if __name__ == "__main__":
    main()
