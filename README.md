# SmartHire GenAI — Resume Matching & AI Career Mentor

This repository implements the SmartHire capstone described in the supplied assignment:

- Resume Parser: PDF/DOCX -> structured JSON
- Semantic Job Search: embeddings + FAISS -> top-N jobs
- CV Improvement Generator
- AI Career Mentor: RAG over career notes
- Guardrails before mentor LLM calls
- Streamlit portal

The assignment requires a pre-collected job dataset rather than live LinkedIn/Naukri scraping. Replace the tiny sample CSV with the permitted Kaggle job corpus for the real submission.

## Quick start

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your API key.

Then build the job index:

```bash
python scripts/build_job_index.py
```

Run:

```bash
streamlit run app/streamlit_app.py
```

If no API key is configured, set `DEMO_MODE=true` to smoke-test the UI. Demo mode is not a substitute for the final GenAI evaluation.

## Real data

Put your permitted Kaggle job CSV at `data/jobs/jobs.csv`. The loader recognizes common column names:
- title / job_title
- company / company_name
- location
- skills / required_skills
- description / job_description / job_desc

Add sample/test resumes under `data/resumes/`.

## Evaluation

Create manually reviewed evaluation data using the template in `data/evaluation/retrieval_eval.csv`, then run:

```bash
python scripts/run_evaluation.py
```

Do not invent evaluation metrics. Replace TODOs in the report with results actually produced by your runs.

## Structure

```text
app/streamlit_app.py
src/
  parsing/loader.py
  parsing/resume_parser.py
  search/embed.py
  search/job_search.py
  generate/prompts.py
  generate/cv_suggestions.py
  mentor/rag_chain.py
  safety/guardrails.py
  evaluate.py
scripts/
data/
vectorstore/
reports/
tests/
```

## Submission note

This is a runnable implementation scaffold with sample data. The real dataset, human-labelled evaluation, API key, measured results, final PDF and deployment URL must be supplied/run by the project owner.
