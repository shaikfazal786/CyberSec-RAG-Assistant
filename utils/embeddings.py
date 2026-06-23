"""LangChain Hugging Face embeddings used by ingestion and retrieval."""

from functools import lru_cache

from langchain_community.embeddings import HuggingFaceEmbeddings


DEFAULT_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

embedding_model = HuggingFaceEmbeddings(
    model_name=DEFAULT_MODEL_NAME,
    encode_kwargs={"normalize_embeddings": True},
)


@lru_cache(maxsize=2)
def get_embedding_model(model_name: str) -> HuggingFaceEmbeddings:
    if model_name == DEFAULT_MODEL_NAME:
        return embedding_model
    return HuggingFaceEmbeddings(
        model_name=model_name,
        encode_kwargs={"normalize_embeddings": True},
    )


def embed_documents(texts: list[str], model_name: str) -> list[list[float]]:
    return get_embedding_model(model_name).embed_documents(texts)


def embed_query(text: str, model_name: str) -> list[float]:
    return get_embedding_model(model_name).embed_query(text)
