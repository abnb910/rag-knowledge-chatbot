"""Retrieval-augmented generation pipeline."""
from .config import require_api_key, settings
from .embeddings import embed_query
from .vectorstore import query as vs_query

SYSTEM_PROMPT = """You answer questions using ONLY the provided context excerpts.
If the answer is not in the excerpts, say you don't know rather than guessing.
Cite the excerpts you used like [1], [2]. Be concise."""


def build_context(results) -> str:
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    parts = []
    for i, (doc, meta) in enumerate(zip(docs, metas), start=1):
        parts.append(f"[{i}] (source: {meta['source']})\n{doc}")
    return "\n\n".join(parts)


def answer(question: str) -> tuple[str, list[str]]:
    """Return (answer_text, source_filenames)."""
    import google.generativeai as genai

    genai.configure(api_key=require_api_key())
    vec = embed_query(question)
    results = vs_query(vec, settings.top_k)
    context = build_context(results)
    model = genai.GenerativeModel(settings.chat_model, system_instruction=SYSTEM_PROMPT)
    resp = model.generate_content(f"Context:\n{context}\n\nQuestion: {question}")
    sources = sorted({m["source"] for m in results["metadatas"][0]})
    return resp.text, sources
