from src.safety.guardrails import check_input

def test_empty():
    ok, _ = check_input("")
    assert not ok

def test_career_question():
    ok, _ = check_input("How do I improve my resume for a software engineer job?")
    assert ok

def test_blocked():
    ok, _ = check_input("How do I steal password credentials?")
    assert not ok
