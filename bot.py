import ccxt
import pandas as pd
import requests
import time
import os

# --- APNA TOKEN AUR CHAT ID YAHAN DAALEIN ---
TELEGRAM_BOT_TOKEN = "9060232480:AAFRGbtRricegezkhR51SbVFMmch6v0kGKQ″
TELEGRAM_CHAT_ID = "5752602878"

exchange = ccxt.binance()

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    except Exception as e:
        print(f"Telegram Error: {e}")

def fetch_data(symbol):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe="1h", limit=100)
    return pd.DataFrame(ohlcv, columns=['time', 'open', 'high', 'low', 'close', 'vol'])

def check_smc(df, symbol):
    c1_high, c3_low = df['high'].iloc[-3], df['low'].iloc[-1]
    c1_low, c3_high = df['low'].iloc[-3], df['high'].iloc[-1]
    price = df['close'].iloc[-1]
    
    if c3_low > c1_high:
        return f"🟢 *BULLISH SMC SETUP (FVG)*\n\n📌 *Pair:* {symbol}\n💵 *Price:* ${price:.2f}\n🎯 *Zone:* {c1_high:.2f} - {c3_low:.2f}\n⏱ *Timeframe:* 1H"
    if c3_high < c1_low:
        return f"🔴 *BEARISH SMC SETUP (FVG)*\n\n📌 *Pair:* {symbol}\n💵 *Price:* ${price:.2f}\n🎯 *Zone:* {c3_high:.2f} - {c1_low:.2f}\n⏱ *Timeframe:* 1H"
    return None

def main():
    symbols = ["BTC/USDT", "ETH/USDT", "SOL/USDT"]
    print("SMC Bot Started...")
    send_telegram("🚀 *SMC Bot Cloud Par Active Ho Gaya Hai!*")
    sent = set()
    
    while True:
        try:
            for symbol in symbols:
                df = fetch_data(symbol)
                alert = check_smc(df, symbol)
                if alert and alert not in sent:
                    send_telegram(alert)
                    sent.add(alert)
            time.sleep(300)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
