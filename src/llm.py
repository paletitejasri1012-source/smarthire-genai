import os
from openai import OpenAI
from .config import OPENAI_MODEL, DEMO_MODE

class LLMClient:
    def __init__(self):
        self.demo_mode = DEMO_MODE or not os.getenv("OPENAI_API_KEY")
        self.client = None if self.demo_mode else OpenAI()

    def generate(self, prompt: str, temperature: float = 0.2) -> str:
        if self.demo_mode:
            return self._demo_response(prompt)

        response = self.client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )
        return response.choices[0].message.content or ""

    @staticmethod
    def _demo_response(prompt: str) -> str:
        if "valid JSON" in prompt:
            return '{"name":"Demo Candidate","skills":["Python","SQL"],"experience":[],"education":["B.Tech"],"target_role":"Software Engineer"}'
        if "CV" in prompt or "resume" in prompt.lower():
            return "Improve the professional summary, quantify project outcomes, and add missing role-relevant skills only when you genuinely have them."
        return "I can help with career planning using the supplied career notes. Connect an LLM API for full grounded generation."
