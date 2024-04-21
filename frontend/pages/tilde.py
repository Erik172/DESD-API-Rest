from pdf2image import convert_from_bytes
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import requests
import os

API_URL_BASE = "http://localhost:5000/tilde"

st.set_page_config(
    page_title="TilDe (Tilted Detection)",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="auto"
)

st.title("TilDe (Tilted Detection) 📐")
st.markdown("This page allows you to detect tilted documents using the TilDe model.")

version = st.selectbox(
    "Select the version of the model to use",
    ("v1", "v2")
)

show_image = st.checkbox("Show uploaded image(s)", value=False)
uploaded_file = st.file_uploader("Upload image(s)", type=["jpg", "jpeg", "png", "tif", "tiff"], accept_multiple_files=True)
uploaded_pdf = st.file_uploader("Upload PDF file", type=["pdf"], accept_multiple_files=False)


placeholder = st.empty()
dataframe = pd.DataFrame(columns=["file", "Prediction", "Confidence", "Time"])
with st.container():
    placeholder.dataframe(dataframe)    

@st.cache_data()
def convert_df(dataframe):
    return dataframe.to_csv(index=False).encode("utf-8")

def process_uploaded_images(uploaded_file, show_image, version="v1"):
    global dataframe
    with st.spinner("Processing..."):
        for file in uploaded_file:
            image = file.read()
            API_URL = f"{API_URL_BASE}/{version}"
            response = requests.post(API_URL, files={"image": image})
            response = response.json()

            st.caption(file.name)   

            if version == "v1":
                st.progress(response['data'][0]['confidence'], f"{response['data'][0]['name']}, {round(response['data'][0]['confidence'], 3)}")
                st.progress(response['data'][1]['confidence'], f"{response['data'][1]['name']}, {round(response['data'][1]['confidence'], 3)}")

                prediction, confidence = st.columns(2)
                prediction.metric("Prediction", response['data'][0]['name'])
                confidence.metric("Confidence", round(response['data'][0]['confidence'], 4))
                dataframe = dataframe.append({"file": file.name, "Prediction": response['data'][0]['name'], "Confidence": round(response['data'][0]['confidence'], 4)}, ignore_index=True)

                if response['data'][0]['name'] == "tilted":
                    st.error(f':warning: La imagen "**{file.name}**" está inclinada. Por favor, enderece la imagen.')

            if version == "v2":
                pass

            
            if show_image:
                st.image(image, use_column_width=True, caption="Uploaded Image")
            print(response)
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

                # st.line_chart(dataframe["Confidence"], use_container_width=True, height=300, x=dataframe["file"].tolist())
                plt.rcParams["figure.figsize"] = (12, 5)
                fig, ax = plt.subplots()
                ax.bar(dataframe["file"], dataframe["Confidence"])
                ax.set_xlabel("File")
                ax.set_ylabel("Confidence")
                ax.set_title("Confidence of Predictions")
                ax.set_xticklabels(dataframe["file"], rotation=45)
                st.pyplot(fig)

def process_pdf_file(uploaded_file, show_image, version="v1"):
    global dataframe
    with st.spinner("Processing..."):
        images = convert_from_bytes(uploaded_file.read())
        for i, image in enumerate(images):
            image.save(f"temp/temp_{i}.jpg")
            image_path = f"temp/temp_{i}.jpg"
            image = open(f"temp/temp_{i}.jpg", "rb")
            API_URL = f"{API_URL_BASE}/{version}"
            response = requests.post(API_URL, files={"image": image})
            response = response.json()

            st.caption(f"Page {i + 1}")

            if version == "v1":
                st.progress(response['data'][0]['confidence'], f"{response['data'][0]['name']}, {round(response['data'][0]['confidence'], 3)}")
                st.progress(response['data'][1]['confidence'], f"{response['data'][1]['name']}, {round(response['data'][1]['confidence'], 3)}")

                prediction, confidence = st.columns(2)
                prediction.metric("Prediction", response['data'][0]['name'])
                confidence.metric("Confidence", round(response['data'][0]['confidence'], 4))
                dataframe = dataframe.append({"file": f'Page {i + 1}', "Prediction": response['data'][0]['name'], "Confidence": round(response['data'][0]['confidence'], 4)}, ignore_index=True)

                if response['data'][0]['name'] == "tilted":
                    st.error(f':warning: La **Página {i + 1}** del PDF está inclinada. Por favor, enderece la imagen.')


            if version == "v2":
                pass

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

                # st.line_chart(dataframe["Confidence"], use_container_width=True, height=300, x=dataframe["file"].tolist())
                plt.rcParams["figure.figsize"] = (12, 5)
                fig, ax = plt.subplots()
                ax.bar(dataframe["file"], dataframe["Confidence"])
                ax.set_xlabel("File")
                ax.set_ylabel("Confidence")
                ax.set_title("Confidence of Predictions")
                ax.set_xticklabels(dataframe["file"], rotation=45)
                # ax.grid(True)
                st.pyplot(fig)

def main():
    if uploaded_file:
        process_uploaded_images(uploaded_file, show_image, version)
    if uploaded_pdf:
        process_pdf_file(uploaded_pdf, show_image, version)

if __name__ == "__main__":
    main()
