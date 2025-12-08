from fastapi import FastAPI
from kafka import KafkaProducer
import json
import random
from datetime import datetime
from prometheus_client import make_asgi_app
from libs.utils.logging import setup_logger
from libs.utils.config import config

logger = setup_logger("stock-producer")
app = FastAPI(title="Stock Producer Service")

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

producer = KafkaProducer(
    bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_tick(symbol: str):
    return {
        "symbol": symbol,
        "price": round(random.uniform(100, 500), 2),
        "volume": random.randint(1000, 10000),
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/produce/{symbol}")
async def produce_tick(symbol: str):
    tick = generate_tick(symbol)
    producer.send("market.ticks", value=tick, key=symbol.encode('utf-8'))
    logger.info(f"Tick produced for {symbol}")
    return tick

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=config.STOCK_PRODUCER_PORT)
