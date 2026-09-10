from pathlib import Path
import numpy as np
import faiss

from ..config import CAREER_NOTES_DIR, TOP_K_RAG
from ..search.embed import Embedder
from ..generate.prompts import MENTOR_PROMPT
from ..llm import LLMClient

class CareerRAG:
    def __init__(self, notes_dir=CAREER_NOTES_DIR, embedder=None, llm=None):
        self.notes_dir = Path(notes_dir)
        self.embedder = embedder or Embedder()
        self.llm = llm or LLMClient()
        self.docs = []
        self.index = None
        self._build()

    def _build(self):
        for path in sorted(self.notes_dir.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            if text.strip():
                self.docs.append({"source": path.name, "text": text})
        if not self.docs:
            return
        vectors = np.asarray(self.embedder.encode([d["text"] for d in self.docs]), dtype="float32")
        self.index = faiss.IndexFlatIP(vectors.shape[1])
        self.index.add(vectors)

    def retrieve(self, question, top_k=TOP_K_RAG):
        if self.index is None:
            return []
        vector = np.asarray(self.embedder.encode([question]), dtype="float32")
        scores, indices = self.index.search(vector, min(top_k, len(self.docs)))
        return [
            {
                "score": float(score),
                "source": self.docs[int(idx)]["source"],
                "text": self.docs[int(idx)]["text"],
            }
            for score, idx in zip(scores[0], indices[0])
        ]

    def answer(self, question):
        retrieved = self.retrieve(question)
        context = "\n\n--- SOURCE ---\n".join(
            f"{r['source']}\n{r['text']}" for r in retrieved
        )
        prompt = MENTOR_PROMPT.format(context=context, question=question)
        answer = self.llm.generate(prompt, temperature=0.1)
        return {"answer": answer, "sources": retrieved}
