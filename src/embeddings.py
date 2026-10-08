"""Gemini embeddings."""
from .config import require_api_key, settings

_genai = None


def _genai_client():
    global _genai
    if _genai is None:
        import google.generativeai as genai

        genai.configure(api_key=require_api_key())
        _genai = genai
    return _genai


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a list of texts. Kept simple (one call each); batch later if slow."""
    genai = _genai_client()
    vectors: list[list[float]] = []
    for text in texts:
        resp = genai.embed_content(model=settings.embedding_model, content=text)
        vectors.append(resp["embedding"])
    return vectors


def embed_query(text: str) -> list[float]:
    return embed_texts([text])[0]
