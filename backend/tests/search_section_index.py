from qdrant_client.models import FieldCondition, Filter, MatchValue

from backend.app.core.qdrant import qdrant_client
from backend.app.ingestion.embedder import generate_embedding
from backend.app.ingestion.ingest_sections import EXPERIMENT_COLLECTION


METHOD_SECTIONS = [
    "MATERIALS AND METHODS",
    "Research design",
    "Subjects",
    "Treatment protocol",
    "Clinical evaluation",
]

questions = [
    "How was modified photodynamic therapy performed in the study?",
    "How did the modified and conventional treatment protocols differ?",
]

for question in questions:
    results = qdrant_client.query_points(
        collection_name=EXPERIMENT_COLLECTION,
        query=generate_embedding(question),
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="source",
                    match=MatchValue(value="sample.pdf"),
                ),
                FieldCondition(
                    key="section_type",
                    match=MatchValue(value="methods"),
                ),
            ]
        ),
        limit=5,
        with_payload=True,
    ).points

    print(f"\nQuestion: {question}")
    for rank, result in enumerate(results, start=1):
        payload = result.payload
        print(
            f"{rank}. Page {payload['page']} — "
            f"{payload['section']} — score {result.score:.3f}"
        )
