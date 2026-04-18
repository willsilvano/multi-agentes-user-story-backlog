# Ponto de entrada do sistema multi-agente
from dotenv import load_dotenv

from src.orchestrator.pipeline import AgentPipeline

load_dotenv()


def main():
    pipeline = AgentPipeline()

    user_story = """
    Precisamos de um dashoard para acompanhar os alunos no ambiente virtual de aprendizagem. 
    O acompanhamento deve focar no acesso, notas e progresso por curso..
    """

    result = pipeline.run(user_story)

    print("\n" + "=" * 60)
    print("RESULTADO FINAL")
    print("=" * 60)
    print(result)


if __name__ == "__main__":
    main()
