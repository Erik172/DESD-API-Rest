# DESD-API-Rest Worker

Este proyecto es un microservicio que procesa tareas de inferencia utilizando modelos de aprendizaje automático. El microservicio se conecta a RabbitMQ para recibir tareas, procesa imágenes y guarda los resultados en MongoDB y PostgreSQL.

## Requisitos

- Python 3.9+
- RabbitMQ
- MongoDB
- PostgreSQL

## Instalación

1. Clona el repositorio:
    ```sh
    git clone <URL_DEL_REPOSITORIO>
    cd DESD-API-Rest/worker
    ```

2. Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    ```

## Configuración

Configura las variables de entorno necesarias en el archivo [config.py](http://_vscodecontentref_/1) o establece las variables de entorno en tu sistema:

- [RABBITMQ_HOST](http://_vscodecontentref_/2): Host de RabbitMQ (por defecto: `rabbitmq`)
- [RABBITMQ_USER](http://_vscodecontentref_/3): Usuario de RabbitMQ (por defecto: `user`)
- [RABBITMQ_PASS](http://_vscodecontentref_/4): Contraseña de RabbitMQ (por defecto: `password`)
- [QUEUE_NAME](http://_vscodecontentref_/5): Nombre de la cola en RabbitMQ (por defecto: `queue_cude`)
- [MONGO_URI](http://_vscodecontentref_/6): URI de conexión a MongoDB (por defecto: `mongodb://root:example@mongodb:27017`)
- [POSTGRES_URI](http://_vscodecontentref_/7): URI de conexión a PostgreSQL (por defecto: `postgresql://user:password@postgres:5432/tasks`)
- [MODEL_ONNX_PATH](http://_vscodecontentref_/8): Ruta al modelo ONNX
- [MODEL_OPENVINO_PATH](http://_vscodecontentref_/9): Ruta al modelo OpenVINO

## Uso

Para iniciar el microservicio, ejecuta el siguiente comando:

```sh
python worker.py