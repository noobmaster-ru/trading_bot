import requests
import time
import csv
from datetime import datetime

def get_binance_price(symbol="BTCUSDT"):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        response = requests.get(url)
        if response.status_code == 200:
            resp_json = response.json()
            # print(float(resp_json.get("price")))
            return float(resp_json.get("price"))
    except Exception as e:
        print("erro in get_binance_price")

def get_kucoin_price(symbol="BTC-USDT"):
    try:
        url = f"https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={symbol}"
        response = requests.get(url)
        if response.status_code == 200:
            resp_json = response.json()
            # print(float(resp_json.get("data").get("price")))
            return float(resp_json.get("data").get("price"))
    except Exception as e:
        print("erro in get_kucoin_price")

def get_bybit_price(symbol="BTCUSDT"):
    try:
        url = f"https://api.bybit.com/v5/market/tickers?category=spot&symbol={symbol}"
        response = requests.get(url)
        if response.status_code == 200:
            resp_json = response.json()
            # print(resp_json)
            return float(resp_json["result"]["list"][0]["lastPrice"])
    except Exception as e:
        print("erro in get_bybiy_price")

def get_okx_price(symbol="BTC-USDT"):
    try:
        url = f"https://www.okx.com/api/v5/market/ticker?instId={symbol}"
        response = requests.get(url)
        if response.status_code == 200:
            resp_json = response.json()
            # print(resp_json)
            return float(resp_json["data"][0]["last"])
    except Exception as e:
        print("erro in get_okx_price")

def check_arbitrage():
    prices = {
        "Binance": get_binance_price(),
        "KuCoin": get_kucoin_price(),
        "Bybit": get_bybit_price(),
        "OKX": get_okx_price(),
    }

    min_exchange = min(prices, key=prices.get)
    max_exchange = max(prices, key=prices.get)

    min_price = prices[min_exchange]
    max_price = prices[max_exchange]

    diff = max_price - min_price
    diff_percent = diff / min_price * 100

    print("=== Текущие цены ===")
    for exch, price in prices.items():
        print(f"{exch}: {price:.2f}")

    print(f"\nДешевле всего: {min_exchange} ({min_price:.2f})")
    print(f"Дороже всего: {max_exchange} ({max_price:.2f})")
    print(f"Потенциальный спред: {diff:.2f} USD ({diff_percent:.4f}%)")
    print("-" * 40)
    print("\n" * 8)

if __name__ == "__main__":
    while True:
        try:
            check_arbitrage()
            time.sleep(5)  # опрос каждые 3 секунды
        except Exception as e:
            print("Ошибка:", e)
            time.sleep(5)