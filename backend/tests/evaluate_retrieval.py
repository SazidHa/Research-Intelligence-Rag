from backend.app.retrieval.query_rewriter import rewrite_query
from backend.app.retrieval.retriever import retrieve_chunks


def method_rank(query: str) -> int | None:
    results = retrieve_chunks(query, source="sample.pdf", limit=20)

    for rank, result in enumerate(results, start=1):
        text = result["text"].lower()
        if (
            result["page"] == 2
            and "3 h" in text
            and "0.5 h" in text
            and "144 j/cm2" in text
            and "288 j/cm2" in text
        ):
            return rank

    return None


questions = [
    "How was modified photodynamic therapy performed in the study?",
    "How did the modified and conventional treatment protocols differ?",
]

for question in questions:
    rewritten = rewrite_query(
    question,
    paper_title=(
        "Modified painless photodynamic therapy for facial "
        "multiple actinic keratosis"
    ),
)
    print(f"\nQuestion: {question}")
    print(f"Rewritten: {rewritten}")
    print(f"Original rank: {method_rank(question) or 'not in top 8'}")
    print(f"Rewritten rank: {method_rank(rewritten) or 'not in top 8'}")