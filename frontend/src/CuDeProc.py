from .process_files import ImageProccesing
from datetime import datetime
import random

def procces_image_cude(image, name, version="v1", data_file: dict = {}):
    response = ImageProccesing("cude").process_file(image, version, data_file)

    # cambiar nombres a español
    response['data'][0]['name'] = "con corte de informacion" if response['data'][0]['name'] == "cut" else "normal"
    response['data'][1]['name'] = "con corte de informacion" if response['data'][1]['name'] == "cut" else "normal"

    data = {
            "archivo": [name],
            "predicción": [response['data'][0]['name']],
            "confianza": [response['data'][0]['confidence'] * 100],
            "tiempo(s)": [response['time']],
            "fecha": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    }

    return data, response

def procces_pdf2image_cude(image, name, version="v1", i=0, data_file: dict = {}):
    name_file_rand = f'temp/{"".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10))}.jpg'
    image.save(name_file_rand)
    image_path = name_file_rand

    with open(image_path, "rb") as image:
        response = ImageProccesing("cude").process_file(image, version, data_file)

    #change names to spanish
    response['data'][0]['name'] = "con corte de informacion" if response['data'][0]['name'] == "cut" else "normal"

    data = {
        "archivo": [name],
        "pagina": [f'Page {i + 1}'], # "Page 1
        "predicción": [response['data'][0]['name']],
        "confianza": [response['data'][0]['confidence'] * 100],
        "tiempo(s)": [response['time']],
        "fecha": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    }

    return data, response, image_path, name_file_rand
