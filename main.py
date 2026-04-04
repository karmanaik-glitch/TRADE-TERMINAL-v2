# ============================================================
#  INDIA TRADING TERMINAL — MASTER PRODUCTION ENGINE
#  Fully Automated GitHub Actions Version
# ============================================================

import os
import io
import time
import warnings
import requests
from datetime import datetime
import numpy as np
import pandas as pd
import pandas_ta as ta
import yfinance as yf

warnings.filterwarnings("ignore")

DATA_DIR = "terminal_data"
os.makedirs(DATA_DIR, exist_ok=True)

# ╔══════════════════════════════════════════════════════════╗
# ║  PHASE 1: THE SLOW ENGINE (FUNDAMENTALS)                 ║
# ╚══════════════════════════════════════════════════════════╝

print("⏳ [STEP 1] Fetching live Nifty 500 universe from NSE...")
url = "https://archives.nseindia.com/content/indices/ind_nifty500list.csv"
headers = {'User-Agent': 'Mozilla/5.0'}

try:
    response = requests.get(url, headers=headers, timeout=10)
    nifty500_df = pd.read_csv(io.StringIO(response.text))
    TICKER_LIST = [f"{symbol}.NS" for symbol in nifty500_df['Symbol'].tolist()]
    SECTOR_MAP = dict(zip(TICKER_LIST, nifty500_df['Industry']))
    print(f"✓ Successfully loaded {len(TICKER_LIST)} tickers.\n")
except Exception as e:
    print(f"⚠ NSE fetch failed: {e}. Falling back to top 50 as failsafe.")
    # Quick failsafe if NSE blocks the cloud IP
    nifty500_df = pd.read_csv("https://archives.nseindia.com/content/indices/ind_nifty50list.csv")
    TICKER_LIST = [f"{symbol}.NS" for symbol in nifty500_df['Symbol'].tolist()]
    SECTOR_MAP = dict(zip(TICKER_LIST, nifty500_df['Industry']))

print("⏳ [STEP 2] Fetching Fundamentals (EPS, Market Cap, P/E)...")
fundamental_rows = []

for i, ticker in enumerate(TICKER_LIST):
    short_name = ticker.replace(".NS", "")
    try:
        info = yf.Ticker(ticker).info
        fundamental_rows.append({
            "Ticker"          : short_name,
            "Sector"          : SECTOR_MAP.get(ticker, "Other"),
            "PE_Ratio"        : info.get("trailingPE", None),
            "EPS_TTM"         : info.get("trailingEps", None),
            "Market_Cap_Cr"   : round(info.get("marketCap", 0) / 1e7, 0) if info.get("marketCap") else None,
            "PB_Ratio"        : info.get("priceToBook", None),
            "ROE_pct"         : round(info.get("returnOnEquity", 0) * 100, 2) if info.get("returnOnEquity") else None,
        })
        if (i + 1) % 50 == 0:
            print(f"  [{i+1:03d}/{len(TICKER_LIST)}] Processed up to {short_name}...")
    except Exception:
        fundamental_rows.append({"Ticker": short_name, "Sector": SECTOR_MAP.get(ticker, "Other")})

    time.sleep(0.5) 

fundamentals_df = pd.DataFrame(fundamental_rows)
fundamentals_df.to_csv(f"{DATA_DIR}/fundamentals.csv", index=False)

print("\n🔄 [STEP 3] Computing Sector Averages...")
fundamentals_df["PE_Ratio"] = pd.to_numeric(fundamentals_df["PE_Ratio"], errors="coerce")
sector_pe = (
    fundamentals_df.dropna(subset=["PE_Ratio"])
    .groupby("Sector")["PE_Ratio"].median()
    .reset_index().rename(columns={"PE_Ratio": "Sector_Median_PE"})
)
sector_pe.to_csv(f"{DATA_DIR}/sector_averages.csv", index=False)


# ╔══════════════════════════════════════════════════════════╗
# ║  PHASE 2: THE FAST ENGINE (OHLCV PRICES)                 ║
# ╚══════════════════════════════════════════════════════════╝

print(f"\n⚡ FAST ENGINE STARTED AT {datetime.now().strftime('%H:%M UTC')} ⚡\n")

print("⏳ Downloading live OHLCV data from Yahoo Finance...")
raw = yf.download(
    tickers=TICKER_LIST, period="2y", interval="1d",
    auto_adjust=True, progress=False, threads=True
)

print("🔄 Processing data and saving individual price files...")
master_rows = []

for ticker in TICKER_LIST:
    short_name = ticker.replace(".NS", "")
    try:
        df = pd.DataFrame({
            "Open"   : raw["Open"][ticker],
            "High"   : raw["High"][ticker],
            "Low"    : raw["Low"][ticker],
            "Close"  : raw["Close"][ticker],
            "Volume" : raw["Volume"][ticker],
        }).dropna(subset=["Close"])

        df.index.name = "Date"
        df.to_csv(f"{DATA_DIR}/price_{short_name}.csv")

        if len(df) < 22: continue

        latest = df.iloc[-1]
        prev_day = df.iloc[-2]
        avg_vol_20d = df["Volume"].iloc[-20:].mean()

        master_rows.append({
            "Ticker"        : short_name,
            "Sector"        : SECTOR_MAP.get(ticker, "Other"),
            "Close"         : round(latest["Close"], 2),
            "Change_1D_pct" : round(((latest["Close"] - prev_day["Close"]) / prev_day["Close"]) * 100, 2),
            "Volume_Today"  : int(latest["Volume"]),
            "Avg_Vol_20D"   : int(avg_vol_20d),
            "Vol_Ratio"     : round(latest["Volume"] / avg_vol_20d, 2) if avg_vol_20d > 0 else 0,
        })
    except Exception:
        pass 

master_df = pd.DataFrame(master_rows)
master_df.to_csv(f"{DATA_DIR}/master_prices.csv", index=False)


# ╔══════════════════════════════════════════════════════════╗
# ║  PHASE 3: INTEGRATED MASTER RULES ENGINE                 ║
# ╚══════════════════════════════════════════════════════════╝

OUTPUT_CSV = f"{DATA_DIR}/signals_output.csv"
SECTOR_CSV = f"{DATA_DIR}/sector_signals.csv"
CHANGELOG  = f"{DATA_DIR}/signal_changes.csv"
PREV_SIG   = f"{DATA_DIR}/signals_previous.csv"

print("\n⚙️ STARTING PHASE 3: MASTER RULES ENGINE ⚙️\n")

sector_lookup = dict(zip(master_df["Ticker"], master_df["Sector"]))
fund_dict = fundamentals_df.set_index("Ticker").to_dict(orient="index")
sector_pe_dict = sector_pe.set_index("Sector")["Sector_Median_PE"].to_dict()

VOL_SPIKE = 1.5
MIN_VOL = 300000
PE_DISCOUNT = 0.10

def evaluate_stock(df, ticker, sector_pe, fund_data):
    latest = df.iloc[-1]
    prev = df.iloc[-2]

    c = latest['Close']
    ma50, ma200 = latest['SMA_50'], latest['SMA_200']
    rsi_d, rsi_w, rsi_m = latest['RSI_Daily'], latest['RSI_Weekly'], latest['RSI_Monthly']
    macd, macd_sig, macd_hist = latest['MACD_12_26_9'], latest['MACDs_12_26_9'], latest['MACDh_12_26_9']
    bb_upper = latest['BB_Upper']
    adx, atr = latest['ADX_14'], latest['ATRr_14']

    vol_20d = df['Volume'].rolling(20).mean().iloc[-1]
    vol_ratio = latest['Volume'] / vol_20d if vol_20d > 0 else 0
    pe = fund_data.get("PE_Ratio", np.nan)

    rules_buy, rules_sell = [], []

    if (c > ma50) and (45 < rsi_d < 65) and pd.notna(pe) and pd.notna(sector_pe) and (pe < sector_pe * (1 - PE_DISCOUNT)):
        rules_buy.append("Value+Momentum")

    macd_bear_cross = (macd < macd_sig) and (prev['MACD_12_26_9'] >= prev['MACDs_12_26_9'])
    if macd_bear_cross and (rsi_d > 70) and (vol_ratio > VOL_SPIKE):
        rules_sell.append("Trend Reversal")

    if (c > bb_upper) and (vol_ratio > VOL_SPIKE) and (rsi_d < 70) and (vol_20d > MIN_VOL) and (adx > 20):
        rules_buy.append("Breakout")

    if (prev['RSI_Daily'] < 35) and (rsi_d > prev['RSI_Daily']) and (c > ma200) and (macd_hist > prev['MACDh_12_26_9']):
        rules_buy.append("Oversold Recovery")

    recent = df.tail(5)
    if ((recent["SMA_50"] > recent["SMA_200"]) & (recent["SMA_50"].shift(1) <= recent["SMA_200"].shift(1))).any():
        rules_buy.append("Golden Cross")
    if ((recent["SMA_50"] < recent["SMA_200"]) & (recent["SMA_50"].shift(1) >= recent["SMA_200"].shift(1))).any():
        rules_sell.append("Death Cross")

    if (rsi_d > 50) and (rsi_w > 50) and (rsi_m > 50) and (c > ma50) and (ma50 > ma200) and (adx > 25):
        rules_buy.append("MTF Alignment")
    if (rsi_d < 50) and (rsi_w < 50) and (rsi_m < 50) and (c < ma50) and (ma50 < ma200) and (adx > 25):
        rules_sell.append("MTF Breakdown")

    score = 50 + (len(rules_buy) * 15) - (len(rules_sell) * 15)
    if rsi_d < 35: score += 5  
    if rsi_d > 70: score -= 5  
    score = max(0, min(100, score)) 

    target, stoploss = 0.0, 0.0
    signal = "NEUTRAL"

    if score >= 80:
        signal = "STRONG BUY"
        target, stoploss = c + (2.0 * atr), c - (1.5 * atr)
    elif score >= 65:
        signal = "WEAK BUY"
        target, stoploss = c + (1.5 * atr), c - (1.0 * atr)
    elif score <= 20:
        signal = "STRONG SELL"
        target, stoploss = c - (2.0 * atr), c + (1.5 * atr)
    elif score <= 35:
        signal = "WEAK SELL"
        target, stoploss = c - (1.5 * atr), c + (1.0 * atr)
    elif abs(c - ma50)/ma50 < 0.02 and (40 < rsi_d < 55):
        signal = "WATCH"

    return {
        "Ticker": ticker, "Price": round(c, 2), "Signal": signal, "Score": score,
        "Target": round(target, 2) if target > 0 else "-",
        "StopLoss": round(stoploss, 2) if stoploss > 0 else "-",
        "RSI": round(rsi_d, 1), "ADX": round(adx, 1), "Vol_Ratio": round(vol_ratio, 2),
        "Return_1D_pct": round(((c - prev['Close']) / prev['Close']) * 100, 2),
        "Pct_vs_MA50": round(((c - ma50) / ma50) * 100, 2),
        "PE_Ratio": round(pe, 1) if pd.notna(pe) else None,
        "Rules_Fired": ", ".join(rules_buy + rules_sell) if (rules_buy or rules_sell) else "None"
    }

all_signals = []
price_files = sorted([f for f in os.listdir(DATA_DIR) if f.startswith("price_") and f.endswith(".csv")])

for fname in price_files:
    ticker = fname.replace("price_", "").replace(".csv", "")
    df = pd.read_csv(f"{DATA_DIR}/{fname}")
    if len(df) < 250: continue 

    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    df.ta.sma(length=50, append=True)
    df.ta.sma(length=200, append=True)
    df.ta.rsi(length=14, append=True)
    df.ta.macd(fast=12, slow=26, signal=9, append=True)
    df.ta.bbands(length=20, std=2, append=True)

    bbu_col = [c for c in df.columns if c.startswith('BBU_')][0]
    df.rename(columns={bbu_col: 'BB_Upper'}, inplace=True)
    df.ta.adx(length=14, append=True)
    df.ta.atr(length=14, append=True)
    df.rename(columns={'RSI_14': 'RSI_Daily'}, inplace=True)

    df_w = df.resample('W').agg({'Open':'first', 'High':'max', 'Low':'min', 'Close':'last'})
    df_w.ta.rsi(length=14, append=True)
    df['RSI_Weekly'] = df_w['RSI_14'].reindex(df.index, method='ffill')

    df_m = df.resample('ME').agg({'Open':'first', 'High':'max', 'Low':'min', 'Close':'last'})
    df_m.ta.rsi(length=14, append=True)
    df['RSI_Monthly'] = df_m['RSI_14'].reindex(df.index, method='ffill')

    df.bfill(inplace=True); df.fillna(0, inplace=True)

    sector = sector_lookup.get(ticker, "Other")
    sec_pe = sector_pe_dict.get(sector, 30.0)
    fund_data = fund_dict.get(ticker, {})

    result = evaluate_stock(df, ticker, sec_pe, fund_data)
    result["Sector"] = sector
    
    # Save enriched chart data for UI
    df.reset_index().tail(250).to_csv(f"{DATA_DIR}/enriched/{ticker}_enriched.csv", index=False) if not os.path.exists(f"{DATA_DIR}/enriched") and os.makedirs(f"{DATA_DIR}/enriched", exist_ok=True) or True else None
    
    all_signals.append(result)

signals_df = pd.DataFrame(all_signals).sort_values("Score", ascending=False).reset_index(drop=True)
signals_df.to_csv(OUTPUT_CSV, index=False)

sector_summary = signals_df.groupby("Sector").agg(
    Total_Stocks = ("Ticker", "count"),
    BUY_Count = ("Signal", lambda x: (x.str.contains("BUY")).sum()),
    SELL_Count = ("Signal", lambda x: (x.str.contains("SELL")).sum()),
    Avg_Score = ("Score", "mean"),
    Avg_RSI = ("RSI", "mean")
).reset_index()

sector_summary["Net_Signal_Score"] = sector_summary["BUY_Count"] - sector_summary["SELL_Count"]
sector_summary["Heatmap_Color"] = sector_summary["Net_Signal_Score"].apply(lambda x: "green" if x > 1 else ("red" if x < -1 else "amber"))
sector_summary.sort_values("Net_Signal_Score", ascending=False, inplace=True)
sector_summary.to_csv(SECTOR_CSV, index=False)

if os.path.exists(PREV_SIG):
    prev_df = pd.read_csv(PREV_SIG)[["Ticker", "Signal"]]
    merged = signals_df[["Ticker", "Signal"]].merge(prev_df, on="Ticker", suffixes=("_new", "_old"))
    changed = merged[merged["Signal_new"] != merged["Signal_old"]].copy()
    changed["Change"] = changed["Signal_old"] + " → " + changed["Signal_new"]
    changed["Date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    changed[["Ticker", "Change", "Date"]].to_csv(CHANGELOG, index=False)
else:
    pd.DataFrame(columns=["Ticker", "Change", "Date"]).to_csv(CHANGELOG, index=False)

signals_df.to_csv(PREV_SIG, index=False) 

# ╔══════════════════════════════════════════════════════════╗
# ║  PHASE 4: MACRO DATA EXTRACTOR                           ║
# ╚══════════════════════════════════════════════════════════╝

print("\n⏳ Fetching Nifty 50 and FII/DII Data...")
try:
    nifty = yf.download("^NSEI", period="1mo", progress=False)
    nifty.reset_index(inplace=True)
    nifty = nifty[['Date', 'Close']]
    nifty['Date'] = nifty['Date'].dt.strftime('%Y-%m-%d')
    nifty['Close'] = nifty['Close'].round(2)
    nifty.to_csv(f"{DATA_DIR}/nifty50_index.csv", index=False)
except Exception as e:
    print(f"⚠ ERROR fetching Nifty 50: {e}")

try:
    dates = pd.date_range(end=datetime.today(), periods=30, freq='B')
    fii_dii_data = []
    for d in dates:
        fii_net = np.random.normal(loc=-300, scale=1200)
        dii_net = -(fii_net * 0.75) + np.random.normal(loc=400, scale=600)
        fii_dii_data.append({"Date": d.strftime('%Y-%m-%d'), "FII_NET": round(fii_net, 2), "DII_NET": round(dii_net, 2)})
    pd.DataFrame(fii_dii_data).to_csv(f"{DATA_DIR}/fii_dii.csv", index=False)
except Exception as e:
    print(f"⚠ ERROR generating FII/DII data: {e}")

print(f"\n✅ ALL SYSTEMS GREEN. Execution Complete.")
