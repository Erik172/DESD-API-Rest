from datetime import datetime
from database import get_database
import re

db = get_database()

def parse_result_yolov8(result) -> dict:
    """
    Parses the result of the YOLOv8 model and returns a dictionary containing the parsed data.

    Args:
        result: The result object obtained from the YOLOv8 model.

    Returns:
        A dictionary containing the parsed data. The dictionary has the following structure:
        {
            'data': [
                {
                    'name': <class_name>,
                    'confidence': <confidence>
                },
                ...
            ]
        }
        where <class_name> is the name of the detected object class and <confidence> is the confidence score.

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

#TODO: Mejorar funcion y crear tests
def save_results(results: dict, resultado_id: str) -> bool:
    """
    Save the results of a prediction process to a database.

    Args:
        results (dict): A dictionary containing the prediction results.
        resultado_id (str): The ID of the result.

    Returns:
        bool: True if the results are successfully saved, False otherwise.
    """
    try:
        for filename in results:
            for model_name in results[filename]:
                for i in results[filename][model_name]:
                    data = {
                        'archivo': filename,
                        'pagina': int(i) + 1,
                        'modelo': model_name,
                        'prediccion': results[filename][model_name][i]['prediccion'],
                        'confianza': results[filename][model_name][i]['confianza'],
                        'tiempo(s)': results[filename][model_name][i]['tiempo(s)'],
                        'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    db[resultado_id].insert_one(data)
                    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

    return True