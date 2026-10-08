"""Capa RAG: recuperacion sobre los manuales de planta indexados en Pinecone."""

from functools import lru_cache

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from app import config


@lru_cache(maxsize=1)
def obtener_vectorstore() -> PineconeVectorStore:
    """Conecta con el indice de Pinecone que contiene los manuales de planta.

    Se cachea con `lru_cache` para no reconstruir el cliente en cada consulta:
    la conexion y el modelo de embeddings se instancian una sola vez por proceso.
    """
    embeddings = GoogleGenerativeAIEmbeddings(
        model=config.EMBEDDING_MODEL,
        google_api_key=config.GEMINI_API_KEY,
    )
    return PineconeVectorStore(
        index_name=config.INDEX_NAME,
        embedding=embeddings,
        namespace=config.PINECONE_NAMESPACE,
    )


async def buscar_en_manuales(consulta: str, k: int = 3) -> list[dict[str, str]]:
    """Recupera los fragmentos de manual mas relevantes para una consulta.

    Devuelve una lista de diccionarios con el contenido y su fuente, de modo
    que la respuesta del agente pueda citar de que documento salio cada dato
    (trazabilidad de proveniencia).
    """
    vectorstore = obtener_vectorstore()
    documentos = await vectorstore.asimilarity_search(consulta, k=k)
    return [
        {
            "contenido": doc.page_content,
            "fuente": doc.metadata.get("source", "desconocida"),
        }
        for doc in documentos
    ]