# Cliente Qdrant compartilhado entre os agentes
import json
import os

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from sentence_transformers import SentenceTransformer

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
COLLECTION_NAME = "user_storyes"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_SIZE = 384

_model = None


def _get_embedding_model() -> SentenceTransformer:
    """Retorna modelo de embeddings (singleton)."""
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def get_qdrant_client():
    """Retorna cliente Qdrant configurado"""
    return QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)


def create_collection_if_not_exists():
    """Cria coleção se não existir"""
    client = get_qdrant_client()

    collections = client.get_collections().collections
    collection_names = [c.name for c in collections]

    if COLLECTION_NAME not in collection_names:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=EMBEDDING_SIZE,
                distance=Distance.COSINE,
            ),
        )
        print(f"✅ Coleção '{COLLECTION_NAME}' criada.")
    else:
        print(f"ℹ️ Coleção '{COLLECTION_NAME}' já existe.")


def save_to_qdrant(data: dict, source: str, run_id: int) -> None:
    """Salva o resultado de um agente no Qdrant com embedding local.

    Args:
        data: Dicionário com o resultado do agente (ex: backlog JSON).
        source: Identificador da origem (ex: 'agente_01_scrum').
        run_id: ID do pipeline_run no PostgreSQL (usado como point ID).
    """
    client = get_qdrant_client()
    model = _get_embedding_model()

    create_collection_if_not_exists()

    # Gerar texto para embedding
    text = json.dumps(data, ensure_ascii=False)
    vector = model.encode(text).tolist()

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=run_id,
                vector=vector,
                payload={"source": source, "data": data, "run_id": run_id},
            )
        ],
    )
    print(f"  ✅ Embedding salvo no Qdrant (source: {source}, id: {run_id})")
