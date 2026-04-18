# Agente 03 — Auditoria de Requisitos

## O que faz

Audita a coerência e completude de todo o pipeline, cruzando o backlog do Agente 01 com os requisitos ocultos do Agente 02. Gera um relatório com scores de qualidade, gaps encontrados e sugestões de melhoria.

## Por que esse agente é poderoso

Ele vê o pipeline completo — acessa no Qdrant o que os Agentes 01 e 02 produziram e audita a coerência entre eles. É impossível fazer isso sem memória compartilhada.

## O que audita

| Dimensão | Score | Pergunta |
|---|---|---|
| **Completude** | 0-1 | Todos os critérios de aceitação estão cobertos pelas tasks? |
| **Consistência** | 0-1 | As tasks são consistentes entre si? Não há contradições ou sobreposições? |
| **Cobertura de riscos** | 0-1 | Os requisitos ocultos do Agente 02 estão endereçados no backlog? |
| **Testabilidade** | 0-1 | Cada task é testável e tem critério de done claro? |
| **Score geral** | 0-1 | Média ponderada das 4 dimensões |

## Input

- User story original
- Backlog do Agente 01 + Requisitos ocultos do Agente 02 (via busca semântica no Qdrant)

## Output (JSON)

```json
{
  "scores": {
    "completude": 0.82,
    "consistencia": 0.91,
    "cobertura_riscos": 0.65,
    "testabilidade": 0.78,
    "score_geral": 0.79
  },
  "gaps": [
    "T2 não menciona tratamento de erro para token inválido",
    "Nenhuma task cobre LGPD para dados do usuário"
  ],
  "sugestoes": [
    "Adicionar T5: Validação de expiração com refresh token",
    "Incluir task de anonimização de dados pessoais"
  ],
  "relatorio": "O backlog cobre bem os requisitos funcionais, mas apresenta lacunas em segurança e compliance. Recomenda-se adicionar tasks específicas para tratamento de tokens e LGPD antes de iniciar o desenvolvimento."
}
```

## Tools

| Tool | Descrição | Fonte |
|---|---|---|
| `audit_reqs` | Cruza tasks do backlog com requisitos ocultos para identificar gaps | Local |
| `search_qdrant` | Busca semântica nos resultados dos Agentes 01 e 02 | Qdrant |
| `score_quality` | Calcula score de qualidade por dimensão com base em evidências | Local |

## Memória

- **Long-term (Qdrant)** — busca semanticamente tanto o backlog (Agente 01) quanto os requisitos ocultos (Agente 02) para cruzar informações

## Persistência

- **PostgreSQL** — atualiza `agente_03_resultado` no registro existente em `pipeline_runs`
- **Qdrant** — salva embedding do relatório final

## Modelo

- Gemini 2.5 Flash (configurável via `GEMINI_MODEL`)
- Automatic function calling — o modelo decide quando e quais tools chamar
