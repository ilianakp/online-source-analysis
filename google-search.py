from googlesearch import search
import requests
from bs4 import BeautifulSoup
import re

# Define your custom queries
queries = [
    "σταυρός χανιά ιστορία",
    "ζορμπάς σταυρός",
    "σταυρός χανιά κτίρια σπίτια"
]
filenames = []

# Dictionary to hold collected texts for each query
collected_texts = {}

for query in queries:
    urls = []
    for url in search(query, num_results=20, lang='en'):
        urls.append(url)
    texts = []
    for url in urls:
        try:
            response = requests.get(url, timeout=5)
            # encoding for greek
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            # Split into sentences (works for Greek, English, etc.)
            sentences = re.split(r'(?<=[.!?])\s+', text)
            # Keep only sentences with more than 3 words
            filtered_sentences = []
            for sentence in sentences:
                words = re.findall(r'\w+', sentence)
                if len(words) > 3:
                    filtered_sentences.append(sentence)
            filtered_text = ' '.join(filtered_sentences)
            texts.append(filtered_text)
        except Exception as e:
            texts.append(f"Could not retrieve {url}: {e}")
    collected_texts[query] = texts

for query, texts in collected_texts.items():
    filename = query.replace(" ", "_") + ".txt"
    filenames.append(filename)
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n\n--- NEXT RESULT ---\n\n".join(texts))
    print(f"Saved texts for query '{query}' to {filename}")

with open("collected_filenames.txt", "w", encoding="utf-8") as f:
    for filename in filenames:
        f.write(filename + "\n")
print("Saved list of filenames to collected_filenames.txt")
