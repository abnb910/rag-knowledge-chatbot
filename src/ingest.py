"""Document loading and chunking."""
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Chunk:
    text: str
    source: str
    index: int


def load_documents(docs_dir: Path) -> list[tuple[str, str]]:
    """Return (text, filename) for every supported file under docs_dir."""
    docs: list[tuple[str, str]] = []
    for path in sorted(docs_dir.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() in {".md", ".txt"}:
            docs.append((path.read_text(encoding="utf-8", errors="ignore"), path.name))
        elif path.suffix.lower() == ".pdf":
            try:
                from pypdf import PdfReader

                reader = PdfReader(str(path))
                text = "\n".join(page.extract_text() or "" for page in reader.pages)
                docs.append((text, path.name))
            except ImportError:
                print(f"Skipping {path.name}: install pypdf to read PDFs")
    return docs


def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Simple recursive-style splitter: hard window, soft break on newlines."""
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        if end < len(text):
            newline = text.rfind("\n", start, end)
            if newline > start + chunk_size // 2:
                end = newline
        piece = text[start:end].strip()
        if piece:
            chunks.append(piece)
        if end - overlap <= start:  # avoid infinite loop on tiny inputs
            break
        start = end - overlap
    return chunks


def ingest(docs_dir: Path, chunk_size: int, overlap: int) -> list[Chunk]:
    chunks: list[Chunk] = []
    for text, source in load_documents(docs_dir):
        for i, piece in enumerate(chunk_text(text, chunk_size, overlap)):
            chunks.append(Chunk(text=piece, source=source, index=i))
    return chunks
