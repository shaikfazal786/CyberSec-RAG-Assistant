"""Retrieval and grounded Gemini answer generation."""

from dataclasses import dataclass
from typing import Any

from google import genai
from langchain_community.vectorstores import Chroma

from config import settings
from utils.embeddings import embedding_model


def _get_db():
    return Chroma(
        persist_directory=str(settings.chroma_path),
        embedding_function=embedding_model,
        collection_name=settings.collection_name,
    )


@dataclass(frozen=True)
class Source:
    filename: str
    page: int
    text: str
    distance: float | None


@dataclass(frozen=True)
class RAGResponse:
    answer: str
    sources: list[Source]


def retrieve(question: str, top_k: int | None = None) -> list[Source]:
    db = _get_db()
    retriever = db.as_retriever(search_kwargs={"k": settings.top_k})

    if db._collection.count() == 0:
        raise RuntimeError("The document index is empty. Run `python ingest.py` first.")

    active_retriever = retriever
    if top_k is not None:
        active_retriever = db.as_retriever(search_kwargs={"k": top_k})

    documents = active_retriever.invoke(question)
    sources: list[Source] = []
    for document in documents:
        metadata = document.metadata
        sources.append(
            Source(
                filename=str(metadata.get("source", "unknown")),
                page=int(metadata.get("page", 0)),
                text=document.page_content,
                distance=None,
            )
        )
    return sources


def _build_prompt(question: str, sources: list[Source]) -> str:
    context = "\n\n".join(
        f"[Source {index}: {source.filename}, page {source.page}]\n{source.text}"
        for index, source in enumerate(sources, start=1)
    )
    return f"""You are a cybersecurity document assistant. Answer using only the context below.
If the context does not contain the answer, say that the indexed documents do not provide enough information.
Do not invent facts. Cite supporting passages inline as [Source N].

Context:
{context}

Question: {question}
Answer:"""


def answer_question(question: str) -> RAGResponse:

    question = question.strip()

    if not question:
        raise ValueError("Question cannot be empty.")

    if not settings.google_api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY is not configured."
        )

    sources = retrieve(question)

    prompt = _build_prompt(
        question=question,
        sources=sources,
    )

    client = genai.Client(
        api_key=settings.google_api_key
    )

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
    )

    answer = getattr(response, "text", None)

    if not answer:
        raise RuntimeError(
            "Gemini returned empty response."
        )

    return RAGResponse(
        answer=answer.strip(),
        sources=sources,
    )


def format_sources(
    sources: list[Source]
) -> str:

    result = []

    for i, source in enumerate(sources, start=1):

        result.append(
            f"[Source {i}] "
            f"{source.filename} "
            f"(Page {source.page})"
        )

    return "\n".join(result)


def main():

    print(
        "\nCyberSec RAG Assistant\n"
    )

    while True:

        question = input(
            "\nAsk Question (q to quit): "
        )

        if question.lower() == "q":
            break

        try:

            response = answer_question(
                question
            )

            print("\nAnswer:\n")
            print(response.answer)

            print("\nSources:\n")
            print(
                format_sources(
                    response.sources
                )
            )

        except Exception as e:

            print(f"\nError: {e}")

if __name__ == "__main__":
    main()
