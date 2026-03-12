import requests
import pandas as pd
from datetime import datetime

print("🚀 AfriTerminal MEGA Scraper Starting...")
print("=" * 50)

timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# =====================
# 1. CRYPTO PRICES (CoinGecko - Free, no API key)
# =====================
print("\n₿ Fetching Crypto prices...")
try:
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum,binancecoin,ripple,solana,cardano",
        "vs_currencies": "usd,ngn",
        "include_24hr_change": "true"
    }
    res = requests.get(url, params=params, timeout=10)
    crypto = res.json()
    
    crypto_rows = []
    names = {"bitcoin":"Bitcoin","ethereum":"Ethereum","binancecoin":"BNB","ripple":"XRP","solana":"Solana","cardano":"Cardano"}
    symbols = {"bitcoin":"BTC","ethereum":"ETH","binancecoin":"BNB","ripple":"XRP","solana":"SOL","cardano":"ADA"}
    
    for coin_id, info in crypto.items():
        crypto_rows.append({
            "Name": names.get(coin_id, coin_id),
            "Symbol": symbols.get(coin_id, coin_id),
            "Price USD": info.get("usd", 0),
            "Price NGN": info.get("ngn", 0),
            "24h Change %": round(info.get("usd_24h_change", 0), 2)
        })
    
    df_crypto = pd.DataFrame(crypto_rows)
    print(df_crypto.to_string())
    df_crypto.to_csv("crypto_data.csv", index=False)
    print("✅ Crypto data saved!")
except Exception as e:
    print(f"❌ Crypto error: {e}")

# =====================
# 2. COMMODITIES (free APIs)
# =====================
print("\n🛢️ Fetching Commodity prices...")
try:
    commodity_rows = []
    
    # Oil price via open API
    oil_res = requests.get("https://api.api-ninjas.com/v1/commodityprice?name=crude_oil", 
                          headers={"X-Api-Key": "free"}, timeout=10)
    
    # Use alternative free source - frankfurter for commodity ETFs approximation
    # Brent crude via commodity price API
    commodities_url = "https://query1.finance.yahoo.com/v8/finance/chart/BZ=F"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    tickers = {
        "BZ=F": {"name": "Brent Crude Oil", "unit": "USD/barrel"},
        "GC=F": {"name": "Gold", "unit": "USD/oz"},
        "CC=F": {"name": "Cocoa", "unit": "USD/tonne"},
        "NG=F": {"name": "Natural Gas", "unit": "USD/MMBtu"},
        "W=F":  {"name": "Wheat", "unit": "USD/bushel"},
    }
    
    for ticker, info in tickers.items():
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
            r = requests.get(url, headers=headers, timeout=10)
            data = r.json()
            price = data["chart"]["result"][0]["meta"]["regularMarketPrice"]
            prev = data["chart"]["result"][0]["meta"]["chartPreviousClose"]
            change = round(((price - prev) / prev) * 100, 2)
            commodity_rows.append({
                "Commodity": info["name"],
                "Ticker": ticker,
                "Price": round(price, 2),
                "Unit": info["unit"],
                "24h Change %": change
            })
            print(f"  ✅ {info['name']}: ${round(price,2)}")
        except Exception as e:
            print(f"  ⚠️ {ticker}: {e}")
    
    df_commodities = pd.DataFrame(commodity_rows)
    df_commodities.to_csv("commodities_data.csv", index=False)
    print("✅ Commodities saved!")
except Exception as e:
    print(f"❌ Commodities error: {e}")

# =====================
# 3. MORE AFRICAN EXCHANGES
# =====================
print("\n🌍 Fetching African Exchange data...")

exchanges = {
    "Ghana (GSE)": "https://www.african-markets.com/en/stock-markets/gse/listed-companies",
    "Kenya (NSE)": "https://www.african-markets.com/en/stock-markets/nse/listed-companies",
    "Egypt (EGX)": "https://www.african-markets.com/en/stock-markets/egx/listed-companies",
}

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}

from bs4 import BeautifulSoup
all_exchange_data = []

for exchange_name, url in exchanges.items():
    try:
        print(f"  📡 Fetching {exchange_name}...")
        res = requests.get(url, headers=headers, timeout=15)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            rows = soup.find_all("tr", class_="tabrow")
            companies = []
            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 3:
                    company = cols[0].get_text(strip=True)
                    # Skip header rows that got scraped as data rows
                    if company in ("Company", "Name", ""):
                        continue
                    companies.append({
                        "Exchange": exchange_name,
                        "Company": company,
                        "Sector": cols[1].get_text(strip=True),
                        "Price": cols[2].get_text(strip=True)
                    })
            all_exchange_data.extend(companies)
            print(f"  ✅ {exchange_name}: {len(companies)} companies")
        else:
            print(f"  ⚠️ {exchange_name}: Status {res.status_code}")
    except Exception as e:
        print(f"  ❌ {exchange_name}: {e}")

if all_exchange_data:
    df_exchanges = pd.DataFrame(all_exchange_data)
    df_exchanges.to_csv("african_exchanges.csv", index=False)
    print(f"✅ {len(all_exchange_data)} total companies across African exchanges saved!")

# =====================
# 4. MACRO DATA (World Bank - Free, no API key)
# =====================
print("\n📈 Fetching Macro economic data...")

macro_indicators = {
    "NY.GDP.MKTP.CD": "GDP (USD)",
    "FP.CPI.TOTL.ZG": "Inflation Rate %",
    "FR.INR.RINR": "Real Interest Rate %",
    "SL.UEM.TOTL.ZS": "Unemployment %",
    "BN.CAB.XOKA.GD.ZS": "Current Account % GDP",
}

countries = {
    "NG": "Nigeria",
    "GH": "Ghana", 
    "KE": "Kenya",
    "ZA": "South Africa",
    "EG": "Egypt",
    "ET": "Ethiopia",
}

macro_rows = []
for country_code, country_name in countries.items():
    for indicator_code, indicator_name in macro_indicators.items():
        try:
            url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}?format=json&mrv=1"
            res = requests.get(url, timeout=10)
            data = res.json()
            if len(data) > 1 and data[1] and data[1][0]["value"] is not None:
                value = data[1][0]["value"]
                year = data[1][0]["date"]
                macro_rows.append({
                    "Country": country_name,
                    "Indicator": indicator_name,
                    "Value": round(value, 2),
                    "Year": year
                })
        except Exception as e:
            print(f"  ⚠️ {country_code}/{indicator_code}: {e}")

if macro_rows:
    df_macro = pd.DataFrame(macro_rows)
    print(df_macro.to_string())
    df_macro.to_csv("macro_data.csv", index=False)
    print(f"\n✅ Macro data saved! ({len(macro_rows)} data points)")

print("\n" + "=" * 50)
print(f"🎉 MEGA SCRAPER COMPLETE — {timestamp}")
print("Files saved: crypto_data.csv, commodities_data.csv, african_exchanges.csv, macro_data.csv")
