#!/bin/sh
set -e

CHROMA_DIR="${CHROMA_PATH:-chroma_db}"

if [ ! -d "$CHROMA_DIR" ] || [ -z "$(ls -A "$CHROMA_DIR" 2>/dev/null)" ]; then
  if find data -maxdepth 1 -type f -name "*.pdf" | grep -q .; then
    echo "No vector index found. Building ChromaDB from PDFs..."
    python ingest.py
  else
    echo "No vector index or PDFs found. App will start, but questions need an indexed knowledge base."
  fi
fi

exec gunicorn --bind "0.0.0.0:${PORT:-10000}" web:app
