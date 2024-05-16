@echo off
REM Actualizar el repositorio
cd /d %~dp0
git fetch
git pull

REM Iniciar MongoDB
start "MongoDB" cmd /c "net start MongoDB"

REM Ejecutar el servidor backend en un terminal
start "Backend" cmd /c "cd backend && py -3 app.py"
if %errorlevel% neq 0 (
    start "Backend" cmd /c "cd backend && python3 app.py"
)

REM Esperar unos segundos para asegurar que el servidor backend esté en funcionamiento
timeout /t 5

REM Ejecutar el servidor Streamlit en otro terminal
start "Streamlit" cmd /c "cd frontend && streamlit run main.py"
