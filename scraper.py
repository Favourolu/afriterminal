import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

print("🚀 AfriTerminal - NGX Data Scraper Starting...")

url = "https://www.african-markets.com/en/stock-markets/ngse/listed-companies"
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}

print("📡 Fetching NGX data...")
response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("✅ Connected successfully!")
    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.find_all("tr", class_="tabrow")
    
    companies = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 3:
            name = cols[0].get_text(strip=True)
            sector = cols[1].get_text(strip=True)
            price = cols[2].get_text(strip=True)
            companies.append({"Company": name, "Sector": sector, "Price": price})
    
    if companies:
        df = pd.DataFrame(companies)
        print(f"\n📊 Found {len(df)} companies on NGX\n")
        print(df.head(10).to_string())
        filename = f"ngx_data_{datetime.now().strftime('%Y%m%d')}.csv"
        df.to_csv(filename, index=False)
        print(f"\n💾 Data saved to {filename}")
    else:
        print("⚠️ No rows found")
else:
    print(f"❌ Failed: {response.status_code}")
