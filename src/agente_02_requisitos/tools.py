# Tools para o Agente de Requisitos
# - exa: busca externa
# - find_edges: identifica dependências
# - qdrant: busca em base de conhecimento

from src.memory.qdrant_client import get_qdrant_client


def exa_search(query: str) -> list[dict]:
    """Busca informações externas usando Exa."""
    # TODO: implementar integração com Exa
    raise NotImplementedError


def find_edges(tasks: list[dict]) -> list[dict]:
    """Identifica dependências entre requisitos."""
    # TODO: implementar lógica de dependências
    raise NotImplementedError


def qdrant_search(query: str, limit: int = 5) -> list[dict]:
    """Busca em base de conhecimento vetorial."""
    # TODO: implementar busca vetorial
    client = get_qdrant_client()
    raise NotImplementedError
