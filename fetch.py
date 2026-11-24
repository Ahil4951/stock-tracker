import sqlite3
import yfinance as yf

TICKERS = ["TCS.NS", "RELIANCE.NS", "INFY.NS", "HDFCBANK.NS"]

conn = sqlite3.connect("stocks.db")
conn.execute("""
    CREATE TABLE IF NOT EXISTS prices (
        ticker TEXT,
        date TEXT,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        volume INTEGER,
        PRIMARY KEY (ticker, date)
    )
""")

for ticker in TICKERS:
    df = yf.Ticker(ticker).history(period="1y")
    if df.empty:
        print(f"No data for {ticker}")
        continue
    for date, row in df.iterrows():
        conn.execute(
            "INSERT OR REPLACE INTO prices VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                ticker,
                date.strftime("%Y-%m-%d"),
                row["Open"],
                row["High"],
                row["Low"],
                row["Close"],
                int(row["Volume"]),
            ),
        )
    conn.commit()
    print(f"Saved {len(df)} rows for {ticker}")

print("--- Stored in database ---")
for row in conn.execute("SELECT ticker, COUNT(*) FROM prices GROUP BY ticker"):
    print(row)

conn.close()