# Agente 01 — Scrum Master

## O que faz

Recebe uma user story bruta e transforma em um backlog técnico priorizado e estruturado para o time de desenvolvimento.

## Fluxo de trabalho

1. **Analisa a User Story** — entende contexto, objetivo do usuário e critérios de aceitação implícitos e explícitos
2. **Busca no Exa** — pesquisa referências técnicas relevantes para o domínio da story (arquitetura, padrões, riscos)
3. **Quebra em tarefas** — decompõe em tasks técnicas com estimativas e dependências entre elas
4. **Prioriza (RICE)** — atribui score numérico a cada task usando Reach, Impact, Confidence e Effort

## Input

- User story em texto livre

## Output (JSON)

```json
{
  "user_story_rewritten": "Versão reescrita e mais clara da user story",
  "acceptance_criteria": ["Critério 1", "Critério 2"],
  "tasks": [
    {
      "id": "T1",
      "title": "Criar endpoint /auth",
      "rice_score": 42,
      "effort": "3 dias",
      "depends_on": []
    }
  ],
  "dependencies": ["Serviço externo X"],
  "open_questions": ["Dúvida para refinar com o PO"]
}
```

## Tools

| Tool | Descrição | Fonte |
|---|---|---|
| `search_exa` | Pesquisa referências técnicas sobre arquitetura, padrões e boas práticas | Exa API |
| `break_tasks` | Decompõe a user story em tasks técnicas com estimativas e dependências | Local |
| `prioritize` | Prioriza tasks com framework RICE (Reach, Impact, Confidence, Effort) | Local |

## Persistência

- **PostgreSQL** — cria registro em `pipeline_runs` com a user story e o resultado JSON
- **Qdrant** — salva embedding do resultado para busca semântica pelos agentes seguintes

## Modelo

- Gemini 2.5 Flash (configurável via `GEMINI_MODEL`)
- Automatic function calling — o modelo decide quando e quais tools chamar
