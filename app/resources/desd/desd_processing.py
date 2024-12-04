from pdf2image import convert_from_path
from PIL import Image, ImageSequence
import os

class DESDProcessing:
    def process_pdf(self, models: dict, results: dict, filename: str, file_path: str):
        """
        Procesa un archivo PDF convirtiéndolo en imágenes y aplicando modelos de predicción a cada imagen.

        Args:
            models (dict): Un diccionario donde las claves son nombres de modelos y los valores son instancias de modelos de predicción.
            results (dict): Un diccionario donde se almacenarán los resultados de las predicciones.
            filename (str): El nombre del archivo PDF que se está procesando.
            file_path (str): La ruta completa del archivo PDF que se va a procesar.

        Returns:
            None: Los resultados se almacenan en el diccionario `results` proporcionado.
        """
        images = convert_from_path(file_path, thread_count=os.cpu_count())
        
        for model_name, model in models.items():
            results[filename][model_name] = {}
            for i, image in enumerate(images):
                image.save(f'temp/{filename}_{i}.png')
                model_results = model.predict(f'temp/{filename}_{i}.png')
                results[filename][model_name][str(i)] = {
                    'prediccion': model_results['data'][0]['name'],
                    'confianza': model_results['data'][0]['confidence'],
                    'tiempo(s)': model_results['time']
                }
                self._cleanup_file(f'temp/{filename}_{i}.png')
                
    def process_tiff(self, models: dict, results: dict, filename: str, file_path: str):
        """
        Procesa un archivo TIFF utilizando modelos de predicción y guarda los resultados.

        Args:
            models (dict): Un diccionario donde las claves son nombres de modelos y los valores son instancias de modelos de predicción.
            results (dict): Un diccionario donde se almacenarán los resultados de las predicciones.
            filename (str): El nombre del archivo TIFF que se está procesando.
            file_path (str): La ruta completa del archivo TIFF que se va a procesar.

        Returns:
            None
        """
        tiff_image = Image.open(file_path)
        for model_name, model in models.items():
            results[filename][model_name] = {}
            for i, page in enumerate(ImageSequence.Iterator(tiff_image)):
                jpg_file_path = f"temp/{filename}_{i}.jpg"
                page.save(jpg_file_path, "JPEG")
                model_results = model.predict(jpg_file_path)
                results[filename][model_name][str(i)] = {
                    'prediccion': model_results['data'][0]['name'],
                    'confianza': model_results['data'][0]['confidence'],
                    'tiempo(s)': model_results['time']
                }
                self._cleanup_file(jpg_file_path)
                
    def process_image(self, models: dict, results: dict, filename: str, file_path: str):
        """
        Procesa una imagen utilizando múltiples modelos y almacena los resultados.

        Args:
            models (dict): Un diccionario donde las claves son nombres de modelos y los valores son instancias de modelos que tienen un método `predict`.
            results (dict): Un diccionario donde se almacenarán los resultados de las predicciones. La estructura esperada es results[filename][model_name].
            filename (str): El nombre del archivo de imagen que se está procesando.
            file_path (str): La ruta completa del archivo de imagen que se está procesando.

        Returns:
            None: Esta función no retorna ningún valor. Los resultados se almacenan directamente en el diccionario `results`.
        """
        for model_name, model in models.items():
            model_results = model.predict(file_path)
            results[filename][model_name] = {
                '0': {
                    'prediccion': model_results['data'][0]['name'],
                    'confianza': model_results['data'][0]['confidence'],
                    'tiempo(s)': model_results['time']
                }
            }
                
    def _cleanup_file(self, file_path: str) -> None:
        """
        Elimina el archivo especificado por la ruta.

        Args:
            file_path (str): La ruta del archivo a eliminar.

        Raises:
            Imprime un mensaje de error si no se puede eliminar el archivo.
        """
        try:
            os.remove(file_path)
        except:
            print(f"Unable to remove file: {file_path}")