# ============================================================
#  INDIA TRADING TERMINAL — MASTER PRODUCTION ENGINE v2.0
#  Enhanced: EMA9/21, Supertrend, StochRSI, Williams%R, OBV
#  Weighted Scoring | Multi-TF RSI | Market Breadth | Pivots
# ============================================================

import os, io, time, warnings, requests
from datetime import datetime
import numpy as np
import pandas as pd
import pandas_ta as ta  # noqa
import yfinance as yf

warnings.filterwarnings("ignore")

DATA_DIR     = "terminal_data"
ENRICHED_DIR = f"{DATA_DIR}/enriched"
for _d in [DATA_DIR, ENRICHED_DIR]:
    os.makedirs(_d, exist_ok=True)

# ╔══════════════════════════════════════════════════════════╗
# ║  PHASE 1: SLOW ENGINE — FUNDAMENTALS                     ║
# ╚══════════════════════════════════════════════════════════╝

print("⏳ [STEP 1] Fetching live Nifty 500 universe from NSE...")
_url = "https://archives.nseindia.com/content/indices/ind_nifty500list.csv"
_hdr = {'User-Agent': 'Mozilla/5.0'}
try:
    _r = requests.get(_url, headers=_hdr, timeout=10)
    _nf = pd.read_csv(io.StringIO(_r.text))
    TICKER_LIST = [f"{s}.NS" for s in _nf['Symbol']]
    SECTOR_MAP  = dict(zip(TICKER_LIST, _nf['Industry']))
    print(f"✓ {len(TICKER_LIST)} tickers loaded.")
except Exception as e:
    print(f"⚠ NSE fetch failed ({e}). Using Nifty 50 fallback.")
    _nf = pd.read_csv("https://archives.nseindia.com/content/indices/ind_nifty50list.csv",
                      headers=_hdr)
    TICKER_LIST = [f"{s}.NS" for s in _nf['Symbol']]
    SECTOR_MAP  = dict(zip(TICKER_LIST, _nf['Industry']))

print("⏳ [STEP 2] Fetching Fundamentals (PE, EPS, ROE, Debt, Div)...")
fund_rows = []
for i, t in enumerate(TICKER_LIST):
    sym = t.replace(".NS", "")
    try:
        info = yf.Ticker(t).info
        fund_rows.append({
            "Ticker"        : sym,
            "Sector"        : SECTOR_MAP.get(t, "Other"),
            "PE_Ratio"      : info.get("trailingPE"),
            "EPS_TTM"       : info.get("trailingEps"),
            "Market_Cap_Cr" : round(info.get("marketCap", 0) / 1e7, 0) if info.get("marketCap") else None,
            "PB_Ratio"      : info.get("priceToBook"),
            "ROE_pct"       : round(info.get("returnOnEquity", 0) * 100, 2) if info.get("returnOnEquity") else None,
            "Debt_Equity"   : info.get("debtToEquity"),
            "Div_Yield"     : round(info.get("dividendYield", 0) * 100, 2) if info.get("dividendYield") else 0,
            "Revenue_Growth": round(info.get("revenueGrowth", 0) * 100, 2) if info.get("revenueGrowth") else None,
            "Current_Ratio" : info.get("currentRatio"),
        })
        if (i + 1) % 50 == 0:
            print(f"  [{i+1:03d}/{len(TICKER_LIST)}] ...{sym}")
    except Exception:
        fund_rows.append({"Ticker": sym, "Sector": SECTOR_MAP.get(t, "Other")})
    time.sleep(0.5)

fund_df = pd.DataFrame(fund_rows)
fund_df.to_csv(f"{DATA_DIR}/fundamentals.csv", index=False)

print("\n🔄 [STEP 3] Computing Sector Averages...")
fund_df["PE_Ratio"] = pd.to_numeric(fund_df["PE_Ratio"], errors="coerce")
sector_pe = (
    fund_df.dropna(subset=["PE_Ratio"])
    .groupby("Sector")["PE_Ratio"].median()
    .reset_index().rename(columns={"PE_Ratio": "Sector_Median_PE"})
)
sector_pe.to_csv(f"{DATA_DIR}/sector_averages.csv", index=False)


# ╔══════════════════════════════════════════════════════════╗
# ║  PHASE 2: FAST ENGINE — OHLCV + NIFTY RELATIVE STRENGTH ║
# ╚══════════════════════════════════════════════════════════╝

print(f"\n⚡ PHASE 2 STARTED AT {datetime.now():%H:%M UTC}\n")

print("⏳ Downloading OHLCV data from Yahoo Finance...")
raw = yf.download(
    tickers=TICKER_LIST, period="2y", interval="1d",
    auto_adjust=True, progress=False, threads=True
)

# Nifty 50 for relative strength benchmark
print("⏳ Downloading Nifty 50 benchmark...")
try:
    nifty_raw = yf.download("^NSEI", period="2y", interval="1d",
                            auto_adjust=True, progress=False)
    nifty_close = nifty_raw['Close'].squeeze()
    nifty_ret_20d = float(((nifty_close.iloc[-1] - nifty_close.iloc[-21]) / nifty_close.iloc[-21]) * 100)
    # Save last 30 trading days for dashboard
    (nifty_raw.reset_index()[['Date', 'Close']]
     .tail(30)
     .assign(Date=lambda d: d['Date'].dt.strftime('%Y-%m-%d'),
             Close=lambda d: d['Close'].round(2))
     .to_csv(f"{DATA_DIR}/nifty50_index.csv", index=False))
    print(f"✓ Nifty benchmark: 20D return = {nifty_ret_20d:.2f}%")
except Exception as e:
    print(f"⚠ Nifty download failed: {e}")
    nifty_ret_20d = 0.0

print("🔄 Processing OHLCV and saving price files...")
master_rows = []
for t in TICKER_LIST:
    sym = t.replace(".NS", "")
    try:
        df_p = pd.DataFrame({
            'Open': raw['Open'][t], 'High': raw['High'][t],
            'Low': raw['Low'][t],   'Close': raw['Close'][t], 'Volume': raw['Volume'][t],
        }).dropna(subset=['Close'])
        df_p.index.name = 'Date'
        df_p.to_csv(f"{DATA_DIR}/price_{sym}.csv")
        if len(df_p) < 22: continue
        lat = df_p.iloc[-1]; prv = df_p.iloc[-2]
        avg_vol = df_p['Volume'].iloc[-20:].mean()
        master_rows.append({
            "Ticker": sym, "Sector": SECTOR_MAP.get(t, "Other"),
            "Close": round(float(lat['Close']), 2),
            "Change_1D_pct": round(((lat['Close'] - prv['Close']) / prv['Close']) * 100, 2),
            "Volume_Today": int(lat['Volume']), "Avg_Vol_20D": int(avg_vol),
            "Vol_Ratio": round(lat['Volume'] / avg_vol, 2) if avg_vol > 0 else 0,
        })
    except Exception:
        pass

master_df = pd.DataFrame(master_rows)
master_df.to_csv(f"{DATA_DIR}/master_prices.csv", index=False)
print(f"✓ {len(master_df)} stocks processed.")


# ╔══════════════════════════════════════════════════════════╗
# ║  PHASE 3: INTEGRATED MASTER RULES ENGINE v2.0            ║
# ╚══════════════════════════════════════════════════════════╝

OUTPUT_CSV  = f"{DATA_DIR}/signals_output.csv"
SECTOR_CSV  = f"{DATA_DIR}/sector_signals.csv"
CHANGELOG   = f"{DATA_DIR}/signal_changes.csv"
PREV_SIG    = f"{DATA_DIR}/signals_previous.csv"
BREADTH_CSV = f"{DATA_DIR}/market_breadth.csv"

print("\n⚙️  PHASE 3: MASTER RULES ENGINE v2.0\n")

sector_lkp   = dict(zip(master_df['Ticker'], master_df['Sector']))
fund_dict    = fund_df.set_index('Ticker').to_dict(orient='index')
sec_pe_dict  = sector_pe.set_index('Sector')['Sector_Median_PE'].to_dict()

VOL_SPIKE = 1.5
MIN_VOL   = 300_000
PE_DISC   = 0.10

# ── Weighted scoring tables ────────────────────────────────
BUY_W = {
    "Value+Momentum": 15, "Breakout": 20, "Oversold Recovery": 12,
    "Golden Cross": 18,   "MTF Alignment": 15, "Supertrend Bull": 10,
    "EMA Ribbon Bull": 10,"EMA Cross": 10,  "StochRSI Reversal": 8,
    "OBV Confirm": 6,     "Rel Strong": 5,  "Near 52W High": 6,
    "Low Debt Quality": 5,
}
SELL_W = {
    "Trend Reversal": 20, "Death Cross": 18, "MTF Breakdown": 15,
    "Supertrend Bear": 10,"EMA Ribbon Bear": 10, "StochRSI Topped": 8,
    "OBV Diverge": 6,     "Overbought Ext": 10,
}

# ── Column rename map for enriched CSV ────────────────────
ENRICH_RENAME = {
    'SMA_50': 'MA50',   'SMA_200': 'MA200',
    'EMA_9': 'EMA9',    'EMA_21': 'EMA21',
    'BB_Upper': 'BB_Upper', 'BB_Lower': 'BB_Lower', 'BB_Mid': 'BB_Mid',
    'RSI_Daily': 'RSI', 'RSI_Weekly': 'RSI_W', 'RSI_Monthly': 'RSI_M',
    'MACD_12_26_9': 'MACD', 'MACDs_12_26_9': 'MACD_Signal', 'MACDh_12_26_9': 'MACD_Hist',
    'ADX_14': 'ADX',    'ATRr_14': 'ATR',
    'StochRSI_K': 'StochRSI_K', 'StochRSI_D': 'StochRSI_D',
    'Williams_R': 'Williams_R', 'OBV': 'OBV', 'OBV_SMA20': 'OBV_SMA20',
    'SUPERT_Dir': 'Supertrend_Dir',
}
BASE_COLS = ['Open', 'High', 'Low', 'Close', 'Volume']


def _safe(df, col, default=np.nan):
    """Safely get latest value of a column."""
    return float(df[col].iloc[-1]) if col in df.columns and not pd.isna(df[col].iloc[-1]) else default


def evaluate_stock(df, ticker, sec_pe, fund_data, nifty_ret_20d=0.0):
    """Core rules engine — returns a result dict for this stock."""
    lat  = df.iloc[-1];  prv  = df.iloc[-2]
    c    = float(lat['Close'])

    ma50   = _safe(df, 'SMA_50');   ma200  = _safe(df, 'SMA_200')
    ema9   = _safe(df, 'EMA_9');    ema21  = _safe(df, 'EMA_21')
    rsi_d  = _safe(df, 'RSI_Daily', 50)
    rsi_w  = _safe(df, 'RSI_Weekly', 50)
    rsi_m  = _safe(df, 'RSI_Monthly', 50)
    macd   = _safe(df, 'MACD_12_26_9');   macd_sig = _safe(df, 'MACDs_12_26_9')
    macd_h = _safe(df, 'MACDh_12_26_9')
    bb_u   = _safe(df, 'BB_Upper');  bb_l = _safe(df, 'BB_Lower')
    adx    = _safe(df, 'ADX_14');    atr  = _safe(df, 'ATRr_14')
    st_dir = _safe(df, 'SUPERT_Dir', 0)   # 1=bull, -1=bear
    sk     = _safe(df, 'StochRSI_K', 50)
    willr  = _safe(df, 'Williams_R', -50)
    obv    = _safe(df, 'OBV', 0);    obv_sma = _safe(df, 'OBV_SMA20', 0)

    vol20  = df['Volume'].rolling(20).mean().iloc[-1]
    vol_r  = float(lat['Volume']) / vol20 if vol20 > 0 else 0
    pe     = fund_data.get('PE_Ratio', np.nan)
    roe    = fund_data.get('ROE_pct', np.nan)
    de     = fund_data.get('Debt_Equity', np.nan)

    # Previous bar values
    prv_macd = float(df['MACD_12_26_9'].iloc[-2]) if 'MACD_12_26_9' in df.columns else macd
    prv_macs = float(df['MACDs_12_26_9'].iloc[-2]) if 'MACDs_12_26_9' in df.columns else macd_sig
    prv_mh   = float(df['MACDh_12_26_9'].iloc[-2]) if 'MACDh_12_26_9' in df.columns else macd_h
    prv_rsi  = float(df['RSI_Daily'].iloc[-2]) if 'RSI_Daily' in df.columns else rsi_d
    prv_sk   = float(df['StochRSI_K'].iloc[-2]) if 'StochRSI_K' in df.columns else sk
    prv_e9   = float(df['EMA_9'].iloc[-2]) if 'EMA_9' in df.columns else ema9
    prv_e21  = float(df['EMA_21'].iloc[-2]) if 'EMA_21' in df.columns else ema21

    rb, rs = [], []  # rules_buy, rules_sell

    # ── BUY RULES ─────────────────────────────────────────
    # 1. Value + Momentum: below-sector PE + price above MA50 + RSI trending
    if (c > ma50) and (45 < rsi_d < 68) and pd.notna(pe) and pd.notna(sec_pe) and (pe < sec_pe * (1 - PE_DISC)):
        rb.append("Value+Momentum")

    # 2. Breakout: price above BB upper with vol + ADX confirms trend
    if (c > bb_u) and (vol_r > VOL_SPIKE) and (rsi_d < 73) and (vol20 > MIN_VOL) and (adx > 20):
        rb.append("Breakout")

    # 3. Oversold recovery: RSI bounce from below 35, above MA200
    if (prv_rsi < 35) and (rsi_d > prv_rsi) and (c > ma200) and (macd_h > prv_mh):
        rb.append("Oversold Recovery")

    # 4. Golden / Death Cross (last 5 bars)
    recent = df.tail(5)
    if pd.notna(ma50) and pd.notna(ma200):
        if ((recent['SMA_50'] > recent['SMA_200']) & (recent['SMA_50'].shift(1) <= recent['SMA_200'].shift(1))).any():
            rb.append("Golden Cross")
        if ((recent['SMA_50'] < recent['SMA_200']) & (recent['SMA_50'].shift(1) >= recent['SMA_200'].shift(1))).any():
            rs.append("Death Cross")

    # 5. Multi-Timeframe Alignment (all 3 TFs agree)
    if (rsi_d > 50) and (rsi_w > 50) and (rsi_m > 50) and (c > ma50) and (ma50 > ma200) and (adx > 25):
        rb.append("MTF Alignment")
    if (rsi_d < 50) and (rsi_w < 50) and (rsi_m < 50) and (c < ma50) and (ma50 < ma200) and (adx > 25):
        rs.append("MTF Breakdown")

    # 6. Supertrend
    if st_dir == 1 and c > ma50:
        rb.append("Supertrend Bull")
    elif st_dir == -1 and c < ma50:
        rs.append("Supertrend Bear")

    # 7. EMA Ribbon (9 > 21 > 50 > 200 = fully stacked)
    if pd.notna(ema9) and pd.notna(ema21) and pd.notna(ma50) and pd.notna(ma200):
        if (ema9 > ema21) and (ema21 > ma50) and (ma50 > ma200):
            rb.append("EMA Ribbon Bull")
        elif (ema9 < ema21) and (ema21 < ma50) and (ma50 < ma200):
            rs.append("EMA Ribbon Bear")

    # 8. EMA 9/21 fresh crossover (last 3 bars)
    if pd.notna(ema9) and pd.notna(ema21) and pd.notna(prv_e9) and pd.notna(prv_e21):
        if (ema9 > ema21) and (prv_e9 <= prv_e21):
            rb.append("EMA Cross")

    # 9. Stochastic RSI oversold reversal
    if (prv_sk < 25) and (sk > prv_sk) and (sk < 80) and (c > ma200):
        rb.append("StochRSI Reversal")
    if (prv_sk > 80) and (sk < prv_sk) and (c < ma50):
        rs.append("StochRSI Topped")

    # 10. OBV confirmation
    if pd.notna(obv) and pd.notna(obv_sma) and obv_sma > 0:
        if (obv > obv_sma) and (c > ma50):
            rb.append("OBV Confirm")
        elif (obv < obv_sma) and (c < ma50):
            rs.append("OBV Diverge")

    # 11. MACD bearish crossover with overbought + volume spike
    if (macd < macd_sig) and (prv_macd >= prv_macs) and (rsi_d > 68) and (vol_r > VOL_SPIKE):
        rs.append("Trend Reversal")

    # 12. Overbought extreme (RSI + Williams%R + above BB)
    if (rsi_d > 80) and (willr > -10) and (c > bb_u):
        rs.append("Overbought Ext")

    # 13. Relative Strength vs Nifty
    if len(df) >= 21:
        stk_ret = ((c - float(df['Close'].iloc[-21])) / float(df['Close'].iloc[-21])) * 100
        if stk_ret > nifty_ret_20d + 3.0:
            rb.append("Rel Strong")

    # 14. Near 52-week high with momentum
    if len(df) >= 250:
        h52 = df['High'].rolling(250).max().iloc[-1]
        if (h52 > 0) and (c / h52 >= 0.97) and (rsi_d > 50) and (vol_r > 1.2):
            rb.append("Near 52W High")

    # 15. Quality fundamental (low debt, high ROE)
    if pd.notna(roe) and pd.notna(de) and (roe > 15) and (de < 1.0) and (c > ma50):
        rb.append("Low Debt Quality")

    # ── Weighted score ─────────────────────────────────────
    score = 50
    for r in rb: score += BUY_W.get(r, 10)
    for r in rs: score -= SELL_W.get(r, 10)
    if rsi_d < 35: score += 5
    if rsi_d > 72: score -= 5
    if adx > 30:   score += 3   # strong trend bonus
    if adx < 15:   score -= 3   # choppy market penalty
    score = max(0, min(100, int(score)))

    # ── Signal classification ──────────────────────────────
    if   score >= 80: signal = "STRONG BUY"
    elif score >= 65: signal = "WEAK BUY"
    elif score <= 20: signal = "STRONG SELL"
    elif score <= 35: signal = "WEAK SELL"
    elif abs(c - ma50) / max(ma50, 1) < 0.02 and (40 < rsi_d < 56): signal = "WATCH"
    else:             signal = "NEUTRAL"

    # ── Target / StopLoss via ATR ──────────────────────────
    tgt, sl = 0.0, 0.0
    if "BUY" in signal:
        mult = 2.5 if "STRONG" in signal else 1.8
        tgt = c + mult * atr;  sl = c - (mult * 0.6) * atr
    elif "SELL" in signal:
        mult = 2.5 if "STRONG" in signal else 1.8
        tgt = c - mult * atr;  sl = c + (mult * 0.6) * atr

    # ── Derived metrics ────────────────────────────────────
    high_52w = df['High'].rolling(252).max().iloc[-1] if len(df) >= 252 else c
    low_52w  = df['Low'].rolling(252).min().iloc[-1]  if len(df) >= 252 else c
    pct_52h  = ((c - high_52w) / high_52w) * 100 if high_52w > 0 else 0
    pct_52l  = ((c - low_52w)  / low_52w)  * 100 if low_52w  > 0 else 0

    # Daily Pivot Points (previous bar)
    pvt  = (float(lat['High']) + float(lat['Low']) + c) / 3
    r1   = 2 * pvt - float(lat['Low'])
    r2   = pvt + (float(lat['High']) - float(lat['Low']))
    s1   = 2 * pvt - float(lat['High'])
    s2   = pvt - (float(lat['High']) - float(lat['Low']))

    # Trend phase (Wyckoff-inspired)
    if   c > ma50 > ma200 and macd > 0 and rsi_d > 50:  phase = "Markup"
    elif c < ma50 < ma200 and macd < 0 and rsi_d < 50:  phase = "Markdown"
    elif c > ma200 and abs(c - ma200) / max(ma200, 1) < 0.08: phase = "Accumulation"
    else: phase = "Consolidation"

    # BB %B (position within Bollinger Bands)
    bb_pct_b = ((c - bb_l) / (bb_u - bb_l) * 100) if (bb_u - bb_l) > 0 else 50

    return {
        "Ticker"         : ticker,
        "Close"          : round(c, 2),
        "Signal"         : signal,
        "Score"          : score,
        "Target"         : round(tgt, 2) if tgt > 0 else "-",
        "StopLoss"       : round(sl,  2) if sl  > 0 else "-",
        "RSI"            : round(rsi_d, 1),
        "RSI_Weekly"     : round(rsi_w, 1),
        "RSI_Monthly"    : round(rsi_m, 1),
        "ADX"            : round(adx, 1),
        "Vol_Ratio"      : round(vol_r, 2),
        "Return_1D_pct"  : round(((c - float(prv['Close'])) / float(prv['Close'])) * 100, 2),
        "Pct_vs_MA50"    : round(((c - ma50) / ma50) * 100, 2)  if pd.notna(ma50)  else None,
        "Pct_vs_MA200"   : round(((c - ma200) / ma200) * 100, 2) if pd.notna(ma200) else None,
        "PE_Ratio"       : round(pe, 1)    if pd.notna(pe)  else None,
        "MACD"           : round(macd, 4),
        "MACD_Signal_Line": round(macd_sig, 4),
        "MACD_Hist"      : round(macd_h, 4),
        "ATR"            : round(atr, 2),
        "StochRSI_K"     : round(sk, 1),
        "Williams_R"     : round(willr, 1),
        "Supertrend_Dir" : int(st_dir),
        "BB_PctB"        : round(bb_pct_b, 1),
        "Pct_from_52W_High": round(pct_52h, 1),
        "Pct_from_52W_Low" : round(pct_52l, 1),
        "Pivot"          : round(pvt, 2),
        "R1"             : round(r1, 2),
        "R2"             : round(r2, 2),
        "S1"             : round(s1, 2),
        "S2"             : round(s2, 2),
        "Trend_Phase"    : phase,
        "Buy_Rules"      : ", ".join(rb) if rb else "None",
        "Sell_Rules"     : ", ".join(rs) if rs else "None",
        "Rules_Fired"    : ", ".join(rb + rs) if (rb or rs) else "None",
        "ROE_pct"        : round(roe, 1) if pd.notna(roe) else None,
        "Debt_Equity"    : round(de, 2)  if pd.notna(de)  else None,
        "Div_Yield"      : fund_data.get("Div_Yield", 0),
    }


# ── Main processing loop ───────────────────────────────────
all_signals = []
price_files = sorted([f for f in os.listdir(DATA_DIR) if f.startswith("price_") and f.endswith(".csv")])
total = len(price_files)
print(f"Processing {total} price files...\n")

for idx, fname in enumerate(price_files):
    ticker = fname.replace("price_", "").replace(".csv", "")
    try:
        df = pd.read_csv(f"{DATA_DIR}/{fname}", index_col='Date', parse_dates=True)
        if len(df) < 252:
            continue

        # ── Compute all indicators ──────────────────────────
        df.ta.sma(length=50, append=True)
        df.ta.sma(length=200, append=True)
        df.ta.ema(length=9,  append=True)
        df.ta.ema(length=21, append=True)
        df.ta.rsi(length=14, append=True)
        df.ta.macd(fast=12, slow=26, signal=9, append=True)
        df.ta.bbands(length=20, std=2, append=True)
        df.ta.adx(length=14, append=True)
        df.ta.atr(length=14, append=True)
        df.ta.stochrsi(length=14, rsi_length=14, k=3, d=3, append=True)
        df.ta.willr(length=14, append=True)
        df.ta.obv(append=True)
        try:
            df.ta.supertrend(length=10, multiplier=3.0, append=True)
        except Exception:
            df['SUPERT_Dir'] = 0  # fallback if supertrend fails

        # ── Rename columns to standard names ───────────────
        ren_map = {}
        for col in df.columns:
            if   col.startswith('BBU_'):       ren_map[col] = 'BB_Upper'
            elif col.startswith('BBL_'):       ren_map[col] = 'BB_Lower'
            elif col.startswith('BBM_'):       ren_map[col] = 'BB_Mid'
            elif col.startswith('STOCHRSIk_'): ren_map[col] = 'StochRSI_K'
            elif col.startswith('STOCHRSId_'): ren_map[col] = 'StochRSI_D'
            elif col.startswith('WILLR_'):     ren_map[col] = 'Williams_R'
            elif col.startswith('SUPERTd_'):   ren_map[col] = 'SUPERT_Dir'
            elif col.startswith('SUPERT_') and not any(
                    col.startswith(p) for p in ('SUPERTl_', 'SUPERTs_', 'SUPERTd_')):
                ren_map[col] = 'SUPERT_Line'
            elif col == 'RSI_14':              ren_map[col] = 'RSI_Daily'
            elif col == 'DMP_14':              ren_map[col] = 'DMP'
            elif col == 'DMN_14':              ren_map[col] = 'DMN'
        df.rename(columns=ren_map, inplace=True)

        # OBV smoothing
        if 'OBV' in df.columns:
            df['OBV_SMA20'] = df['OBV'].rolling(20).mean()

        # ── Weekly RSI ─────────────────────────────────────
        df_w = df.resample('W').agg({'Open':'first','High':'max','Low':'min','Close':'last'})
        df_w.ta.rsi(length=14, append=True)
        if 'RSI_14' in df_w.columns:
            df['RSI_Weekly'] = df_w['RSI_14'].reindex(df.index, method='ffill')
        else:
            df['RSI_Weekly'] = 50.0

        # ── Monthly RSI ────────────────────────────────────
        df_m = df.resample('ME').agg({'Open':'first','High':'max','Low':'min','Close':'last'})
        df_m.ta.rsi(length=14, append=True)
        if 'RSI_14' in df_m.columns:
            df['RSI_Monthly'] = df_m['RSI_14'].reindex(df.index, method='ffill')
        else:
            df['RSI_Monthly'] = 50.0

        df.bfill(inplace=True)
        df.fillna(0, inplace=True)

        # ── Evaluate & record ──────────────────────────────
        sector    = sector_lkp.get(ticker, "Other")
        sec_pe    = sec_pe_dict.get(sector, 30.0)
        fund_data = fund_dict.get(ticker, {})

        result = evaluate_stock(df, ticker, sec_pe, fund_data, nifty_ret_20d)
        result["Sector"] = sector
        all_signals.append(result)

        # ── Save enriched CSV for chart UI ─────────────────
        avail_cols = BASE_COLS + [c for c in ENRICH_RENAME.keys() if c in df.columns]
        enrich_df  = (df[avail_cols]
                      .rename(columns=ENRICH_RENAME)
                      .reset_index()
                      .tail(300))
        enrich_df.to_csv(f"{ENRICHED_DIR}/{ticker}_enriched.csv", index=False)

        if (idx + 1) % 100 == 0:
            print(f"  [{idx+1:03d}/{total}] Processed {ticker}...")

    except Exception as ex:
        print(f"  ⚠ Skipped {ticker}: {ex}")

# ── Signals output ─────────────────────────────────────────
signals_df = (pd.DataFrame(all_signals)
              .sort_values("Score", ascending=False)
              .reset_index(drop=True))
signals_df.to_csv(OUTPUT_CSV, index=False)
print(f"\n✓ Signals saved: {len(signals_df)} stocks | "
      f"{signals_df['Signal'].str.contains('BUY').sum()} BUY | "
      f"{signals_df['Signal'].str.contains('SELL').sum()} SELL")

# ── Sector summary ─────────────────────────────────────────
sector_summary = signals_df.groupby("Sector").agg(
    Total_Stocks =("Ticker", "count"),
    BUY_Count    =("Signal", lambda x: x.str.contains("BUY").sum()),
    SELL_Count   =("Signal", lambda x: x.str.contains("SELL").sum()),
    Avg_Score    =("Score",  "mean"),
    Avg_RSI      =("RSI",    "mean"),
    Avg_PE       =("PE_Ratio","mean"),
    Avg_ADX      =("ADX",    "mean"),
).reset_index()
sector_summary["Net_Signal_Score"] = sector_summary["BUY_Count"] - sector_summary["SELL_Count"]
sector_summary["Heatmap_Color"] = sector_summary["Net_Signal_Score"].apply(
    lambda x: "green" if x > 1 else ("red" if x < -1 else "amber"))
sector_summary.sort_values("Net_Signal_Score", ascending=False, inplace=True)
sector_summary.to_csv(SECTOR_CSV, index=False)

# ── Signal changelog ────────────────────────────────────────
if os.path.exists(PREV_SIG):
    prev_df = pd.read_csv(PREV_SIG)[["Ticker", "Signal"]]
    merged  = signals_df[["Ticker","Signal"]].merge(prev_df, on="Ticker", suffixes=("_new","_old"))
    changed = merged[merged["Signal_new"] != merged["Signal_old"]].copy()
    changed["Change"]       = changed["Signal_old"] + " → " + changed["Signal_new"]
    changed["Date_Changed"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    changed[["Ticker","Change","Date_Changed"]].to_csv(CHANGELOG, index=False)
else:
    pd.DataFrame(columns=["Ticker","Change","Date_Changed"]).to_csv(CHANGELOG, index=False)
signals_df.to_csv(PREV_SIG, index=False)

# ── Market breadth stats ────────────────────────────────────
if len(signals_df) > 0:
    n = len(signals_df)
    adv = int((signals_df["Return_1D_pct"] > 0).sum())
    dec = int((signals_df["Return_1D_pct"] < 0).sum())
    breadth = {
        "As_Of"          : datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Total_Stocks"   : n,
        "Pct_Above_MA50" : round((signals_df["Pct_vs_MA50"].fillna(0) > 0).sum() / n * 100, 1),
        "Pct_Above_MA200": round((signals_df["Pct_vs_MA200"].fillna(0) > 0).sum() / n * 100, 1),
        "Pct_Buy"        : round(signals_df["Signal"].str.contains("BUY").sum()  / n * 100, 1),
        "Pct_Sell"       : round(signals_df["Signal"].str.contains("SELL").sum() / n * 100, 1),
        "Avg_RSI"        : round(signals_df["RSI"].mean(), 1),
        "Avg_Score"      : round(signals_df["Score"].mean(), 1),
        "Strong_Buy"     : int(signals_df["Signal"].eq("STRONG BUY").sum()),
        "Strong_Sell"    : int(signals_df["Signal"].eq("STRONG SELL").sum()),
        "Near_52W_High"  : int((signals_df["Pct_from_52W_High"] >= -3).sum()),
        "Adv"            : adv,
        "Dec"            : dec,
        "Unch"           : n - adv - dec,
        "AD_Ratio"       : round(adv / max(dec, 1), 2),
    }
    pd.DataFrame([breadth]).to_csv(BREADTH_CSV, index=False)
    print(f"✓ Market breadth: A/D={adv}/{dec} | {breadth['Pct_Above_MA50']}% above MA50")


# ╔══════════════════════════════════════════════════════════╗
# ║  PHASE 4: MACRO DATA                                     ║
# ╚══════════════════════════════════════════════════════════╝

print("\n⏳ Generating FII/DII data...")
try:
    dates = pd.date_range(end=datetime.today(), periods=30, freq='B')
    fii_rows = []
    for d in dates:
        fii_net = np.random.normal(loc=-300, scale=1200)
        dii_net = -(fii_net * 0.75) + np.random.normal(loc=400, scale=600)
        fii_rows.append({
            "Date"   : d.strftime('%Y-%m-%d'),
            "FII_NET": round(fii_net, 2),
            "DII_NET": round(dii_net, 2)
        })
    pd.DataFrame(fii_rows).to_csv(f"{DATA_DIR}/fii_dii.csv", index=False)
    print("✓ FII/DII data saved (simulated — replace with real NSE API when available).")
except Exception as e:
    print(f"⚠ FII/DII error: {e}")

print(f"\n{'='*60}")
print(f"  ✅ ALL SYSTEMS GREEN — {datetime.now():%Y-%m-%d %H:%M UTC}")
print(f"  Stocks analysed : {len(signals_df)}")
print(f"  STRONG BUY      : {signals_df['Signal'].eq('STRONG BUY').sum()}")
print(f"  STRONG SELL     : {signals_df['Signal'].eq('STRONG SELL').sum()}")
print(f"{'='*60}\n")
