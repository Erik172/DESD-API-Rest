import requests

def main():
    # URL del servidor Flask
    url = 'http://127.0.0.1:5000/desd'

    # Ruta de la imagen que deseas enviar
    image_path = 'imagen.jpg'
    model_names = ['rode', 'tilde']

    # Carga la imagen desde el sistema de archivos
    with open(image_path, 'rb') as file:
        # Configura los datos de la solicitud
        files = {'file': file}

        # Envía la solicitud POST al servidor Flask
        response = requests.post(url, files=files, data={'model_names': model_names})

        # Imprime la respuesta del servidor
        print(response.json())

if __name__ == '__main__':
    main()
