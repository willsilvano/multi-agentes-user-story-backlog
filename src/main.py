# Ponto de entrada do sistema multi-agente
import json

from dotenv import load_dotenv

from src.orchestrator.pipeline import AgentPipeline

load_dotenv()


def main():
    pipeline = AgentPipeline()

    user_story = """
    Precisamos de um dashoard para acompanhar os alunos no ambiente virtual de aprendizagem. 
    O acompanhamento deve focar no acesso, notas e progresso por curso.
    """

    result = pipeline.run(user_story)

    print("\n" + "=" * 60)
    print("📊 RELATÓRIO FINAL")
    print("=" * 60)

    # Backlog
    print("\n📋 Backlog (Agente 01):")
    print(json.dumps(result["backlog"], indent=2, ensure_ascii=False))

    # Requisitos Ocultos
    print("\n🔍 Requisitos Ocultos (Agente 02):")
    print(json.dumps(result["requirements"], indent=2, ensure_ascii=False))

    # Auditoria
    print("\n✅ Auditoria (Agente 03):")
    audit = result["audit"]
    print(json.dumps(audit, indent=2, ensure_ascii=False))

    # Score resumido
    if "scores" in audit:
        scores = audit["scores"]
        print(f"\n🎯 Score Geral: {scores.get('score_geral', 'N/A')}")


if __name__ == "__main__":
    main()
