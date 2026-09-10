from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
JOBS_FILE = DATA_DIR / "jobs" / "jobs.csv"
CAREER_NOTES_DIR = DATA_DIR / "career_notes"
VECTOR_DIR = ROOT / "vectorstore"

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
TOP_K_JOBS = int(os.getenv("TOP_K_JOBS", "10"))
TOP_K_RAG = int(os.getenv("TOP_K_RAG", "5"))
DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"
