from backend.app.core.qdrant import (
    qdrant_client,
    COLLECTION_NAME,
)
from backend.app.ingestion.embedder import generate_embedding


queries = [
    "Which methods are used for stroke classification?",
    "How is microwave sensing used in healthcare?",
    "What is hybrid retrieval?",
    "How can MRI image quality be assessed automatically?",
]


for query in queries:
    query_vector = generate_embedding(query)

    results = qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=3,
    ).points

    print("\n" + "=" * 80)
    print(f"Query: {query}")
    print("=" * 80)

    for rank, result in enumerate(results, start=1):
        print(f"\nRank {rank}")
        print(f"Score: {result.score:.4f}")
        print(f"Paper: {result.payload['paper_title']}")
        print(f"Section: {result.payload['section']}")
        print(f"Year: {result.payload['year']}")
        print(f"Text: {result.payload['text']}")