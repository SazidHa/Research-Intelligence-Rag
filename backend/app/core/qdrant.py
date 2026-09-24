from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "research_papers"
VECTOR_SIZE = 768

qdrant_client = QdrantClient(url=QDRANT_URL)


def check_qdrant_connection() -> bool:
    try:
        qdrant_client.get_collections()
        return True
    except Exception:
        return False


def create_collection():
    if not qdrant_client.collection_exists(COLLECTION_NAME):

        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )

        print(f"Collection '{COLLECTION_NAME}' created.")

    else:
        print(f"Collection '{COLLECTION_NAME}' already exists.")