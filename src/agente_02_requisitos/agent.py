# Agente 02 - Descoberta de Requisitos Ocultos
# Entrada: busca semântica no Qdrant (backlog do Agente 01)
# Saída: riscos, casos de borda, dependências

from google.genai import types

from .prompts import SYSTEM_PROMPT
from .tools import search_exa, find_edge_cases, search_qdrant
from src.utils import extract_json, get_genai_client, DEFAULT_MODEL
from src.memory.db import update_pipeline_run
from src.memory.qdrant_client import save_to_qdrant


class RequirementsAgent:
    """Agente que descobre requisitos ocultos a partir do backlog do Agente 01."""

    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model
        self.client = get_genai_client()

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
        result = extract_json(response.text)

        # Salvar no PostgreSQL
        update_pipeline_run(run_id, agente_02_resultado=result)
        print(f"  💾 Atualizado no PostgreSQL (id: {run_id})")

        # Salvar embedding no Qdrant
        save_to_qdrant(result, source="agente_02_requisitos", run_id=run_id + 100000)

        return result
