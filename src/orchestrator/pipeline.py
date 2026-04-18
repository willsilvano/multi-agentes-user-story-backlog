# Pipeline que conecta os 3 agentes
from src.agente_01_scrum.agent import ScrumAgent
from src.agente_02_requisitos.agent import RequirementsAgent
from src.agente_03_auditoria.agent import AuditAgent


class AgentPipeline:
    """
    Orquestra a execução dos 3 agentes em sequência:
    1. Scrum Master: quebra história em tarefas
    2. Analista de Requisitos: identifica requisitos e dependências
    3. Auditor: valida qualidade
    """

    def __init__(self):
        self.scrum_agent = ScrumAgent()
        self.requirements_agent = RequirementsAgent()
        self.audit_agent = AuditAgent()

    def run(self, user_story: str) -> dict:
        """
        Executa o pipeline completo.

        Args:
            user_story: História de usuário para processar.

        Returns:
            dict com resultados de cada agente.
        """
        print("🚀 Iniciando pipeline...")

        # Etapa 1: Scrum Master
        print("\n📋 Agente 01 - Scrum Master")
        tasks = self.scrum_agent.run(user_story)

        # Etapa 2: Analista de Requisitos
        # print("\n📝 Agente 02 - Analista de Requisitos")
        # requirements = self.requirements_agent.run(tasks)

        # Etapa 3: Auditor
        # print("\n✅ Agente 03 - Auditor de Qualidade")
        # audit_result = self.audit_agent.run(requirements, tasks)

        return {
            "tasks": tasks,
            # "requirements": requirements,
            # "audit": audit_result,
        }
