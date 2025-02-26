from skimage.metrics import structural_similarity as ssim
from PIL import Image
import numpy as np
import imagehash
import cv2

def get_image_hash(image_path: str) -> imagehash.ImageHash:
    """
    Calcula el hash perceptual (pHash) de una imagen.

    Args:
        image_path (str): La ruta del archivo de la imagen.

    Returns:
        imagehash.ImageHash: El hash perceptual de la imagen.
    """
    img = Image.open(image_path).convert('L').resize((32, 32))
    return imagehash.phash(img)

def load_image_grey(image_path: str) -> np.ndarray:
    """
    Carga una imagen en escala de grises.

    Args:
        image_path (str): La ruta del archivo de la imagen a cargar.

    Returns:
        numpy.ndarray: La imagen cargada en escala de grises.
    """
    return cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

def compare_images(image1_path: str, image2_path: str) -> float:
    """
    Compara dos imágenes y devuelve un puntaje de similitud.
    Args:
        image1_path (str): Ruta del archivo de la primera imagen.
        image2_path (str): Ruta del archivo de la segunda imagen.
    Returns:
        float: Puntaje de similitud entre las dos imágenes. Un valor de 1.0 indica que las imágenes son idénticas, 
               mientras que un valor de 0 indica que no hay similitud.
    Nota:
        - Las imágenes se convierten a escala de grises antes de la comparación.
        - Si las imágenes no tienen el mismo tamaño, la segunda imagen se redimensiona para que coincida con el tamaño de la primera.
        - Si ocurre un error al cargar las imágenes, se imprime un mensaje de error y se devuelve un puntaje de 0.
    """
    img1 = load_image_grey(image1_path)
    img2 = load_image_grey(image2_path)
    
    if img1 is None or img2 is None:
        print(f"Error loading images {image1_path} or {image2_path}")
        return 0
    
    # Asegurar tamaños iguales
    if img1.shape != img2.shape:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
        
    score, _ = ssim(img1, img2, full=True)
    return score