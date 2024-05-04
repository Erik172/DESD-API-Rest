import pytesseract
import numpy as np
import cv2

def hoja_control(image) -> bool:
    if type(image) == bytes:
        image = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
    text = pytesseract.image_to_string(image)
    return "hoja de control" in text[:44].lower()