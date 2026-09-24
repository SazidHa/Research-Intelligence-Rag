from fastapi import FastAPI

from backend.app.core.qdrant import (
    qdrant_client,
    check_qdrant_connection,
)

app = FastAPI(
    title="Research Intelligence RAG API",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "Research Intelligence RAG API is running"
    }


@app.get("/health")
def health():
    connected = check_qdrant_connection()

    if not connected:
        return {
            "status": "unhealthy",
            "qdrant": "disconnected",
        }

    collections = qdrant_client.get_collections()

    return {
        "status": "healthy",
        "qdrant": "connected",
        "collections": len(collections.collections),
    }