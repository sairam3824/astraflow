from fastapi import FastAPI
from kafka import KafkaConsumer
import json
import pandas as pd
import redis
from prometheus_client import make_asgi_app
from libs.utils.logging import setup_logger
from libs.utils.config import config

logger = setup_logger("stock-analysis")
app = FastAPI(title="Stock Analysis Service")

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

redis_client = redis.Redis.from_url(config.REDIS_URL)

def compute_indicators(ticks: list):
    df = pd.DataFrame(ticks)
    return {
        "sma_20": df['price'].rolling(20).mean().iloc[-1] if len(df) >= 20 else None,
        "ema_12": df['price'].ewm(span=12).mean().iloc[-1] if len(df) >= 12 else None,
        "vwap": (df['price'] * df['volume']).sum() / df['volume'].sum() if len(df) > 0 else None,
        "volatility": df['price'].std() if len(df) > 1 else None
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=config.STOCK_ANALYSIS_PORT)
