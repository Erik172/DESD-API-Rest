import json
import os
from pymongo import MongoClient
from utils.preprocess_image import preprocess_image
from config import Config
from services import *

messaging_service = MessagingService()
inference_service = InferenceService()
database_service = DatabaseService()

# Configuración de MongoDB
mongo_client = MongoClient(Config.MONGO_URI)
db = mongo_client.results

def process_file(task_id, file_path, filename, model, page):
    """Procesa el archivo usando el modelo correspondiente."""
    print(f"Processing file: {file_path} with task ID: {task_id}")
    input_data = preprocess(file_path)
    results, inference_time = inference_service.infer(input_data)
    output_data, class_name = postprocess(results)
    data = {
        'task_id': task_id,
        'filename': filename,
        'page': page,
        'confidence': float(output_data.max()),
        'class_name': class_name,
        'model': model,
        'inference_time': inference_time
    }
    
    # Guarda los resultados en MongoDB en la coleccion segun el task_id
    db[f"task_{task_id}"].insert_one(data)
    
    status = database_service.get_result_status(task_id)
    if status['total_files_processed'] == status['total_files']:
        database_service.update_result_status(task_id, status='COMPLETED')
    
    print(f"Completed processing file: {file_path} with task ID: {task_id}")

def preprocess(file_path):
    """Preprocesa el archivo antes de la inferencia."""
    print(f"Preprocessing {file_path}...")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    input_data = preprocess_image(file_path, *Config.metadata['imgsz'])
    return input_data

def postprocess(results):
    """Postprocesa los resultados de la inferencia."""
    # Implementa la lógica de postprocesamiento aquí
    results = results[0][0]
    class_name = Config.metadata['names'][results.argmax()]

    return results, class_name

def callback(ch, method, properties, body):
    """Callback que se ejecuta cuando se recibe una tarea."""
    task = json.loads(body)
    file_path = task['file_path']
    filename = task['filename']
    task_id = task['task_id']
    model = task['model_name']
    file_index = task['file_index']
    page = task['page']
    
    database_service.update_result_status(task_id, status='RUNNING', current_file=filename, total_files_processed=file_index)
    
    process_file(task_id, file_path, filename, model, page)
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Conectar a RabbitMQ y consumir tareas
messaging_service.consume(callback)