# Agente 02 - Analista de Requisitos
# Responsável por identificar requisitos e dependências

from .prompts import SYSTEM_PROMPT
from .tools import exa_search, find_edges, qdrant_search


class RequirementsAgent:
    """Agente que identifica requisitos e mapeia dependências."""

    def __init__(self):
        self.system_prompt = SYSTEM_PROMPT

    def run(self, tasks: dict) -> dict:
        """
        Analisa tarefas e identifica requisitos.

        Args:
            tasks: Tarefas técnicas do Agente 01.

        Returns:
            dict com requisitos e dependências.
        """
        # TODO: implementar chamada ao LLM com tools
        raise NotImplementedError
