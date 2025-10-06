from fastapi import FastAPI
import requests
from datetime import datetime, timedelta, timezone

app = FastAPI()

BINANCE_BASE = "https://api.binance.com"

@app.get("/")
def home():
    return {"status": "ok", "msg": "Proxy running (UTC timestamps)"}

@app.get("/kline")
async def get_kline(symbol: str = "BTCUSDT", interval: str = "5m", limit: int = 1000):
    url = f"{BINANCE_BASE}/api/v3/klines"
    interval_minutes = {
        '1m': 1, '3m': 3, '5m': 5, '15m': 15, '30m': 30,
        '1h': 60, '2h': 120, '4h': 240, '6h': 360, '8h': 480, '12h': 720,
        '1d': 1440, '3d': 4320, '1w': 10080, '1M': 43200
    }
    
    minutes_back = limit * interval_minutes.get(interval, 5)
    # 🔹 Force UTC time
    now_utc = datetime.now(timezone.utc)
    start_time = int((now_utc - timedelta(minutes=minutes_back)).timestamp() * 1000)

    params = {"symbol": symbol, "interval": interval, "limit": limit, "startTime": start_time}
    r = requests.get(url, params=params)
    return r.json()

@app.get("/ticker")
async def get_ticker(symbol: str = "BTCUSDT"):
    url = f"{BINANCE_BASE}/api/v3/ticker/price"
    r = requests.get(url, params={"symbol": symbol})
    return r.json()
