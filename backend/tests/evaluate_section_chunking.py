import numpy as np
from rank_bm25 import BM25Okapi

from backend.app.ingestion.embedder import generate_embedding
from backend.app.ingestion.pdf_loader import load_pdf
from backend.app.ingestion.section_chunker import chunk_pages_by_section
from backend.app.retrieval.keyword_retriever import tokenize


chunks = chunk_pages_by_section(load_pdf("data/papers/sample.pdf"))
print(f"Section-aware chunks: {len(chunks)}")

target = next(
    index for index, chunk in enumerate(chunks)
    if chunk["page"] == 2
    and chunk["section"].lower() == "treatment protocol"
)

# Embed once; reuse these vectors for both questions.
vectors = np.array([generate_embedding(c["text"]) for c in chunks])
bm25 = BM25Okapi([tokenize(c["text"]) for c in chunks])

questions = [
    "How was modified photodynamic therapy performed in the study?",
    "How did the modified and conventional treatment protocols differ?",
]

for question in questions:
    
    query_vector = np.array(generate_embedding(question))

    # Both BGE document and query vectors are normalized.
    dense_scores = vectors @ query_vector
    keyword_scores = bm25.get_scores(tokenize(question))

    dense_order = np.argsort(-dense_scores)
    keyword_order = np.argsort(-keyword_scores)

    dense_rank = int(np.where(dense_order == target)[0][0]) + 1
    keyword_rank = int(np.where(keyword_order == target)[0][0]) + 1

    print(f"\nQuestion: {question}")
    print(f"Treatment section dense rank: {dense_rank}")
    print(f"Treatment section BM25 rank: {keyword_rank}")
    method_sections = {
        "materials and methods",
        "research design",
        "subjects",
        "treatment protocol",
        "clinical evaluation",
    }
    method_indices = [
        i for i, chunk in enumerate(chunks)
        if chunk["section"].lower() in method_sections
    ]

    filtered_dense = sorted(
        method_indices,
        key=lambda i: dense_scores[i],
        reverse=True,
    )
    filtered_bm25 = sorted(
        method_indices,
        key=lambda i: keyword_scores[i],
        reverse=True,
    )

    print("Within methods — dense rank:", filtered_dense.index(target) + 1)
    print("Within methods — BM25 rank:", filtered_bm25.index(target) + 1)