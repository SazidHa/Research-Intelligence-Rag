


def chunk_pages(
    pages: list[dict],
    chunk_size: int = 1000,
    overlap: int = 200,
) -> list[dict]:
    if chunk_size <= 0 or not 0 <= overlap < chunk_size:
        raise ValueError("Use chunk_size > 0 and 0 <= overlap < chunk_size")

    chunks = []

    for page in pages:
        text = " ".join(page["text"].split())
        start = 0
        chunk_number = 1

        while start < len(text):
            end = min(start + chunk_size, len(text))

            chunks.append({
                "text": text[start:end],
                "source": page["source"],
                "page": page["page"],
                "chunk_number": chunk_number,
            })

            if end == len(text):
                break

            start = end - overlap
            chunk_number += 1

    return chunks


if __name__ == "__main__":
    import sys
    from backend.app.ingestion.pdf_loader import load_pdf
    chunks = chunk_pages(load_pdf(sys.argv[1]))
    print(f"Created {len(chunks)} chunks")
    if chunks:
        first = chunks[0]
        print(
            f"{first['source']} — page {first['page']}, "
            f"chunk {first['chunk_number']}"
        )
        print(first["text"][:300])