@echo off
REM Levanta el sistema completo con una sola instruccion en Windows.
REM
REM   run.bat
REM
REM Requiere un archivo .env completo (ver .env.example).

if not exist .env (
    echo ERROR: falta el archivo .env. Copia .env.example a .env y completa las claves.
    exit /b 1
)

if not exist .venv (
    echo Creando entorno virtual...
    py -3 -m venv .venv
)

echo Activando entorno e instalando dependencias...
call .venv\Scripts\activate
pip install -q -r requirements.txt

echo.
echo Levantando la API en http://127.0.0.1:8000
echo Documentacion interactiva: http://127.0.0.1:8000/docs
echo.

uvicorn app.main:app --host 0.0.0.0 --port 8000