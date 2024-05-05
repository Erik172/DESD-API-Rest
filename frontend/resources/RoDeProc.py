from .process_files import ImageProccesing
from datetime import datetime
import streamlit as st
import random

def procces_image_rode(image, name, version="v1"):
    response = ImageProccesing("rode").process_file(image, version)

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

def procces_pdf2image_rode(image, name, version="v1", i=0):
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
