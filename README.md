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

## Notes

- Model IDs change — check Google AI Studio for current chat/embedding model names and set them in `.env`.
- Built as Portfolio Project 1 of an AI-skills coaching programme targeting AI Product Manager and AI Adoption / Transformation Lead roles.
