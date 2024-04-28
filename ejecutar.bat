@echo off
REM Actualizar el repositorio
cd ruta/a/tu/repositorio
git fetch
git pull

REM Ejecutar el servidor backend en un terminal
start cmd /k py backend/main.py
if %errorlevel% neq 0 (
    start cmd /k python3 backend/main.py
)

REM Esperar unos segundos para asegurar que el servidor backend esté en funcionamiento
timeout /t 5

REM Ejecutar el servidor Streamlit en otro terminal
start cmd /k streamlit run frontend/main.py
