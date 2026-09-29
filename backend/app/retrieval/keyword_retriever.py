import re

from qdrant_client.models import FieldCondition, Filter, MatchValue
from rank_bm25 import BM25Okapi

from backend.app.core.qdrant import qdrant_client, COLLECTION_NAME


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def retrieve_keyword_chunks(
    question: str,
    source: str,
    limit: int = 8,
) -> list[dict]:
    source_filter = Filter(
        must=[
            FieldCondition(
                key="source",
                match=MatchValue(value=source),
            )
        ]
    )

    points = []
    offset = None

    while True:
        batch, offset = qdrant_client.scroll(
            collection_name=COLLECTION_NAME,
            scroll_filter=source_filter,
            limit=256,
            offset=offset,
            with_payload=True,
            with_vectors=False,
        )
        points.extend(batch)

        if offset is None:
            break

    if not points:
        return []

    texts = [point.payload["text"] for point in points]
    bm25 = BM25Okapi([tokenize(text) for text in texts])
    scores = bm25.get_scores(tokenize(question))

    ranked = sorted(
        zip(points, scores),
        key=lambda item: item[1],
        reverse=True,
    )

    return [
        {
            "text": point.payload["text"],
            "source": point.payload["source"],
            "page": point.payload["page"],
            "score": float(score),
        }
        for point, score in ranked[:limit]
    ]


if __name__ == "__main__":
    question = "How did the modified and conventional treatment protocols differ?"
    results = retrieve_keyword_chunks(
        question,
        source="sample.pdf",
        limit=50,
    )

    for rank, result in enumerate(results, start=1):
        text = result["text"].lower()
        if (
            result["page"] == 2
            and "3 h" in text
            and "0.5 h" in text
            and "144 j/cm2" in text
            and "288 j/cm2" in text
        ):
            print(f"Exact method chunk BM25 rank: {rank}")
            print(result["text"][:500])
            break
    else:
        print("Exact method chunk not found")