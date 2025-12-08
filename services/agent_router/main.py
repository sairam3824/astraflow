from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_client import make_asgi_app
import chromadb
from libs.utils.logging import setup_logger
from libs.utils.config import config
from libs.model_router import model_router

logger = setup_logger("agent-router")
app = FastAPI(title="Agent Router Service")

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

chroma_client = chromadb.HttpClient(host=config.CHROMA_HOST, port=config.CHROMA_PORT)

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    generate_answer: bool = True

class SearchResponse(BaseModel):
    chunks: list
    answer: str = None

@app.get("/collections/{collection_id}/search", response_model=SearchResponse)
async def search_collection(collection_id: str, query: str, top_k: int = 5):
    try:
        # Retrieve from vector store
        collection = chroma_client.get_collection(f"collection_{collection_id}")
        results = collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        chunks = []
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                chunks.append({
                    "text": doc,
                    "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                    "distance": results['distances'][0][i] if results['distances'] else 0
                })
        
        # Build prompt with context
        context = "\n\n".join([chunk["text"] for chunk in chunks])
        prompt = f"""Based on the following context, answer the question.

Context:
{context}

Question: {query}

Answer:"""
        
        # Generate answer using model router
        answer = await model_router.complete(prompt, task_type="rag")
        
        logger.info(f"RAG search completed for collection {collection_id}")
        return SearchResponse(chunks=chunks, answer=answer)
    
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return SearchResponse(chunks=[], answer=f"Error: {str(e)}")

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=config.AGENT_ROUTER_PORT)
