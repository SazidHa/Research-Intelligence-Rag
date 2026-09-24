from backend.app.ingestion.embedder import generate_embedding

text = "Deep learning models can be used for stroke classification."

embedding = generate_embedding(text)

print("Embedding created successfully.")
print("Vector length:", len(embedding))
print("First 5 values:", embedding[:5])