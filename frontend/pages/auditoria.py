from pdf2image import convert_from_bytes
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import requests
import os

API_URL_BASE = "http://localhost:5000/audit"

st.set_page_config(
    page_title="Auditoría",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="auto"
)

st.title("Auditoría 🔍")
st.markdown("Esta página es para auditar las imágenes y archivos PDF. Puede subir imágenes o archivos PDF para obtener las predicciones.")
    
show_image = st.checkbox("Show uploaded image(s)", value=False)
uploaded_file = st.file_uploader("Upload image(s)", type=["jpg", "jpeg", "png", "tif", "tiff"], accept_multiple_files=True)
uploaded_pdf = st.file_uploader("Upload PDF file", type=["pdf"], accept_multiple_files=False)

placeholder = st.empty()
dataframe = pd.DataFrame(columns=["file", "Tilted", "Tilted Confidence", "Rotated", "Rotated Confidence"])
with st.container():
    placeholder.dataframe(dataframe)    

@st.cache_data()
def convert_df(dataframe):
    return dataframe.to_csv(index=False).encode("utf-8")

def process_uploaded_images(uploaded_file, show_image):
    global dataframe
    with st.spinner("Processing..."):
        for file in uploaded_file:
            image = file.read()
            response = requests.post(API_URL_BASE, files={"image": image})
            response = response.json()

            st.caption(file.name)  

            tilted, tilded_confidence = st.columns(2)
            tilted.metric("Tilted", response['tilde']['name'])
            tilded_confidence.metric("Confidence", round(response['tilde']['confidence'], 4))

            rotated, rotated_confidence = st.columns(2)
            rotated.metric("Rotated", response['rode']['name'])
            rotated_confidence.metric("Confidence", round(response['rode']['confidence'], 4))

            dataframe = dataframe.append({"file": file.name, "Tilted": response['tilde']['name'], "Tilted Confidence": round(response['tilde']['confidence'], 4), "Rotated": response['rode']['name'], "Rotated Confidence": round(response['rode']['confidence'], 4)}, ignore_index=True)

            if response['tilde']['name'] == "tilted":
                st.error(f':warning: La imagen "**{file.name}**" está inclinada. Por favor, enderece la imagen.')

            if response['rode']['name'] == "rotated":
                st.error(f':warning: La imagen "**{file.name}**" está rotada. Por favor, gire la imagen.')


            if show_image:
                st.image(image, use_column_width=True, caption="Uploaded Image")
            st.divider()
            placeholder.dataframe(dataframe)

        if dataframe.shape[0] > 0:
            with st.container():
                st.dataframe(dataframe)

                csv = convert_df(dataframe)

                st.download_button(
                    label="Download data as CSV",
                    data=csv,
                    file_name=f'{file.name}_results.csv', # 'tilde_results.csv'
                    mime='text/csv',
                )

def process_pdf_file(uploaded_file, show_image):
    global dataframe
    with st.spinner("Processing..."):
        images = convert_from_bytes(uploaded_file.read())
        for i, image in enumerate(images):
            image.save(f"temp/temp_{i}.jpg")
            image_path = f"temp/temp_{i}.jpg"
            image = open(f"temp/temp_{i}.jpg", "rb")

            response = requests.post(API_URL_BASE, files={"image": image})
            response = response.json()

            st.caption(f"Page {i + 1}")

            tilted, tilded_confidence = st.columns(2)
            tilted.metric("Tilted", response['tilde']['name'])
            tilded_confidence.metric("Confidence", round(response['tilde']['confidence'], 4))

            rotated, rotated_confidence = st.columns(2)
            rotated.metric("Rotated", response['rode']['name'])
            rotated_confidence.metric("Confidence", round(response['rode']['confidence'], 4))

            dataframe = dataframe.append({"file": f'Page {i + 1}', "Tilted": response['tilde']['name'], "Tilted Confidence": round(response['tilde']['confidence'], 4), "Rotated": response['rode']['name'], "Rotated Confidence": round(response['rode']['confidence'], 4)}, ignore_index=True)

            if response['tilde']['name'] == "tilted":
                st.error(f':warning: La Página **{i + 1}** en el PDF está inclinada. Por favor, enderece la imagen.')

            if response['rode']['name'] == "rotated":
                st.error(f':warning: La Página **{i + 1}** en el PDF está rotada. Por favor, gire la imagen.')


            if show_image:
                st.image(image_path, use_column_width=True, caption="Uploaded Image", output_format="JPEG")
            
            try:
                os.remove(f"temp/temp_{i}.jpg")
            except PermissionError:
                print("PermissionError: Unable to delete the temporary file.")

            st.divider()
            placeholder.dataframe(dataframe)

        if dataframe.shape[0] > 0:
            
            with st.container():
                st.dataframe(dataframe)

                csv = convert_df(dataframe)

                st.download_button(
                    label="Download data as CSV",
                    data=csv,
                    file_name=f'{uploaded_file.name}_results.csv', # 'tilde_results.csv'
                    mime='text/csv',
                )


def main():
    if uploaded_file:
        process_uploaded_images(uploaded_file, show_image)
    if uploaded_pdf:
        process_pdf_file(uploaded_pdf, show_image)

if __name__ == "__main__":
    main()