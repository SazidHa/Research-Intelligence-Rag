from qdrant_client.models import PointStruct

from backend.app.core.qdrant import (
    qdrant_client,
    COLLECTION_NAME,
)
from backend.app.ingestion.embedder import generate_embedding


sample_chunks = [
    {
        "id": 1,
        "text": "Convolutional neural networks have been widely used for stroke classification from medical imaging data.",
        "paper_title": "Deep Learning for Stroke Classification",
        "section": "Introduction",
        "year": 2024,
    },
    {
        "id": 2,
        "text": "Transformer architectures can capture long-range dependencies and have shown strong performance in biomedical text analysis.",
        "paper_title": "Transformers in Biomedical AI",
        "section": "Methods",
        "year": 2025,
    },
    {
        "id": 3,
        "text": "Microwave sensing has been investigated as a non-invasive technique for detecting differences in biological tissue properties.",
        "paper_title": "Microwave Sensing for Medical Diagnosis",
        "section": "Background",
        "year": 2023,
    },
    {
        "id": 4,
        "text": "Hybrid retrieval combines semantic vector search with keyword-based retrieval to improve document retrieval performance.",
        "paper_title": "Advanced Retrieval-Augmented Generation",
        "section": "Retrieval",
        "year": 2025,
    },
    {
        "id": 5,
        "text": "Magnetic resonance imaging quality assessment can be automated using deep neural networks to identify low-quality scans.",
        "paper_title": "Automated MRI Quality Assessment",
        "section": "Results",
        "year": 2024,
    },
]


points = []

for chunk in sample_chunks:
    embedding = generate_embedding(chunk["text"])

    points.append(
        PointStruct(
            id=chunk["id"],
            vector=embedding,
            payload={
                "text": chunk["text"],
                "paper_title": chunk["paper_title"],
                "section": chunk["section"],
                "year": chunk["year"],
            },
        )
    )


qdrant_client.upsert(
    collection_name=COLLECTION_NAME,
    points=points,
)

print(f"Inserted {len(points)} sample research chunks.")