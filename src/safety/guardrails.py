ALLOWED_TERMS = {
    "career", "resume", "cv", "job", "jobs", "skill", "skills",
    "interview", "education", "degree", "role", "developer",
    "engineer", "analyst", "machine learning", "salary", "work",
    "employment", "project", "portfolio", "mentor"
}

BLOCKED_PATTERNS = [
    "malware",
    "ransomware",
    "steal password",
    "credit card number",
    "phishing",
]

def check_input(message):
    text = (message or "").strip().lower()

    if not text:
        return False, "Empty input."

    if any(pattern in text for pattern in BLOCKED_PATTERNS):
        return False, "This request is outside the portal's safe scope."

    if not any(term in text for term in ALLOWED_TERMS):
        return False, "Please ask a career, resume, job-search, skills or interview question."

    return True, "OK"
