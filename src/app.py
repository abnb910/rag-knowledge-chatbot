"""Streamlit chat UI."""
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import settings  # noqa: E402
from src.embeddings import embed_texts  # noqa: E402
from src.ingest import ingest  # noqa: E402
from src.rag import answer  # noqa: E402
from src.vectorstore import upsert_chunks  # noqa: E402

st.set_page_config(page_title="Knowledge Base Chatbot", page_icon="💬")
st.title("Knowledge Base Chatbot")
st.caption("Ask questions about your documents — answers are grounded in the indexed content.")

with st.sidebar:
    st.header("Setup")
    st.write(f"Docs folder: `{settings.docs_dir}`")
    if st.button("Rebuild index"):
        with st.spinner("Ingesting documents and building embeddings..."):
            chunks = ingest(settings.docs_dir, settings.chunk_size, settings.chunk_overlap)
            if not chunks:
                st.warning("No documents found. Add .md, .txt or .pdf files to the docs folder.")
            else:
                embs = embed_texts([c.text for c in chunks])
                n = upsert_chunks(chunks, embs)
                st.success(f"Indexed {n} chunks.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Ask about your documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                text, sources = answer(prompt)
            except Exception as e:  # surface config/API errors in the UI
                text, sources = f"⚠️ {e}", []
        st.markdown(text)
        if sources:
            st.caption("Sources: " + ", ".join(sources))
    st.session_state.messages.append({"role": "assistant", "content": text})
