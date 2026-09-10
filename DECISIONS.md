# Decision Log

1. One Streamlit portal keeps the parse -> match -> advise flow visible.
2. Structured JSON is used for resume extraction.
3. PDF and DOCX are supported.
4. Sentence-transformer embeddings are used for semantic matching.
5. Normalized embeddings + FAISS inner product approximate cosine similarity.
6. Job metadata is stored with the FAISS index.
7. Prompts are kept in a dedicated module.
8. The mentor uses RAG rather than unrestricted generation.
9. A guardrail runs before mentor generation.
10. The mentor is instructed to say it does not know when context is insufficient.
11. API keys are kept in environment variables.
12. Demo mode allows UI smoke testing without API spend; it is not final evaluation.
13. A tiny sample job CSV makes the repository runnable immediately.
14. The real Kaggle corpus should be supplied according to its terms rather than committed to Git.
15. Evaluation is separate from the UI demo.
