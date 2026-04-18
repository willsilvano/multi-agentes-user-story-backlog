# Agente 03 — Auditoria de Requisitos

## O que faz
Audita a coerência e completude do pipeline, cruzando o backlog do Agente 01 com os requisitos ocultos do Agente 02.

## Input
- User Story original
- Backlog do Agente 01 + Requisitos do Agente 02 (via Qdrant)

## Output
- Scores de qualidade (0-1): completude, consistência, cobertura de riscos, testabilidade
- Score geral (média ponderada)
- Gaps encontrados
- Sugestões de melhoria
- Relatório executivo

## Tools
- `audit_reqs`: Cruza tasks com requisitos para identificar gaps
- `search_qdrant`: Busca semântica nos resultados dos agentes anteriores
- `score_quality`: Calcula score por dimensão de qualidade
