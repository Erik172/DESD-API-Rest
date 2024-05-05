from pdf2image import convert_from_bytes
from datetime import datetime
import dask.dataframe as dd
import streamlit as st
import pandas as pd
import os

from resources import (
    single_model_metrics, 
    hoja_control,
    procces_image_rode,
    procces_pdf2image_rode
)

st.set_page_config(
    page_title="RoDe (Rotation Detection)",
    page_icon="🔄",
    layout="centered",
    initial_sidebar_state="auto"
)

st.title("RoDe (Rotation Detection) Detección de rotación 🔄")

version = "v1"

filters = st.multiselect(
    "Selecciona los filtros a utilizar",
    ["Hoja de Control", "Hoja en Blanco"],
    ["Hoja de Control"]
)
    
show_image = st.checkbox("Mostrar imagenes", value=False)
uploaded_file = st.file_uploader("Upload image(s)", type=["jpg", "jpeg", "png", "tif", "tiff"], accept_multiple_files=True)
uploaded_pdf = st.file_uploader("Upload PDF file", type=["pdf"], accept_multiple_files=True)

st.caption("Resultados de imagenes con problemas")
bad_placeholder = st.empty()

st.caption("Todos los resultados")
placeholder = st.empty()

alerts = st.empty()

dataframe = dd.from_pandas(pd.DataFrame(columns=["archivo", "predicción", "confianza", "tiempo(s)"]), npartitions=1)
bad_dataframe = dd.from_pandas(pd.DataFrame(columns=["archivo", "predicción", "confianza", "tiempo(s)"]), npartitions=1)

def process_uploaded_images(uploaded_file, show_image, version="v1"):
    global bad_dataframe
    global dataframe

    errors = []

    with st.spinner("Procesando..."):
        st.info(f'Procesando **{len(uploaded_file)}** imágenes.')
        st.info(f'Inicio del procesamiento: **{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}**')
        inicio_time = datetime.now()
        fin_process = st.empty()

        for file in uploaded_file:
            image = file.read()
            data, response = procces_image_rode(image, file.name, version)

            if "Hoja de Control" in filters:
                filtered = hoja_control(image)

                if filtered:
                    st.toast(f'Existe una hoja de control en la imagen **{file.name}**', icon="⚠️")
                    errors.append(f'Existe una hoja de control en la imagen **{file.name}**')
                    data["filtros"] = ["hoja de control"]

            st.caption(file.name)   

            if version == "v1":
                single_model_metrics(response)

                dataframe = dd.concat([dataframe, dd.from_pandas(pd.DataFrame(data), npartitions=1)], axis=0)

                if response['data'][0]['name'] == "rotado":
                    bad_dataframe = dd.concat([bad_dataframe, dd.from_pandas(pd.DataFrame(data), npartitions=1)], axis=0)
                    st.error(f':warning: La imagen "**{file.name}**" está rotada.')

            if show_image:
                st.image(image, use_column_width=True, caption="Uploaded Image")

            if errors:
                alerts.error(f':warning: {", ".join(errors)}')

            st.divider()

            placeholder.dataframe(dataframe.compute())
            bad_placeholder.dataframe(bad_dataframe.compute())

        fin_process.info(f'Fin del procesamiento: **{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}**, tiempo total (Segundos): **{round((datetime.now() - inicio_time).total_seconds(), 2)}**')


def process_pdf_file(uploaded_pdf, show_image, version="v1"):
    global bad_dataframe
    global dataframe

    errors = []

    with st.spinner(f"Procesando {len(uploaded_pdf)} PDFs..."):
        st.info(f'Procesando **{len(uploaded_pdf)}** PDFs.')
        st.info(f'Inicio del procesamiento: **{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}**')
        inicio_time = datetime.now()
        fin_process = st.empty()

        for pdf in uploaded_pdf:
            images = convert_from_bytes(pdf.read())
            for i, image in enumerate(images):
                data, response, image_path, name_file_rand = procces_pdf2image_rode(image, pdf.name, version, i)
                
                if "Hoja de Control" in filters:
                    filtered = hoja_control(image_path)
                    if filtered:
                        st.error(f':warning: Existe una hoja de control en la página **{i + 1}** del PDF **{pdf.name}**')
                        errors.append(f'Existe una hoja de control en la página **{i + 1}** del PDF **{pdf.name}**')
                        data["filtros"] = ["hoja de control"]

                if version == "v1":
                    single_model_metrics(response)
                    dataframe = dd.concat([dataframe, dd.from_pandas(pd.DataFrame(data), npartitions=1)], axis=0)

                    if response['data'][0]['name'] == "rotado":
                        bad_dataframe = dd.concat([bad_dataframe, dd.from_pandas(pd.DataFrame(data), npartitions=1)], axis=0)
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

                placeholder.dataframe(dataframe.compute())
                bad_placeholder.dataframe(bad_dataframe.compute())

        fin_process.info(f'Fin del procesamiento: **{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}**, tiempo total: **{(datetime.now() - inicio_time).total_seconds()}** Segundos')

def main():
    if uploaded_file:
        process_uploaded_images(uploaded_file, show_image, version)
    if uploaded_pdf:
        process_pdf_file(uploaded_pdf, show_image, version)

if __name__ == "__main__":
    main()