CREATE TABLE IF NOT EXISTS pipeline_runs (
    id SERIAL PRIMARY KEY,
    user_story TEXT NOT NULL,
    agente_01_resultado JSONB,
    agente_02_resultado JSONB,
    -- coluna para o próximo agente
    -- agente_03_resultado JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

COMMENT ON COLUMN pipeline_runs.agente_01_resultado IS 'JSON com: user_story_rewritten, acceptance_criteria, tasks (RICE), dependencies, open_questions';
COMMENT ON COLUMN pipeline_runs.agente_02_resultado IS 'JSON com: edge_cases, undeclared_dependencies, security_risks, non_functional_requirements, specification_gaps';
