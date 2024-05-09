from pdf2image import convert_from_bytes
from datetime import datetime
import streamlit as st
import pandas as pd
import os

from components import single_model_metrics

from src import (
    procces_image_cude,
    procces_pdf2image_cude
)

st.set_page_config(
    page_title="CuDe (Cut Detection)",
    page_icon="✂️",
    layout="centered",
    initial_sidebar_state="auto"
)

st.title("CuDe (Cut Detection) Detección de cortes ✂️")

work_id = st.text_input("Identificador de trabajo", placeholder=f"Identificador de trabajo (Opcional)")
work_id_default = f"cude_{datetime.now().strftime('%Y%m%d%H%M%S')}"

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

dataframe = pd.DataFrame(columns=["archivo", "predicción", "confianza", "tiempo(s)"])
bad_dataframe = pd.DataFrame(columns=["archivo", "predicción", "confianza", "tiempo(s)"])

def process_uploaded_images(uploaded_file, show_image, version="v1"):
    global bad_dataframe
    global dataframe
    global work_id, work_id_default

    errors = []

    with st.spinner(f"Procesando {len(uploaded_file)} imágenes..."):
        if not work_id:
            work_id = work_id_default

        bar_progress = st.progress(0, text="Procesando...")

        st.info(f'Identificador de trabajo: **{work_id}**')
        st.info(f'Procesando **{len(uploaded_file)}** imágenes.')
        st.info(f'Inicio del procesamiento: **{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}**')
        inicio_time = datetime.now()
        fin_process = st.empty()
        i = 0.0
        for file in uploaded_file:
            image = file.read()
            bar_progress.progress(i / len(uploaded_file), text=f"Procesando {file.name}...")
            i += 1

            data_file = {
                "work_id": work_id,
                "archivo": file.name,
                "tipo": "image",
                "filtros": [f for f in filters]
            }

            data, response = procces_image_cude(image, file.name, version, data_file)

            if "filtros" in response:
                if "hoja de control" in response['filtros']:
                    st.error(f':warning: Existe una hoja de control en la imagen "**{file.name}**"')
                    errors.append(f'Existe una hoja de control en la imagen "**{file.name}**"')
                    data["filtros"] = ["hoja de control"]

            st.caption(file.name)   

            if version == "v1":
                single_model_metrics(response)

                dataframe = pd.concat([dataframe, pd.DataFrame(data)], axis=0, ignore_index=True)

                if response['data'][0]['name'] == "con corte de informacion" or data.get("filtros"):
                    bad_dataframe = pd.concat([bad_dataframe, pd.DataFrame(data)], axis=0, ignore_index=True)
                    st.error(f':warning: La imagen "**{file.name}**" tiene corte de información.')

            if show_image:
                st.image(image, use_column_width=True, caption="Uploaded Image")

            if errors:
                alerts.error(f':warning: {", ".join(errors)}')

            st.divider()

            placeholder.dataframe(dataframe)
            bad_placeholder.dataframe(bad_dataframe)

        bar_progress.progress(1.0, text="Fin del procesamiento")
        fin_process.info(f'Fin del procesamiento: **{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}**, tiempo total (Minutos): **{round((datetime.now() - inicio_time).total_seconds() / 60, 2)}**')


def process_pdf_file(uploaded_pdf, show_image, version="v1"):
    global work_id, work_id_default
    global bad_dataframe
    global dataframe

    errors = []

    with st.spinner(f"Procesando {len(uploaded_pdf)} PDFs..."):
        if not work_id:
            work_id = work_id_default

        count, pages_count = 0, 0
        bar_progress = st.progress(0, text="Procesando...")
        pages_progress = st.progress(0, text="Procesando las páginas...")

        st.info(f'Identificador de trabajo: **{work_id}**')
        st.info(f'Procesando **{len(uploaded_pdf)}** PDFs.')
        st.info(f'Inicio del procesamiento: **{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}**')
        inicio_time = datetime.now()
        fin_process = st.empty()

        if len(uploaded_pdf) > 3:
            st.warning(f":warning: solo se mostrarán los resultados con problemas, para ver todos los resultados puede ir a la pagina de **trabajos** y seleccionar el trabajo: **{work_id}**")

        st.divider()

        for pdf in uploaded_pdf:
            images = convert_from_bytes(pdf.read())
            bar_progress.progress(count / len(uploaded_pdf), text=f"Procesando {pdf.name}...")
            count += 1
            for i, image in enumerate(images):
                pages_progress.progress(pages_count / len(images), text=f"Procesando página {i + 1} de {pdf.name}...")
                pages_count += 1
                data_file = {
                    "work_id": work_id,
                    "archivo": pdf.name,
                    "tipo": "pdf",
                    "pagina": i + 1,
                    "filtros": [f for f in filters]
                }

                data, response, image_path, name_file_rand = procces_pdf2image_cude(image, pdf.name, version, i, data_file)
                
                if "filtros" in response:
                    if "hoja de control" in response['filtros']:
                        st.error(f':warning: Existe una hoja de control en la página **{i + 1}** del PDF "**{pdf.name}**"')
                        errors.append(f'Existe una hoja de control en la página **{i + 1}** del PDF "**{pdf.name}**"')
                        data["filtros"] = ["hoja de control"]

                if version == "v1":
                    if len(uploaded_pdf) < 3:
                        st.caption(f"Pagina {i + 1} del PDF {pdf.name}")
                        single_model_metrics(response)
                        dataframe = pd.concat([dataframe, pd.DataFrame(data)], axis=0, ignore_index=True)
                        placeholder.dataframe(dataframe)


                    if response['data'][0]['name'] == "con corte de informacion" or data.get("filtros"):
                        if len(uploaded_pdf) >= 3:
                            st.caption(f"Pagina {i + 1} del PDF {pdf.name}")
                            single_model_metrics(response)

                        bad_dataframe = pd.concat([bad_dataframe, pd.DataFrame(data)], axis=0, ignore_index=True)
                        bad_placeholder.dataframe(bad_dataframe)

                        if response['data'][0]['name'] == "con corte de informacion":
                            st.error(f':warning: La Página **{i + 1}** en del PDF {pdf.name} tiene corte de información.')

                            if show_image and len(uploaded_pdf) >= 3:
                                st.image(image_path, use_column_width=True, caption="Uploaded Image", output_format="JPEG")

                if show_image and len(uploaded_pdf) < 3:
                    st.image(image_path, use_column_width=True, caption="Uploaded Image", output_format="JPEG")

                if errors:
                    alerts.error(f':warning: {", ".join(errors)}')
                
                try:
                    os.remove(name_file_rand)
                except PermissionError:
                    print(f"Error al eliminar el archivo {image_path}")

                st.divider()

            pages_progress.progress(1.0, text="Fin del procesamiento")
            pages_count = 0

        bar_progress.progress(1.0, text="Fin del procesamiento")
        fin_process.info(f'Fin del procesamiento: **{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}**, tiempo total (Minutos): **{round((datetime.now() - inicio_time).total_seconds() / 60, 2)}**')

def main():
    if st.button("Procesar archivos", help="Presiona el botón para procesar los archivos cargados", use_container_width=True):
        if uploaded_file:
            process_uploaded_images(uploaded_file, show_image, version)
        if uploaded_pdf:
            process_pdf_file(uploaded_pdf, show_image, version)

if __name__ == "__main__":
    main()