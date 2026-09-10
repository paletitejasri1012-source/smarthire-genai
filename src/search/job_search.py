import json
from pathlib import Path
import faiss
import numpy as np
import pandas as pd

from .embed import Embedder
from ..config import JOBS_FILE, VECTOR_DIR, TOP_K_JOBS

TEXT_COLUMNS = {
    "title": ["title", "job_title"],
    "company": ["company", "company_name"],
    "location": ["location", "job_location"],
    "skills": ["skills", "required_skills"],
    "description": ["description", "job_description", "job_desc"],
}

def _find_column(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None

def load_jobs(path=JOBS_FILE):
    df = pd.read_csv(path).fillna("")
    mapping = {k: _find_column(df, v) for k, v in TEXT_COLUMNS.items()}
    if mapping["title"] is None or mapping["description"] is None:
        raise ValueError("Job CSV needs title and description columns.")

    rows = []
    for _, row in df.iterrows():
        item = {
            "title": str(row[mapping["title"]]),
            "company": str(row[mapping["company"]]) if mapping["company"] else "",
            "location": str(row[mapping["location"]]) if mapping["location"] else "",
            "skills": str(row[mapping["skills"]]) if mapping["skills"] else "",
            "description": str(row[mapping["description"]]),
        }
        item["search_text"] = (
            f"Title: {item['title']}\n"
            f"Skills: {item['skills']}\n"
            f"Description: {item['description']}"
        )
        rows.append(item)
    return rows

class JobSearch:
    def __init__(self, embedder=None):
        self.embedder = embedder or Embedder()
        self.index = None
        self.jobs = []

    def build(self, jobs):
        self.jobs = jobs
        vectors = np.asarray(
            self.embedder.encode([j["search_text"] for j in jobs]),
            dtype="float32",
        )
        self.index = faiss.IndexFlatIP(vectors.shape[1])
        self.index.add(vectors)

    def search(self, query, top_k=TOP_K_JOBS):
        if self.index is None:
            raise RuntimeError("Job index has not been built.")
        vector = np.asarray(self.embedder.encode([query]), dtype="float32")
        scores, indices = self.index.search(vector, min(top_k, len(self.jobs)))
        return [
            {"score": float(score), "job": self.jobs[int(idx)]}
            for score, idx in zip(scores[0], indices[0])
        ]

    def save(self, directory=VECTOR_DIR):
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(directory / "jobs.faiss"))
        (directory / "jobs.json").write_text(json.dumps(self.jobs, indent=2), encoding="utf-8")

    def load(self, directory=VECTOR_DIR):
        directory = Path(directory)
        self.index = faiss.read_index(str(directory / "jobs.faiss"))
        self.jobs = json.loads((directory / "jobs.json").read_text(encoding="utf-8"))

def profile_to_text(profile):
    return (
        f"Target role: {profile.get('target_role','')}\n"
        f"Skills: {', '.join(profile.get('skills', []))}\n"
        f"Experience: {'; '.join(profile.get('experience', []))}\n"
        f"Education: {'; '.join(profile.get('education', []))}"
    )
