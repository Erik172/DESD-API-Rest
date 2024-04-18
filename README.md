# DESD (Detection Errors Scanned Documents) API Rest

**Menu:**
- [DESD (Detection Errors Scanned Documents) API Rest](#desd-detection-errors-scanned-documents-api-rest)
  - [Description](#description)
  - [Installation](#installation)
    - [Ejecución con Docker](#ejecución-con-docker)
    - [Ejecución Local](#ejecución-local)
      - [Instalación de Dependencias](#instalación-de-dependencias)
      - [Inicio del Servidor Backend](#inicio-del-servidor-backend)
      - [Inicio del Servior Frontend](#inicio-del-servior-frontend)
  - [Usage](#usage)
  - [Endpoints](#endpoints)
  - [Models](#models)
    - [TilDeV1 (Tilted Detection Version 1)](#tildev1-tilted-detection-version-1)

## Description
## Installation
### Ejecución con Docker

Para ejecutar la aplicación utilizando Docker, necesitarás utilizar Docker Compose, una herramienta que permite definir y manejar aplicaciones multi-contenedor con Docker.

Sigue los siguientes pasos para iniciar la aplicación:

1. **Levantar los servicios con Docker Compose**

    Ejecuta el siguiente comando para iniciar todos los servicios definidos en el archivo `docker-compose.yml`:

    ```bash
    docker-compose up -d
    ```

    La opción `-d` hace que los servicios se ejecuten en segundo plano.

2. **Acceso a los servicios**

    Tras ejecutar el comando anterior, se expondrán dos puertos:

    - **Puerto 5000**: Aquí se encuentra la API de la aplicación.
    - **Puerto 80**: Aquí se encuentra la interfaz web de la aplicación.

    Puedes acceder a estos servicios a través de un navegador web o cualquier cliente HTTP, utilizando `localhost` seguido del número de puerto correspondiente (por ejemplo, `http://localhost:5000` para la API).

### Ejecución Local

Para ejecutar este proyecto localmente, necesitarás instalar algunas dependencias tanto para el backend como para el frontend.

#### Instalación de Dependencias

Primero, instala las dependencias del backend con el siguiente comando:

```bash
pip install -r backend/requirements.txt
```

Si también deseas ejecutar el frontend, instala sus dependencias con:
    
```bash
pip install -r frontend/requirements.txt
```

#### Inicio del Servidor Backend

Para iniciar el servidor backend, ejecuta el siguiente comando:

```bash
python backend/app.py
```

El servidor se iniciará en la dirección `http://localhost:5000/`.

#### Inicio del Servior Frontend

Para iniciar el frontend, ejecuta el siguiente comando:

```bash
streamlit run frontend/main.py --server.port=80 --server.address=0.0.0.0
```

Esto iniciará la interfaz web en el puerto 80, la cual hará peticiones a la API del backend en el puerto 5000. Para acceder a la interfaz, abre tu navegador y dirígete a `http://localhost`.

## Usage
## Endpoints
## Models
table of all models
| Model | Description | Accuracy | Precision |
| --- | --- | --- | --- |
| [TilDeV1](#TilDeV1) | Modelo de detección de inclinación en documentos escaneados. | 0.97 | 0.98 |

### TilDeV1 (Tilted Detection Version 1)
Modelo de detección de inclinación de documentos escaneados. Entrenado mediante fine-tuning de un modelo pre-entrenado de detección de objetos YOLOv8n y con un dataset de 319 imagenes de documentos escaneados con y sin inclinación.

**Accuracy**: 0.97 \
**Precision**: 0.98

![TilDeV1 Confusion Matrix](docs/images/TilDeV1(ConfusionMatrix).png)
