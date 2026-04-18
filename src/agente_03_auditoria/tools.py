# Tools para o Agente de Auditoria
# - qdrant: busca em base de conhecimento
# - score_quality: pontua qualidade dos requisitos

from src.memory.qdrant_client import get_qdrant_client


def qdrant_search(query: str, limit: int = 5) -> list[dict]:
    """Busca em base de conhecimento vetorial."""
    # TODO: implementar busca vetorial
    client = get_qdrant_client()
    raise NotImplementedError


def score_quality(requirements: dict, tasks: dict) -> dict:
    """Pontua qualidade dos requisitos."""
    # TODO: implementar lógica de scoring
    raise NotImplementedError
