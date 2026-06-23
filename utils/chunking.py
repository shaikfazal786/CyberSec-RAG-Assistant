"""Split PDF pages into retrieval-sized chunks."""

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_chunks(
    documents: list[Document], chunk_size: int = 500, chunk_overlap: int = 100
) -> list[Document]:
    """Create overlapping text chunks and attach a stable batch index."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    chunks = splitter.split_documents(documents)
    for index, chunk in enumerate(chunks):
        chunk.metadata["chunk"] = index
    return chunks


def split_documents(
    documents: list[Document], chunk_size: int, chunk_overlap: int
) -> list[Document]:
    """Backward-compatible alias for callers using the previous function name."""
    return create_chunks(documents, chunk_size, chunk_overlap)
