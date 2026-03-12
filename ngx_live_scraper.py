import requests
import pandas as pd
from datetime import datetime

import os
API_KEY = os.environ.get("ITICK_API_KEY")
if not API_KEY:
    print("❌ ITICK_API_KEY environment variable not set. Skipping NGX live scrape.")
    exit(0)

headers = {"token": API_KEY}

NGX_STOCKS = [
    "DANGCEM","MTNN","ZENITHBA","ACCESSCORP","GTCO",
    "AIRTELAFRI","BUACEMENT","STANBIC","TRANSCORP","UBA",
    "FBNH","SEPLAT","OANDO","NB","NESTLE",
    "FLOURMILL","CADBURY","UNILEVER","WAPCO","PRESCO",
    "FIDSON","MAYBAKER","UNIVINSURE","MANSARD","CORNERST",
    "JAIZBANK","FIDELITYBK","FCMB","STERBANK","WEMABANK"
]

print("🚀 AfriTerminal — Live NGX Price Fetcher")
print(f"Fetching {len(NGX_STOCKS)} stocks from iTick API...")

results = []
for ticker in NGX_STOCKS:
    try:
        url = f"https://api.itick.org/stock/quote?region=NG&code={ticker}"
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()
        if data.get("data"):
            d = data["data"]
            results.append({
                "Ticker": ticker,
                "Price": d.get("p", 0),
                "Open": d.get("o", 0),
                "High": d.get("h", 0),
                "Low": d.get("l", 0),
                "Change": d.get("ch", 0),
                "Change%": d.get("chp", 0),
                "Volume": d.get("v", 0),
            })
            print(f"  ✅ {ticker}: ₦{d.get('p',0)} ({d.get('chp',0):+.2f}%)")
        else:
            print(f"  ⚠️ {ticker}: no data")
    except Exception as e:
        print(f"  ❌ {ticker}: {e}")

df = pd.DataFrame(results)
print(f"\n📊 Got {len(df)} stocks with live prices")
print(df.to_string())
df.to_csv("ngx_live_prices.csv", index=False)
print("\n💾 Saved to ngx_live_prices.csv")
