# Knowledge Base Chatbot (RAG)

An open-source retrieval-augmented generation chatbot: ask questions in plain English, get answers grounded in *your* documents, with sources cited. The unblocked, portfolio-grade version of a SharePoint-knowledge Copilot chatbot — no paid Copilot licence needed.

**Skills demonstrated:** RAG pipelines · chunking & retrieval · vector databases (Chroma) · prompt engineering · LLM evals · Streamlit · Python packaging · Gemini API

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # then add your GEMINI_API_KEY from Google AI Studio
streamlit run src/app.py     # open the URL it prints, click "Rebuild index", start chatting
```

Put your own documents (`.md`, `.txt`, `.pdf`) in `data/sample/` (or point `DOCS_DIR` at another folder), hit **Rebuild index**, and ask away.

## How it works

```
data/sample/*.md ──▶ ingest.py (load + chunk) ──▶ embeddings.py (Gemini)
                                                        │
                                                        ▼
User question ──▶ embed query ──▶ vectorstore.py (Chroma, top-k) ──▶ rag.py ──▶ answer + sources
                                              (Streamlit UI: src/app.py)
```

## Project structure

- `src/ingest.py` — document loading (md/txt/pdf) and chunking
- `src/embeddings.py` — Gemini embedding calls
- `src/vectorstore.py` — persistent Chroma collection
- `src/rag.py` — retrieval + grounded generation pipeline
- `src/app.py` — Streamlit chat UI
- `src/evals.py` — golden Q&A eval harness (`data/golden.json`)
- `docs/PRODUCT_SPEC.md` — one-page product spec (the PM-muscle artefact)
- `docs/ADOPTION_PLAN.md` — rollout & adoption-KPI plan (the transformation-lead artefact)

## Roadmap

- [ ] Hybrid retrieval (keyword + vector) and reranking
- [ ] Conversation memory
- [ ] Eval dashboard (RAGAS-style metrics on the golden set)
- [ ] Docker + deploy (Azure)

## Troubleshooting

- **404 `model not found` on first run** — Google retires model IDs regularly (`text-embedding-004` and `gemini-2.0-flash` both died during this project's first run). Check the current list in AI Studio, then override with zero code changes:
  ```bash
  GEMINI_CHAT_MODEL=gemini-3.5-flash
  GEMINI_EMBEDDING_MODEL=gemini-embedding-001
  ```
  Known-good pair as of Oct 2026: `gemini-embedding-001` + `gemini-3.5-flash`.
- **503 `high demand`** — transient free-tier capacity. Wait ~20s and retry; the eval harness will pass once the spike clears.
- **`google.generativeai` deprecation warning** — this repo uses the supported `google-genai` SDK (`requirements.txt` pins `google-genai>=1.0`).

## Notes

- Built as Portfolio Project 1 of an AI-skills coaching programme targeting AI Product Manager and AI Adoption / Transformation Lead roles.
