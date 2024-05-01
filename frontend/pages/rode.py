from pdf2image import convert_from_bytes
import logging
import streamlit as st
import pandas as pd
import requests
import os

API_URL_BASE = "http://localhost:5000/rode"

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S", filename="rode.log")

st.set_page_config(
    page_title="RoDe (Rotation Detection)",
    page_icon="🔄",
    layout="centered",
    initial_sidebar_state="auto"
)

st.title("RoDe (Rotation Detection) Detección de rotación 🔄")
st.markdown("Esta página es para detectar la rotación en las imágenes y archivos PDF. Puede subir imágenes o archivos PDF para obtener las predicciones.")

version = "v1"
    
show_image = st.checkbox("Show uploaded image(s)", value=False)
uploaded_file = st.file_uploader("Upload image(s)", type=["jpg", "jpeg", "png", "tif", "tiff"], accept_multiple_files=True)
uploaded_pdf = st.file_uploader("Upload PDF file", type=["pdf"], accept_multiple_files=True)

st.caption("Todos los resultados")
placeholder = st.empty()

st.caption("Resultados de imagenes con problemas")
bad_placeholder = st.empty()

dataframe = pd.DataFrame(columns=["archivo", "predicción", "confianza"])
bad_dataframe = pd.DataFrame(columns=["archivo", "predicción", "confianza"])

with st.container():
    bad_placeholder.dataframe(bad_dataframe)
    placeholder.dataframe(dataframe)    

@st.cache_data
def convert_df(dataframe):
    return dataframe.to_csv(index=False).encode("utf-8")

def process_uploaded_images(uploaded_file, show_image, version="v1"):
    global bad_placeholder
    global bad_dataframe
    global dataframe

    with st.spinner("Procesando..."):
        for file in uploaded_file:
            image = file.read()
            API_URL = f"{API_URL_BASE}/{version}"
            response = requests.post(API_URL, files={"image": image})
            response = response.json()

            # cambiar nombres a español
            response['data'][0]['name'] = "rotado" if response['data'][0]['name'] == "rotated" else "no rotado"
            response['data'][1]['name'] = "rotado" if response['data'][1]['name'] == "rotated" else "no rotado"

            data = {
                    "archivo": [image.name],
                    "predicción": [response['data'][0]['name']],
                    "confianza": [response['data'][0]['confidence'] * 100]
            }

            st.caption(file.name)   

            if version == "v1":
                st.progress(response['data'][0]['confidence'], f"{response['data'][0]['name']}, {round(response['data'][0]['confidence'], 3)}")
                st.progress(response['data'][1]['confidence'], f"{response['data'][1]['name']}, {round(response['data'][1]['confidence'], 3)}")

                prediction, confidence = st.columns(2)
                prediction.metric("Prediction", response['data'][0]['name'])
                confidence.metric("Confidence", round(response['data'][0]['confidence'], 4))

                dataframe = pd.concat([dataframe, pd.DataFrame(data)], ignore_index=True)

                if response['data'][0]['name'] == "rotado":
                    bad_dataframe = pd.concat([bad_dataframe, pd.DataFrame(data)], ignore_index=True)
                    st.error(f':warning: La imagen "**{file.name}**" está rotada.')

            if show_image:
                st.image(image, use_column_width=True, caption="Uploaded Image")
            st.divider()
            placeholder.dataframe(dataframe)

        if dataframe.shape[0] > 0:
            with st.container():
                st.dataframe(dataframe)

def process_pdf_file(uploaded_pdf, show_image, version="v1"):
    global bad_placeholder
    global bad_dataframe
    global dataframe

    with st.spinner("Procesando..."):
        logging.info("Processing PDF file...")
        logging.info(f"Uploaded PDF: {uploaded_pdf}")
        for pdf in uploaded_pdf:
            logging.info(f"Processing PDF: {pdf.name}")
            images = convert_from_bytes(pdf.read())
            for i, image in enumerate(images):
                logging.info(f"Processing page {i + 1} of the PDF {pdf.name}")
                image.save(f"temp/temp_{i}.jpg")
                image_path = f"temp/temp_{i}.jpg"
                image = open(f"temp/temp_{i}.jpg", "rb")
                API_URL = f"{API_URL_BASE}/{version}"
                response = requests.post(API_URL, files={"image": image})
                response = response.json()

                logging.info(response.status_code)

                if response.status_code != 200:
                    st.error(f":warning: Error al procesar la página {i + 1} del PDF {pdf.name}.")
                    dataframe = pd.concat([dataframe, pd.DataFrame({"archivo": [pdf.name], "pagina": [f'Page {i + 1}'], "predicción": ["Error al procesar"], "confianza": [0]})], ignore_index=True)
                    
                    continue
                #change names to spanish
                response['data'][0]['name'] = "rotado" if response['data'][0]['name'] == "rotated" else "no rotado"

                st.caption(f"Page {i + 1} del PDF {pdf.name}")

                data = {
                    "archivo": [pdf.name],
                    "pagina": [f'Page {i + 1}'], # "Page 1
                    "predicción": [response['data'][0]['name']],
                    "confianza": [response['data'][0]['confidence'] * 100]
                }

                if version == "v1":
                    st.progress(response['data'][0]['confidence'], f"{response['data'][0]['name']}, {round(response['data'][0]['confidence'], 3)}")
                    st.progress(response['data'][1]['confidence'], f"{response['data'][1]['name']}, {round(response['data'][1]['confidence'], 3)}")

                    prediction, confidence = st.columns(2)
                    prediction.metric("Prediction", response['data'][0]['name'])
                    confidence.metric("Confidence", round(response['data'][0]['confidence'], 4))
                    dataframe = pd.concat([dataframe, pd.DataFrame(data)], ignore_index=True)

                    if response['data'][0]['name'] == "rotado":
                        bad_dataframe = pd.concat([bad_dataframe, pd.DataFrame(data)], ignore_index=True)
                        st.error(f':warning: La Página **{i + 1}** en el PDF está rotada.')


                if version == "v2":
                    pass

                if show_image:
                    st.image(image_path, use_column_width=True, caption="Uploaded Image", output_format="JPEG")
                
                try:
                    os.remove(f"temp/temp_{i}.jpg")
                except PermissionError:
                    print("PermissionError: Unable to delete the temporary file.")

                st.divider()

                bad_placeholder.dataframe(bad_dataframe)
                placeholder.dataframe(dataframe)

        if dataframe.shape[0] > 0:
                
                with st.container():
                    st.dataframe(dataframe)

def main():
    if uploaded_file:
        process_uploaded_images(uploaded_file, show_image, version)
    if uploaded_pdf:
        process_pdf_file(uploaded_pdf, show_image, version)

if __name__ == "__main__":
    main()