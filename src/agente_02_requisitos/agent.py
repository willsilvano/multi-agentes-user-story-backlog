# Agente 02 - Descoberta de Requisitos Ocultos
# Entrada: busca semântica no Qdrant (backlog do Agente 01)
# Saída: riscos, casos de borda, dependências

import json
import os
import re

from google import genai
from google.genai import types

from .prompts import SYSTEM_PROMPT
from .tools import search_exa, find_edge_cases, search_qdrant
from src.memory.db import update_pipeline_run
from src.memory.qdrant_client import save_to_qdrant


def _extract_json(text: str) -> dict:
    """Extrai JSON de uma resposta que pode conter markdown ou texto extra."""
    if not text:
        raise ValueError("Resposta vazia do modelo")

    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"```(?:json)?\s*\n?(.*?)\n?\s*```", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Não foi possível extrair JSON da resposta:\n{text[:500]}")


class RequirementsAgent:
    """Agente que descobre requisitos ocultos a partir do backlog do Agente 01."""

    def __init__(self, model: str = "gemini-2.5-flash"):
        self.model = model
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.client = genai.Client(api_key=api_key)

    def run(self, user_story: str, run_id: int) -> dict:
        """
        Descobre requisitos ocultos via automatic function calling.
        Busca o backlog do Agente 01 no Qdrant como contexto.

        Args:
            user_story: User story original.
            run_id: ID do pipeline_run para atualizar no PostgreSQL.

        Returns:
            dict com riscos, casos de borda e dependências.
        """
        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=[search_exa, find_edge_cases, search_qdrant],
            temperature=0.7,
        )

        print(f"  🤖 Enviando para {self.model} (automatic function calling)...")
        response = self.client.models.generate_content(
            model=self.model,
            contents=f"User Story:\n{user_story}",
            config=config,
        )

        print(f"  📨 Resposta recebida ({len(response.text or '')} chars)")
        result = _extract_json(response.text)

        # Salvar no PostgreSQL
        update_pipeline_run(run_id, agente_02_resultado=result)
        print(f"  💾 Atualizado no PostgreSQL (id: {run_id})")

        # Salvar embedding no Qdrant
        save_to_qdrant(result, source="agente_02_requisitos", run_id=run_id + 100000)
        
        return result
