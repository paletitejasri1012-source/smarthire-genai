from .prompts import CV_SUGGESTION_PROMPT
from ..llm import LLMClient

def generate_suggestions(resume_text, job, llm=None):
    llm = llm or LLMClient()
    prompt = CV_SUGGESTION_PROMPT.format(
        resume=resume_text,
        job=job.get("search_text", str(job)),
    )
    return llm.generate(prompt, temperature=0.2)
