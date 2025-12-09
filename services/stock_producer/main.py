from fastapi import FastAPI, BackgroundTasks
from kafka import KafkaProducer
import json
import asyncio
import aiohttp
from datetime import datetime
from prometheus_client import make_asgi_app
from libs.utils.logging import setup_logger
from libs.utils.config import config
import os

logger = setup_logger("stock-producer")
app = FastAPI(title="Stock Producer Service")

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Alpha Vantage configuration
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "AZRFGV343I9NG93H")
ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"

# Kafka producer
producer = KafkaProducer(
    bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Stock symbols to track
SYMBOLS = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]

# Cache for stock data
stock_cache = {}
is_streaming = False

async def fetch_stock_quote(session: aiohttp.ClientSession, symbol: str):
    """Fetch real-time stock quote from Alpha Vantage"""
    try:
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": ALPHA_VANTAGE_API_KEY
        }
        
        async with session.get(ALPHA_VANTAGE_BASE_URL, params=params) as response:
            if response.status == 200:
                data = await response.json()
                
                if "Global Quote" in data and data["Global Quote"]:
                    quote = data["Global Quote"]
                    
                    tick = {
                        "symbol": symbol,
                        "price": float(quote.get("05. price", 0)),
                        "open": float(quote.get("02. open", 0)),
                        "high": float(quote.get("03. high", 0)),
                        "low": float(quote.get("04. low", 0)),
                        "volume": int(quote.get("06. volume", 0)),
                        "change": float(quote.get("09. change", 0)),
                        "change_percent": quote.get("10. change percent", "0%"),
                        "timestamp": datetime.utcnow().isoformat(),
                        "source": "alpha_vantage"
                    }
                    
                    # Update cache
                    stock_cache[symbol] = tick
                    
                    # Send to Kafka
                    producer.send("market.ticks", value=tick, key=symbol.encode('utf-8'))
                    logger.info(f"Real tick produced for {symbol}: ${tick['price']}")
                    
                    return tick
                else:
                    logger.warning(f"No data returned for {symbol}: {data}")
                    return None
            else:
                logger.error(f"API error for {symbol}: {response.status}")
                return None
                
    except Exception as e:
        logger.error(f"Error fetching {symbol}: {str(e)}")
        return None

async def fetch_intraday_data(session: aiohttp.ClientSession, symbol: str):
    """Fetch intraday data for more frequent updates"""
    try:
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol,
            "interval": "1min",
            "apikey": ALPHA_VANTAGE_API_KEY
        }
        
        async with session.get(ALPHA_VANTAGE_BASE_URL, params=params) as response:
            if response.status == 200:
                data = await response.json()
                
                if "Time Series (1min)" in data:
                    time_series = data["Time Series (1min)"]
                    latest_time = list(time_series.keys())[0]
                    latest_data = time_series[latest_time]
                    
                    tick = {
                        "symbol": symbol,
                        "price": float(latest_data.get("4. close", 0)),
                        "open": float(latest_data.get("1. open", 0)),
                        "high": float(latest_data.get("2. high", 0)),
                        "low": float(latest_data.get("3. low", 0)),
                        "volume": int(latest_data.get("5. volume", 0)),
                        "timestamp": latest_time,
                        "source": "alpha_vantage_intraday"
                    }
                    
                    stock_cache[symbol] = tick
                    producer.send("market.ticks", value=tick, key=symbol.encode('utf-8'))
                    logger.info(f"Intraday tick for {symbol}: ${tick['price']}")
                    
                    return tick
                    
    except Exception as e:
        logger.error(f"Error fetching intraday for {symbol}: {str(e)}")
        return None

async def stream_stock_data():
    """Background task to continuously stream stock data"""
    global is_streaming
    
    async with aiohttp.ClientSession() as session:
        while is_streaming:
            for symbol in SYMBOLS:
                # Fetch quote data
                await fetch_stock_quote(session, symbol)
                
                # Alpha Vantage has rate limits (5 calls/min for free tier)
                # Wait between calls
                await asyncio.sleep(12)  # 5 symbols * 12 sec = 60 sec (5 calls/min)
            
            logger.info("Completed one cycle of all symbols")

@app.post("/start-stream")
async def start_stream(background_tasks: BackgroundTasks):
    """Start streaming real-time stock data"""
    global is_streaming
    
    if is_streaming:
        return {"status": "already_streaming"}
    
    is_streaming = True
    background_tasks.add_task(stream_stock_data)
    logger.info("Started stock data streaming")
    
    return {"status": "streaming_started", "symbols": SYMBOLS}

@app.post("/stop-stream")
async def stop_stream():
    """Stop streaming stock data"""
    global is_streaming
    is_streaming = False
    logger.info("Stopped stock data streaming")
    
    return {"status": "streaming_stopped"}

@app.get("/stream-status")
async def stream_status():
    """Check streaming status"""
    return {
        "is_streaming": is_streaming,
        "symbols": SYMBOLS,
        "cached_data": stock_cache
    }

@app.post("/produce/{symbol}")
async def produce_tick(symbol: str):
    """Manually fetch and produce a tick for a specific symbol"""
    async with aiohttp.ClientSession() as session:
        tick = await fetch_stock_quote(session, symbol)
        
        if tick:
            return tick
        else:
            return {"error": "Failed to fetch data", "symbol": symbol}

@app.get("/quote/{symbol}")
async def get_quote(symbol: str):
    """Get the latest cached quote for a symbol"""
    if symbol in stock_cache:
        return stock_cache[symbol]
    else:
        # Fetch fresh data
        async with aiohttp.ClientSession() as session:
            tick = await fetch_stock_quote(session, symbol)
            return tick if tick else {"error": "No data available"}

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "streaming": is_streaming,
        "symbols_tracked": len(SYMBOLS)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=config.STOCK_PRODUCER_PORT)
