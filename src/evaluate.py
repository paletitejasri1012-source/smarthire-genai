from pathlib import Path
import json

def retrieval_hit_rate(rows):
    if not rows:
        return 0.0
    return sum(bool(r.get("hit")) for r in rows) / len(rows)

def save_json(data, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")
