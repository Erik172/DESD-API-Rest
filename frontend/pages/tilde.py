from pdf2image import convert_from_bytes
from datetime import datetime
from io import BytesIO
import streamlit as st
import pandas as pd

from components import single_model_metrics

from src import (
    procces_image_tilde,
    procces_pdf2image_tilde,
    UploadFile2dict
)

st.set_page_config(
    page_title="TilDe (Tilted Detection)",
    page_icon="📐",
    layout="centered",
    initial_sidebar_state="auto"
)

st.title("TilDe (Tilted Detection) Detección de inclinación 📐")
st.success("Versiones estable para uso en producción", icon="🚀")

work_id_default = f"tilde_{datetime.now().strftime('%Y%m%d%H%M%S')}"
work_id = st.text_input("Identificador de trabajo", placeholder=f"Identificador de trabajo (Opcional)")

filters = st.multiselect(
    "Selecciona los filtros a utilizar",
    ["Hoja de Control", "Hoja en Blanco"],
    ["Hoja de Control"]
)

show_image = st.checkbox("Mostar imagen previa", value=False)
uploaded_file = st.file_uploader("Subir Imagenes", type=["jpg", "jpeg", "png", "tif", "tiff"], accept_multiple_files=True)
uploaded_pdf = st.file_uploader("Subir Archivos PDF", type=["pdf"], accept_multiple_files=True)

st.caption("Resultados de imagenes con problemas")
bad_placeholder = st.empty()

st.caption("Todos los resultados")
placeholder = st.empty()

alerts = st.empty()

bad_dataframe = pd.DataFrame(columns=["archivo", "predicción", "confianza", "tiempo(s)"])
dataframe = pd.DataFrame(columns=["archivo", "predicción", "confianza", "tiempo(s)"])

def process_uploaded_images(uploaded_file, show_image):
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
            file = UploadFile2dict(file)
            bar_progress.progress(i / len(uploaded_file), text=f"Procesando {file.get('name')}...")
            i += 1

            file["work_id"] = work_id
            file["filtros"] = [f for f in filters]
            file["filtros"] = ",".join(file["filtros"])

            data, response = procces_image_tilde(file)

            if "filtros" in response:
                if "hoja de control" in response['filtros']:
                    st.error(f':warning: Existe una hoja de control en la imagen **{file.get("name")}**')
                    errors.append(f'Existe una hoja de control en la imagen **{file.get("name")}**')
                    data["filtros"] = ["hoja de control"]

            st.caption(file.get("name"))   

            single_model_metrics(response)

            dataframe = pd.concat([dataframe, pd.DataFrame(data)], axis=0, ignore_index=True)

            if response['data'][0]['name'] == "rotado":
                bad_dataframe = pd.concat([bad_dataframe, pd.DataFrame(data)], axis=0, ignore_index=True)
                st.error(f':warning: La imagen "**{file.get("name")}**" está rotada.')

            if show_image:
                st.image(file.get("data"), use_column_width=True, caption=f"Uploaded Image {file.get('name')}", output_format="JPEG")

            if errors:
                alerts.error(f':warning: {", ".join(errors)}')

            st.divider()

            placeholder.dataframe(dataframe)
            bad_placeholder.dataframe(bad_dataframe)

        bar_progress.progress(1.0, text="Fin del procesamiento")
        fin_process.info(f'Fin del procesamiento: **{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}**, tiempo total (Minutos): **{round((datetime.now() - inicio_time).total_seconds() / 60, 2)}**')


def process_pdf_file(uploaded_pdf, show_image):
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

        if len(uploaded_pdf) >= 3:
            st.warning(f":warning: solo se mostrarán los resultados con problemas, para ver todos los resultados puede ir a la pagina de **trabajos** y seleccionar el trabajo: **{work_id}**")

        st.divider()

        for pdf in uploaded_pdf:
            pdf = UploadFile2dict(pdf)
            pdf['work_id'] = work_id
            pdf['filtros'] = [f for f in filters]
            pdf['filtros'] = ",".join(pdf['filtros'])

            images = convert_from_bytes(pdf.get("data").read())
            pdf['page_total'] = len(images)

            bar_progress.progress(count / len(uploaded_pdf), text=f"Procesando {pdf.get('name')}...")
            count += 1

            for i, image in enumerate(images):
                pdf['page'] = i + 1
                pages_progress.progress(pages_count / len(images), text=f"Procesando página {pdf.get('page')}/{pdf.get('page_total')} del PDF {pdf.get('name')}...")
                pages_count += 1

                with BytesIO() as output:
                    image.save(output, format="JPEG")
                    pdf['data'] = output.getvalue()

                data, response = procces_pdf2image_tilde(pdf)
                
                if "filtros" in response:
                    if "hoja de control" in response['filtros']:
                        st.error(f':warning: Existe una hoja de control en la página **{pdf.get("page")}** del PDF **{pdf.get("name")}**')
                        errors.append(f'Existe una hoja de control en la página **{pdf.get("page")}** del PDF **{pdf.get("name")}**')
                        data["filtros"] = ["hoja de control"]
                if len(uploaded_pdf) < 3:
                    st.caption(f"Pagina {pdf.get('page')}/{pdf.get('page_total')} del PDF {pdf.get('name')}")
                    single_model_metrics(response)

                    dataframe = pd.concat([dataframe, pd.DataFrame(data)], axis=0, ignore_index=True)
                    placeholder.dataframe(dataframe)


                if response['data'][0]['name'] == "rotado" or data.get("filtros"):
                    if len(uploaded_pdf) >= 3:
                        st.caption(f"Pagina {pdf.get('page')}/{pdf.get('page_total')} del PDF {pdf.get('name')}")
                        single_model_metrics(response)

                    bad_dataframe = pd.concat([bad_dataframe, pd.DataFrame(data)], axis=0, ignore_index=True)
                    bad_placeholder.dataframe(bad_dataframe)

                    if response['data'][0]['name'] == "rotado":
                        st.error(f':warning: La Página **{pdf.get("page")}** del PDF "**{pdf.get("name")}**" está rotada.')

                        if show_image and len(uploaded_pdf) >= 3:
                            st.image(pdf['data'], use_column_width=True, caption=f"Pagina {pdf.get('page')}/{pdf.get('page_total')} del PDF {pdf.get('name')}", output_format="JPEG")

                        st.divider()

                if show_image and len(uploaded_pdf) < 3:
                    st.image(pdf['data'], use_column_width=True, caption=f"Pagina {pdf.get('page')}/{pdf.get('page_total')} del PDF {pdf.get('name')}", output_format="JPEG")

                if errors:
                    alerts.error(f':warning: {", ".join(errors)}')

            pages_progress.progress(1.0, text="Fin del procesamiento")
            pages_count = 0

        bar_progress.progress(1.0, text="Fin del procesamiento")
        fin_process.info(f'Fin del procesamiento: **{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}**, tiempo total (Minutos): **{round((datetime.now() - inicio_time).total_seconds() / 60, 2)}')

def main():
    if st.button("Procesar archivos", help="Presiona el botón para procesar los archivos cargados", use_container_width=True):
        if uploaded_file:
            process_uploaded_images(uploaded_file, show_image)
        if uploaded_pdf:
            process_pdf_file(uploaded_pdf, show_image)

if __name__ == "__main__":
    main()