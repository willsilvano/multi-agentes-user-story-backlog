# Agente 02 — Descoberta de Requisitos Ocultos

## O que faz
Descobre requisitos ocultos que o Agente 01 não cobriu.

## Input
- User Story original
- Backlog do Agente 01 (via busca semântica no Qdrant)

## Output
- Casos de borda
- Dependências não declaradas
- Riscos de segurança (OWASP)
- Requisitos não-funcionais
- Gaps de especificação

## Tools
- `search_exa`: Busca artigos e referências técnicas
- `find_edge_cases`: Identifica cenários de borda
- `search_qdrant`: Busca semântica no backlog do Agente 01

## Memória
- **Short-term**: Recebe resumo do backlog via orquestrador
- **Long-term (Qdrant)**: Busca semanticamente o backlog completo
