import json
import numpy as np
from sentence_transformers import SentenceTransformer
import os

DATA_FILE = "data/qa_data.json"
EMBED_FILE = "data/qa_embeddings.npy"
os.makedirs("data", exist_ok=True)

try:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        qa_pairs = json.load(f)
except Exception as e:
    print(f"Error loading JSON: {e}")
    qa_pairs = []

questions = [q["question"] for q in qa_pairs]

# Load sentence-transformer model
try:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(questions, show_progress_bar=True)
    np.save(EMBED_FILE, embeddings)
    print("Embeddings saved successfully.")
except Exception as e:
    print(f"Error generating embeddings: {e}")
