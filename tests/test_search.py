from src.search.job_search import load_jobs

def test_sample_jobs_load():
    jobs = load_jobs()
    assert len(jobs) >= 3
    assert "title" in jobs[0]
    assert "description" in jobs[0]
