# data/

- `sample/` — documents to index. Replace the sample wiki with your own `.md`, `.txt` or `.pdf` files.
- `chroma/` — the persistent Chroma vector store (created on first index; git-ignored).
- `golden.json` — golden Q&A pairs for the eval harness (`python -m src.evals`).
