from celery import Celery
from libs.utils.config import config
from libs.utils.logging import setup_logger

logger = setup_logger("celery-worker")

celery_app = Celery(
    'astraflow',
    broker=config.CELERY_BROKER_URL,
    backend=config.CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,
    task_soft_time_limit=3000,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_default_retry_delay=60,
    task_max_retries=3,
)

@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_jitter=True)
def ingest_document_task(self, doc_id: str, collection_id: str, object_name: str):
    """Complete PDF ingestion pipeline: download, extract, chunk, embed, store in ChromaDB"""
    import tempfile
    import os
    from minio import Minio
    from pdfminer.high_level import extract_text
    import asyncio
    import aiosqlite
    import chromadb
    from openai import OpenAI
    import uuid
    
    try:
        logger.info(f"Starting ingestion for document {doc_id}")
        
        # 1. Download PDF from MinIO
        minio_client = Minio(
            config.MINIO_ENDPOINT,
            access_key=config.MINIO_ACCESS_KEY,
            secret_key=config.MINIO_SECRET_KEY,
            secure=False
        )
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_path = tmp_file.name
            minio_client.fget_object(config.MINIO_BUCKET, object_name, tmp_path)
            logger.info(f"Downloaded PDF from MinIO: {object_name}")
        
        # 2. Extract text from PDF
        text = extract_text(tmp_path)
        os.unlink(tmp_path)  # Clean up temp file
        
        if not text or len(text.strip()) == 0:
            logger.error(f"No text extracted from {doc_id}")
            raise ValueError("No text extracted from PDF")
        
        logger.info(f"Extracted {len(text)} characters from PDF")
        
        # 3. Chunk text
        chunks = semantic_chunk(text)
        logger.info(f"Created {len(chunks)} chunks")
        
        # 4. Store chunks in SQLite
        async def store_chunks():
            async with aiosqlite.connect(config.SQLITE_DB_PATH) as conn:
                chunk_ids = []
                for chunk in chunks:
                    chunk_id = str(uuid.uuid4())
                    chunk_ids.append(chunk_id)
                    await conn.execute(
                        "INSERT INTO chunks (id, doc_id, text, tokens, offset) VALUES (?, ?, ?, ?, ?)",
                        (chunk_id, doc_id, chunk['text'], chunk['tokens'], chunk['offset'])
                    )
                await conn.commit()
                return chunk_ids
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        chunk_ids = loop.run_until_complete(store_chunks())
        loop.close()
        
        # 5. Generate embeddings
        openai_client = OpenAI(api_key=config.OPENAI_API_KEY)
        texts = [chunk['text'] for chunk in chunks]
        
        response = openai_client.embeddings.create(
            model="text-embedding-ada-002",
            input=texts
        )
        embeddings = [item.embedding for item in response.data]
        logger.info(f"Generated {len(embeddings)} embeddings")
        
        # 6. Store in ChromaDB
        chroma_client = chromadb.HttpClient(host=config.CHROMA_HOST, port=config.CHROMA_PORT)
        collection = chroma_client.get_or_create_collection(f"collection_{collection_id}")
        
        collection.add(
            ids=chunk_ids,
            embeddings=embeddings,
            metadatas=[{
                "chunk_id": chunk_id,
                "doc_id": doc_id,
                "collection_id": collection_id
            } for chunk_id in chunk_ids],
            documents=texts
        )
        logger.info(f"Stored {len(chunk_ids)} chunks in ChromaDB")
        
        # 7. Update document status
        async def update_status():
            async with aiosqlite.connect(config.SQLITE_DB_PATH) as conn:
                await conn.execute(
                    "UPDATE documents SET status = 'indexed' WHERE id = ?",
                    (doc_id,)
                )
                await conn.commit()
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(update_status())
        loop.close()
        
        logger.info(f"Ingestion completed for {doc_id}: {len(chunks)} chunks indexed")
        return {"doc_id": doc_id, "chunks": len(chunks), "status": "indexed"}
        
    except Exception as e:
        logger.error(f"Ingestion task failed for {doc_id}: {e}", exc_info=True)
        
        # Update document status to failed
        async def mark_failed():
            async with aiosqlite.connect(config.SQLITE_DB_PATH) as conn:
                await conn.execute(
                    "UPDATE documents SET status = 'failed' WHERE id = ?",
                    (doc_id,)
                )
                await conn.commit()
        
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(mark_failed())
            loop.close()
        except:
            pass
        
        raise

def semantic_chunk(text: str, max_tokens: int = 512, overlap: int = 50):
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

@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_jitter=True)
def embed_chunks_task(self, chunk_ids: list, collection_id: str):
    """Generate embeddings for chunks"""
    try:
        logger.info(f"Embedding task started for {len(chunk_ids)} chunks")
        # Implementation in embedding service
        return {"chunk_ids": chunk_ids, "collection_id": collection_id}
    except Exception as e:
        logger.error(f"Embedding task failed: {e}", exc_info=True)
        raise

@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_jitter=True)
def summarize_document_task(self, doc_id: str):
    """Generate document summary"""
    try:
        logger.info(f"Summarization task started for {doc_id}")
        return {"doc_id": doc_id}
    except Exception as e:
        logger.error(f"Summarization task failed: {e}", exc_info=True)
        raise

@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_jitter=True)
def run_workflow_task(self, workflow_id: str, inputs: dict):
    """Execute workflow"""
    try:
        logger.info(f"Workflow task started for {workflow_id}")
        return {"workflow_id": workflow_id, "inputs": inputs}
    except Exception as e:
        logger.error(f"Workflow task failed: {e}", exc_info=True)
        raise

@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_jitter=True)
def analyze_github_repo_task(self, repo_url: str, analysis_id: str):
    """Analyze GitHub repository"""
    try:
        logger.info(f"GitHub analysis task started for {repo_url}")
        return {"repo_url": repo_url, "analysis_id": analysis_id}
    except Exception as e:
        logger.error(f"GitHub analysis task failed: {e}", exc_info=True)
        raise
