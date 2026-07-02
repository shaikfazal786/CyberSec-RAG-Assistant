# CyberSec RAG Assistant

A local retrieval-augmented generation (RAG) application for asking questions about cybersecurity PDFs. Documents are parsed and chunked locally, embedded with Sentence Transformers, stored in ChromaDB, and supplied as grounded context to Google Gemini.

## Architecture

```text
Cybersecurity PDFs -> PDF loader -> text chunks -> embeddings -> ChromaDB
                                                               |
User question -> similarity search -> relevant chunks -> Gemini -> answer
```

## Stack

| Component | Technology |
| --- | --- |
| Frontend | Flask + HTML/CSS/JavaScript |
| LLM | Google Gemini API |
| Embeddings | Sentence Transformers |
| Vector database | ChromaDB |
| PDF parsing | PyPDF |
| Framework | LangChain |
| Language | Python |

## Setup

Python 3.10 or newer is recommended.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Add your Gemini API key to `.env`, place PDF files in `data/`, and build the index:

```powershell
python ingest.py
```

Then start the web frontend with Flask:

```powershell
python web.py
```

Open `http://127.0.0.1:5000` in a browser to access the home page.
A quick service check is available at `http://127.0.0.1:5000/health`.
Re-run `python ingest.py` whenever PDFs change. The ingestion command rebuilds the collection to prevent stale and duplicate chunks.

## Configuration

Settings can be changed through environment variables in `.env`:

| Variable | Default |
| --- | --- |
| `GOOGLE_API_KEY` | required |
| `GEMINI_MODEL` | `gemini-2.5-flash` |
| `EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` |
| `CHROMA_PATH` | `chroma_db` |
| `COLLECTION_NAME` | `cybersecurity_documents` |
| `CHUNK_SIZE` | `500` |
| `CHUNK_OVERLAP` | `100` |
| `TOP_K` | `5` |

The assistant is instructed to use only retrieved context and return direct answers without exposing document filenames, page numbers, or source metadata to end users. Treat its output as educational material, not as a substitute for professional incident response.
