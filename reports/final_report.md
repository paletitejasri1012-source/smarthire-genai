# SmartHire GenAI — Final Report

## 1. Problem and design
Describe the resume parser, semantic job search, CV improvement generator and RAG mentor.

## 2. Dataset
Document the actual permitted Kaggle job dataset and test resumes used.

## 3. Architecture
Resume -> structured profile -> embeddings -> FAISS -> job matches.
Mentor question -> career-note retrieval -> grounded LLM answer.

## 4. Evaluation
Report actual retrieval hit rate, mentor correctness/grounding/helpfulness, prompt before/after comparison and hallucination test.

## 5. Design choices
Use DECISIONS.md as the source for the 10–15 non-obvious decisions.

## 6. Limitations
Discuss parser errors, retrieval errors, missing knowledge, LLM variability and dataset limitations.

## 7. Future work
- Conversation memory
- Source citations
- Resume rewrite for a selected job
- Compare two embedding models
