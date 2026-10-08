"""Configuracion central del sistema: variables de entorno y validacion."""

import os

from dotenv import load_dotenv

load_dotenv()

# --- Proveedor de LLM y embeddings ---
GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")
MODEL_NAME: str = os.getenv("MODEL_NAME", "gemini-3.5-flash-lite")
EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "models/gemini-embedding-001")

# --- Base vectorial (RAG) ---
PINECONE_API_KEY: str | None = os.getenv("PINECONE_API_KEY")
INDEX_NAME: str = os.getenv("INDEX_NAME", "planta-docs")
PINECONE_NAMESPACE: str = os.getenv("PINECONE_NAMESPACE", "manuales")

# --- Estado y checkpoints ---
REDIS_HOST: str | None = os.getenv("REDIS_HOST")
REDIS_PORT: str | None = os.getenv("REDIS_PORT")
REDIS_PASSWORD: str | None = os.getenv("REDIS_PASSWORD")

# --- Observabilidad ---
LANGSMITH_API_KEY: str | None = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_PROJECT: str = os.getenv("LANGSMITH_PROJECT", "sistema-final")

# --- Parametros del orquestador ---
MAX_PASOS: int = int(os.getenv("MAX_PASOS", "6"))
RECURSION_LIMIT: int = int(os.getenv("RECURSION_LIMIT", "15"))
COSTO_APROBACION_USD: float = float(os.getenv("COSTO_APROBACION_USD", "20000"))
TTL_JOB_SEGUNDOS: int = int(os.getenv("TTL_JOB_SEGUNDOS", str(60 * 60 * 24)))


def redis_url() -> str:
    """Arma la URL de conexion a Redis a partir de las piezas del .env."""
    return f"redis://default:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"


def validar_entorno() -> None:
    """Verifica que esten todas las variables obligatorias.

    No se ejecuta al importar el modulo: la llama explicitamente la aplicacion
    al arrancar. De esta forma importar `config` no produce efectos
    secundarios, y los tests pueden importarlo sin un .env completo.
    """
    obligatorias = (
        ("GEMINI_API_KEY", GEMINI_API_KEY),
        ("PINECONE_API_KEY", PINECONE_API_KEY),
        ("REDIS_HOST", REDIS_HOST),
        ("REDIS_PORT", REDIS_PORT),
        ("REDIS_PASSWORD", REDIS_PASSWORD),
    )
    faltantes = [nombre for nombre, valor in obligatorias if not valor]
    if faltantes:
        raise RuntimeError(
            f"Faltan variables de entorno en el archivo .env: {', '.join(faltantes)}"
        )