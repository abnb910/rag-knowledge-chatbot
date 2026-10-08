# Build plan — roughly 4 weeks at 8–10 hrs/week

## Week 1 — First run
- [ ] Create the GitHub repo (public) and push this scaffold
- [ ] `python -m venv .venv`, `pip install -r requirements.txt`
- [ ] Copy `.env.example` → `.env`, add a free Gemini key from Google AI Studio
- [ ] `streamlit run src/app.py` → click **Rebuild index** → chat with the sample wiki
- [ ] Write-up: note anything that broke in the README troubleshooting section

## Week 2 — Make it yours
- [ ] Replace `data/sample/` with real documents you care about
- [ ] Tune chunking (`CHUNK_SIZE` / `CHUNK_OVERLAP`) — try a question that fails, inspect the chunks
- [ ] Experiment: change `TOP_K`, rewrite the system prompt, compare answers
- [ ] Fill in `docs/PRODUCT_SPEC.md`

## Week 3 — Trust & polish
- [ ] Extend `data/golden.json` to 10+ Q&A pairs, run `python -m src.evals`
- [ ] Add source-quality handling: what happens with no relevant chunks?
- [ ] Fill in `docs/ADOPTION_PLAN.md`
- [ ] README polish: architecture diagram, demo GIF/screenshot

## Week 4 — Code review & ship
- [ ] Self-review: run through the code, note what you'd refactor
- [ ] Coaching code review (together): structure, tests, docs
- [ ] Tag v1.0, add the repo link to the CV header

## Stretch (later phases)
- Hybrid retrieval (keyword + vector) and reranking
- Conversation memory
- Docker + Azure deployment
