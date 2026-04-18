# Agente 03 - Auditoria de Requisitos
# Entrada: busca semântica no Qdrant (backlog + requisitos ocultos)
# Saída: relatório + score de qualidade

from google.genai import types

from .prompts import SYSTEM_PROMPT
from .tools import audit_reqs, search_qdrant, score_quality
from src.utils import extract_json, get_genai_client, DEFAULT_MODEL
from src.memory.db import update_pipeline_run
from src.memory.qdrant_client import save_to_qdrant


class AuditAgent:
    """Agente que audita a coerência entre backlog e requisitos ocultos."""

    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model
        self.client = get_genai_client()

    def run(self, user_story: str, run_id: int) -> dict:
        """
        Audita o pipeline via automatic function calling.
        Busca backlog e requisitos no Qdrant como contexto.

        Args:
            user_story: User story original.
            run_id: ID do pipeline_run para atualizar no PostgreSQL.

        Returns:
            dict com scores, gaps, sugestões e relatório.
        """
        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=[audit_reqs, search_qdrant, score_quality],
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
        update_pipeline_run(run_id, agente_03_resultado=result)
        print(f"  💾 Atualizado no PostgreSQL (id: {run_id})")

        # Salvar embedding no Qdrant
        save_to_qdrant(result, source="agente_03_auditoria", run_id=run_id + 200000)

        return result
