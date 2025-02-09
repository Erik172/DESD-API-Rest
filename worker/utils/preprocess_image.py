import numpy as np
import cv2

def preprocess_image(image_path: str, width: int = 640, height: int = 640) -> np.ndarray:
    """
    Preprocesa una imagen para su uso en un modelo de aprendizaje automático.

    Args:
        image_path (str): Ruta al archivo de imagen.
        width (int, opcional): Ancho al que se redimensionará la imagen. Por defecto es 640.
        height (int, opcional): Altura a la que se redimensionará la imagen. Por defecto es 640.

    Returns:
        np.ndarray: Imagen preprocesada en formato de arreglo numpy.
    """
    img = cv2.imread(image_path)
    img = cv2.resize(img, (width, height))  # Ajusta según el modelo
    img = img / 255.0  # Normalizar
    img = img.transpose(2, 0, 1)  # (H, W, C) → (C, H, W)
    img = np.expand_dims(img, axis=0).astype(np.float32)  # Agregar batch
    return img
