from sentence_transformers import SentenceTransformer

import requests
import json

# Ollama local API
OLLAMA_URL = "http://localhost:11434/api/embed"

# Model name
MODEL_NAME = "deepseek-r1:1.5b"


def generate_embedding(text):
    payload = {
        "model": MODEL_NAME,
        "input": text
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload
        )

        response.raise_for_status()

        data = response.json()

        # Get first embedding vector
        embedding = data["embeddings"][0]

        return embedding

    except Exception as e:
        print("Error:", e)
        return None


# Example user input
user_input = "Create user story for RAG based proposal generation"

vector = generate_embedding(user_input)

if vector:
    print("Embedding created successfully")
    print("Vector length:", len(vector))
    print("First 10 values:", vector[:10])