from datetime import datetime
from app.models import mongo_db
import re

db = mongo_db()

def parse_result_yolov8(result) -> dict:
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