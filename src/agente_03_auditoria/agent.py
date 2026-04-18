# Agente 03 - Auditor de Qualidade
# Responsável por validar e pontuar a qualidade dos requisitos

from .prompts import SYSTEM_PROMPT
from .tools import qdrant_search, score_quality


class AuditAgent:
    """Agente que valida e pontua a qualidade dos requisitos."""

    def __init__(self):
        self.system_prompt = SYSTEM_PROMPT

    def run(self, requirements: dict, tasks: dict) -> dict:
        """
        Audita requisitos e tarefas.

        Args:
            requirements: Requisitos do Agente 02.
            tasks: Tarefas do Agente 01.

        Returns:
            dict com score e sugestões.
        """
        # TODO: implementar chamada ao LLM com tools
        raise NotImplementedError
