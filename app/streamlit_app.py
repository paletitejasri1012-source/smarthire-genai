import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import tempfile
import streamlit as st

from src.parsing.loader import load_resume
from src.parsing.resume_parser import parse_resume
from src.search.job_search import JobSearch, profile_to_text
from src.generate.cv_suggestions import generate_suggestions
from src.mentor.rag_chain import CareerRAG
from src.safety.guardrails import check_input

st.set_page_config(page_title="SmartHire GenAI", page_icon="💼", layout="wide")
st.title("💼 SmartHire GenAI")
st.caption("Resume matching + CV improvement + grounded AI Career Mentor")

@st.cache_resource
def get_job_search():
    search = JobSearch()
    if Path("vectorstore/jobs.faiss").exists():
        search.load()
    else:
        from src.search.job_search import load_jobs
        jobs = load_jobs()
        search.build(jobs)
        search.save()
    return search

@st.cache_resource
def get_rag():
    return CareerRAG()

uploaded = st.file_uploader("Upload your resume", type=["pdf", "docx"])

if uploaded:
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded.name).suffix) as tmp:
        tmp.write(uploaded.getbuffer())
        tmp_path = Path(tmp.name)

    try:
        resume_text = load_resume(tmp_path)
        profile = parse_resume(resume_text)
        st.session_state["resume_text"] = resume_text
        st.session_state["profile"] = profile
    except Exception as exc:
        st.error(f"Could not parse the resume: {exc}")

if "profile" in st.session_state:
    profile = st.session_state["profile"]
    resume_text = st.session_state["resume_text"]

    st.subheader("1. Parsed profile")
    left, right = st.columns(2)
    with left:
        st.write("**Name:**", profile["name"])
        st.write("**Target role:**", profile["target_role"])
        st.write("**Education:**", profile["education"])
    with right:
        st.write("**Skills:**", ", ".join(profile["skills"]))
        st.write("**Experience:**", profile["experience"])

    search = get_job_search()
    st.subheader("2. Matching jobs")
    results = search.search(profile_to_text(profile), top_k=10)

    for i, result in enumerate(results, 1):
        job = result["job"]
        with st.container(border=True):
            st.markdown(f"### {i}. {job['title']}")
            st.write(f"**Company:** {job['company']} | **Location:** {job['location']}")
            st.write(f"**Similarity:** {result['score']:.3f}")
            st.write(f"**Skills:** {job['skills']}")
            st.write(job["description"])

    st.subheader("3. CV improvement")
    selected = st.selectbox(
        "Choose a target job",
        range(len(results)),
        format_func=lambda i: f"{results[i]['job']['title']} — {results[i]['job']['company']}",
    )
    if st.button("Generate CV suggestions"):
        st.markdown(generate_suggestions(resume_text, results[selected]["job"]))

st.divider()
st.subheader("4. AI Career Mentor")
question = st.chat_input("Ask a career question...")

if question:
    allowed, reason = check_input(question)
    if not allowed:
        st.warning(reason)
    else:
        result = get_rag().answer(question)
        st.chat_message("user").write(question)
        st.chat_message("assistant").write(result["answer"])

        if result["sources"]:
            with st.expander("Retrieved sources"):
                for source in result["sources"]:
                    st.write(f"**{source['source']}** — similarity {source['score']:.3f}")
