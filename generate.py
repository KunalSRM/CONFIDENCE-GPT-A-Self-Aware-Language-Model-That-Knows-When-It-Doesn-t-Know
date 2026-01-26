import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os

DATA_FILE = "data/qa_data.json"
EMBED_FILE = "data/qa_embeddings.npy"
CONFIDENCE_THRESHOLD = 0.7  # Mathematical threshold

# Load data
try:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        qa_pairs = json.load(f)
except Exception as e:
    print(f"Error loading JSON: {e}")
    qa_pairs = []

# Load embeddings
try:
    embeddings = np.load(EMBED_FILE)
except Exception as e:
    print(f"Error loading embeddings: {e}")
    embeddings = np.zeros((len(qa_pairs), 384))  # fallback

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_answer(query: str):
    try:
        query_emb = model.encode([query])
        sims = cosine_similarity(query_emb, embeddings)[0]
        idx = np.argmax(sims)
        confidence = float(sims[idx])
        if confidence < CONFIDENCE_THRESHOLD:
            return {
                "question": query,
                "answer": "⚠️ I am not confident enough to answer this reliably.",
                "confidence": confidence,
                "verdict": "ABSTAINED"
            }
        return {
            "question": query,
            "answer": qa_pairs[idx]["answer"],
            "confidence": confidence,
            "verdict": "ANSWERED"
        }
    except Exception as e:
        return {
            "question": query,
            "answer": f"Error generating answer: {e}",
            "confidence": 0,
            "verdict": "ERROR"
        }
