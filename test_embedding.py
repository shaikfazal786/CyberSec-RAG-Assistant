"""Smoke test for the configured sentence embedding model."""

from utils.embeddings import embedding_model


vector = embedding_model.embed_query("What is cyber threats?")

print("Vector Length:", len(vector))
