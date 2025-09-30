import pandas as pd
import matplotlib.pyplot as plt

# читаем CSV
df = pd.read_csv("arbitrage_log_async.csv")

# переводим колонку времени в datetime
df["time"] = pd.to_datetime(df["time"])

# строим график
plt.figure(figsize=(12,6))
plt.plot(df["time"], df["diff_percent"], marker="o", linestyle="-", markersize=3)

plt.title("Арбитражный спред BTC/USDT между биржами (%)")
plt.xlabel("Время (UTC)")
plt.ylabel("Разница (%)")
plt.grid(True)
plt.savefig(f"plot_async_{df["time"]}.jpg")
plt.tight_layout()
plt.show()
