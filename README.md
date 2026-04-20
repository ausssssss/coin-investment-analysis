# 📊 Crypto Coin Investment Analysis

**Author:** Austin | Data Analyst  
**Completed:** 12 February 2026  
**Source:** CoinMarketCap (Top 200 Coins)

---

## 📌 Problem Statement

Investors need quick insight into short-term crypto price movements.  
The analysis team scrapes **200 crypto coins** from CoinMarketCap and:

1. Filters coins priced between **$0 and $5 (inclusive)**
2. Identifies the **Top 10** coins by **1-hour price increase**
3. Plots their **7-day-before price** vs **24-hour-before price** side-by-side

### Assumptions

| Metric | Direction |
|--------|-----------|
| 1h % change | ↑ Increase |
| 24h % change | ↓ Decrease |
| 7d % change | ↑ Increase |

---

## 🗂️ Project Structure

```
crypto-analysis/
├── crypto_analysis.py        # Main script (scrape → filter → chart → export)
├── crypto_top10_results.csv  # Output: top 10 coins data
├── crypto_top10_chart.png    # Output: bar chart
├── requirements.txt          # Python dependencies
└── README.md
```

---

## ⚙️ Setup

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/crypto-analysis.git
cd crypto-analysis

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Add your CoinMarketCap API key
#    Edit crypto_analysis.py → line: CMC_API_KEY = "YOUR_CMC_API_KEY_HERE"
#    Get a free key at: https://coinmarketcap.com/api/

# 4. Run
python crypto_analysis.py
```

> **No API key?** The script runs with built-in demo data by default (`use_demo=True`).  
> Set `use_demo=False` in `main()` to use live CoinMarketCap data.

---

## 📈 Output

### Chart
A grouped bar chart showing **7-day-before price** (blue) vs **24-hour-before price** (orange)  
for the **Top 10 coins** ranked by 1-hour gain within the $0–$5 price range.

### CSV
`crypto_top10_results.csv` with columns:

| Column | Description |
|--------|-------------|
| name | Coin name |
| symbol | Ticker symbol |
| price | Current price (USD) |
| change_1h | 1-hour % change (increase) |
| change_24h | 24-hour % change (decrease) |
| change_7d | 7-day % change (increase) |
| price_7d_ago | Back-calculated price 7 days ago |
| price_24h_ago | Back-calculated price 24 hours ago |

---

## 🧮 Price Derivation Logic

```
price_7d_ago  = current_price ÷ (1 + change_7d  / 100)
price_24h_ago = current_price ÷ (1 − change_24h / 100)
```

---

## 📦 Dependencies

```
requests
pandas
matplotlib
seaborn
```

---

## 🔗 Data Source

- **CoinMarketCap API:** https://coinmarketcap.com/api/
- Free tier: 10,000 credits/month (sufficient for daily runs)

---

## 📄 License

MIT License — free to use and modify.
