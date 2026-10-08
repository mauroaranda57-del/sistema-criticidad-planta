#!/usr/bin/env bash
# Levanta el sistema completo con una sola instruccion.
#
#   bash run.sh
#
# Requiere un archivo .env completo (ver .env.example).

set -e

if [ ! -f .env ]; then
  echo "ERROR: falta el archivo .env. Copia .env.example a .env y completa las claves."
  exit 1
fi

if [ ! -d .venv ]; then
  echo "Creando entorno virtual..."
  python -m venv .venv
fi

echo "Activando entorno e instalando dependencias..."
if [ -f .venv/bin/activate ]; then
  source .venv/bin/activate
else
  source .venv/Scripts/activate
fi

pip install -q -r requirements.txt

echo ""
echo "Levantando la API en http://127.0.0.1:8000"
echo "Documentacion interactiva: http://127.0.0.1:8000/docs"
echo ""

uvicorn app.main:app --host 0.0.0.0 --port 8000