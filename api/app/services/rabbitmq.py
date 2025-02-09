import pika
import json
import os

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'user')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'password')
QUEUE_CUDE = 'queue_cude'
QUEUE_RODE = 'queue_rode'

def enqueue_task(task_data, queue_name):
    """Encola una tarea en la cola especificada."""
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=json.dumps(task_data),
        properties=pika.BasicProperties(delivery_mode=2)  # Hace el mensaje persistente
    )
    connection.close()