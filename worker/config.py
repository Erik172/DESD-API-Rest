import yaml
import os

class Config:
    """Configuration settings for the worker."""
    with open('/models/metadata.yaml', 'r') as file:
        metadata = yaml.safe_load(file)
    
    # RabbitMQ configuration
    RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
    RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'user')
    RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'password')
    QUEUE_NAME = os.getenv('QUEUE_NAME', 'queue_cude')

    # MongoDB configuration
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://root:example@mongodb:27017')

    # PostgreSQL configuration
    POSTGRES_URI = os.getenv('POSTGRES_URI', 'postgresql://user:password@postgres:5432/desd')

    # Model path
    MODEL_ONNX_PATH = os.getenv('MODEL_ONNX_PATH')  # Ruta al modelo ONNX
    MODEL_OPENVINO_PATH = os.getenv('MODEL_OPENVINO_PATH')  # Ruta al modelo OpenVINO