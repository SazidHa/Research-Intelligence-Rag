import hashlib
import uuid
from pathlib import Path

from qdrant_client.models import Distance, PointStruct, VectorParams

from backend.app.core.qdrant import qdrant_client
from backend.app.ingestion.embedder import generate_embedding
from backend.app.ingestion.pdf_loader import load_pdf
from backend.app.ingestion.section_chunker import chunk_pages_by_section


EXPERIMENT_COLLECTION = "research_papers_section_v1"


def ingest_sections(pdf_path: str) -> int:
    path = Path(pdf_path)
    chunks = chunk_pages_by_section(load_pdf(str(path)))
    document_id = hashlib.sha256(path.read_bytes()).hexdigest()

    if not qdrant_client.collection_exists(EXPERIMENT_COLLECTION):
        qdrant_client.create_collection(
            collection_name=EXPERIMENT_COLLECTION,
            vectors_config=VectorParams(
                size=768,
                distance=Distance.COSINE,
            ),
        )

    points = []
    for chunk in chunks:
        point_id = str(uuid.uuid5(
            uuid.NAMESPACE_URL,
            f"section-v1:{document_id}:{chunk['page']}:{chunk['chunk_number']}",
        ))
        method_headings = {
            "materials and methods",
            "patients and methods",
            "methods",
            "methodology",
            "research design",
            "subjects",
            "treatment protocol",
            "clinical evaluation",
        }
        section_type = (
            "methods"
            if chunk["section"].strip().lower() in method_headings
            else "other"
        )
        points.append(PointStruct(
            id=point_id,
            vector=generate_embedding(chunk["text"]),
            payload={
                **chunk,
                "document_id": document_id,
                "section_type": section_type,
            },
        ))

    qdrant_client.upsert(
        collection_name=EXPERIMENT_COLLECTION,
        points=points,
    )
    return len(points)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("pdf_path", help="Path to the PDF to index")
    args = parser.parse_args()

    count = ingest_sections(args.pdf_path)
    print(
        f"Indexed {count} section-aware chunks "
        f"in {EXPERIMENT_COLLECTION}"
    )