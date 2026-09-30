from backend.app.retrieval.retriever import retrieve_chunks
from backend.app.core.qdrant import COLLECTION_NAME


def build_context(
    question: str,
    source: str,
    limit: int = 3,
    collection_name: str = COLLECTION_NAME,
    section_type: str | None = None,
) -> str:
    results = retrieve_chunks(
        question,
        source=source,
        limit=limit,
        collection_name=collection_name,
        section_type=section_type,
    )

    if not results:
        return "No relevant passages found."

    return "\n\n".join(
        f"PASSAGE_ID: passage_{number}\n"
        f"SOURCE: {result['source']}\n"
        f"PDF_PAGE: {result['page']}\n"
        f"CITATION: [{result['source']}, p. {result['page']}]\n"
        f"TEXT:\n{result['text']}"
        for number, result in enumerate(results, start=1)
    )