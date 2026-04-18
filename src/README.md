# Sistema Multi-Agente

Sistema de 3 agentes especializados que trabalham em pipeline para processar histórias de usuário.

## Arquitetura

```
User Story
    ↓
┌─────────────────────────────────────┐
│  Agente 01 - Scrum Master           │
│  • Quebra em tarefas técnicas       │
│  • Tools: exa, break_tasks          │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Agente 02 - Analista Requisitos    │
│  • Identifica requisitos            │
│  • Mapeia dependências              │
│  • Tools: exa, find_edges, qdrant   │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Agente 03 - Auditor Qualidade      │
│  • Valida requisitos                │
│  • Pontua qualidade                 │
│  • Tools: qdrant, score_quality     │
└─────────────────────────────────────┘
    ↓
Resultado Final
```

## Estrutura de Pastas

```
src/
├── agente_01_scrum/
│   ├── __init__.py
│   ├── agent.py          ← lógica do agente
│   ├── tools.py          ← tools: exa, break_tasks
│   ├── prompts.py        ← system prompt + templates
│   └── README.md         ← o que faz, input, output
│
├── agente_02_requisitos/
│   ├── __init__.py
│   ├── agent.py
│   ├── tools.py          ← exa, find_edges, qdrant
│   ├── prompts.py
│   └── README.md
│
├── agente_03_auditoria/
│   ├── __init__.py
│   ├── agent.py
│   ├── tools.py          ← qdrant, score_quality
│   ├── prompts.py
│   └── README.md
│
├── memory/
│   ├── __init__.py
│   └── qdrant_client.py  ← conexão compartilhada
│
├── orchestrator/
│   ├── __init__.py
│   └── pipeline.py       ← conecta os 3 agentes
│
└── README.md             ← este arquivo
```
