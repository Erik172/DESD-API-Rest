from pdf2image import convert_from_bytes
import streamlit as st
import requests
import os


API_URL = "http://localhost:5000/black-documents-detector"

st.set_page_config(
    page_title="Black Document Detector",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="auto",
)

def process_uploaded_images(uploaded_file, show_image):
    """
    Process the uploaded images and display the results.

    Args:
        uploaded_file (list): List of uploaded image files.
        show_image (bool): Flag indicating whether to show the uploaded image.

    Returns:
        None
    """
    metrics = list()
    with st.spinner("Processing..."):
        for file in uploaded_file:
            image = file.read()
            response = requests.post(API_URL, files={"image": image})
            response = response.json()

            st.caption(file.name)

            prediction, confidence, time = st.columns(3)        
            prediction.metric("Prediction", response["top"])
            confidence.metric("Confidence", response["confidence"])
            time.metric("Time", round(response["time"], 3), "seconds")

            metrics.append(response['top'])
            
            if show_image:
                st.image(image, use_column_width=True, caption="Uploaded Image")

def process_pdf_file(pdf_file, show_image):
    """
    Process the uploaded PDF file and display the results.

    Args:
        pdf_file (file): Uploaded PDF file.
        show_image (bool): Flag indicating whether to show the image from the PDF.

    Returns:
        None
    """
    st.caption(pdf_file.name)
    pdf = pdf_file.read()
    images = convert_from_bytes(pdf)
    with st.spinner("Processing..."):
        for i, image in enumerate(images):
            st.subheader(f"Page {i + 1}")
            image = image.convert("RGB")
            image.save(f"temp_{i}.jpg", "JPEG")
            image_path = f"temp_{i}.jpg"
            response = requests.post(API_URL, files={"image": open(image_path, "rb")})
            response = response.json()

            prediction, confidence, time = st.columns(3)
            prediction.metric("Prediction", response["top"])
            confidence.metric("Confidence", response["confidence"])
            time.metric("Time", round(response["time"], 3), "seconds")

            if show_image:
                st.image(image_path, use_column_width=True, caption=pdf_file.name, output_format="JPEG")

            os.remove(image_path)

st.title('Black Document Detector 📄')
# upload image or select folder with images
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "webp", "bmp", "tiff", "gif"], accept_multiple_files=True)
pdf_file = st.file_uploader("Choose a PDF file...", type=["pdf"], accept_multiple_files=False)
show_image = st.checkbox("Show image", value=False)

if uploaded_file:
    process_uploaded_images(uploaded_file, show_image)

if pdf_file:
    process_pdf_file(pdf_file, show_image)
