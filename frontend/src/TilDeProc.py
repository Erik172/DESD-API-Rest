from .process_files import ImageProccesing
from datetime import datetime

def procces_image_tilde(file: dict) -> tuple:
    response = ImageProccesing("rode").process_file(file)

    # cambiar nombres a español
    response['data'][0]['name'] = "inclinado" if response['data'][0]['name'] == "tilted" else "no inclinado"
    response['data'][1]['name'] = "inclinado" if response['data'][1]['name'] == "tilted" else "no inclinado"

    data = {
            "archivo": [file.get('name')],
            "predicción": [response['data'][0]['name']],
            "confianza": [response['data'][0]['confidence'] * 100],
            "tiempo(s)": [response['time']],
            "fecha": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    }

    return data, response

def procces_pdf2image_tilde(file: dict) -> tuple:
    response = ImageProccesing("tilde").process_file(file)
    #change names to spanish
    response['data'][0]['name'] = "inclinado" if response['data'][0]['name'] == "tilted" else "no inclinado"

    data = {
        "archivo": [file.get('name')],
        "pagina": [file.get('page')],
        "total_paginas": [file.get('page_total')],     
        "predicción": [response['data'][0]['name']],
        "confianza": [response['data'][0]['confidence'] * 100],
        "tiempo(s)": [response['time']],
        "fecha": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    }

    return data, response
