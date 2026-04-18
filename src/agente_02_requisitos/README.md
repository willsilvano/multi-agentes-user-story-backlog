# Agente 02 — Descoberta de Requisitos Ocultos

## O que faz

Investiga o que ficou de fora do backlog do Agente 01. Descobre casos de borda, dependências não declaradas, riscos de segurança, requisitos não-funcionais e ambiguidades na especificação.

## Por que esse agente existe

O Scrum Master foca no "caminho feliz". Este agente faz as perguntas difíceis: *"E se o usuário não tiver conexão?"*, *"Esse endpoint precisa de rate limiting?"*, *"A LGPD se aplica aqui?"*.

## Fluxo de trabalho

1. **Busca no Qdrant** — recupera semanticamente o backlog completo do Agente 01
2. **Busca no Exa** — pesquisa referências sobre riscos, segurança e padrões técnicos
3. **Identifica edge cases** — cenários de borda que podem causar falhas
4. **Gera relatório** — consolida tudo em JSON estruturado

## Input

- User story original
- Backlog do Agente 01 (via busca semântica no Qdrant)

## Output (JSON)

```json
{
  "edge_cases": [
    "E se o token expirar durante a operação?",
    "E se o usuário tentar acessar sem permissão?"
  ],
  "undeclared_dependencies": [
    "Serviço de envio de email para recuperação de senha"
  ],
  "security_risks": [
    "SQL Injection no campo de busca (OWASP A03)"
  ],
  "non_functional_requirements": [
    "Tempo de resposta < 200ms para o dashboard"
  ],
  "specification_gaps": [
    "Não está claro se o progresso é por módulo ou por curso inteiro"
  ]
}
```

## Tools

| Tool | Descrição | Fonte |
|---|---|---|
| `search_exa` | Busca artigos e referências técnicas sobre riscos e padrões | Exa API (neural search) |
| `find_edge_cases` | Identifica cenários de borda e casos não cobertos | Local |
| `search_qdrant` | Busca semântica no backlog do Agente 01 | Qdrant |

## Memória

- **Short-term (messages)** — recebe a user story via orquestrador como contexto imediato
- **Long-term (Qdrant)** — busca semanticamente o backlog completo do Agente 01 (ex: *"quais tasks envolvem autenticação?"*)

## Persistência

- **PostgreSQL** — atualiza `agente_02_resultado` no registro existente em `pipeline_runs`
- **Qdrant** — salva embedding do resultado para o Agente 03 consultar

## Modelo

- Gemini 2.5 Flash (configurável via `GEMINI_MODEL`)
- Automatic function calling — o modelo decide quando e quais tools chamar
