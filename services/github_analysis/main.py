from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_client import make_asgi_app
import git
from libs.utils.logging import setup_logger
from libs.utils.config import config

logger = setup_logger("github-analysis")
app = FastAPI(title="GitHub Analysis Service")

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

class AnalyzeRequest(BaseModel):
    repo_url: str

@app.post("/analyze")
async def analyze_repository(req: AnalyzeRequest):
    logger.info(f"Analyzing repository: {req.repo_url}")
    return {
        "analysis_id": "analysis_123",
        "status": "processing"
    }

@app.get("/analysis/{analysis_id}")
async def get_analysis(analysis_id: str):
    return {
        "analysis_id": analysis_id,
        "status": "completed",
        "readme": "# Sample README",
        "license": "MIT"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=config.GITHUB_ANALYSIS_PORT)
