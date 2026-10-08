"""Central configuration. Override via environment variables or a .env file."""
import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent


@dataclass
class Settings:
    gemini_api_key: str = field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))
    # Check Google AI Studio for current model IDs; these are sensible defaults.
    chat_model: str = field(default_factory=lambda: os.getenv("GEMINI_CHAT_MODEL", "gemini-2.0-flash"))
    embedding_model: str = field(
        default_factory=lambda: os.getenv("GEMINI_EMBEDDING_MODEL", "text-embedding-004")
    )
    chroma_dir: Path = field(
        default_factory=lambda: Path(os.getenv("CHROMA_DIR", str(PROJECT_ROOT / "data" / "chroma")))
    )
    docs_dir: Path = field(
        default_factory=lambda: Path(os.getenv("DOCS_DIR", str(PROJECT_ROOT / "data" / "sample")))
    )
    chunk_size: int = field(default_factory=lambda: int(os.getenv("CHUNK_SIZE", "800")))
    chunk_overlap: int = field(default_factory=lambda: int(os.getenv("CHUNK_OVERLAP", "120")))
    top_k: int = field(default_factory=lambda: int(os.getenv("TOP_K", "5")))


settings = Settings()


def require_api_key() -> str:
    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Copy .env.example to .env and add your key from Google AI Studio."
        )
    return settings.gemini_api_key
