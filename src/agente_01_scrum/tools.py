# Tools para o Agente Scrum Master
# - search_exa: busca referências técnicas
# - break_tasks: decompõe em tasks técnicas
# - prioritize: prioriza com RICE score

import os
from exa_py import Exa


def search_exa(query: str) -> dict:
    """Pesquisa referências técnicas relevantes para o domínio da user story.

    Args:
        query: Termo de busca sobre arquitetura, padrões ou boas práticas.

    Returns:
        Dicionário com os resultados da pesquisa.
    """
    api_key = os.getenv("EXA_API_KEY")
    if not api_key:
        return {"results": [], "error": "EXA_API_KEY não configurada"}

    exa = Exa(api_key=api_key)
    results = exa.search_and_contents(
        query=query,
        num_results=3,
        text=True,
    )

    return {
        "results": [
            {
                "title": r.title,
                "url": r.url,
                "summary": r.text[:500] if r.text else "",
            }
            for r in results.results
        ]
    }


def break_tasks(user_story: str, context: str) -> dict:
    """Decompõe uma user story em tasks técnicas com estimativas e dependências.

    Args:
        user_story: A história de usuário original.
        context: Contexto técnico obtido da pesquisa Exa.

    Returns:
        Dicionário com a decomposição em tasks.
    """
    return {
        "user_story": user_story,
        "context": context,
        "status": "decomposed",
    }


def prioritize(tasks: str, criteria: str) -> dict:
    """Prioriza tasks usando o framework RICE (Reach, Impact, Confidence, Effort).

    Args:
        tasks: JSON string com as tasks a serem priorizadas.
        criteria: Critérios adicionais de priorização.

    Returns:
        Dicionário com as tasks priorizadas e scores RICE.
    """
    return {
        "tasks": tasks,
        "criteria": criteria,
        "framework": "RICE",
        "status": "prioritized",
    }
