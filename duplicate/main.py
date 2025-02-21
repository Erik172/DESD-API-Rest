import json
import os
from pymongo import MongoClient
from config import Config
from services import *
from datetime import datetime

# Configuración de MongoDB
mongo_client = MongoClient(Config.MONGO_URI)
db = mongo_client.results

def process_file(task_id, folder_path):
    """Procesa el archivo usando el modelo correspondiente."""
    search_service = SearchService(folder_path, task_id)
    report = search_service.execute()

    print(f"Report: {report}", type(report))
    if report: 
        if isinstance(report, dict):
            db[str(task_id)].insert_one(report)
        else:
            for item in report:
                db[str(task_id)].insert_one(item)
        
    else:
        db[str(task_id)].insert_one({'msg': 'No se encontraron duplicados'})
    
    status = database_service.get_result_status(task_id)
    if status['total_files_processed'] == status['total_files']:
        database_service.update_result_status(task_id, status='COMPLETED', last_updated=datetime.now())
    

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