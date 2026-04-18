# Agente 01 - Scrum Master
# Responsável por quebrar histórias de usuário em tarefas técnicas

import json
import os
import re

from google import genai
from google.genai import types

from .prompts import SYSTEM_PROMPT
from .tools import search_exa, break_tasks, prioritize
from src.memory.db import save_pipeline_run
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


class ScrumAgent:
    """Agente Scrum Master que transforma user stories em backlog técnico."""

    def __init__(self, model: str = "gemini-2.5-flash"):
        self.model = model
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.client = genai.Client(api_key=api_key)

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

        # generate_content com automatic function calling (padrão do SDK)
        # O SDK executa as tools automaticamente e retorna a resposta final
        print(f"  🤖 Enviando para {self.model} (automatic function calling)...")
        response = self.client.models.generate_content(
            model=self.model,
            contents=f"User Story:\n{user_story}",
            config=config,
        )

        print(f"  📨 Resposta recebida ({len(response.text or '')} chars)")
        backlog = _extract_json(response.text)

        # Salvar no PostgreSQL
        run_id = save_pipeline_run(user_story, backlog)
        backlog["_run_id"] = run_id
        print(f"  💾 Salvo no PostgreSQL (id: {run_id})")

        # Salvar embedding no Qdrant
        save_to_qdrant(backlog, source="agente_01_scrum", run_id=run_id)

        return backlog
