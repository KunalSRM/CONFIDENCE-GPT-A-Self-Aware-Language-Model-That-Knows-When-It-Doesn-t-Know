import requests
from bs4 import BeautifulSoup
import json
import os
from tqdm import tqdm

DATA_FILE = "data/qa_data.json"
os.makedirs("data", exist_ok=True)

# Wikipedia pages to scrape (major topics)
WIKI_PAGES = [
    "Physics", "Mathematics", "Chemistry", "Biology", "History",
    "Geography", "Computer_science", "Artificial_intelligence",
    "Economics", "Medicine", "Space", "Sports", "Philosophy",
    "Art", "Environment", "Psychology", "Engineering"
]

qa_pairs = []

for page in tqdm(WIKI_PAGES, desc="Scraping Wikipedia"):
    try:
        url = f"https://en.wikipedia.org/wiki/{page}"
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            continue
        soup = BeautifulSoup(resp.text, "html.parser")
        
        paragraphs = soup.select("p")
        for p in paragraphs:
            text = p.get_text().strip()
            if len(text) > 50:  # only meaningful content
                # Simple Q&A generation heuristic
                question = f"What is {page}? (based on Wikipedia)"
                answer = text
                qa_pairs.append({"question": question, "answer": answer})
    except Exception as e:
        print(f"Skipping {page}: {e}")

# Save to JSON
try:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(qa_pairs, f, ensure_ascii=False, indent=4)
    print(f"Scraped {len(qa_pairs)} Q&A pairs.")
except Exception as e:
    print(f"Error saving JSON: {e}")
