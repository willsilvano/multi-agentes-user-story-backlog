# Cliente PostgreSQL compartilhado entre os agentes
import json
import os
from datetime import datetime

from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/multi_agentes")

_engine = None


def get_engine():
    """Retorna engine SQLAlchemy (singleton)."""
    global _engine
    if _engine is None:
        _engine = create_engine(DATABASE_URL)
    return _engine


def save_pipeline_run(user_story: str, agente_01_resultado: dict) -> int:
    """Salva a user story e o resultado do Agente 01 no PostgreSQL.

    Args:
        user_story: Texto original da user story.
        agente_01_resultado: Dict com o resultado do Agente 01.

    Returns:
        ID do registro criado.
    """
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                INSERT INTO pipeline_runs (user_story, agente_01_resultado, created_at, updated_at)
                VALUES (:user_story, :resultado, :now, :now)
                RETURNING id
            """),
            {
                "user_story": user_story.strip(),
                "resultado": json.dumps(agente_01_resultado, ensure_ascii=False),
                "now": datetime.now(),
            },
        )
        conn.commit()
        row_id = result.scalar()
        print(f"✅ Pipeline run salvo no PostgreSQL (id: {row_id})")
        return row_id


def update_pipeline_run(run_id: int, **kwargs) -> None:
    """Atualiza colunas de um pipeline_run existente.

    Args:
        run_id: ID do registro a atualizar.
        **kwargs: Colunas a atualizar (ex: agente_02_resultado=dict).
    """
    if not kwargs:
        return

    engine = get_engine()
    set_clauses = ", ".join(f"{col} = :{col}" for col in kwargs)
    params = {col: json.dumps(val, ensure_ascii=False) if isinstance(val, dict) else val for col, val in kwargs.items()}
    params["run_id"] = run_id
    params["now"] = datetime.now()

    with engine.connect() as conn:
        conn.execute(
            text(f"UPDATE pipeline_runs SET {set_clauses}, updated_at = :now WHERE id = :run_id"),
            params,
        )
        conn.commit()
        print(f"  ✅ Pipeline run atualizado no PostgreSQL (id: {run_id})")
