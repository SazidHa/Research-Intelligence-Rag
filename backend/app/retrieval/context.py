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
        f"[{number}] {result['source']}, page {result['page']}\n"
        f"{result['text']}"
        for number, result in enumerate(results, start=1)
    )

if __name__ == "__main__":
    question = (
        "Treatment protocol for C-PDT side and M-PDT side: "
        "ALA cream incubation and red light irradiation"
    )
    print(build_context(question, source="sample.pdf", limit=8))