from fastapi import FastAPI
from pdfminer.high_level import extract_text
from prometheus_client import make_asgi_app
import uuid
import aiosqlite
from typing import List
from libs.utils.logging import setup_logger
from libs.utils.config import config

logger = setup_logger("ingestion-service")
app = FastAPI(title="Ingestion Service")

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

def semantic_chunk(text: str, max_tokens: int = 512, overlap: int = 50) -> List[dict]:
    """Simple semantic chunking by sentences"""
    sentences = text.split('. ')
    chunks = []
    current_chunk = []
    current_tokens = 0
    offset = 0
    
    for sentence in sentences:
        sentence_tokens = len(sentence.split())
        
        if current_tokens + sentence_tokens > max_tokens and current_chunk:
            chunk_text = '. '.join(current_chunk) + '.'
            chunks.append({
                'text': chunk_text,
                'tokens': current_tokens,
                'offset': offset
            })
            # Keep overlap
            current_chunk = current_chunk[-overlap:] if len(current_chunk) > overlap else []
            current_tokens = sum(len(s.split()) for s in current_chunk)
            offset += len(chunk_text)
        
        current_chunk.append(sentence)
        current_tokens += sentence_tokens
    
    if current_chunk:
        chunk_text = '. '.join(current_chunk) + '.'
        chunks.append({
            'text': chunk_text,
            'tokens': current_tokens,
            'offset': offset
        })
    
    return chunks

async def ingest_document(doc_id: str, file_path: str):
    """Extract text and chunk document"""
    try:
        # Extract text from PDF
        text = extract_text(file_path)
        
        if not text or len(text.strip()) == 0:
            logger.error(f"No text extracted from {doc_id}")
            return
        
        # Chunk text
        chunks = semantic_chunk(text)
        
        # Store chunks in database
        async with aiosqlite.connect(config.SQLITE_DB_PATH) as conn:
            for chunk in chunks:
                chunk_id = str(uuid.uuid4())
                await conn.execute(
                    "INSERT INTO chunks (id, doc_id, text, tokens, offset) VALUES (?, ?, ?, ?, ?)",
                    (chunk_id, doc_id, chunk['text'], chunk['tokens'], chunk['offset'])
                )
            await conn.commit()
        
        logger.info(f"Document {doc_id} ingested: {len(chunks)} chunks")
        return len(chunks)
    
    except Exception as e:
        logger.error(f"Ingestion failed for {doc_id}: {e}")
        raise

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=config.INGESTION_SERVICE_PORT)
