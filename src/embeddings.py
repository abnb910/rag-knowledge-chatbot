"""Gemini embeddings (google-genai SDK)."""
from google import genai

from .config import require_api_key, settings

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = genai.Client(api_key=require_api_key())
    return _client


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a list of texts in one batched call."""
    client = _get_client()
    resp = client.models.embed_content(model=settings.embedding_model, contents=texts)
    return [e.values for e in resp.embeddings]


def embed_query(text: str) -> list[float]:
    return embed_texts([text])[0]
