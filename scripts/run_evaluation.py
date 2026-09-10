from pathlib import Path
import pandas as pd
from src.evaluate import retrieval_hit_rate
from src.search.job_search import JobSearch

eval_file = Path("data/evaluation/retrieval_eval.csv")

if not eval_file.exists():
    print("Create data/evaluation/retrieval_eval.csv first.")
    raise SystemExit(0)

search = JobSearch()
search.load()

df = pd.read_csv(eval_file).fillna("")
rows = []

for _, row in df.iterrows():
    results = search.search(row["profile_text"], top_k=5)
    titles = [r["job"]["title"] for r in results]
    rows.append({
        "hit": row["expected_title"] in titles,
        "expected": row["expected_title"],
        "returned": titles,
    })

print(f"Retrieval hit rate: {retrieval_hit_rate(rows):.3f}")
print("Use a larger manually reviewed set for the final submission.")
