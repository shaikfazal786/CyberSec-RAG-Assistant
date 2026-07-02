"""Application configuration loaded from environment variables."""

from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    data_dir: Path = BASE_DIR / "data"
    chroma_path: Path = BASE_DIR / os.getenv("CHROMA_PATH", "chroma_db")
    collection_name: str = os.getenv("COLLECTION_NAME", "cybersecurity_documents")
    embedding_model: str = os.getenv(
        "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
    )
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    google_api_key: str | None = os.getenv("GOOGLE_API_KEY")
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "500"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "100"))
    top_k: int = int(os.getenv("TOP_K", "5"))

    def __post_init__(self) -> None:
        if self.chunk_size <= 0:
            raise ValueError("CHUNK_SIZE must be positive")
        if not 0 <= self.chunk_overlap < self.chunk_size:
            raise ValueError("CHUNK_OVERLAP must be between 0 and CHUNK_SIZE")
        if self.top_k <= 0:
            raise ValueError("TOP_K must be positive")


settings = Settings()
