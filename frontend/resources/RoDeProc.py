from .process_files import ImageProccesing
from datetime import datetime
import streamlit as st
import random

def procces_image_rode(image, name, version="v1", data_file: dict = {}):
    """
    Process the given image using the RoDe algorithm.

    Args:
        image: The image to be processed.
        name: The name of the image file.
        version: The version of the RoDe algorithm to use (default is "v1").
        data_file: Additional data file to be used during processing (default is an empty dictionary).

    Returns:
        A tuple containing the processed data and the response from the image processing.

    Example usage:
        data, response = procces_image_rode(image, "example.jpg", version="v2", data_file={"param": "value"})
    """
    response = ImageProccesing("rode").process_file(image, version, data_file)

    # cambiar nombres a español
    response['data'][0]['name'] = "rotado" if response['data'][0]['name'] == "rotated" else "no rotado"
    response['data'][1]['name'] = "rotado" if response['data'][1]['name'] == "rotated" else "no rotado"

    data = {
            "archivo": [name],
            "predicción": [response['data'][0]['name']],
            "confianza": [response['data'][0]['confidence'] * 100],
            "tiempo(s)": [response['time']],
            "fecha": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    }

    return data, response

def procces_pdf2image_rode(image, name, version="v1", i=0, data_file: dict = {}):
    name_file_rand = f'temp/{"".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10))}.jpg'
    image.save(name_file_rand)
    image_path = name_file_rand

    with open(image_path, "rb") as image:
        response = ImageProccesing("rode").process_file(image, version)

    #change names to spanish
    response['data'][0]['name'] = "rotado" if response['data'][0]['name'] == "rotated" else "no rotado"

    st.caption(f"Pagina {i + 1} del PDF {name}")

    data = {
        "archivo": [name],
        "pagina": [f'Page {i + 1}'], # "Page 1
        "predicción": [response['data'][0]['name']],
        "confianza": [response['data'][0]['confidence'] * 100],
        "tiempo(s)": [response['time']],
        "fecha": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    }

    return data, response, image_path, name_file_rand
