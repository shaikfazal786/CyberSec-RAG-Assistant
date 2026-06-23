"""Load all PDF pages from a directory as LangChain documents."""

from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


def load_all_pdfs(data_path: str | Path = "data") -> list[Document]:
    data_dir = Path(data_path)
    if not data_dir.exists():
        raise FileNotFoundError(f"PDF directory does not exist: {data_dir}")
    if not data_dir.is_dir():
        raise NotADirectoryError(f"PDF path is not a directory: {data_dir}")

    documents: list[Document] = []
    pdf_paths = sorted(
        path
        for path in data_dir.iterdir()
        if (
            path.is_file()
            and path.suffix.lower() == ".pdf"
            and not path.name.startswith("~$")
        )
    )

    for pdf_path in pdf_paths:
        try:
            loaded_documents = PyPDFLoader(str(pdf_path)).load()
        except Exception as exc:
            raise RuntimeError(
                f"Failed to load '{pdf_path.name}'. Ensure it is a valid PDF file."
            ) from exc

        for document in loaded_documents:
            # PyPDFLoader uses zero-based pages; citations use human-readable numbers.
            document.metadata["source"] = pdf_path.name
            document.metadata["page"] = int(document.metadata.get("page", 0)) + 1
            if document.page_content.strip():
                documents.append(document)

    return documents


def load_pdfs(data_dir: str | Path) -> list[Document]:
    """Compatibility wrapper used by the ingestion pipeline."""
    return load_all_pdfs(data_dir)
