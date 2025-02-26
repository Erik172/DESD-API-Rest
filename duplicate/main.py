import json
import os
import shutil
from pymongo import MongoClient
from config import Config
from services import *
from datetime import datetime
from services import find_duplicate_pages

# Configuración de MongoDB
mongo_client = MongoClient(Config.MONGO_URI)
db = mongo_client.results

def process_file(task_id, folder_path):
    """Procesa el archivo usando el modelo correspondiente."""
    foldernames = [name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]
    for index, foldername in enumerate(foldernames, start=1):
        image_paths = [f'{folder_path}/{foldername}/{name}' for name in os.listdir(os.path.join(folder_path, foldername)) if name.endswith('.jpg')]
        image_paths = sorted(image_paths, key=lambda x: int(x.split('_')[-1].split('.')[0]))
        
        database_service.update_result_status(task_id, total_files_processed=index, current_file=foldername, last_updated=datetime.now())
        
        _, report = find_duplicate_pages(image_paths)
        if report:
            report = [{'task_id': task_id, 'filename': foldername, **item} for item in report]
            
            for item in report:
                db[str(task_id)].insert_one(item)
        else:
            db[str(task_id)].insert_one({'task_id': task_id, 'filename': foldername, 'message': 'No se encontraron duplicados.'})
        
    status = database_service.get_result_status(task_id)
    if status['total_files_processed'] == status['total_files']:
        database_service.update_result_status(task_id, status='COMPLETED', last_updated=datetime.now())
        
    # Eliminar la carpeta
    for foldername in foldernames:
        shutil.rmtree(os.path.join(folder_path, foldername))
        
    shutil.rmtree(folder_path)

def callback(ch, method, properties, body):
    """Callback que se ejecuta cuando se recibe una tarea."""
    task = json.loads(body)
    folder_path = task['folder_path']
    task_id = task['task_id']
    
    database_service.update_result_status(task_id, status='RUNNING', last_updated=datetime.now())
    
    process_file(task_id, folder_path)
    ch.basic_ack(delivery_tag=method.delivery_tag)


if Config.DEBUG:
    process_file('testing', 'data/')
else:
    messaging_service = MessagingService()
    database_service = DatabaseService()
    
    messaging_service.consume(callback)