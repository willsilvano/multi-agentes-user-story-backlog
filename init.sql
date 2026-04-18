CREATE TABLE IF NOT EXISTS pipeline_runs (
    id SERIAL PRIMARY KEY,
    user_story TEXT NOT NULL,
    agente_01_resultado JSONB,
    -- colunas para os próximos agentes serão adicionadas aqui
    -- agente_02_resultado JSONB,
    -- agente_03_resultado JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

COMMENT ON COLUMN pipeline_runs.agente_01_resultado IS 'JSON com: user_story_rewritten, acceptance_criteria, tasks (RICE), dependencies, open_questions';
