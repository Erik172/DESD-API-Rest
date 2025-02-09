import pika
from config import Config

class MessagingService:
    def __init__(self):
        self.credentials = pika.PlainCredentials(Config.RABBITMQ_USER, Config.RABBITMQ_PASS)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=Config.RABBITMQ_HOST, credentials=self.credentials))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=Config.QUEUE_NAME, durable=True)  # Cambiado a durable=True
        self.channel.basic_qos(prefetch_count=5)
        
    def consume(self, callback):
        self.channel.basic_consume(queue=Config.QUEUE_NAME, on_message_callback=callback)
        print(f"Worker for {Config.QUEUE_NAME} is running...")
        self.channel.start_consuming()