from PIL import Image
import pytesseract

def hoja_control(image):
    image = Image.open(image)
    text = pytesseract.image_to_string(image)
    return "hoja de control" in text[:44].lower()