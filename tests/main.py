from locust import HttpUser, task, between
import os

class APIUser(HttpUser):
    wait_time = between(1, 5)  # Tiempo de espera entre tareas (1 a 5 segundos)

    @task
    def upload_files(self):
        url = '/v2/desd'  # Reemplaza con tu endpoint
        result_id = self.client.get('/v2/generate_id').json().get('random_id')  # Genera un ID aleatorio
        models = ['inclinacion', 'rotacion']  # Modelos a usar

        # Datos a enviar
        data = {
            'result_id': result_id,
            'models': ','.join(models)
        }

        # Archivos a enviar
        file_paths = [
            r'D:\Documentos\DESD-API-Rest\tests\AliciaEnElPaisDeLasMaravillas.pdf',
        ]

        files = []
        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            files.append(('files', (file_name, open(file_path, 'rb'))))

        # Realiza la solicitud POST
        with self.client.post(url, data=data, files=files, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 400:
                response.failure(f"Error: {response.json().get('message')}")
            else:
                response.failure(f"Error inesperado: {response.status_code} - {response.text}")

        # Cierra los archivos
        for _, (file_name, file) in files:
            file.close()

    @task
    def check_status(self):
        url = '/v2/status'

        # Realiza la solicitud GET
        with self.client.get(url, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Error inesperado: {response.status_code} - {response.text}")

    @task
    def get_models(self):
        url = '/v2/desd'

        # Realiza la solicitud GET
        with self.client.get(url, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Error inesperado: {response.status_code} - {response.text}")
