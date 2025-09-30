import requests
import time

def get_binance_price(symbol="BTCUSDT"):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        response = requests.get(url)
        if response.status_code == 200:
            resp_json = response.json()
            print(float(resp_json.get("price")))
            return float(resp_json.get("price"))
    except Exception as e:
        print("erro in get_binance_price")

def get_kucoin_price(symbol="BTC-USDT"):
    try:
        url = f"https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={symbol}"
        response = requests.get(url)
        if response.status_code == 200:
            resp_json = response.json()
            print(float(resp_json.get("data").get("price")))
            return float(resp_json.get("data").get("price"))
    except Exception as e:
        print("erro in get_kucoin_price")

def check_arbitrage():
    binance_price = get_binance_price()
    kucoin_price = get_kucoin_price()

    diff = kucoin_price - binance_price
    diff_percent = diff / binance_price * 100

    print(f"Binance: {binance_price:.2f} | KuCoin: {kucoin_price:.2f} | Разница: {diff:.2f} USD ({diff_percent:.2f}%)")

if __name__ == "__main__":
    while True:
        try:
            check_arbitrage()
            time.sleep(3)  # опрос каждые 3 секунды
        except Exception as e:
            print("Ошибка:", e)
            time.sleep(5)