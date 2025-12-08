from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_client import make_asgi_app
from libs.utils.logging import setup_logger
from libs.utils.config import config

logger = setup_logger("workflow-runner")
app = FastAPI(title="Workflow Runner Service")

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

class WorkflowRequest(BaseModel):
    name: str
    definition: dict

@app.post("/workflows")
async def create_workflow(req: WorkflowRequest):
    logger.info(f"Workflow created: {req.name}")
    return {"status": "created", "workflow_id": "wf_123"}

@app.post("/workflows/{workflow_id}/run")
async def run_workflow(workflow_id: str, inputs: dict = {}):
    logger.info(f"Workflow {workflow_id} executed")
    return {"status": "completed", "results": {}}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=config.WORKFLOW_RUNNER_PORT)
