from pathlib import Path
from pypdf import PdfReader
from docx import Document

def load_pdf(path):
    reader = PdfReader(str(path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def load_docx(path):
    doc = Document(str(path))
    return "\n".join(p.text for p in doc.paragraphs)

def load_resume(path):
    path = Path(path)
    if path.suffix.lower() == ".pdf":
        return load_pdf(path)
    if path.suffix.lower() == ".docx":
        return load_docx(path)
    raise ValueError("Only PDF and DOCX resumes are supported.")
