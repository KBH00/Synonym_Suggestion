from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("GerMedBERT/medbert-512")
model = AutoModel.from_pretrained("GerMedBERT/medbert-512")

def get_embedding(text):
    """Generate an embedding for the input text."""
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    outputs = model(**inputs)
    # Use the pooled output as a simple representation of the entire input
    return outputs.pooler_output

def cosine_similarity(a, b):
    """Compute the cosine similarity between two vectors."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Example candidate words (extend this list with your medical terms)
candidate_words = ["diabetes", "hyperglycemia", "insulin", "glucose", "hypoglycemia"]

# Precompute embeddings for the candidate words
candidate_embeddings = {word: get_embedding(word).detach().numpy() for word in candidate_words}

# Input word for which you want to find synonyms
input_word = "diabetes"
input_embedding = get_embedding(input_word).detach().numpy()

# Calculate similarity and rank candidate words
similarities = {word: cosine_similarity(input_embedding, emb) for word, emb in candidate_embeddings.items()}
sorted_similarities = sorted(similarities.items(), key=lambda x: x[1], reverse=True)

# Recommend top N synonyms
top_n = 3
print(f"Top {top_n} synonyms for '{input_word}':")
for i, (word, similarity) in enumerate(sorted_similarities[:top_n], 1):
    print(f"{i}. {word} (similarity: {similarity:.4f})")