from qdrant_client.models import FieldCondition, Filter, MatchValue

from backend.app.core.qdrant import qdrant_client, COLLECTION_NAME
from backend.app.ingestion.embedder import generate_embedding


def retrieve_chunks(
    question: str,
    source: str | None = None,
    limit: int = 5,
    collection_name: str = COLLECTION_NAME,
    section_type: str | None = None,
) -> list[dict]:
    conditions = []

    if source:
        conditions.append(
            FieldCondition(
                key="source",
                match=MatchValue(value=source),
            )
        )

    if section_type:
        conditions.append(
            FieldCondition(
                key="section_type",
                match=MatchValue(value=section_type),
            )
        )

    results = qdrant_client.query_points(
        collection_name=collection_name,
        query=generate_embedding(question),
        query_filter=Filter(must=conditions) if conditions else None,
        limit=limit,
        with_payload=True,
    ).points

    return [
        {
            "text": result.payload["text"],
            "source": result.payload.get("source"),
            "page": result.payload.get("page"),
            "section": result.payload.get("section"),
            "score": result.score,
        }
        for result in results
    ]