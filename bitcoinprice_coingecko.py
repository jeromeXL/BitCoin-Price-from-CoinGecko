import requests
import psycopg2
from datetime import datetime

# === 1. Fetch Bitcoin Price ===
def fetch_bitcoin_price():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin",
        "vs_currencies": "usd"
    }
    response = requests.get(url, params=params)
    data = response.json()
    return {
        "symbol": "BTC",
        "price": data["bitcoin"]["usd"],
        "scraped_at": datetime.utcnow(),
        "source": "coingecko"
    }

# === 2. Insert into Render DB ===
def save_to_db(price_data):
    conn = psycopg2.connect(
        dbname="bitcoinprice_hdmm",
        user="bitcoinprice_hdmm_user",
        password="0s1bwvj1fqvAbfhLFnhrKUqaQ6BJN5bz",  # Replace this with your Render DB password
        host="dpg-d22bmfre5dus739fn5h0-a.singapore-postgres.render.com",
        port="5432",
        sslmode="require"
    )
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO bitcoin_prices (symbol, price, scraped_at, source)
        VALUES (%s, %s, %s, %s)
    """, (
        price_data["symbol"],
        price_data["price"],
        price_data["scraped_at"],
        price_data["source"]
    ))
    conn.commit()
    cur.close()
    conn.close()
    print("Inserted into DB:", price_data)

# === 3. Run it ===
if __name__ == "__main__":
    data = fetch_bitcoin_price()
    save_to_db(data)
