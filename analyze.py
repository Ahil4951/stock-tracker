import sqlite3
import pandas as pd

conn = sqlite3.connect("stocks.db")
df = pd.read_sql("SELECT * FROM prices ORDER BY ticker, date", conn)
conn.close()

df["date"] = pd.to_datetime(df["date"])

# calculations are done separately for each stock
df["daily_change_pct"] = df.groupby("ticker")["close"].pct_change() * 100
df["ma_50"] = df.groupby("ticker")["close"].transform(lambda s: s.rolling(50).mean())
df["trend"] = (df["close"] > df["ma_50"]).map({True: "above MA", False: "below MA"})

latest = df.groupby("ticker").tail(1)[["ticker", "date", "close", "daily_change_pct", "ma_50", "trend"]].copy()
latest["date"] = latest["date"].dt.strftime("%Y-%m-%d")
print(latest.round(2).to_string(index=False))
import matplotlib.pyplot as plt

for ticker in df["ticker"].unique():
    s = df[df["ticker"] == ticker]
    plt.figure(figsize=(9, 5))
    plt.plot(s["date"], s["close"], label="Daily price (Rs)", linewidth=1.5)
    plt.plot(s["date"], s["ma_50"], label="50-day average", linewidth=2.5, linestyle="--")
    plt.title(f"{ticker}: last 1 year")
    plt.ylabel("Price in Rs")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.show()