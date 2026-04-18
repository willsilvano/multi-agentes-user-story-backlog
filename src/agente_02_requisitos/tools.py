# Tools para o Agente de Requisitos Ocultos
# - search_exa: busca artigos e referências técnicas
# - find_edge_cases: identifica casos de borda via LLM
# - search_qdrant: busca no Qdrant pelo backlog do Agente 01

import os

from exa_py import Exa
from src.memory.qdrant_client import search_qdrant as _search_qdrant


def search_exa(query: str) -> list[str]:
    """Busca artigos e referências técnicas via Exa.

    Args:
        query: Termo de busca sobre riscos, segurança ou padrões técnicos.

    Returns:
        Lista de textos resumidos dos resultados encontrados.
    """
    api_key = os.getenv("EXA_API_KEY")
    if not api_key:
        return ["EXA_API_KEY não configurada"]

    exa = Exa(api_key=api_key)
    results = exa.search_and_contents(
        query=query,
        num_results=5,
        type="neural",
        text=True,
    )

    return [r.text[:500] if r.text else r.title for r in results.results]


def find_edge_cases(story: str, context: str) -> list[str]:
    """Identifica casos de borda e cenários não cobertos pela user story.

    Args:
        story: A user story original ou reescrita.
        context: Contexto técnico do backlog (tasks, dependências).

    Returns:
        Lista de casos de borda identificados.
    """
    return [
        f"Caso de borda para: {story[:100]}",
        f"Contexto analisado: {context[:100]}",
    ]


def search_qdrant(query: str) -> list[str]:
    """Busca no Qdrant pelo backlog do Agente 01.

    Args:
        query: Texto para busca semântica no backlog existente.

    Returns:
        Lista de textos dos resultados encontrados no Qdrant.
    """
    results = _search_qdrant(query, limit=3)
    return [
        f"[score={r['score']:.2f}] source={r['source']}: {str(r['data'])[:500]}"
        for r in results
    ]
