"""Chroma-backed vector store (local, persistent)."""
import chromadb

from .config import settings
from .ingest import Chunk


def get_collection():
    client = chromadb.PersistentClient(path=str(settings.chroma_dir))
    return client.get_or_create_collection(name="knowledge_base")


def upsert_chunks(chunks: list[Chunk], embeddings: list[list[float]]) -> int:
    col = get_collection()
    col.upsert(
        ids=[f"{c.source}#{c.index}" for c in chunks],
        documents=[c.text for c in chunks],
        metadatas=[{"source": c.source, "index": c.index} for c in chunks],
        embeddings=embeddings,
    )
    return col.count()


def query(vector: list[float], top_k: int):
    col = get_collection()
    return col.query(query_embeddings=[vector], n_results=top_k)
