# DESD API Rest

## Descripción

`DESD API Rest` es una API RESTful desarrollada con Flask que proporciona servicios para la gestión de usuarios, modelos de IA, resultados y procesamiento de documentos.

## Requisitos

- Docker
- Docker Compose

## Instalación

1. Clona el repositorio:

    ```sh
    git clone <URL_DEL_REPOSITORIO>
    cd DESD-API-Rest
    ```

2. Crea un archivo [.env](http://_vscodecontentref_/0) en el directorio raíz del proyecto con las siguientes variables de entorno:

    ```env
    FLASK_SECRET_KEY="your_flask_secret_key"
    JWT_SECRET_KEY="your_jwt_secret_key"
    MONGO_URI="mongodb://username:password@mongo:27017"
    SQLALCHEMY_DATABASE_URI="postgresql://username:password@db:5432/desd_db"
    ADMIN_EMAIL="admin@example.com"
    ADMIN_PASSWORD="admin_password"
    DEBUG=False
    ```

3. Construye y levanta los contenedores:

    ```sh
    docker-compose up --build -d
    ```

4. Verifica que todos los contenedores estén corriendo correctamente:

    ```sh
    docker-compose ps
    ```

5. Abre tu navegador web y navega a `http://localhost:8080` para acceder a la aplicación.

## Endpoints

![DESD UML](docs/pictures/DESD.drawio.png)

### Autenticación

- **POST /api/v1/auth/login**: Inicia sesión y obtiene un token de acceso.

    ```json
    {
      "email": "admin@example.com",
      "password": "admin_password"
    }
    ```

    Auth sequence diagram:

    ![Auth Sequence diagram](docs/pictures/auth-sequence-diagram.png)

### Usuarios

- **GET /api/v1/users**: Obtiene todos los usuarios (requiere acceso de administrador).
- **GET /api/v1/users/<user_id>**: Obtiene un usuario específico (requiere acceso de administrador o ser el propio usuario).
- **POST /api/v1/users**: Crea un nuevo usuario.
- **PUT /api/v1/users/<user_id>**: Actualiza un usuario existente (requiere acceso de administrador o ser el propio usuario).
- **DELETE /api/v1/users/<user_id>**: Elimina un usuario (requiere acceso de administrador).

### Modelos de IA

- **GET /api/v1/models**: Obtiene todos los modelos de IA.
- **GET /api/v1/models/<model_id>**: Obtiene un modelo de IA específico.
- **POST /api/v1/models**: Crea un nuevo modelo de IA.

### Resultados

- **GET /api/v1/results**: Obtiene todos los resultados.
- **GET /api/v1/results/<result_id>**: Obtiene un resultado específico.
- **DELETE /api/v1/results/<result_id>**: Elimina un resultado.

### Exportar Resultados

- **GET /api/v1/results/<collection_name>/export**: Exporta una colección de MongoDB a un archivo CSV.

### Procesamiento de Documentos

- **POST /api/v1/desd**: Procesa documentos utilizando modelos de IA.

    ```json
    {
      "result_id": "test_result",
      "models": "inclinacion,rotacion,corte informacion",
      "files": [<archivo1>, <archivo2>, ...]
    }
    ```

    DESD sequence diagram:

    ![DESD Sequence diagram](docs/pictures/desd-sequence-diagram.png)

## Comandos útiles

- **Construir y levantar contenedores**: `docker-compose up --build -d`
- **Detener contenedores**: `docker-compose down`
- **Verificar el estado de los contenedores**: `docker-compose ps`
- **Ver los registros de los contenedores**: `docker-compose logs -f`