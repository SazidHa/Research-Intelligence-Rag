import hashlib
import sys
import uuid
from pathlib import Path

from qdrant_client.models import PointStruct

from backend.app.core.qdrant import qdrant_client, COLLECTION_NAME
from backend.app.ingestion.chunker import chunk_pages
from backend.app.ingestion.embedder import generate_embedding
from backend.app.ingestion.pdf_loader import load_pdf


def ingest_pdf(pdf_path: str) -> int:
    path = Path(pdf_path)
    pages = load_pdf(str(path))
    chunks = chunk_pages(pages)

    if not chunks:
        raise ValueError(f"No extractable text found in {path}")

    document_id = hashlib.sha256(path.read_bytes()).hexdigest()
    points = []

    for chunk in chunks:
        point_id = str(uuid.uuid5(
            uuid.NAMESPACE_URL,
            f"{document_id}:{chunk['page']}:{chunk['chunk_number']}",
        ))

        points.append(PointStruct(
            id=point_id,
            vector=generate_embedding(chunk["text"]),
            payload={
                **chunk,
                "paper_title": path.stem,
                "document_id": document_id,
            },
        ))

    qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )
    return len(points)


if __name__ == "__main__":
    count = ingest_pdf(sys.argv[1])
    print(f"Inserted {count} PDF chunks into {COLLECTION_NAME}.")