from src.search.job_search import load_jobs, JobSearch

jobs = load_jobs()
search = JobSearch()
search.build(jobs)
search.save()

print(f"Built FAISS job index with {len(jobs)} jobs.")
