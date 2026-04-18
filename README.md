# Multi-Agentes User Story Backlogs

Sistema multi-agente que transforma user stories em backlog técnico completo usando LLMs (Gemini), busca semântica (Qdrant) e persistência relacional (PostgreSQL).

## Arquitetura

```mermaid
flowchart TD
    US["📝 User Story"] --> A1

    subgraph A1["📋 Agente 01 — Scrum Master"]
        A1T["Tools: search_exa, break_tasks, prioritize"]
    end

    A1 -->|PostgreSQL + Qdrant| DB[(🐘 PostgreSQL)]
    A1 -->|embedding| QD[(🔮 Qdrant)]

    QD -->|busca semântica| A2

    subgraph A2["🔍 Agente 02 — Requisitos Ocultos"]
        A2T["Tools: search_exa, find_edge_cases, search_qdrant"]
    end

    A2 -->|atualiza| DB
    A2 -->|embedding| QD

    QD -->|busca semântica| A3

    subgraph A3["✅ Agente 03 — Auditoria"]
        A3T["Tools: audit_reqs, search_qdrant, score_quality"]
    end

    A3 -->|atualiza| DB
    A3 -->|embedding| QD

    A3 --> RF["📊 Relatório Final<br/>Backlog + Riscos + Score + Sugestões"]
```

## Estrutura do Projeto

```
├── docker-compose.yml        # PostgreSQL + Qdrant + App
├── Dockerfile
├── init.sql                  # Schema inicial do banco
├── pyproject.toml
├── .env.example
│
└── src/
    ├── main.py               # Ponto de entrada
    ├── utils.py              # Código compartilhado (extract_json, genai client)
    │
    ├── agente_01_scrum/      # Scrum Master
    │   ├── agent.py
    │   ├── tools.py          # search_exa, break_tasks, prioritize
    │   ├── prompts.py
    │   └── README.md
    │
    ├── agente_02_requisitos/ # Requisitos Ocultos
    │   ├── agent.py
    │   ├── tools.py          # search_exa, find_edge_cases, search_qdrant
    │   ├── prompts.py
    │   └── README.md
    │
    ├── agente_03_auditoria/  # Auditoria
    │   ├── agent.py
    │   ├── tools.py          # audit_reqs, search_qdrant, score_quality
    │   ├── prompts.py
    │   └── README.md
    │
    ├── memory/
    │   ├── db.py             # PostgreSQL (save/update pipeline_runs)
    │   └── qdrant_client.py  # Qdrant (save/search embeddings)
    │
    └── orchestrator/
        └── pipeline.py       # Conecta os 3 agentes em sequência
```

## Pré-requisitos

- Docker e Docker Compose
- Chave da API Gemini — [Google AI Studio](https://aistudio.google.com/apikey)
- Chave da API Exa — [Exa](https://exa.ai)

## Setup

1. Clone o repositório e copie o `.env`:

```bash
cp .env.example .env
```

2. Preencha as chaves no `.env`:

```
GEMINI_API_KEY=sua_chave_gemini
EXA_API_KEY=sua_chave_exa
```

3. Suba os containers:

```bash
docker compose up -d
```

4. Execute o pipeline:

```bash
docker compose run --rm app uv run python -m src.main
```

## Pipeline

| Etapa | Agente | Input | Output | Docs |
|---|---|---|---|---|
| 1 | Scrum Master | User Story | Backlog priorizado (RICE) + critérios de aceitação | [README](src/agente_01_scrum/README.md) |
| 2 | Requisitos Ocultos | User Story + Qdrant (backlog) | Casos de borda, riscos, dependências, gaps | [README](src/agente_02_requisitos/README.md) |
| 3 | Auditoria | User Story + Qdrant (backlog + requisitos) | Scores de qualidade, gaps, sugestões, relatório | [README](src/agente_03_auditoria/README.md) |

## Stack

| Componente | Tecnologia |
|---|---|
| LLM | Gemini 2.5 Flash (Google GenAI SDK) |
| Busca externa | Exa API |
| Banco vetorial | Qdrant |
| Embeddings | all-MiniLM-L6-v2 (sentence-transformers) |
| Banco relacional | PostgreSQL 17 |
| ORM | SQLAlchemy |
| Gerenciador de deps | uv |
| Runtime | Python 3.13 |

## Banco de Dados

A tabela `pipeline_runs` armazena o resultado de cada execução:

| Coluna | Tipo | Descrição |
|---|---|---|
| `user_story` | TEXT | Story original informada |
| `agente_01_resultado` | JSONB | Backlog com tasks, RICE, critérios |
| `agente_02_resultado` | JSONB | Riscos, edge cases, dependências |
| `agente_03_resultado` | JSONB | Scores, gaps, sugestões, relatório |

## Variáveis de Ambiente

| Variável | Descrição |
|---|---|
| `GEMINI_API_KEY` | Chave da API Google Gemini |
| `EXA_API_KEY` | Chave da API Exa |
| `GEMINI_MODEL` | Modelo Gemini (padrão: gemini-2.5-flash) |
| `POSTGRES_USER` | Usuário do PostgreSQL |
| `POSTGRES_PASSWORD` | Senha do PostgreSQL |
| `POSTGRES_DB` | Nome do banco |
| `DATABASE_URL` | Connection string do PostgreSQL |
| `QDRANT_HOST` | Host do Qdrant |
| `QDRANT_PORT` | Porta do Qdrant |
