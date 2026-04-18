# Utilitários compartilhados entre os agentes
import json
import os
import re

from google import genai
from google.genai import types


def extract_json(text: str) -> dict:
    """Extrai JSON de uma resposta que pode conter markdown ou texto extra."""
    if not text:
        raise ValueError("Resposta vazia do modelo")

    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"```(?:json)?\s*\n?(.*?)\n?\s*```", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Não foi possível extrair JSON da resposta:\n{text[:500]}")


def get_genai_client() -> genai.Client:
    """Retorna cliente Google GenAI configurado."""
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    return genai.Client(api_key=api_key)


DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
