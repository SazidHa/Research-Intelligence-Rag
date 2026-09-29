from backend.app.retrieval.retriever import retrieve_chunks


question = (
    "How was modified photodynamic therapy performed in the study, "
    "and how did it differ from conventional treatment?"
)

results = retrieve_chunks(
    question=question,
    source="sample.pdf",
    limit=3,
)

for result in results:
    print(f"\nScore: {result['score']:.3f}")
    print(f"Source: {result['source']}, page {result['page']}")
    print(result["text"][:500])