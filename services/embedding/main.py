from fastapi import FastAPI
from prometheus_client import make_asgi_app
import aiosqlite
import chromadb
from openai import OpenAI
from libs.utils.logging import setup_logger
from libs.utils.config import config

logger = setup_logger("embedding-service")
app = FastAPI(title="Embedding Service")

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

openai_client = OpenAI(api_key=config.OPENAI_API_KEY)
chroma_client = chromadb.HttpClient(host=config.CHROMA_HOST, port=config.CHROMA_PORT)

async def embed_chunks(chunk_ids: list, collection_id: str):
    """Generate embeddings and store in ChromaDB"""
    try:
        async with aiosqlite.connect(config.SQLITE_DB_PATH) as conn:
            # Fetch chunks
            placeholders = ','.join('?' * len(chunk_ids))
            cursor = await conn.execute(
                f"SELECT id, text, doc_id FROM chunks WHERE id IN ({placeholders})",
                chunk_ids
            )
            chunks = await cursor.fetchall()
        
        if not chunks:
            return
        
        # Generate embeddings
        texts = [chunk[1] for chunk in chunks]
        response = openai_client.embeddings.create(
            model="text-embedding-ada-002",
            input=texts
        )
        
        embeddings = [item.embedding for item in response.data]
        
        # Store in ChromaDB
        collection = chroma_client.get_or_create_collection(f"collection_{collection_id}")
        
        collection.add(
            ids=[chunk[0] for chunk in chunks],
            embeddings=embeddings,
            metadatas=[{
                "chunk_id": chunk[0],
                "doc_id": chunk[2],
                "collection_id": collection_id
            } for chunk in chunks],
            documents=texts
        )
        
        # Update document status
        doc_ids = list(set(chunk[2] for chunk in chunks))
        async with aiosqlite.connect(config.SQLITE_DB_PATH) as conn:
            for doc_id in doc_ids:
                await conn.execute(
                    "UPDATE documents SET status = 'ingested' WHERE id = ?",
                    (doc_id,)
                )
            await conn.commit()
        
        logger.info(f"Embedded {len(chunks)} chunks for collection {collection_id}")
        return len(chunks)
    
    except Exception as e:
        logger.error(f"Embedding failed: {e}")
        raise

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=config.EMBEDDING_SERVICE_PORT)
