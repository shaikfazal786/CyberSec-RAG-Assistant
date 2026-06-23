"""Build the persistent ChromaDB index from cybersecurity PDFs."""

import chromadb
from chromadb.errors import NotFoundError
from langchain_community.vectorstores import Chroma

from config import settings
from utils.chunking import create_chunks
from utils.embeddings import embedding_model
from utils.pdf_loader import load_all_pdfs


def rebuild_index() -> int:
    settings.data_dir.mkdir(exist_ok=True)
    documents = load_all_pdfs(settings.data_dir)
    if not documents:
        raise RuntimeError(f"No readable PDF pages found in {settings.data_dir}")

    chunks = create_chunks(
        documents,
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    print(f"Chunks: {len(chunks)}")

    # Remove the old collection so repeated ingestion cannot create duplicates.
    client = chromadb.PersistentClient(path=str(settings.chroma_path))
    try:
        client.delete_collection(settings.collection_name)
    except (NotFoundError, ValueError):
        pass

    Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=str(settings.chroma_path),
        collection_name=settings.collection_name,
        collection_metadata={"hnsw:space": "cosine"},
    )
    return len(chunks)


def main() -> None:
    try:
        rebuild_index()
    except Exception as exc:
        raise SystemExit(f"Ingestion failed: {exc}") from exc
    print("Vector Database Created")


if __name__ == "__main__":
    main()
