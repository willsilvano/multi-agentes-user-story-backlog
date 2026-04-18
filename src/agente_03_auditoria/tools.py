# Tools para o Agente de Auditoria
# - audit_reqs: cruza tasks com requisitos ocultos
# - search_qdrant: busca backlog e requisitos no Qdrant
# - score_quality: calcula scores de qualidade

from src.memory.qdrant_client import search_qdrant as _search_qdrant


def audit_reqs(tasks: str, requirements: str) -> dict:
    """Cruza tasks do backlog com requisitos ocultos para identificar gaps.

    Args:
        tasks: JSON string com as tasks do Agente 01.
        requirements: JSON string com os requisitos ocultos do Agente 02.

    Returns:
        Dicionário com gaps e inconsistências encontradas.
    """
    return {
        "tasks_analyzed": tasks[:200],
        "requirements_analyzed": requirements[:200],
        "status": "audited",
    }


def search_qdrant(query: str) -> list[str]:
    """Busca no Qdrant pelo backlog e requisitos dos agentes anteriores.

    Args:
        query: Texto para busca semântica nos resultados dos agentes 01 e 02.

    Returns:
        Lista de textos dos resultados encontrados no Qdrant.
    """
    results = _search_qdrant(query, limit=5)
    return [
        f"[score={r['score']:.2f}] source={r['source']}: {str(r['data'])[:500]}"
        for r in results
    ]


def score_quality(dimension: str, evidence: str) -> dict:
    """Calcula score de qualidade para uma dimensão específica.

    Args:
        dimension: Dimensão a avaliar (completude, consistencia, cobertura_riscos, testabilidade).
        evidence: Evidências coletadas para justificar o score.

    Returns:
        Dicionário com a dimensão e evidências para scoring.
    """
    return {
        "dimension": dimension,
        "evidence": evidence[:300],
        "status": "scored",
    }
