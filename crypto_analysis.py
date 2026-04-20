"""
Crypto Coin Investment Analysis Tool
Author  : Austin (Data Analyst)
Company : Internal Analysis Team
Done    : 12 Feb 2026

Problem Statement:
    Scrape top 200 crypto coins from CoinMarketCap. Filter coins priced
    between $0-$5. From those, pick the top 10 by 1-hour price increase,
    then chart their 7-day-before price and 24-hour-before price side by side.

    Assumptions:
      - 1h  % change  → INCREASE  (positive direction assumed)
      - 7d  % change  → INCREASE  (positive direction assumed)
      - 24h % change  → DECREASE  (negative direction assumed)

Dependencies:
    pip install requests pandas matplotlib seaborn
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import json
from datetime import datetime


# ── 1. FETCH DATA FROM COINMARKETCAP ─────────────────────────────────────────

def fetch_cmc_data(limit: int = 200) -> pd.DataFrame:
    """
    Fetch the latest listings from CoinMarketCap public API.
    Replace CMC_API_KEY with your actual key from https://coinmarketcap.com/api/
    """
    CMC_API_KEY = "YOUR_CMC_API_KEY_HERE"   # ← paste your key here
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

    params = {
        "start"   : 1,
        "limit"   : limit,
        "convert" : "USD",
    }
    headers = {
        "Accepts"    : "application/json",
        "X-CMC_PRO_API_KEY": CMC_API_KEY,
    }

    response = requests.get(url, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    raw = response.json()["data"]

    rows = []
    for coin in raw:
        q = coin["quote"]["USD"]
        rows.append({
            "name"         : coin["name"],
            "symbol"       : coin["symbol"],
            "price"        : q.get("price", 0),
            "change_1h"    : q.get("percent_change_1h",  0),   # increase assumed
            "change_24h"   : q.get("percent_change_24h", 0),   # decrease assumed
            "change_7d"    : q.get("percent_change_7d",  0),   # increase assumed
        })

    return pd.DataFrame(rows)


# ── 2. DEMO / FALLBACK DATA (no API key needed) ───────────────────────────────

def demo_data() -> pd.DataFrame:
    """Synthetic data that mirrors real CMC structure for offline testing."""
    import random, math
    random.seed(42)

    names = [
        "Shiba Inu","Dogecoin","Floki","Baby Doge","SafeMoon",
        "Kishu Inu","Hoge Finance","Dogelon Mars","Akita Inu","Samoyedcoin",
        "BitTorrent","Stellar","Cardano","TRON","VeChain","Chiliz",
        "Holo","IOTA","Gala","Ankr","Coti","Render","Ocean Protocol",
        "Fetch.ai","Injective","Algorand","Hedera","Jasmy","eCash","STEPN"
    ]

    rows = []
    for i, name in enumerate(names):
        price    = round(random.uniform(0.00001, 4.99), 6)
        ch_1h    = round(random.uniform(0.1, 12.0),  2)  # increase
        ch_24h   = round(random.uniform(0.1, 15.0),  2)  # decrease (value is +ve, interpreted as drop)
        ch_7d    = round(random.uniform(0.5, 20.0),  2)  # increase
        rows.append({
            "name"      : name,
            "symbol"    : name[:3].upper(),
            "price"     : price,
            "change_1h" : ch_1h,
            "change_24h": ch_24h,
            "change_7d" : ch_7d,
        })

    # Add a few coins outside the $0-$5 range (should be filtered out)
    for name in ["Bitcoin","Ethereum","BNB","Solana","Avalanche"]:
        rows.append({
            "name": name, "symbol": name[:3].upper(),
            "price": round(random.uniform(10, 60000), 2),
            "change_1h": round(random.uniform(-5, 5), 2),
            "change_24h": round(random.uniform(-5, 5), 2),
            "change_7d": round(random.uniform(-5, 5), 2),
        })

    return pd.DataFrame(rows)


# ── 3. DERIVE HISTORICAL PRICES ───────────────────────────────────────────────

def derive_prices(df: pd.DataFrame) -> pd.DataFrame:
    """
    Back-calculate prices from percent changes (assumptions applied):
      price_7d_ago  = current_price / (1 + change_7d/100)   [7d was lower, 7d% is increase]
      price_24h_ago = current_price / (1 - change_24h/100)  [24h was higher, 24h% is decrease]
    """
    df = df.copy()
    df["price_7d_ago"]  = df["price"] / (1 + df["change_7d"]  / 100)
    df["price_24h_ago"] = df["price"] / (1 - df["change_24h"] / 100)
    return df


# ── 4. FILTER & RANK ──────────────────────────────────────────────────────────

def get_top10(df: pd.DataFrame) -> pd.DataFrame:
    """Filter $0–$5 coins, rank by 1h increase, take top 10."""
    filtered = df[(df["price"] >= 0) & (df["price"] <= 5)].copy()
    filtered = filtered.sort_values("change_1h", ascending=False)
    return filtered.head(10).reset_index(drop=True)


# ── 5. CHART ──────────────────────────────────────────────────────────────────

def plot_chart(top10: pd.DataFrame, save_path: str = "crypto_top10_chart.png"):
    sns.set_theme(style="darkgrid", palette="deep")
    fig, ax = plt.subplots(figsize=(14, 7))

    x      = range(len(top10))
    width  = 0.35
    labels = [f"{r['name']}\n({r['symbol']})" for _, r in top10.iterrows()]

    bars1 = ax.bar([i - width/2 for i in x], top10["price_7d_ago"],
                   width, label="Price 7 Days Ago",  color="#4E79A7", alpha=0.85)
    bars2 = ax.bar([i + width/2 for i in x], top10["price_24h_ago"],
                   width, label="Price 24 Hours Ago", color="#F28E2B", alpha=0.85)

    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel("Price (USD)", fontsize=11)
    ax.set_title(
        "Top 10 Crypto Coins (Price $0–$5) by 1-Hour Gain\n"
        "Comparing 7-Day-Before vs 24-Hour-Before Prices",
        fontsize=13, fontweight="bold", pad=14
    )
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("$%.4f"))
    ax.legend(fontsize=10)

    for bar in bars1:
        h = bar.get_height()
        ax.annotate(f"${h:.4f}", xy=(bar.get_x()+bar.get_width()/2, h),
                    xytext=(0, 3), textcoords="offset points",
                    ha="center", va="bottom", fontsize=7, color="#4E79A7")
    for bar in bars2:
        h = bar.get_height()
        ax.annotate(f"${h:.4f}", xy=(bar.get_x()+bar.get_width()/2, h),
                    xytext=(0, 3), textcoords="offset points",
                    ha="center", va="bottom", fontsize=7, color="#F28E2B")

    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    print(f"[✓] Chart saved → {save_path}")
    plt.show()


# ── 6. EXPORT CSV ─────────────────────────────────────────────────────────────

def export_csv(top10: pd.DataFrame, path: str = "crypto_top10_results.csv"):
    cols = ["name","symbol","price","change_1h","change_24h","change_7d",
            "price_7d_ago","price_24h_ago"]
    top10[cols].to_csv(path, index=False)
    print(f"[✓] CSV saved  → {path}")


# ── 7. MAIN ───────────────────────────────────────────────────────────────────

def main(use_demo: bool = True):
    print("=" * 60)
    print("  Crypto Investment Analysis — Austin, Data Analyst")
    print(f"  Run date : {datetime.now().strftime('%d %b %Y %H:%M')}")
    print("=" * 60)

    if use_demo:
        print("[i] Using demo data (set use_demo=False + add API key for live data)")
        df = demo_data()
    else:
        print("[i] Fetching live data from CoinMarketCap…")
        df = fetch_cmc_data(limit=200)

    df     = derive_prices(df)
    top10  = get_top10(df)

    print(f"\n[✓] Total coins fetched     : {len(df)}")
    print(f"[✓] Coins in $0–$5 range    : {len(df[(df.price >= 0) & (df.price <= 5)])}")
    print(f"[✓] Top 10 by 1h increase   :\n")
    print(top10[["name","symbol","price","change_1h","change_24h","change_7d"]].to_string(index=False))

    plot_chart(top10)
    export_csv(top10)
    print("\n[✓] Done.")


if __name__ == "__main__":
    main(use_demo=True)   # ← change to False for live CoinMarketCap data
