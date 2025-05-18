"""
Retrieval module: loads FAQ data, computes embeddings,
and retrieves top-K contexts using cosine similarity.
"""
import os
import csv
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI

client = OpenAI(api_key="API_KEY")

class RAGRetriever:
    """
    Embedding-based retriever for FAQ entries
    Precomputes embeddings on init, then ranks by cosine similarity
    """
    def __init__(self, csv_path: str, model: str = "text-embedding-ada-002"):
        self.entries = [] # [(id, question, answer)]
        self.embeddings = None  # np.ndarray
        self._load_csv(csv_path)
        self._embed_entries(model)

    def _load_csv(self, path: str):
        """Load FAQ entries from CSV into memory"""
        with open(path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.entries.append((row["id"], row["question"], row["answer"]))

    def _embed_entries(self, model: str):
        """Compute embeddings for all entries at init"""
        texts = [q + " " + a for _, q, a in self.entries]
        resp = client.embeddings.create(model=model, input=texts)
        # Store embeddings matrix for similarity search
        self.embeddings = np.array([d.embedding for d in resp.data])

    def retrieve(self, query: str, top_k: int = 3):
        """Embed the query, compute similarities, and return top-K answers"""
        q_resp = client.embeddings.create(model="text-embedding-ada-002", input=[query])
        q_vec = np.array(q_resp.data[0].embedding)
        sims = cosine_similarity([q_vec], self.embeddings)[0]
        idxs = sims.argsort()[-top_k:][::-1]
        return [self.entries[i][2] for i in idxs]

BASE_DIR = os.path.dirname(__file__)
retriever = RAGRetriever(csv_path=os.path.join(BASE_DIR, "faq.csv"))

def get_contexts(question: str):
    if question.strip() == "":
        return []
    return retriever.retrieve(question)
