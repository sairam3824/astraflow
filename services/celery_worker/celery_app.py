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
def ingest_document_task(self, doc_id: str, file_path: str):
    """Ingest document: extract text and chunk"""
    try:
        from services.ingestion.main import ingest_document
        import asyncio
        
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(ingest_document(doc_id, file_path))
        
        logger.info(f"Ingestion task completed for {doc_id}")
        return {"doc_id": doc_id, "chunks": result}
    except Exception as e:
        logger.error(f"Ingestion task failed for {doc_id}: {e}", exc_info=True)
        raise

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
