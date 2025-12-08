#!/usr/bin/env python3
import chromadb
from chromadb.config import Settings

# Initialize ChromaDB client
client = chromadb.HttpClient(
    host="localhost",
    port=8000,
    settings=Settings(allow_reset=True)
)

print("ChromaDB initialized and ready")
print(f"Collections: {client.list_collections()}")
