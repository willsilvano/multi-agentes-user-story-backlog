# Agente 01 - Scrum Master
# Responsável por quebrar histórias de usuário em tarefas técnicas

from google.genai import types

from .prompts import SYSTEM_PROMPT
from .tools import search_exa, break_tasks, prioritize
from src.utils import extract_json, get_genai_client, DEFAULT_MODEL
from src.memory.db import save_pipeline_run
from src.memory.qdrant_client import save_to_qdrant


class ScrumAgent:
    """Agente Scrum Master que transforma user stories em backlog técnico."""

    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model
        self.client = get_genai_client()

    def run(self, user_story: str) -> dict:
        """
        Processa uma user story via automatic function calling.
        O modelo decide quando chamar search_exa, break_tasks e prioritize.
        """
        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=[search_exa, break_tasks, prioritize],
            temperature=0.7,
        )

        print(f"  🤖 Enviando para {self.model} (automatic function calling)...")
        response = self.client.models.generate_content(
            model=self.model,
            contents=f"User Story:\n{user_story}",
            config=config,
        )

        print(f"  📨 Resposta recebida ({len(response.text or '')} chars)")
        backlog = extract_json(response.text)

        # Salvar no PostgreSQL
        run_id = save_pipeline_run(user_story, backlog)
        backlog["_run_id"] = run_id
        print(f"  💾 Salvo no PostgreSQL (id: {run_id})")

        # Salvar embedding no Qdrant
        save_to_qdrant(backlog, source="agente_01_scrum", run_id=run_id)

        return backlog
