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

dataframe = pd.DataFrame(columns=["file", "Prediction", "Confidence", "Time"])

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

            if version == "v2":
                prediction, confidence, time = st.columns(3)
                prediction.metric("Prediction", response["top"])
                confidence.metric("Confidence", response["confidence"])
                time.metric("Time", round(response["time"], 3), "seconds")
                dataframe = dataframe.append({"file": file.name, "Prediction": response["top"], "Confidence": response["confidence"], "Time": round(response["time"], 3)}, ignore_index=True)

            
            if show_image:
                st.image(image, use_column_width=True, caption="Uploaded Image")
            print(response)
            st.divider()

        if dataframe.shape[0] > 0:
            with st.container():
                st.dataframe(dataframe)

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


            if version == "v2":
                prediction, confidence, time = st.columns(3)
                prediction.metric("Prediction", response["top"])
                confidence.metric("Confidence", response["confidence"])
                time.metric("Time", round(response["time"], 3), "seconds")
                dataframe = dataframe.append({"file": f'Page {i + 1}', "Prediction": response["top"], "Confidence": response["confidence"], "Time": round(response["time"], 3)}, ignore_index=True)


            if show_image:
                st.image(image_path, use_column_width=True, caption="Uploaded Image", output_format="JPEG")
            
            try:
                os.remove(f"temp/temp_{i}.jpg")
            except PermissionError:
                print("PermissionError: Unable to delete the temporary file.")

            st.divider()

        if dataframe.shape[0] > 0:
            with st.container():
                st.dataframe(dataframe)

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
    st.title("TilDe (Tilted Detection) 📐")
    st.markdown("This page allows you to detect tilted documents using the TilDe model.")
    st.markdown("**V1:** __YOLOv8n-CLS (Ultralytics)__ - This version of the model offers better performance, but it has a more complex architecture and slower inference time.")
    st.markdown("**V2:** __MobileNetV2 (Roboflow)__ - This version of the model is smaller, resulting in faster inference time, but it may have lower performance compared to V1.")

    version = st.selectbox(
        "Select the version of the model to use",
        ("v1", "v2")
    )
    
    show_image = st.checkbox("Show uploaded image(s)", value=True)
    uploaded_file = st.file_uploader("Upload image(s)", type=["jpg", "jpeg", "png", "tif", "tiff"], accept_multiple_files=True)
    uploaded_pdf = st.file_uploader("Upload PDF file", type=["pdf"], accept_multiple_files=False)
    
    if uploaded_file:
        process_uploaded_images(uploaded_file, show_image, version)
    if uploaded_pdf:
        process_pdf_file(uploaded_pdf, show_image, version)

if __name__ == "__main__":
    main()
