import re

def parse_result_yolov8(result) -> dict:
    """
    Parsea el resultado de YOLOv8 y lo convierte en un diccionario.
    Args:
        result: Objeto que contiene el resultado de YOLOv8.
    Returns:
        dict: Un diccionario con los nombres de las clases y sus respectivas confianzas.
              El diccionario tiene la estructura:
              {
                  'data': [
                      {
                          'name': str,        # Nombre de la clase
                          'confidence': float # Confianza en porcentaje
                      },
                      ...
                  ]
    """
    verbose = result.verbose().split(',')
    result_dict = {'data': []}
    
    for i in verbose:
        try:
            class_name, confidence = re.split(r'(\d+\.\d+)', i.strip())[:2]
            
            class_name_mapping = {
                'rotated ': 'rotado',
                'no_rotated ': 'no_rotado',
                'tilted ': 'inclinado',
                'no tilted ': 'no_inclinado',
                'cut ': 'con_corte_de_información',
                'no_cut ': 'sin_corte_de_información'
            }
            
            class_name = class_name_mapping.get(class_name, class_name)
            confidence = float(confidence) * 100
            
            result_dict['data'].append({
                'name': class_name,
                'confidence': confidence
            })
        except:
            pass

    return result_dict