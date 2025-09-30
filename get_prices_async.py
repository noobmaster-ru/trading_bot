import aiohttp
import asyncio
import time
import csv
from datetime import datetime, UTC


async def get_price(session, url, path):
    async with session.get(url) as resp:
        data = await resp.json()
        return path(data)


async def fetch_all():
    async with aiohttp.ClientSession() as session:
        tasks = [
            get_price(session, "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",
                      lambda d: float(d["price"])),
            get_price(session, "https://api.kucoin.com/api/v1/market/orderbook/level1?symbol=BTC-USDT",
                      lambda d: float(d["data"]["price"])),
            get_price(session, "https://api.bybit.com/v5/market/tickers?category=spot&symbol=BTCUSDT",
                      lambda d: float(d["result"]["list"][0]["lastPrice"])),
            get_price(session, "https://www.okx.com/api/v5/market/ticker?instId=BTC-USDT",
                      lambda d: float(d["data"][0]["last"])),
        ]
        results = await asyncio.gather(*tasks)
        return {"Binance": results[0], "KuCoin": results[1], "Bybit": results[2], "OKX": results[3]}

async def main():
    filename = "arbitrage_log_async.csv"
    fieldnames = [
        "time", "Binance", "KuCoin", "Bybit", "OKX",
        "min_exchange", "min_price", "max_exchange", "max_price",
        "diff_usd", "diff_percent"
    ]

    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=fieldnames).writeheader()

    while True:
        try:
            prices = await fetch_all()

            min_exchange = min(prices, key=prices.get)
            max_exchange = max(prices, key=prices.get)
            min_price = prices[min_exchange]
            max_price = prices[max_exchange]

            diff = max_price - min_price
            diff_percent = diff / min_price * 100

            data = {
                "time": datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S"),
                **prices,
                "min_exchange": min_exchange,
                "min_price": min_price,
                "max_exchange": max_exchange,
                "max_price": max_price,
                "diff_usd": diff,
                "diff_percent": diff_percent,
            }

            print(f"[{data['time']}] "
                  f"Мин: {min_exchange} {min_price:.2f} | "
                  f"Макс: {max_exchange} {max_price:.2f} | "
                  f"Спред: {diff:.2f} USD ({diff_percent:.4f}%)")

            with open(filename, mode="a", newline="", encoding="utf-8") as f:
                csv.DictWriter(f, fieldnames=fieldnames).writerow(data)

            await asyncio.sleep(0.5)  # можно опрашивать раз в 1 сек
        except Exception as e:
            print("Ошибка:", e)
            await asyncio.sleep(3)

if __name__ == "__main__":
    asyncio.run(main())

