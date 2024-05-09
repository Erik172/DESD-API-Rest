import pytesseract
import numpy as np
import cv2

def hoja_control(image) -> bool:
    """
    Check if the given image contains the text "hoja de control" in the first 44 characters.

    Args:
        image: The image to be processed. It can be either a bytes object representing the image data or a string representing the file path.

    Returns:
        bool: True if the text "hoja de control" is found in the image, False otherwise.
    """
    if type(image) == bytes:
        image = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
    elif type(image) == str:
        image = cv2.imread(image, cv2.IMREAD_COLOR)

    text = pytesseract.image_to_string(image)
    return "hoja de control" in text[:44].lower()

def apply_filters(file_name, requests, response):
    if "filtros" in requests:
        filtros = requests["filtros"].split(",")
        if "Hoja de Control" in filtros:
            if hoja_control(file_name):
                if "filtros" in response:
                    response["filtros"].append("hoja de control")
                else:
                    response["filtros"] = ["hoja de control"]
    return response