import requests
import pandas as pd
from datetime import datetime

print("🚀 AfriTerminal - FX Rates Scraper Starting...")

url = "https://open.er-api.com/v6/latest/USD"
headers = {"User-Agent": "Mozilla/5.0"}

print("📡 Fetching live USD exchange rates...")
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    rates = data["rates"]
    
    # African currencies we care about
    african_currencies = ["NGN", "GHS", "KES", "ZAR", "EGP", "XOF", "ETB", "UGX", "TZS", "MAD"]
    
    rows = []
    for currency in african_currencies:
        if currency in rates:
            rows.append({
                "Currency": currency,
                "Rate vs USD": rates[currency],
                "Updated": data["time_last_update_utc"]
            })
    
    df = pd.DataFrame(rows)
    print(f"\n💱 Live African FX Rates (per 1 USD):\n")
    print(df.to_string())
    
    filename = f"fx_rates_{datetime.now().strftime('%Y%m%d')}.csv"
    df.to_csv(filename, index=False)
    print(f"\n💾 Saved to {filename}")
else:
    print(f"❌ Failed: {response.status_code}")
