@echo off
REM Actualizar el repositorio
cd ruta/a/tu/repositorio
git fetch
git pull

REM Ejecutar el servidor backend en un terminal
start cmd /k cd backend
start cmd /k py app.py
if %errorlevel% neq 0 (
    start cmd /k python3 backend/app.py
)

REM Esperar unos segundos para asegurar que el servidor backend esté en funcionamiento
timeout /t 5

REM Ejecutar el servidor Streamlit en otro terminal
start cmd /k cd frontend
start cmd /k streamlit run main.py
