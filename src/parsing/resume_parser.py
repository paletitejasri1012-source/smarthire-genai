import json
from ..llm import LLMClient

SCHEMA_KEYS = ["name", "skills", "experience", "education", "target_role"]

PARSER_PROMPT = '''
Extract the resume into this JSON schema:
{
  "name": "string",
  "skills": ["string"],
  "experience": ["string"],
  "education": ["string"],
  "target_role": "string"
}

Rules:
- Return ONLY valid JSON.
- Do not invent information.
- Use an empty string/list when information is absent.
- Preserve the candidate's actual information.

RESUME:
'''

def validate_profile(profile):
    if not isinstance(profile, dict):
        raise ValueError("Resume parser did not return an object.")
    clean = {}
    for key in SCHEMA_KEYS:
        if key == "skills":
            value = profile.get(key, [])
            clean[key] = value if isinstance(value, list) else [str(value)]
        elif key in ("experience", "education"):
            value = profile.get(key, [])
            clean[key] = value if isinstance(value, list) else [str(value)]
        else:
            clean[key] = str(profile.get(key, "") or "")
    return clean

def parse_resume(resume_text, llm=None):
    llm = llm or LLMClient()
    raw = llm.generate(PARSER_PROMPT + resume_text, temperature=0)
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.replace("```json", "", 1).replace("```", "", 1).strip()
    return validate_profile(json.loads(raw))
