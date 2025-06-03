import re
import os
import random
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity


with open("collected_filenames.txt", "r", encoding="utf-8") as f:
    filenames = [line.strip() for line in f]

# Read and filter text from each file
all_sentences = []
for file in filenames:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            text = f.read()
            # Split into sentences (works for Greek, English, etc.)
            sentences = re.split(r'(?<=[.!?])\s+', text)
            for sentence in sentences:
                words = re.findall(r'\w+', sentence)
                all_sentences.append(sentence)
    except FileNotFoundError:
        print(f"File not found: {file}")
    except Exception as e:
        print(f"Error reading {file}: {e}")

if not all_sentences:
    print("No valid sentences found.")
    exit()

# Convert sentences to TF-IDF vectors
tfidf = TfidfVectorizer(max_features=1000)
X = tfidf.fit_transform(all_sentences)

# Cluster using K-Means (choose number of clusters, e.g., 3)
n_clusters = 10
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
clusters = kmeans.fit_predict(X)

# region cluster grouping
# group sentences by cluster
cluster_groups = defaultdict(list)
for sentence, cluster in zip(all_sentences, clusters):
    cluster_groups[cluster].append(sentence)

for cluster_id, sentences in cluster_groups.items():
    # shuffle sentences for randomness
    random.shuffle(sentences)
    
    # sort by similarity to cluster center
    cluster_center = kmeans.cluster_centers_[cluster_id]
    sentence_scores = []
    for sentence in sentences:
        sentence_vec = tfidf.transform([sentence])
        similarity = cosine_similarity(sentence_vec, [cluster_center])[0][0]
        sentence_scores.append((similarity, sentence))
    sentences_sorted = [s[1] for s in sorted(sentence_scores, reverse=True)]
    
    # shuffled version for mixing
    mixed_sentences = sentences
    
    with open(f"cluster_{cluster_id}_mix.txt", "w", encoding="utf-8") as f:
        f.write("\n---\n".join(mixed_sentences))
        
    print(f"Saved {len(mixed_sentences)} mixed sentences for cluster {cluster_id}")

# master mix with all clusters
with open("full_mix.txt", "w", encoding="utf-8") as f:
    for cluster_id in range(n_clusters):
        f.write(f"\n\n=== CLUSTER {cluster_id} ===\n")
        f.write("\n---\n".join(cluster_groups[cluster_id][:100]))
# endregion

