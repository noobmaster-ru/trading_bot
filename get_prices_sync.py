import requests
import time
import csv
from datetime import datetime, UTC


def get_binance_price(symbol="BTCUSDT"):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        response = requests.get(url)
        if response.status_code == 200:
            resp_json = response.json()
            # print(float(resp_json.get("price")))
            return float(resp_json.get("price"))
    except Exception as e:
        print("error in get_binance_price")

def get_kucoin_price(symbol="BTC-USDT"):
    try:
        url = f"https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={symbol}"
        response = requests.get(url)
        if response.status_code == 200:
            resp_json = response.json()
            # print(float(resp_json.get("data").get("price")))
            return float(resp_json.get("data").get("price"))
    except Exception as e:
        print("error in get_kucoin_price")

def get_bybit_price(symbol="BTCUSDT"):
    try:
        url = f"https://api.bybit.com/v5/market/tickers?category=spot&symbol={symbol}"
        response = requests.get(url)
        if response.status_code == 200:
            resp_json = response.json()
            # print(resp_json)
            return float(resp_json["result"]["list"][0]["lastPrice"])
    except Exception as e:
        print("error in get_bybiy_price")

def get_okx_price(symbol="BTC-USDT"):
    try:
        url = f"https://www.okx.com/api/v5/market/ticker?instId={symbol}"
        response = requests.get(url)
        if response.status_code == 200:
            resp_json = response.json()
            # print(resp_json)
            return float(resp_json["data"][0]["last"])
    except Exception as e:
        print("error in get_okx_price")

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

    return {
        "time": datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S"),
        "Binance": prices["Binance"],
        "KuCoin": prices["KuCoin"],
        "Bybit": prices["Bybit"],
        "OKX": prices["OKX"],
        "min_exchange": min_exchange,
        "min_price": min_price,
        "max_exchange": max_exchange,
        "max_price": max_price,
        "diff_usd": diff,
        "diff_percent": diff_percent,
    }


if __name__ == "__main__":
    filename = "arbitrage_log_sync.csv"

    # создаём файл и пишем заголовок, если его ещё нет
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "time", "Binance", "KuCoin", "Bybit", "OKX",
            "min_exchange", "min_price",
            "max_exchange", "max_price",
            "diff_usd", "diff_percent"
        ])
        writer.writeheader()

    while True:
        try:
            data = check_arbitrage()

            # вывод в консоль
            print(f"[{data['time']}] "
                  f"Мин: {data['min_exchange']} {data['min_price']:.2f} | "
                  f"Макс: {data['max_exchange']} {data['max_price']:.2f} | "
                  f"Спред: {data['diff_usd']:.2f} USD ({data['diff_percent']:.4f}%)")
            
            # запись в CSV
            with open(filename, mode="a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=data.keys())
                writer.writerow(data)
            print("-" * 40)
            print("\n" * 8)

            time.sleep(5)  # опрос каждые 5 секунд
        except Exception as e:
            print("Ошибка:", e)
            time.sleep(5)