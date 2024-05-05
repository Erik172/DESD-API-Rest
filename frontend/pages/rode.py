from pdf2image import convert_from_bytes
from datetime import datetime
import streamlit as st
import pandas as pd
import random
import os

from resources import (
    ImageProccesing, 
    single_model_metrics, 
    hoja_control
)


st.set_page_config(
    page_title="RoDe (Rotation Detection)",
    page_icon="🔄",
    layout="centered",
    initial_sidebar_state="auto"
)

st.title("RoDe (Rotation Detection) Detección de rotación 🔄")

version = "v1"
    
show_image = st.checkbox("Mostrar imagenes", value=False)
uploaded_file = st.file_uploader("Upload image(s)", type=["jpg", "jpeg", "png", "tif", "tiff"], accept_multiple_files=True)
uploaded_pdf = st.file_uploader("Upload PDF file", type=["pdf"], accept_multiple_files=True)

st.caption("Resultados de imagenes con problemas")
bad_placeholder = st.empty()

st.caption("Todos los resultados")
placeholder = st.empty()

alerts = st.empty()

fin_process = st.empty()

dataframe = pd.DataFrame(columns=["archivo", "predicción", "confianza", "tiempo(s)"])
bad_dataframe = pd.DataFrame(columns=["archivo", "predicción", "confianza", "tiempo(s)"])

with st.container():
    bad_placeholder.dataframe(bad_dataframe)
    placeholder.dataframe(dataframe)    

def process_uploaded_images(uploaded_file, show_image, version="v1"):
    global bad_dataframe
    global dataframe

    errors = []

    with st.spinner("Procesando..."):
        st.info(f'Procesando **{len(uploaded_file)}** imágenes.')
        st.info(f'Inicio del procesamiento: **{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}**')

        for file in uploaded_file:
            image = file.read()
            response = ImageProccesing("rode").process_file(image, version, file.name)
            filtered = hoja_control(image)

            # cambiar nombres a español
            response['data'][0]['name'] = "rotado" if response['data'][0]['name'] == "rotated" else "no rotado"
            response['data'][1]['name'] = "rotado" if response['data'][1]['name'] == "rotated" else "no rotado"

            data = {
                    "archivo": [file.name],
                    "predicción": [response['data'][0]['name']],
                    "confianza": [response['data'][0]['confidence'] * 100],
                    "tiempo(s)": [response['time']],
                    "fecha": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            }

            if filtered:
                st.toast(f'Existe una hoja de control en la imagen **{file.name}**', icon="⚠️")
                errors.append(f'Existe una hoja de control en la imagen **{file.name}**')
                data["filtros"] = ["hoja de control"]

            st.caption(file.name)   

            if version == "v1":
                single_model_metrics(response)

                dataframe = pd.concat([dataframe, pd.DataFrame(data)], ignore_index=True)

                if response['data'][0]['name'] == "rotado":
                    bad_dataframe = pd.concat([bad_dataframe, pd.DataFrame(data)], ignore_index=True)
                    st.error(f':warning: La imagen "**{file.name}**" está rotada.')

            if show_image:
                st.image(image, use_column_width=True, caption="Uploaded Image")

            if errors:
                alerts.error(f':warning: {", ".join(errors)}')

            st.divider()

            placeholder.dataframe(dataframe)
            bad_placeholder.dataframe(bad_dataframe)


def process_pdf_file(uploaded_pdf, show_image, version="v1"):
    global bad_dataframe
    global dataframe

    errors = []

    with st.spinner(f"Procesando {len(uploaded_pdf)} PDFs..."):
        st.info(f'Procesando **{len(uploaded_pdf)}** PDFs.')
        st.info(f'Inicio del procesamiento: **{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}**')

        for pdf in uploaded_pdf:
            images = convert_from_bytes(pdf.read())
            for i, image in enumerate(images):
                name_file_rand = f'temp/{"".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10))}.jpg'
                image.save(name_file_rand)
                image_path = name_file_rand
                filtered = hoja_control(image)

                with open(image_path, "rb") as image:
                    response = ImageProccesing("rode").process_file(image, version, pdf.name, i + 1, "pdf")

                #change names to spanish
                response['data'][0]['name'] = "rotado" if response['data'][0]['name'] == "rotated" else "no rotado"

                st.caption(f"Pagina {i + 1} del PDF {pdf.name}")

                data = {
                    "archivo": [pdf.name],
                    "pagina": [f'Page {i + 1}'], # "Page 1
                    "predicción": [response['data'][0]['name']],
                    "confianza": [response['data'][0]['confidence'] * 100],
                    "tiempo(s)": [response['time']],
                    "fecha": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
                }

                if filtered:
                    st.error(f':warning: Existe una hoja de control en la página **{i + 1}** del PDF **{pdf.name}**')
                    errors.append(f'Existe una hoja de control en la página **{i + 1}** del PDF **{pdf.name}**')
                    data["filtros"] = ["hoja de control"]

                if version == "v1":
                    single_model_metrics(response)
                    dataframe = pd.concat([dataframe, pd.DataFrame(data)], ignore_index=True)

                    if response['data'][0]['name'] == "rotado":
                        bad_dataframe = pd.concat([bad_dataframe, pd.DataFrame(data)], ignore_index=True)
                        st.error(f':warning: La Página **{i + 1}** en el PDF está rotada.')

                if show_image:
                    st.image(image_path, use_column_width=True, caption="Uploaded Image", output_format="JPEG")

                if errors:
                    alerts.error(f':warning: {", ".join(errors)}')
                
                try:
                    os.remove(name_file_rand)
                except PermissionError:
                    print(f"Error al eliminar el archivo {image_path}")

                st.divider()

                bad_placeholder.dataframe(bad_dataframe)
                placeholder.dataframe(dataframe)

def main():
    if uploaded_file:
        process_uploaded_images(uploaded_file, show_image, version)
        fin_process.info(f'Fin del procesamiento: **{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}**')
    if uploaded_pdf:
        process_pdf_file(uploaded_pdf, show_image, version)
        fin_process.info(f'Fin del procesamiento: **{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}**')

if __name__ == "__main__":
    main()