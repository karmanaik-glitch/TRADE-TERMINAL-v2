<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>NSE Terminal v2 — India Trading Dashboard</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Barlow+Condensed:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg0:#06090f;--bg1:#080d16;--bg2:#0c1220;--bg3:#101828;--bg4:#162032;
  --border:#192840;--border2:#1f3050;--border3:#254060;
  --green:#00e676;--gdim:#004d26;--gbg:#011a0d;
  --red:#ff4560;--rdim:#7a1a26;--rbg:#1a0509;
  --amber:#ffb300;--adim:#7a4800;--abg:#1a0f00;
  --blue:#4da6ff;--bdim:#1a3a6a;--bbg:#060f1e;
  --purple:#c084fc;--pdim:#4a1a6a;--pbg:#0d0618;
  --text:#c8dff0;--text2:#5a7a99;--text3:#2a4060;
  --mono:'JetBrains Mono','Courier New',monospace;
  --display:'Barlow Condensed','Impact',sans-serif;
}
html{background:var(--bg0);color:var(--text);font-family:var(--mono);font-size:13px;line-height:1.4;overflow-x:hidden}
body{min-height:100vh}
::-webkit-scrollbar{width:3px;height:3px}
::-webkit-scrollbar-track{background:var(--bg1)}
::-webkit-scrollbar-thumb{background:var(--border2);border-radius:2px}
::selection{background:var(--gdim);color:var(--green)}
body::before{content:'';position:fixed;inset:0;pointer-events:none;z-index:9999;
  background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,.05) 2px,rgba(0,0,0,.05) 4px)}
.wrap{max-width:1800px;margin:0 auto;padding:8px 12px}

/* TOPBAR */
.topbar{display:flex;align-items:center;gap:10px;padding:7px 14px;background:var(--bg2);
  border:1px solid var(--border2);border-radius:4px;margin-bottom:6px;flex-wrap:wrap}
.logo{font-family:var(--display);font-size:22px;font-weight:700;color:var(--green);letter-spacing:.12em;white-space:nowrap}
.logo em{color:var(--text2);font-style:normal;font-size:15px}
.logo sub{font-size:10px;color:var(--text3);vertical-align:super;letter-spacing:.06em}
.live-dot{width:6px;height:6px;border-radius:50%;background:var(--green);
  box-shadow:0 0 6px var(--green);animation:blink 2s ease-in-out infinite;flex-shrink:0}
@keyframes blink{0%,100%{opacity:1;box-shadow:0 0 6px var(--green)}50%{opacity:.3;box-shadow:none}}
.tpill{font-size:10px;padding:2px 8px;border-radius:2px;white-space:nowrap;letter-spacing:.05em;font-weight:500}
.pill-g{background:var(--gbg);color:var(--green);border:1px solid var(--gdim)}
.pill-r{background:var(--rbg);color:var(--red);border:1px solid var(--rdim)}
.pill-d{background:var(--bg3);color:var(--text2);border:1px solid var(--border)}
.topbar-sp{flex:1}
.ttime{font-size:10px;color:var(--text2);letter-spacing:.06em}
.btn{font-family:var(--mono);font-size:10px;padding:4px 11px;letter-spacing:.05em;
  background:var(--bg3);border:1px solid var(--border2);color:var(--text2);border-radius:2px;cursor:pointer;transition:all .15s}
.btn:hover{border-color:var(--green);color:var(--green)}

/* INDEX STRIP */
.idx-strip{display:grid;grid-template-columns:repeat(6,1fr);gap:5px;margin-bottom:5px}
.idx-card{background:var(--bg2);border:1px solid var(--border);border-radius:3px;padding:7px 11px;transition:border-color .2s}
.idx-card:hover{border-color:var(--border2)}
.idx-lbl{font-size:9px;color:var(--text3);letter-spacing:.09em;text-transform:uppercase;margin-bottom:2px}
.idx-val{font-family:var(--display);font-size:20px;font-weight:700;color:var(--text);line-height:1;margin-bottom:1px}
.idx-sub{font-size:10px;color:var(--text2)}

/* BREADTH STRIP */
.breadth-strip{display:flex;gap:5px;margin-bottom:6px;flex-wrap:wrap}
.bcard{background:var(--bg2);border:1px solid var(--border);border-radius:3px;
  padding:5px 12px;display:flex;align-items:center;gap:8px;flex:1;min-width:120px}
.bc-lbl{font-size:9px;color:var(--text3);letter-spacing:.07em;white-space:nowrap}
.bc-val{font-family:var(--display);font-size:16px;font-weight:700}
.bc-bar{flex:1;height:4px;background:var(--bg4);border-radius:2px;overflow:hidden;max-width:80px}
.bc-fill{height:100%;border-radius:2px;transition:width .5s}

/* MAIN GRID */
.main-grid{display:grid;grid-template-columns:minmax(0,1fr) 400px;gap:7px;margin-bottom:7px}
.panel{background:var(--bg1);border:1px solid var(--border);border-radius:4px;overflow:hidden}
.panel-head{display:flex;align-items:center;justify-content:space-between;padding:6px 12px;
  background:var(--bg2);border-bottom:1px solid var(--border);gap:7px;flex-shrink:0}
.ptitle{font-size:10px;font-weight:600;color:var(--text2);letter-spacing:.09em;text-transform:uppercase;white-space:nowrap}
.ptitle .dot{display:inline-block;width:5px;height:5px;border-radius:50%;background:var(--green);margin-right:6px;vertical-align:middle}

/* SCREENER */
.scr-toolbar{display:flex;align-items:center;gap:5px;padding:5px 8px;background:var(--bg2);border-bottom:1px solid var(--border);flex-wrap:wrap}
.scr-search{background:var(--bg1);border:1px solid var(--border2);color:var(--text);
  font-family:var(--mono);font-size:11px;padding:3px 8px;width:110px;border-radius:2px;outline:none}
.scr-search:focus{border-color:var(--text2)}
.scr-search::placeholder{color:var(--text3)}
.ftab{font-family:var(--mono);font-size:10px;padding:3px 8px;border:1px solid var(--border);
  background:transparent;color:var(--text2);border-radius:2px;cursor:pointer;transition:all .12s;letter-spacing:.04em}
.ftab:hover{border-color:var(--border2);color:var(--text)}
.ftab.on{background:var(--gbg);border-color:var(--gdim);color:var(--green)}
.ftab.on-sell{background:var(--rbg);border-color:var(--rdim);color:var(--red)}
.ftab.on-watch{background:var(--abg);border-color:var(--adim);color:var(--amber)}
.scr-wrap{overflow-y:auto;max-height:530px}
.scr-table{width:100%;border-collapse:collapse}
.scr-table th{position:sticky;top:0;z-index:5;padding:5px 8px;font-size:9px;color:var(--text3);
  letter-spacing:.07em;text-transform:uppercase;background:var(--bg3);
  border-bottom:1px solid var(--border);text-align:right;white-space:nowrap;cursor:pointer;user-select:none}
.scr-table th:nth-child(-n+3){text-align:left}
.scr-table th:hover{color:var(--text2)}
.scr-table th.sa::after{content:' ↑';color:var(--green)}
.scr-table th.sd::after{content:' ↓';color:var(--green)}
.scr-table td{padding:5px 8px;font-size:11px;border-bottom:1px solid rgba(25,40,64,.55);text-align:right;white-space:nowrap;transition:background .1s}
.scr-table td:nth-child(-n+3){text-align:left}
.scr-table tr:hover td{background:var(--bg3);cursor:pointer}
.scr-table tr.sel td{background:rgba(0,230,118,.04)!important}
.scr-table tr.sel td:first-child{border-left:2px solid var(--green)}
.star{background:none;border:none;cursor:pointer;color:var(--text3);font-size:12px;padding:0;line-height:1;transition:color .12s}
.star:hover,.star.on{color:var(--amber)}
.t-sym{font-weight:600;color:var(--text);font-size:12px;letter-spacing:.02em}
.t-sec{font-size:9px;color:var(--text3);max-width:80px;overflow:hidden;text-overflow:ellipsis}
.up{color:var(--green)}.dn{color:var(--red)}.nu{color:var(--text2)}
.rhi{color:var(--red)}.rlo{color:var(--green)}.rmi{color:var(--text)}
.sig{display:inline-flex;align-items:center;gap:3px;font-size:9px;font-weight:600;padding:2px 5px;border-radius:2px;letter-spacing:.04em}
.sig.BUY{background:var(--gbg);color:var(--green);border:1px solid var(--gdim)}
.sig.SELL{background:var(--rbg);color:var(--red);border:1px solid var(--rdim)}
.sig.WATCH{background:var(--abg);color:var(--amber);border:1px solid var(--adim)}
.sig.NEUTRAL{background:var(--bg3);color:var(--text2);border:1px solid var(--border)}
.sc-bar{display:flex;align-items:center;gap:4px;justify-content:flex-end}
.sc-n{font-size:11px;min-width:22px;text-align:right}
.sc-t{width:28px;height:3px;background:var(--bg4);border-radius:1px;overflow:hidden}
.sc-f{height:100%;border-radius:1px;transition:width .3s}

/* RIGHT COLUMN */
.right-col{display:flex;flex-direction:column;gap:7px}
.chart-info-bar{padding:9px 12px;background:var(--bg2);border-bottom:1px solid var(--border)}
.cib-top{display:flex;align-items:flex-start;gap:7px;margin-bottom:4px}
.cib-sym{font-family:var(--display);font-size:22px;font-weight:700;color:var(--text);letter-spacing:.04em;line-height:1}
.cib-sector{font-size:9px;color:var(--text3);margin-top:2px}
.cib-price{font-family:var(--display);font-size:20px;font-weight:700;color:var(--text)}
.cib-chg{font-size:11px}
.cib-right{margin-left:auto;text-align:right}
.chart-controls{display:flex;align-items:center;gap:4px;padding:5px 10px;
  background:var(--bg2);border-bottom:1px solid var(--border);flex-wrap:wrap}
.cc-group{display:flex;gap:2px}
.cc-btn{font-family:var(--mono);font-size:9px;padding:2px 7px;border:1px solid var(--border);
  background:transparent;color:var(--text3);border-radius:2px;cursor:pointer;transition:all .1s;letter-spacing:.04em}
.cc-btn:hover{color:var(--text2);border-color:var(--border2)}
.cc-btn.on{background:var(--bg3);border-color:var(--border2);color:var(--text)}
.cc-sep{width:1px;height:14px;background:var(--border);align-self:center;margin:0 3px}
#chart-container{height:260px;background:var(--bg0);position:relative}
.chart-ph{height:260px;display:flex;flex-direction:column;align-items:center;justify-content:center;
  gap:8px;color:var(--text3);font-size:11px;letter-spacing:.06em}

/* MULTI-TF ROW */
.mtf-row{display:grid;grid-template-columns:repeat(3,1fr);border-bottom:1px solid var(--border)}
.mtf-cell{padding:8px 10px;border-right:1px solid var(--border);text-align:center}
.mtf-cell:last-child{border-right:none}
.mtf-lbl{font-size:9px;color:var(--text3);letter-spacing:.08em;margin-bottom:4px;text-transform:uppercase}
.mtf-rsi{font-family:var(--display);font-size:18px;font-weight:700;line-height:1;margin-bottom:3px}
.mtf-sig{font-size:9px;font-weight:600;letter-spacing:.04em}
.mtf-bar{height:3px;border-radius:1px;margin-top:4px;overflow:hidden;background:var(--bg4)}
.mtf-fill{height:100%;border-radius:1px;transition:width .4s}

/* GAUGE + INDICATORS */
.gauge-grid{display:grid;grid-template-columns:1fr 1fr;border-bottom:1px solid var(--border)}
.gbox{padding:9px 12px;border-right:1px solid var(--border)}
.gbox:last-child{border-right:none}
.glabel{font-size:9px;color:var(--text3);letter-spacing:.07em;text-transform:uppercase;margin-bottom:5px}
.gval{font-family:var(--display);font-size:24px;font-weight:700;line-height:1}
.gsub{font-size:9px;color:var(--text2);margin-top:2px}
canvas#rsi-arc{display:block;margin:0 auto}
.macd-rows{padding:2px 0}
.mr{display:flex;justify-content:space-between;align-items:center;padding:2px 0;border-bottom:1px solid rgba(25,40,64,.5)}
.mr:last-child{border-bottom:none}
.mk{font-size:9px;color:var(--text3);letter-spacing:.05em}
.mv{font-size:11px;font-weight:500}
.mbar-wrap{height:3px;background:var(--bg4);border-radius:2px;margin-top:5px;overflow:hidden}
.mbar-fill{height:100%;border-radius:2px;transition:width .3s,background .3s}
.stats-row,.stats-row2{display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid var(--border)}
.stat{padding:7px 9px;border-right:1px solid var(--border)}
.stat:last-child{border-right:none}
.stat-l{font-size:9px;color:var(--text3);letter-spacing:.05em;text-transform:uppercase}
.stat-v{font-family:var(--display);font-size:15px;font-weight:700;color:var(--text);margin-top:1px}

/* TRADE BAR */
.trade-bar{display:flex;align-items:center;gap:6px;padding:8px 12px;
  background:var(--bg2);border-top:1px solid var(--border);flex-wrap:wrap}
.trade-lbl{font-size:9px;color:var(--text3);letter-spacing:.06em;white-space:nowrap}
.trade-inp{background:var(--bg1);border:1px solid var(--border2);color:var(--text);
  font-family:var(--mono);font-size:11px;padding:4px 7px;border-radius:2px;outline:none}
.trade-inp:focus{border-color:var(--text2)}
.tf-sel{font-family:var(--mono);font-size:10px;padding:4px 7px;background:var(--bg3);
  border:1px solid var(--border2);color:var(--text2);border-radius:2px;cursor:pointer;outline:none}
.btn-trade{font-family:var(--mono);font-size:10px;font-weight:600;letter-spacing:.06em;
  padding:5px 14px;border:none;border-radius:2px;cursor:pointer;transition:opacity .15s;white-space:nowrap}
.btn-trade:hover{opacity:.8}
.btn-buy{background:var(--green);color:var(--bg0)}
.btn-sell{background:var(--red);color:var(--bg0)}
#trade-msg{font-size:10px;margin-left:auto}

/* HEATMAP */
.heat-wrap{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:4px;padding:8px}
.hcell{border-radius:3px;padding:8px 10px;cursor:default;border:1px solid;transition:transform .15s}
.hcell:hover{transform:scale(1.03)}
.hcell.g{background:var(--gbg);border-color:var(--gdim)}.hcell.g .hn{color:var(--green)}
.hcell.r{background:var(--rbg);border-color:var(--rdim)}.hcell.r .hn{color:var(--red)}
.hcell.a{background:var(--abg);border-color:var(--adim)}.hcell.a .hn{color:var(--amber)}
.hn{font-size:10px;font-weight:600;letter-spacing:.03em;margin-bottom:3px}
.hc{font-size:9px;color:var(--text2);margin-bottom:2px}.hr{font-size:9px;color:var(--text3)}

/* BOTTOM */
.bot-grid{display:grid;grid-template-columns:1fr 1fr;gap:7px}
#fii-wrap{padding:8px;height:230px;position:relative}
.tabs-bar{display:flex;border-bottom:1px solid var(--border);overflow-x:auto}
.tb{flex-shrink:0;padding:7px 10px;font-family:var(--mono);font-size:10px;color:var(--text2);
  background:none;border:none;border-bottom:2px solid transparent;cursor:pointer;transition:all .15s;letter-spacing:.05em;white-space:nowrap}
.tb.on{color:var(--green);border-bottom-color:var(--green)}
.tp{display:none;overflow-y:auto;max-height:260px}
.tp.on{display:block}
.arow,.wrow{display:flex;align-items:center;gap:7px;padding:7px 12px;
  border-bottom:1px solid rgba(25,40,64,.5);font-size:11px;transition:background .1s}
.arow:hover,.wrow:hover{background:var(--bg2)}
.aticker,.wtick{font-weight:600;color:var(--text);min-width:65px}
.achg{flex:1}.adate{font-size:9px;color:var(--text3);margin-left:auto;white-space:nowrap}
.wrow{cursor:pointer}
.wrm{margin-left:auto;background:none;border:none;cursor:pointer;color:var(--text3);font-size:15px;line-height:1;transition:color .12s}
.wrm:hover{color:var(--red)}
.empty{padding:20px 12px;text-align:center;font-size:10px;color:var(--text3);letter-spacing:.05em;line-height:1.8}
.loading-msg{padding:16px 12px;text-align:center;font-size:10px;color:var(--text3);letter-spacing:.05em}
.err-msg{padding:12px;margin:8px;border:1px dashed var(--border2);border-radius:3px;font-size:10px;color:var(--text3);text-align:center;line-height:1.8}

/* PORTFOLIO */
.pt-summary{display:grid;grid-template-columns:repeat(4,1fr);background:var(--bg2);border-bottom:1px solid var(--border)}
.pt-box{padding:8px 11px;border-right:1px solid var(--border)}
.pt-box:last-child{border-right:none}
.pt-lbl{font-size:9px;color:var(--text3);letter-spacing:.05em;text-transform:uppercase;margin-bottom:1px}
.pt-val{font-family:var(--display);font-size:16px;font-weight:700}

/* JOURNAL */
.jnl-stats{display:grid;grid-template-columns:repeat(4,1fr);background:var(--bg2);border-bottom:1px solid var(--border)}
.jstat{padding:7px 10px;border-right:1px solid var(--border);text-align:center}
.jstat:last-child{border-right:none}
.js-lbl{font-size:9px;color:var(--text3);text-transform:uppercase;letter-spacing:.05em;margin-bottom:2px}
.js-val{font-family:var(--display);font-size:15px;font-weight:700}
.jrow{display:flex;align-items:center;gap:5px;padding:5px 10px;border-bottom:1px solid rgba(25,40,64,.5);font-size:10px;transition:background .1s}
.jrow:hover{background:var(--bg2)}
.jtf{font-size:9px;padding:1px 5px;border-radius:2px;font-weight:600;letter-spacing:.04em;white-space:nowrap}
.jtf.D{background:var(--bg3);color:var(--text2);border:1px solid var(--border)}
.jtf.W{background:var(--bdim);color:var(--blue);border:1px solid var(--bdim)}
.jtf.M{background:var(--pdim);color:var(--purple);border:1px solid var(--pdim)}
.jnotes{font-size:9px;color:var(--text3);flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:80px}
.jnl-toolbar{display:flex;gap:5px;padding:5px 10px;background:var(--bg2);border-bottom:1px solid var(--border);align-items:center}

/* RISK CALCULATOR */
.risk-grid{display:grid;grid-template-columns:1fr 1fr}
.risk-in{padding:10px 14px;border-bottom:1px solid var(--border);border-right:1px solid var(--border)}
.risk-out{padding:10px 14px;border-bottom:1px solid var(--border)}
.risk-lbl{font-size:9px;color:var(--text3);letter-spacing:.06em;text-transform:uppercase;margin-bottom:4px}
.risk-inp{background:var(--bg1);border:1px solid var(--border2);color:var(--text);
  font-family:var(--mono);font-size:12px;padding:5px 8px;width:100%;border-radius:2px;outline:none}
.risk-inp:focus{border-color:var(--text2)}
.risk-val{font-family:var(--display);font-size:20px;font-weight:700}
.risk-slider{width:100%;accent-color:var(--green);cursor:pointer}
.risk-result{padding:12px 14px;background:var(--bg2)}
.rr-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.rr-box{text-align:center;padding:8px;background:var(--bg3);border-radius:3px;border:1px solid var(--border)}
.rr-lbl{font-size:9px;color:var(--text3);margin-bottom:3px;text-transform:uppercase}
.rr-v{font-family:var(--display);font-size:17px;font-weight:700}

/* UTILS */
.c-green{color:var(--green)!important}.c-red{color:var(--red)!important}
.c-amber{color:var(--amber)!important}.c-blue{color:var(--blue)!important}
.c-dim{color:var(--text2)!important}.c-purple{color:var(--purple)!important}
.footer{display:flex;justify-content:space-between;align-items:center;padding:6px 2px;
  margin-top:7px;border-top:1px solid var(--border);font-size:9px;color:var(--text3);letter-spacing:.05em;flex-wrap:wrap;gap:5px}
@media(max-width:1100px){.main-grid{grid-template-columns:1fr}.bot-grid{grid-template-columns:1fr}.idx-strip{grid-template-columns:repeat(3,1fr)}}
@media(max-width:600px){.idx-strip{grid-template-columns:repeat(2,1fr)}.breadth-strip{display:none}}
</style>
</head>
<body>
<div class="wrap">

<div class="topbar">
  <div class="logo">NSE<em>/</em>TERMINAL<sub>v2</sub></div>
  <div class="live-dot"></div>
  <span class="tpill pill-g" id="nifty-pill">Loading…</span>
  <span class="tpill pill-d">RULES-BASED · NO ML</span>
  <span class="tpill pill-d" id="breadth-pill">—</span>
  <div class="topbar-sp"></div>
  <div class="ttime" id="update-time">—</div>
  <button class="btn" onclick="loadAllData()">⟳ REFRESH</button>
</div>

<div class="idx-strip">
  <div class="idx-card"><div class="idx-lbl">Nifty 50</div><div class="idx-val" id="ix-nifty">—</div><div class="idx-sub" id="ix-nifty-chg">—</div></div>
  <div class="idx-card"><div class="idx-lbl">Buy Signals</div><div class="idx-val c-green" id="ix-buy">—</div><div class="idx-sub" id="ix-buy-pct">of universe</div></div>
  <div class="idx-card"><div class="idx-lbl">Sell Signals</div><div class="idx-val c-red" id="ix-sell">—</div><div class="idx-sub" id="ix-sell-pct">of universe</div></div>
  <div class="idx-card"><div class="idx-lbl">Avg Score</div><div class="idx-val" id="ix-score">—</div><div class="idx-sub">0 → 100</div></div>
  <div class="idx-card"><div class="idx-lbl">Avg RSI</div><div class="idx-val" id="ix-rsi">—</div><div class="idx-sub" id="ix-rsi-lbl">market pulse</div></div>
  <div class="idx-card"><div class="idx-lbl">A/D Ratio</div><div class="idx-val" id="ix-ad">—</div><div class="idx-sub" id="ix-ad-sub">adv / dec</div></div>
</div>

<div class="breadth-strip">
  <div class="bcard"><div class="bc-lbl">% ABOVE MA50</div><div class="bc-val c-green" id="br-ma50">—</div><div class="bc-bar"><div class="bc-fill" id="br-ma50-bar" style="background:var(--green);width:0%"></div></div></div>
  <div class="bcard"><div class="bc-lbl">% ABOVE MA200</div><div class="bc-val c-blue" id="br-ma200">—</div><div class="bc-bar"><div class="bc-fill" id="br-ma200-bar" style="background:var(--blue);width:0%"></div></div></div>
  <div class="bcard"><div class="bc-lbl">STRONG BUY</div><div class="bc-val c-green" id="br-sbuy">—</div><div class="bc-bar"><div class="bc-fill" id="br-sbuy-bar" style="background:var(--green);width:0%"></div></div></div>
  <div class="bcard"><div class="bc-lbl">STRONG SELL</div><div class="bc-val c-red" id="br-ssell">—</div><div class="bc-bar"><div class="bc-fill" id="br-ssell-bar" style="background:var(--red);width:0%"></div></div></div>
  <div class="bcard"><div class="bc-lbl">NEAR 52W HIGH</div><div class="bc-val c-amber" id="br-52h">—</div><div class="bc-bar"><div class="bc-fill" id="br-52h-bar" style="background:var(--amber);width:0%"></div></div></div>
</div>

<div class="main-grid">
  <div class="panel">
    <div class="panel-head">
      <div class="ptitle"><span class="dot"></span>SCREENER — NIFTY 500</div>
      <div id="scr-count" style="font-size:9px;color:var(--text3)">—</div>
    </div>
    <div class="scr-toolbar">
      <input type="text" class="scr-search" id="scr-search" placeholder="🔍 Search…" oninput="renderScreener()">
      <button class="ftab on"       onclick="setFilter('ALL',this)">ALL</button>
      <button class="ftab"          onclick="setFilter('BUY',this)">▲ BUY</button>
      <button class="ftab on-sell"  onclick="setFilter('SELL',this)">▼ SELL</button>
      <button class="ftab on-watch" onclick="setFilter('WATCH',this)">◈ WATCH</button>
      <button class="ftab"          onclick="setFilter('STRONG BUY',this)">★ SBUY</button>
      <button class="ftab"          onclick="setFilter('Markup',this)">🚀 MARKUP</button>
    </div>
    <div class="scr-wrap" id="scr-wrap"><div class="loading-msg">Loading screener data…</div></div>
  </div>

  <div class="right-col">
    <div class="panel">
      <div class="chart-info-bar">
        <div class="cib-top">
          <div>
            <div class="cib-sym" id="c-sym">SELECT A STOCK</div>
            <div class="cib-sector" id="c-sec">click any row in the screener</div>
          </div>
          <div id="c-badge" style="margin-left:8px;margin-top:3px"></div>
          <div class="cib-right">
            <div class="cib-price" id="c-price">—</div>
            <div class="cib-chg" id="c-chg">—</div>
          </div>
        </div>
        <div id="c-rules" style="font-size:9px;color:var(--text3);margin-top:3px;line-height:1.7"></div>
        <div style="margin-top:5px;display:flex;gap:8px;flex-wrap:wrap;align-items:center">
          <span style="font-size:9px;color:var(--text3)">PIVOT</span><span id="c-pivot" class="c-dim" style="font-size:10px">—</span>
          <span style="font-size:9px;color:var(--text3)">R1</span><span id="c-r1" class="c-green" style="font-size:10px">—</span>
          <span style="font-size:9px;color:var(--text3)">R2</span><span id="c-r2" class="c-green" style="font-size:10px;opacity:.6">—</span>
          <span style="font-size:9px;color:var(--text3)">S1</span><span id="c-s1" class="c-red" style="font-size:10px">—</span>
          <span style="font-size:9px;color:var(--text3)">S2</span><span id="c-s2" class="c-red" style="font-size:10px;opacity:.6">—</span>
          <span style="font-size:9px;color:var(--text3);margin-left:4px">PHASE</span><span id="c-phase" style="font-size:10px">—</span>
        </div>
      </div>
      <div class="chart-controls">
        <div class="cc-group">
          <button class="cc-btn on" id="tf-D" onclick="setTF('D',this)">D</button>
          <button class="cc-btn"    id="tf-W" onclick="setTF('W',this)">W</button>
          <button class="cc-btn"    id="tf-M" onclick="setTF('M',this)">M</button>
        </div>
        <div class="cc-sep"></div>
        <div class="cc-group">
          <button class="cc-btn"    onclick="setRange(21,this)">1M</button>
          <button class="cc-btn"    onclick="setRange(63,this)">3M</button>
          <button class="cc-btn on" onclick="setRange(126,this)">6M</button>
          <button class="cc-btn"    onclick="setRange(252,this)">1Y</button>
          <button class="cc-btn"    onclick="setRange(9999,this)">ALL</button>
        </div>
        <div class="cc-sep"></div>
        <div class="cc-group">
          <button class="cc-btn on" id="tog-bb"  onclick="toggleOverlay('bb',this)">BB</button>
          <button class="cc-btn on" id="tog-ema" onclick="toggleOverlay('ema',this)">EMA</button>
          <button class="cc-btn on" id="tog-vol" onclick="toggleOverlay('vol',this)">VOL</button>
        </div>
      </div>
      <div id="chart-container">
        <div class="chart-ph">
          <div style="font-size:20px">↙</div>
          <div>SELECT A STOCK TO LOAD CHART</div>
          <div style="font-size:9px;color:var(--text3)">Candles · BB · EMA 9/21 · MA 50/200 · Volume</div>
        </div>
      </div>
      <div class="mtf-row" id="mtf-row" style="display:none">
        <div class="mtf-cell">
          <div class="mtf-lbl">Daily RSI</div>
          <div class="mtf-rsi" id="mtf-d-rsi">—</div>
          <div class="mtf-sig" id="mtf-d-sig">—</div>
          <div class="mtf-bar"><div class="mtf-fill" id="mtf-d-bar"></div></div>
        </div>
        <div class="mtf-cell">
          <div class="mtf-lbl">Weekly RSI</div>
          <div class="mtf-rsi" id="mtf-w-rsi">—</div>
          <div class="mtf-sig" id="mtf-w-sig">—</div>
          <div class="mtf-bar"><div class="mtf-fill" id="mtf-w-bar"></div></div>
        </div>
        <div class="mtf-cell">
          <div class="mtf-lbl">Monthly RSI</div>
          <div class="mtf-rsi" id="mtf-m-rsi">—</div>
          <div class="mtf-sig" id="mtf-m-sig">—</div>
          <div class="mtf-bar"><div class="mtf-fill" id="mtf-m-bar"></div></div>
        </div>
      </div>
    </div>

    <div class="panel">
      <div class="panel-head">
        <div class="ptitle"><span class="dot"></span>RSI · MACD · INDICATORS</div>
        <div id="g-label" style="font-size:9px;color:var(--text2);letter-spacing:.06em">—</div>
      </div>
      <div class="gauge-grid">
        <div class="gbox">
          <div class="glabel">RSI (14)</div>
          <canvas id="rsi-arc" width="120" height="66"></canvas>
          <div style="text-align:center;margin-top:2px">
            <div class="gval" id="g-rsi" style="font-size:20px">—</div>
            <div class="gsub" id="g-rsi-z">—</div>
          </div>
        </div>
        <div class="gbox" style="border-right:none">
          <div class="glabel">MACD (12,26,9)</div>
          <div class="macd-rows">
            <div class="mr"><span class="mk">MACD</span><span class="mv" id="m-line">—</span></div>
            <div class="mr"><span class="mk">SIGNAL</span><span class="mv" id="m-sig">—</span></div>
            <div class="mr"><span class="mk">HISTOGRAM</span><span class="mv" id="m-hist">—</span></div>
            <div class="mr"><span class="mk">CROSSOVER</span><span class="mv" id="m-cross">—</span></div>
          </div>
          <div class="mbar-wrap"><div id="mbar" class="mbar-fill" style="width:0"></div></div>
        </div>
      </div>
      <div class="stats-row">
        <div class="stat"><div class="stat-l">ATR</div><div class="stat-v" id="s-atr">—</div></div>
        <div class="stat"><div class="stat-l">VOL ×</div><div class="stat-v" id="s-vol">—</div></div>
        <div class="stat"><div class="stat-l">52W HI</div><div class="stat-v" id="s-52h">—</div></div>
        <div class="stat"><div class="stat-l">P/E</div><div class="stat-v" id="s-pe">—</div></div>
      </div>
      <div class="stats-row2">
        <div class="stat"><div class="stat-l">Stoch K</div><div class="stat-v" id="s-stoch">—</div></div>
        <div class="stat"><div class="stat-l">Will %R</div><div class="stat-v" id="s-willr">—</div></div>
        <div class="stat"><div class="stat-l">Supertrend</div><div class="stat-v" id="s-supert">—</div></div>
        <div class="stat"><div class="stat-l">BB %B</div><div class="stat-v" id="s-bbpb">—</div></div>
      </div>
      <div class="trade-bar" id="trade-bar" style="display:none">
        <span class="trade-lbl">PAPER TRADE</span>
        <input type="number" id="trade-qty" class="trade-inp" value="1" min="1" placeholder="Qty" style="width:64px">
        <select id="trade-tf" class="tf-sel">
          <option value="D">DAILY</option>
          <option value="W">WEEKLY</option>
          <option value="M">MONTHLY</option>
        </select>
        <button class="btn-trade btn-buy"  onclick="executeTrade('BUY')">BUY</button>
        <button class="btn-trade btn-sell" onclick="executeTrade('SELL')">SELL</button>
        <div id="trade-msg"></div>
      </div>
      <div id="trade-notes-bar" style="display:none;padding:5px 10px;background:var(--bg2);border-top:1px solid var(--border)">
        <input type="text" id="trade-notes" class="trade-inp" placeholder="Trade notes (optional)…" style="width:100%">
      </div>
    </div>
  </div>
</div>

<div class="panel" style="margin-bottom:7px">
  <div class="panel-head">
    <div class="ptitle"><span class="dot"></span>SECTOR HEATMAP</div>
    <div style="font-size:9px;color:var(--text2)">
      <span class="c-green">■</span> net BUY &nbsp;
      <span class="c-red">■</span> net SELL &nbsp;
      <span class="c-amber">■</span> mixed
    </div>
  </div>
  <div id="heat-wrap" class="heat-wrap"><div class="loading-msg">Loading…</div></div>
</div>

<div class="bot-grid">
  <div class="panel">
    <div class="panel-head">
      <div class="ptitle"><span class="dot"></span>FII / DII INSTITUTIONAL FLOW</div>
      <div style="font-size:9px;color:var(--text2)">30-day net · ₹ Crore</div>
    </div>
    <div id="fii-wrap"><canvas id="fii-chart"></canvas></div>
  </div>

  <div class="panel">
    <div class="tabs-bar">
      <button class="tb on" onclick="showTab('alerts',this)">⚡ ALERTS</button>
      <button class="tb"    onclick="showTab('watchlist',this)">★ WATCHLIST</button>
      <button class="tb"    onclick="showTab('portfolio',this)">💼 PORTFOLIO</button>
      <button class="tb"    onclick="showTab('journal',this)">📓 JOURNAL</button>
      <button class="tb"    onclick="showTab('risk',this)">⚖ RISK</button>
    </div>

    <div id="tp-alerts" class="tp on"><div class="loading-msg">Loading alerts…</div></div>

    <div id="tp-watchlist" class="tp">
      <div id="wl-body"><div class="empty">No stocks in watchlist.<br>Click ☆ in the screener to add.</div></div>
    </div>

    <div id="tp-portfolio" class="tp">
      <div class="pt-summary">
        <div class="pt-box"><div class="pt-lbl">Total Value</div><div class="pt-val" id="pt-total">—</div></div>
        <div class="pt-box"><div class="pt-lbl">Cash</div><div class="pt-val" id="pt-cash">—</div></div>
        <div class="pt-box"><div class="pt-lbl">Unrealised P&amp;L</div><div class="pt-val" id="pt-upnl">—</div></div>
        <div class="pt-box"><div class="pt-lbl">Realised P&amp;L</div><div class="pt-val" id="pt-rpnl">—</div></div>
      </div>
      <div id="pt-positions"><div class="empty">No active positions.<br>Select a stock and click BUY to start.</div></div>
      <div style="padding:8px;text-align:center;border-top:1px solid var(--border)">
        <button class="btn" style="color:var(--red);border-color:var(--rdim)" onclick="resetPortfolio()">⚠ RESET PORTFOLIO TO ₹10L</button>
      </div>
    </div>

    <div id="tp-journal" class="tp">
      <div class="jnl-stats">
        <div class="jstat"><div class="js-lbl">Trades</div><div class="js-val" id="js-count">0</div></div>
        <div class="jstat"><div class="js-lbl">Win Rate</div><div class="js-val" id="js-wr">—</div></div>
        <div class="jstat"><div class="js-lbl">Best Trade</div><div class="js-val c-green" id="js-best">—</div></div>
        <div class="jstat"><div class="js-lbl">Realised P&amp;L</div><div class="js-val" id="js-pnl">—</div></div>
      </div>
      <div class="jnl-toolbar">
        <button class="btn" onclick="exportJournal()">↓ EXPORT CSV</button>
        <button class="btn" style="color:var(--red)" onclick="clearJournal()">✕ CLEAR</button>
      </div>
      <div id="jnl-body"><div class="empty">No journal entries yet.<br>Every paper trade is recorded here.</div></div>
    </div>

    <div id="tp-risk" class="tp">
      <div class="risk-grid">
        <div class="risk-in"><div class="risk-lbl">Portfolio Capital (₹)</div><input type="number" class="risk-inp" id="r-capital" value="1000000" oninput="calcRisk()"></div>
        <div class="risk-out">
          <div class="risk-lbl">Risk per Trade — <span id="r-riskpct-v">2%</span></div>
          <input type="range" class="risk-slider" id="r-riskpct" min="0.5" max="5" step="0.5" value="2" oninput="calcRisk()">
        </div>
        <div class="risk-in"><div class="risk-lbl">Entry Price (₹)</div><input type="number" class="risk-inp" id="r-entry" oninput="calcRisk()" placeholder="Auto-filled on select"></div>
        <div class="risk-out"><div class="risk-lbl">Stop Loss (₹)</div><input type="number" class="risk-inp" id="r-sl" oninput="calcRisk()" placeholder="Auto-filled on select"></div>
        <div class="risk-in"><div class="risk-lbl">Target Price (₹)</div><input type="number" class="risk-inp" id="r-target" oninput="calcRisk()" placeholder="Auto-filled on select"></div>
        <div class="risk-out" style="display:flex;flex-direction:column;justify-content:center">
          <div class="risk-lbl">Risk : Reward</div>
          <div class="risk-val" id="r-rr">—</div>
        </div>
      </div>
      <div class="risk-result">
        <div style="font-size:9px;color:var(--text3);letter-spacing:.07em;text-transform:uppercase;margin-bottom:8px">Position Sizing Result</div>
        <div class="rr-grid">
          <div class="rr-box"><div class="rr-lbl">Shares to Buy</div><div class="rr-v c-green" id="r-shares">—</div></div>
          <div class="rr-box"><div class="rr-lbl">Capital Required</div><div class="rr-v c-blue" id="r-capneeded">—</div></div>
          <div class="rr-box"><div class="rr-lbl">Max Risk (₹)</div><div class="rr-v c-red" id="r-maxrisk">—</div></div>
        </div>
        <div style="margin-top:8px;font-size:9px;color:var(--text3);line-height:1.9" id="r-advice"></div>
      </div>
    </div>
  </div>
</div>

<div class="footer">
  <span>NSE/TERMINAL v2 · RULES ENGINE · DATA: YAHOO FINANCE / NSE · NO ML · NO AI PREDICTIONS</span>
  <span id="footer-r">—</span>
</div>
</div>

<script src="https://unpkg.com/lightweight-charts@4.1.3/dist/lightweight-charts.standalone.production.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<script>
// ═══════════════════════════════════════════════════════════
//  NSE TERMINAL v2 — FULL ENGINE
// ═══════════════════════════════════════════════════════════
const D = './terminal_data/';
let signals=[], sectors=[], alerts=[], fiidii=[], breadth={};
let filter='ALL', sort={col:'Score',dir:'desc'};
let selected=null, lwChart=null, fiiChart=null;
let chartTF='D', chartRange=126;
let overlays={bb:true,ema:true,vol:true};
let watchlist = JSON.parse(localStorage.getItem('nse_wl')||'[]');
let pt = JSON.parse(localStorage.getItem('nse_pt'));
if(!pt||!pt.cash) pt={cash:1000000,positions:{},realised:0};
if(pt.realised===undefined) pt.realised=0;
let journal = JSON.parse(localStorage.getItem('nse_journal')||'[]');

// ── CSV loader ────────────────────────────────────────────
function csv(url){
  return new Promise((res,rej)=>{
    Papa.parse(url,{download:true,header:true,skipEmptyLines:true,dynamicTyping:true,
      complete:r=>res(r.data), error:e=>rej(new Error(url+': '+e.message))});
  });
}

// ── Boot ──────────────────────────────────────────────────
async function loadAllData(){
  set('update-time','Loading…');
  try{
    [signals,sectors,alerts,fiidii] = await Promise.all([
      csv(D+'signals_output.csv'), csv(D+'sector_signals.csv'),
      csv(D+'signal_changes.csv'), csv(D+'fii_dii.csv'),
    ]);
    try{ const b=await csv(D+'market_breadth.csv'); breadth=b[0]||{}; }catch(e){ breadth={}; }
    renderStrip(); renderBreadth(); renderScreener();
    renderHeatmap(); renderAlerts(); renderFiiDii();
    renderWatchlist(); renderPortfolio(); loadNiftyIndex();
    renderJournal(); calcRisk();
    const n=new Date();
    set('update-time', n.toLocaleTimeString('en-IN',{hour:'2-digit',minute:'2-digit',timeZone:'Asia/Kolkata'})+' IST');
    set('footer-r', signals.length+' stocks · '+signals.filter(s=>s.Signal&&s.Signal.includes('BUY')).length+' BUY · '+signals.filter(s=>s.Signal&&s.Signal.includes('SELL')).length+' SELL · '+new Date().toLocaleDateString('en-IN'));
  }catch(e){
    console.error(e);
    document.getElementById('scr-wrap').innerHTML='<div class="err-msg">Failed to load data.<br>Run main.py first to generate terminal_data/ files.<br><br>'+e.message+'</div>';
    set('update-time','ERROR');
  }
}

// ── Nifty index ───────────────────────────────────────────
async function loadNiftyIndex(){
  try{
    const rows=await csv(D+'nifty50_index.csv');
    if(!rows.length)return;
    const last=rows[rows.length-1], prev=rows[rows.length-2]||rows[rows.length-1];
    const cl=+last.Close, ch=+(((cl-+prev.Close)/+prev.Close)*100).toFixed(2);
    const s=ch>=0?'+':'';
    set('ix-nifty',cl.toLocaleString('en-IN',{maximumFractionDigits:0}));
    const ce=document.getElementById('ix-nifty-chg');
    ce.textContent=s+ch+'%'; ce.className='idx-sub '+(ch>=0?'c-green':'c-red');
    const pe=document.getElementById('nifty-pill');
    pe.textContent='NIFTY '+s+ch+'%';
    pe.className='tpill '+(ch>=0?'pill-g':'pill-r');
  }catch(e){}
}

// ── Index strip ───────────────────────────────────────────
function renderStrip(){
  const buy=signals.filter(s=>s.Signal&&s.Signal.includes('BUY')).length;
  const sell=signals.filter(s=>s.Signal&&s.Signal.includes('SELL')).length;
  const n=signals.length||1;
  const avgSc=(signals.reduce((a,s)=>a+(+s.Score||0),0)/n).toFixed(0);
  const avgRsi=(signals.reduce((a,s)=>a+(+s.RSI||0),0)/n).toFixed(1);
  const adv=signals.filter(s=>(+s.Return_1D_pct||0)>0).length;
  const dec=signals.filter(s=>(+s.Return_1D_pct||0)<0).length;
  set('ix-buy',buy); set('ix-buy-pct',((buy/n)*100).toFixed(0)+'% of universe');
  set('ix-sell',sell); set('ix-sell-pct',((sell/n)*100).toFixed(0)+'% of universe');
  set('ix-score',avgSc);
  set('ix-rsi',avgRsi);
  setClass('ix-rsi','idx-val '+(+avgRsi>65?'c-red':+avgRsi<40?'c-green':'c-amber'));
  set('ix-rsi-lbl',+avgRsi>65?'OVERBOUGHT':+avgRsi<40?'OVERSOLD':'NEUTRAL ZONE');
  set('ix-ad',(adv/Math.max(dec,1)).toFixed(2));
  set('ix-ad-sub',adv+' adv / '+dec+' dec');
  const bp=document.getElementById('breadth-pill');
  bp.textContent=((buy/n)*100).toFixed(0)+'% BUY · '+((sell/n)*100).toFixed(0)+'% SELL';
  bp.className='tpill '+(buy>sell?'pill-g':sell>buy?'pill-r':'pill-d');
}

function renderBreadth(){
  if(!Object.keys(breadth).length)return;
  const n=+breadth.Total_Stocks||1;
  const ma50=+breadth.Pct_Above_MA50||0, ma200=+breadth.Pct_Above_MA200||0;
  const sbuy=+breadth.Strong_Buy||0, ssell=+breadth.Strong_Sell||0, h52=+breadth.Near_52W_High||0;
  set('br-ma50',ma50+'%'); document.getElementById('br-ma50-bar').style.width=ma50+'%';
  set('br-ma200',ma200+'%'); document.getElementById('br-ma200-bar').style.width=ma200+'%';
  set('br-sbuy',sbuy); document.getElementById('br-sbuy-bar').style.width=Math.min(100,sbuy/n*500)+'%';
  set('br-ssell',ssell); document.getElementById('br-ssell-bar').style.width=Math.min(100,ssell/n*500)+'%';
  set('br-52h',h52); document.getElementById('br-52h-bar').style.width=Math.min(100,h52/n*500)+'%';
}

// ── Helpers ───────────────────────────────────────────────
function set(id,v){const e=document.getElementById(id);if(e)e.textContent=v}
function setClass(id,c){const e=document.getElementById(id);if(e)e.className=c}
function ic(v){if(!v)return'·';if(v.includes('BUY'))return'▲';if(v.includes('SELL'))return'▼';if(v.includes('WATCH'))return'◈';return'·'}
function fmtINR(n){return '₹'+(+n||0).toLocaleString('en-IN',{maximumFractionDigits:0})}
function sigClass(sig){
  if(!sig)return 'NEUTRAL';
  if(sig.includes('BUY'))return 'BUY';
  if(sig.includes('SELL'))return 'SELL';
  if(sig==='WATCH')return 'WATCH';
  return 'NEUTRAL';
}
function rsiToSig(rsi){
  if(rsi>=70)return 'OVERBOUGHT';
  if(rsi>=55)return 'BULLISH';
  if(rsi<=30)return 'OVERSOLD';
  if(rsi<=45)return 'BEARISH';
  return 'NEUTRAL';
}

// ── Screener ─────────────────────────────────────────────
function renderScreener(){
  const q=(document.getElementById('scr-search').value||'').toUpperCase().trim();
  let data=signals.filter(s=>{
    if(filter==='ALL')return true;
    if(filter==='STRONG BUY')return s.Signal==='STRONG BUY';
    if(filter==='Markup')return (s.Trend_Phase||'')==='Markup';
    return s.Signal&&s.Signal.includes(filter);
  });
  if(q) data=data.filter(s=>(s.Ticker||'').toUpperCase().includes(q)||(s.Sector||'').toUpperCase().includes(q));
  data.sort((a,b)=>{
    let av=a[sort.col], bv=b[sort.col];
    if(typeof av==='string')av=av.toLowerCase();
    if(typeof bv==='string')bv=bv.toLowerCase();
    if(av===null||av===undefined)av=-Infinity;
    if(bv===null||bv===undefined)bv=-Infinity;
    return sort.dir==='asc'?(av<bv?-1:av>bv?1:0):(av>bv?-1:av<bv?1:0);
  });
  set('scr-count',data.length+' stocks');
  const cols=[
    {k:'★',l:'★',s:false},{k:'Ticker',l:'TICKER',s:true},{k:'Sector',l:'SECTOR',s:true},
    {k:'Close',l:'PRICE ₹',s:true},{k:'Return_1D_pct',l:'1D %',s:true},
    {k:'RSI',l:'RSI-D',s:true},{k:'RSI_Weekly',l:'RSI-W',s:true},
    {k:'StochRSI_K',l:'STOCH',s:true},{k:'Pct_vs_MA50',l:'▲MA50',s:true},
    {k:'Supertrend_Dir',l:'ST',s:false},
    {k:'ADX',l:'ADX',s:true},{k:'Vol_Ratio',l:'VOL×',s:true},
    {k:'Score',l:'SCORE',s:true},{k:'Signal',l:'SIGNAL',s:true},
  ];
  let h='<thead><tr>';
  cols.forEach(c=>{
    if(!c.s){h+=`<th>${c.l}</th>`;return}
    const cl=sort.col===c.k?(sort.dir==='asc'?'sa':'sd'):'';
    h+=`<th class="${cl}" onclick="doSort('${c.k}')">${c.l}</th>`;
  });
  h+='</tr></thead>';
  let b='<tbody>';
  data.forEach(r=>{
    const wl=watchlist.includes(r.Ticker);
    const chg=+r.Return_1D_pct||0, rsi=+r.RSI||0, rsiw=+r.RSI_Weekly||0;
    const sk=+r.StochRSI_K||0, pma=+r.Pct_vs_MA50||0, vol=+r.Vol_Ratio||0;
    const adx=+r.ADX||0, sc=+r.Score||0, st=+r.Supertrend_Dir||0;
    const scc=sc>=65?'var(--green)':sc<=35?'var(--red)':'var(--amber)';
    const rcl=rsi>65?'rhi':rsi<40?'rlo':'rmi';
    const rwcl=rsiw>60?'c-green':rsiw<40?'c-red':'nu';
    const stEl=st===1?'<span style="color:var(--green)">▲</span>':st===-1?'<span style="color:var(--red)">▼</span>':'<span class="nu">—</span>';
    b+=`<tr onclick="pick('${r.Ticker}')" id="row-${r.Ticker}"${r.Ticker===selected?' class="sel"':''}>
      <td><button class="star${wl?' on':''}" onclick="toggleWL(event,'${r.Ticker}')">${wl?'★':'☆'}</button></td>
      <td><span class="t-sym">${r.Ticker}</span></td>
      <td><span class="t-sec">${r.Sector||'—'}</span></td>
      <td>${(+r.Close||0).toLocaleString('en-IN',{minimumFractionDigits:2,maximumFractionDigits:2})}</td>
      <td class="${chg>=0?'up':'dn'}">${chg>=0?'+':''}${chg.toFixed(2)}%</td>
      <td class="${rcl}">${rsi.toFixed(1)}</td>
      <td class="${rwcl}">${(rsiw||0).toFixed(1)}</td>
      <td class="${sk<25?'rlo':sk>75?'rhi':'rmi'}">${sk.toFixed(0)}</td>
      <td class="${pma>=0?'up':'dn'}">${pma>=0?'+':''}${(pma||0).toFixed(1)}%</td>
      <td>${stEl}</td>
      <td class="${adx>25?'c-amber':'nu'}">${(adx||0).toFixed(0)}</td>
      <td class="${vol>=1.5?'up':'nu'}">${(vol||0).toFixed(2)}×</td>
      <td><div class="sc-bar"><span class="sc-n" style="color:${scc}">${sc}</span><div class="sc-t"><div class="sc-f" style="width:${sc}%;background:${scc}"></div></div></div></td>
      <td><span class="sig ${sigClass(r.Signal)}">${ic(r.Signal)} ${r.Signal||'NEUTRAL'}</span></td>
    </tr>`;
  });
  b+='</tbody>';
  document.getElementById('scr-wrap').innerHTML=`<table class="scr-table">${h}${b}</table>`;
  if(data.length>0&&!selected)pick(data[0].Ticker);
}

function setFilter(f,btn){
  filter=f;
  document.querySelectorAll('.ftab').forEach(b=>b.classList.remove('on','on-sell','on-watch'));
  const map={'ALL':'on','BUY':'on','SELL':'on-sell','WATCH':'on-watch','STRONG BUY':'on','Markup':'on'};
  btn.classList.add(map[f]||'on');
  renderScreener();
}
function doSort(col){
  sort.dir=sort.col===col?(sort.dir==='asc'?'desc':'asc'):'desc';
  sort.col=col; renderScreener();
}

// ── Pick stock ────────────────────────────────────────────
function pick(ticker){
  selected=ticker;
  document.querySelectorAll('.scr-table tr').forEach(r=>r.classList.remove('sel'));
  const row=document.getElementById('row-'+ticker);
  if(row){row.classList.add('sel');row.scrollIntoView({block:'nearest',behavior:'smooth'})}
  const s=signals.find(x=>x.Ticker===ticker);
  if(!s)return;
  const chg=+s.Return_1D_pct||0, sg=chg>=0?'+':'';
  set('c-sym',ticker);
  set('c-sec',s.Sector||'');
  set('c-price','₹'+(+s.Close||0).toLocaleString('en-IN',{minimumFractionDigits:2,maximumFractionDigits:2}));
  const ce=document.getElementById('c-chg'); ce.textContent=sg+chg.toFixed(2)+'%'; ce.className='cib-chg '+(chg>=0?'up':'dn');
  document.getElementById('c-badge').innerHTML=`<span class="sig ${sigClass(s.Signal)}">${ic(s.Signal)} ${s.Signal||'NEUTRAL'}</span>`;
  // Rules fired
  const br=s.Buy_Rules&&s.Buy_Rules!=='None'?`<span class="c-green">▲ ${s.Buy_Rules}</span>`:'';
  const sr=s.Sell_Rules&&s.Sell_Rules!=='None'?`<span class="c-red" style="margin-left:6px"> ▼ ${s.Sell_Rules}</span>`:'';
  document.getElementById('c-rules').innerHTML=br+sr||(br+sr?'':`<span class="c-dim">No rules fired — NEUTRAL zone</span>`);
  // Pivot levels
  set('c-pivot',s.Pivot?'₹'+s.Pivot:'—');
  set('c-r1',s.R1?'₹'+s.R1:'—');
  set('c-r2',s.R2?'₹'+s.R2:'—');
  set('c-s1',s.S1?'₹'+s.S1:'—');
  set('c-s2',s.S2?'₹'+s.S2:'—');
  const ph=s.Trend_Phase||''; const pe2=document.getElementById('c-phase');
  pe2.textContent=ph||'—'; pe2.className=ph==='Markup'?'c-green':ph==='Markdown'?'c-red':ph==='Accumulation'?'c-amber':'c-dim';
  // Trade bar
  document.getElementById('trade-bar').style.display='flex';
  document.getElementById('trade-notes-bar').style.display='flex';
  document.getElementById('trade-msg').textContent='';
  document.getElementById('trade-qty').value=1;
  document.getElementById('trade-notes').value='';
  // Auto-fill risk calc
  if(s.Close) document.getElementById('r-entry').value=+s.Close;
  if(s.StopLoss&&s.StopLoss!=='-') document.getElementById('r-sl').value=+s.StopLoss;
  else document.getElementById('r-sl').value='';
  if(s.Target&&s.Target!=='-') document.getElementById('r-target').value=+s.Target;
  else document.getElementById('r-target').value='';
  calcRisk();
  updateGauges(s);
  updateMTF(s);
  loadChart(ticker);
}

// ── Multi-TF panel ────────────────────────────────────────
function updateMTF(s){
  document.getElementById('mtf-row').style.display='grid';
  const rows=[
    {rsi:+s.RSI||50,     sig:s.Signal||'NEUTRAL', r:'mtf-d-rsi',sg:'mtf-d-sig',b:'mtf-d-bar'},
    {rsi:+s.RSI_Weekly||50,   sig:rsiToSig(+s.RSI_Weekly||50),  r:'mtf-w-rsi',sg:'mtf-w-sig',b:'mtf-w-bar'},
    {rsi:+s.RSI_Monthly||50,  sig:rsiToSig(+s.RSI_Monthly||50), r:'mtf-m-rsi',sg:'mtf-m-sig',b:'mtf-m-bar'},
  ];
  rows.forEach(p=>{
    const re=document.getElementById(p.r);
    re.textContent=p.rsi.toFixed(1);
    re.className='mtf-rsi '+(p.rsi>65?'c-red':p.rsi<40?'c-green':'c-amber');
    const se=document.getElementById(p.sg);
    se.textContent=p.sig;
    se.className='mtf-sig '+(p.sig.includes('BUY')||p.sig==='BULLISH'?'c-green':p.sig.includes('SELL')||p.sig==='BEARISH'||p.sig==='OVERBOUGHT'?'c-red':'c-amber');
    const bf=document.getElementById(p.b);
    bf.style.width=p.rsi+'%';
    bf.style.background=p.rsi>65?'var(--red)':p.rsi<40?'var(--green)':'var(--amber)';
  });
}

// ── RSI gauge ─────────────────────────────────────────────
function drawRsi(rsi){
  const c=document.getElementById('rsi-arc'),x=c.getContext('2d');
  const W=c.width,H=c.height,cx=W/2,cy=H-4,R=44;
  x.clearRect(0,0,W,H);
  [{f:0,t:35,c:'#004d26'},{f:35,t:65,c:'#162032'},{f:65,t:100,c:'#7a1a26'}].forEach(z=>{
    x.beginPath();x.arc(cx,cy,R,Math.PI*(1+z.f/100),Math.PI*(1+z.t/100));x.strokeStyle=z.c;x.lineWidth=8;x.stroke();
  });
  [35,65].forEach(v=>{
    const a=Math.PI*(1+v/100);
    x.beginPath();x.moveTo(cx+(R-3)*Math.cos(a),cy+(R-3)*Math.sin(a));
    x.lineTo(cx+(R+3)*Math.cos(a),cy+(R+3)*Math.sin(a));x.strokeStyle='#192840';x.lineWidth=1.5;x.stroke();
  });
  const a=Math.PI*(1+rsi/100),nc=rsi>65?'#ff4560':rsi<35?'#00e676':'#c8dff0';
  x.beginPath();x.moveTo(cx,cy);x.lineTo(cx+(R-2)*Math.cos(a),cy+(R-2)*Math.sin(a));
  x.strokeStyle=nc;x.lineWidth=2;x.lineCap='round';x.stroke();
  x.beginPath();x.arc(cx,cy,3.5,0,Math.PI*2);x.fillStyle=nc;x.fill();
}

// ── Gauges ────────────────────────────────────────────────
function updateGauges(s){
  const rsi=+s.RSI||50, macd=+s.MACD||0, msig=+s.MACD_Signal_Line||0, mh=+s.MACD_Hist||0;
  set('g-label',s.Ticker);
  const rv=document.getElementById('g-rsi');
  rv.textContent=rsi.toFixed(1);
  rv.className='gval '+(rsi>65?'c-red':rsi<35?'c-green':'');
  set('g-rsi-z',rsi>70?'OVERBOUGHT — EXIT ZONE':rsi<35?'OVERSOLD — REVERSAL WATCH':rsi>55?'BULLISH ZONE':'NEUTRAL ZONE');
  drawRsi(rsi);
  const ml=document.getElementById('m-line'); ml.textContent=macd.toFixed(4); ml.className='mv '+(macd>=0?'c-green':'c-red');
  const mse=document.getElementById('m-sig'); mse.textContent=msig.toFixed(4); mse.className='mv c-dim';
  const mhe=document.getElementById('m-hist'); mhe.textContent=mh.toFixed(4); mhe.className='mv '+(mh>=0?'c-green':'c-red');
  const bull=macd>msig;
  const mce=document.getElementById('m-cross'); mce.textContent=bull?'▲ BULLISH':'▼ BEARISH'; mce.className='mv '+(bull?'c-green':'c-red');
  const bpct=Math.min(100,Math.abs(mh)/Math.max(0.0001,Math.abs(macd))*70);
  const mb=document.getElementById('mbar'); mb.style.width=bpct+'%'; mb.style.background=mh>=0?'var(--green)':'var(--red)';
  // Stats row 1
  const vol=+s.Vol_Ratio||0;
  document.getElementById('s-atr').textContent=(+s.ATR||0).toFixed(2);
  const sve=document.getElementById('s-vol'); sve.textContent=vol.toFixed(2)+'×'; sve.className='stat-v '+(vol>=1.5?'c-green':'');
  const h52v=(+s.Pct_from_52W_High||0).toFixed(1);
  const h52e=document.getElementById('s-52h'); h52e.textContent=h52v+'%'; h52e.className='stat-v '+(+h52v>=-3?'c-green':+h52v<=-20?'c-red':'c-amber');
  document.getElementById('s-pe').textContent=s.PE_Ratio?((+s.PE_Ratio)||0).toFixed(1)+'×':'—';
  // Stats row 2
  const sk=+s.StochRSI_K||0, wr=+s.Williams_R||0, st=+s.Supertrend_Dir||0, bbpb=+s.BB_PctB||0;
  const ske=document.getElementById('s-stoch'); ske.textContent=sk.toFixed(0); ske.className='stat-v '+(sk>75?'c-red':sk<25?'c-green':'');
  const wre=document.getElementById('s-willr'); wre.textContent=wr.toFixed(0); wre.className='stat-v '+(wr>-20?'c-red':wr<-80?'c-green':'');
  const ste=document.getElementById('s-supert'); ste.textContent=st===1?'▲ BULL':st===-1?'▼ BEAR':'—'; ste.className='stat-v '+(st===1?'c-green':st===-1?'c-red':'c-dim');
  const bbe=document.getElementById('s-bbpb'); bbe.textContent=bbpb.toFixed(0)+'%'; bbe.className='stat-v '+(bbpb>80?'c-red':bbpb<20?'c-green':'');
}

// ── Chart controls ────────────────────────────────────────
function setTF(tf,btn){
  chartTF=tf;
  document.querySelectorAll('#tf-D,#tf-W,#tf-M').forEach(b=>b.classList.remove('on'));
  btn.classList.add('on');
  if(selected) loadChart(selected);
}
function setRange(n,btn){
  chartRange=n;
  document.querySelectorAll('.chart-controls .cc-btn').forEach(b=>{
    if(['1M','3M','6M','1Y','ALL'].includes(b.textContent))b.classList.remove('on');
  });
  if(btn) btn.classList.add('on');
  if(selected) loadChart(selected);
}
function toggleOverlay(name,btn){
  overlays[name]=!overlays[name];
  btn.classList.toggle('on',overlays[name]);
  if(selected) loadChart(selected);
}

// ── Aggregate to W/M ──────────────────────────────────────
function aggregateTF(rows,tf){
  if(tf==='D')return rows;
  const grp={};
  rows.forEach(r=>{
    const ds=String(r.Date||'').split(' ')[0];
    if(!ds||ds.length<8)return;
    const d=new Date(ds); let key;
    if(tf==='W'){
      const day=d.getDay()||7; const mon=new Date(d); mon.setDate(d.getDate()-day+1);
      key=mon.toISOString().split('T')[0];
    } else {
      key=ds.slice(0,7)+'-01';
    }
    if(!grp[key]) grp[key]={Date:key,Open:+r.Open,High:+r.High,Low:+r.Low,Close:+r.Close,Volume:+r.Volume||0};
    else{
      grp[key].High=Math.max(grp[key].High,+r.High);
      grp[key].Low=Math.min(grp[key].Low,+r.Low);
      grp[key].Close=+r.Close; grp[key].Volume+=+r.Volume||0;
    }
  });
  return Object.values(grp).sort((a,b)=>a.Date.localeCompare(b.Date));
}

// ── Load chart ────────────────────────────────────────────
async function loadChart(ticker){
  const wrap=document.getElementById('chart-container');
  wrap.innerHTML='<div class="chart-ph"><div>LOADING CHART…</div></div>';
  try{
    const rows=await csv(D+'enriched/'+ticker+'_enriched.csv');
    if(!rows||rows.length<10)throw new Error('Insufficient data');
    renderChart(rows,ticker);
  }catch(e){
    wrap.innerHTML=`<div class="chart-ph"><div>CHART UNAVAILABLE</div><div style="font-size:9px;color:var(--text3)">${e.message}</div></div>`;
  }
}

function renderChart(rawRows,ticker){
  const wrap=document.getElementById('chart-container');
  wrap.innerHTML='';
  if(lwChart){lwChart.remove();lwChart=null}
  let rows=rawRows.slice(-chartRange);
  rows=aggregateTF(rows,chartTF);
  if(!rows.length)return;
  const s=signals.find(x=>x.Ticker===ticker);
  lwChart=LightweightCharts.createChart(wrap,{
    width:wrap.clientWidth, height:260,
    layout:{background:{type:'solid',color:'#06090f'},textColor:'#5a7a99'},
    grid:{vertLines:{color:'#101828'},horzLines:{color:'#101828'}},
    crosshair:{mode:LightweightCharts.CrosshairMode.Normal},
    rightPriceScale:{borderColor:'#192840',scaleMargins:{top:0.06,bottom:overlays.vol?0.28:0.04}},
    timeScale:{borderColor:'#192840',timeVisible:true,fixLeftEdge:true,fixRightEdge:true},
  });
  const cs=lwChart.addCandlestickSeries({upColor:'#00e676',downColor:'#ff4560',borderUpColor:'#00e676',borderDownColor:'#ff4560',wickUpColor:'#00e676',wickDownColor:'#ff4560'});
  let vs=null;
  if(overlays.vol){
    vs=lwChart.addHistogramSeries({color:'#162032',priceFormat:{type:'volume'},priceScaleId:'vol'});
    lwChart.priceScale('vol').applyOptions({scaleMargins:{top:0.84,bottom:0}});
  }
  const ma50s=lwChart.addLineSeries({color:'#ffb300',lineWidth:1,lineStyle:2,priceLineVisible:false,lastValueVisible:false,crosshairMarkerVisible:false});
  const ma200s=lwChart.addLineSeries({color:'#4da6ff',lineWidth:1,lineStyle:0,priceLineVisible:false,lastValueVisible:false,crosshairMarkerVisible:false});
  let ema9s=null,ema21s=null,bbus=null,bbls=null;
  if(overlays.ema){
    ema9s=lwChart.addLineSeries({color:'#c084fc',lineWidth:1,priceLineVisible:false,lastValueVisible:false,crosshairMarkerVisible:false});
    ema21s=lwChart.addLineSeries({color:'#fb923c',lineWidth:1,priceLineVisible:false,lastValueVisible:false,crosshairMarkerVisible:false});
  }
  if(overlays.bb){
    bbus=lwChart.addLineSeries({color:'rgba(77,166,255,.45)',lineWidth:1,lineStyle:2,priceLineVisible:false,lastValueVisible:false,crosshairMarkerVisible:false});
    bbls=lwChart.addLineSeries({color:'rgba(77,166,255,.45)',lineWidth:1,lineStyle:2,priceLineVisible:false,lastValueVisible:false,crosshairMarkerVisible:false});
  }
  const cd=[],vd=[],m50=[],m200=[],e9=[],e21=[],bu=[],bl=[];
  rows.forEach(r=>{
    if(!r.Date||!r.Close)return;
    const t=String(r.Date).split(' ')[0];
    const op=+r.Open||+r.Close, hi=+r.High||+r.Close, lo=+r.Low||+r.Close, cl=+r.Close;
    if(!t||!cl)return;
    cd.push({time:t,open:op,high:hi,low:lo,close:cl});
    if(vs&&+r.Volume)vd.push({time:t,value:+r.Volume,color:cl>=op?'#0a2a18':'#2a0a12'});
    if(r.MA50&&+r.MA50)m50.push({time:t,value:+r.MA50});
    if(r.MA200&&+r.MA200)m200.push({time:t,value:+r.MA200});
    if(ema9s&&r.EMA9&&+r.EMA9)e9.push({time:t,value:+r.EMA9});
    if(ema21s&&r.EMA21&&+r.EMA21)e21.push({time:t,value:+r.EMA21});
    if(bbus&&r.BB_Upper&&+r.BB_Upper)bu.push({time:t,value:+r.BB_Upper});
    if(bbls&&r.BB_Lower&&+r.BB_Lower)bl.push({time:t,value:+r.BB_Lower});
  });
  cs.setData(cd);
  if(vs&&vd.length)vs.setData(vd);
  if(m50.length)ma50s.setData(m50);
  if(m200.length)ma200s.setData(m200);
  if(ema9s&&e9.length)ema9s.setData(e9);
  if(ema21s&&e21.length)ema21s.setData(e21);
  if(bbus&&bu.length)bbus.setData(bu);
  if(bbls&&bl.length)bbls.setData(bl);
  // Signal marker
  if(s&&cd.length){
    const last=cd[cd.length-1];
    const sig=s.Signal||'';
    if(sig.includes('BUY')||sig.includes('SELL')||sig==='WATCH'){
      cs.setMarkers([{time:last.time,position:sig.includes('BUY')?'belowBar':'aboveBar',
        color:sig.includes('BUY')?'#00e676':sig.includes('SELL')?'#ff4560':'#ffb300',
        shape:sig.includes('BUY')?'arrowUp':sig.includes('SELL')?'arrowDown':'circle',text:sig,size:1}]);
    }
  }
  lwChart.timeScale().fitContent();
  new ResizeObserver(()=>{if(lwChart)lwChart.applyOptions({width:wrap.clientWidth})}).observe(wrap);
}

// ── Heatmap ───────────────────────────────────────────────
function renderHeatmap(){
  if(!sectors.length){document.getElementById('heat-wrap').innerHTML='<div class="err-msg">sector_signals.csv not found.</div>';return}
  document.getElementById('heat-wrap').innerHTML=sectors.map(s=>{
    const c=s.Heatmap_Color||'a'; const cl=c==='green'?'g':c==='red'?'r':'a';
    const ni=+s.Net_Signal_Score>0?'▲':+s.Net_Signal_Score<0?'▼':'◈';
    return`<div class="hcell ${cl}"><div class="hn">${ni} ${s.Sector||'?'}</div><div class="hc">▲${s.BUY_Count||0} BUY · ▼${s.SELL_Count||0} SELL</div><div class="hr">RSI ${(+s.Avg_RSI||0).toFixed(1)} · ADX ${(+s.Avg_ADX||0).toFixed(0)}</div></div>`;
  }).join('');
}

// ── FII/DII chart ─────────────────────────────────────────
function renderFiiDii(){
  const wrap=document.getElementById('fii-wrap');
  if(!fiidii.length){wrap.innerHTML='<div class="err-msg">fii_dii.csv not found.</div>';return}
  const keys=Object.keys(fiidii[0]);
  const fc=n=>keys.find(k=>k.toUpperCase().replace(/[_\s]/g,'').includes(n))||null;
  const dc=fc('DATE')||keys[0], fic=fc('FIINET')||fc('FII'), dic=fc('DIINET')||fc('DII');
  const rec=fiidii.slice(-30);
  const labels=rec.map(r=>{const d=String(r[dc]||'');return d.length>=10?d.slice(5,10):d.slice(0,6)});
  const fv=rec.map(r=>fic?+r[fic]||0:0), dv=rec.map(r=>dic?+r[dic]||0:0);
  if(fiiChart){fiiChart.destroy();fiiChart=null}
  const ctx=document.getElementById('fii-chart').getContext('2d');
  fiiChart=new Chart(ctx,{type:'bar',data:{labels,datasets:[
    {label:'FII Net (₹Cr)',data:fv,backgroundColor:fv.map(v=>v>=0?'rgba(0,230,118,.45)':'rgba(255,69,96,.45)'),borderColor:fv.map(v=>v>=0?'#00e676':'#ff4560'),borderWidth:1,borderRadius:2},
    {label:'DII Net (₹Cr)',data:dv,backgroundColor:dv.map(v=>v>=0?'rgba(77,166,255,.35)':'rgba(255,179,0,.35)'),borderColor:dv.map(v=>v>=0?'#4da6ff':'#ffb300'),borderWidth:1,borderRadius:2},
  ]},options:{responsive:true,maintainAspectRatio:false,
    plugins:{legend:{labels:{color:'#5a7a99',font:{family:'JetBrains Mono',size:9},boxWidth:10}},
      tooltip:{backgroundColor:'#0c1220',borderColor:'#1f3050',borderWidth:1,titleColor:'#c8dff0',bodyColor:'#5a7a99',titleFont:{family:'JetBrains Mono',size:10},bodyFont:{family:'JetBrains Mono',size:9}}},
    scales:{x:{ticks:{color:'#2a4060',font:{family:'JetBrains Mono',size:8},maxRotation:45},grid:{color:'#101828'}},
      y:{ticks:{color:'#5a7a99',font:{family:'JetBrains Mono',size:9}},grid:{color:'#101828'}}}}});
}

// ── Alerts ────────────────────────────────────────────────
function renderAlerts(){
  const el=document.getElementById('tp-alerts');
  if(!alerts.length){el.innerHTML='<div class="empty">No signal changes detected yet.<br>Alerts appear when a signal upgrades or downgrades between runs.</div>';return}
  el.innerHTML=alerts.slice(0,60).map(a=>{
    const p=String(a.Change||'').split('→');
    const f=(p[0]||'').trim(), t=(p[1]||'').trim();
    const tc=t.includes('BUY')?'var(--green)':t.includes('SELL')?'var(--red)':t.includes('WATCH')?'var(--amber)':'var(--text)';
    return`<div class="arow" style="cursor:pointer" onclick="pick('${a.Ticker}')">
      <span class="aticker">${a.Ticker}</span>
      <span class="achg"><span class="c-dim">${f}</span><span class="c-dim"> → </span><span style="color:${tc};font-weight:600">${t}</span></span>
      <span class="adate">${a.Date_Changed||'—'}</span></div>`;
  }).join('');
}

// ── Watchlist ─────────────────────────────────────────────
function toggleWL(e,ticker){
  e.stopPropagation();
  const i=watchlist.indexOf(ticker);
  if(i===-1)watchlist.push(ticker);else watchlist.splice(i,1);
  localStorage.setItem('nse_wl',JSON.stringify(watchlist));
  renderScreener(); renderWatchlist();
}
function renderWatchlist(){
  const el=document.getElementById('wl-body');
  if(!watchlist.length){el.innerHTML='<div class="empty">No stocks in watchlist.<br>Click ☆ in the screener to add.</div>';return}
  el.innerHTML=watchlist.map(ticker=>{
    const s=signals.find(x=>x.Ticker===ticker);if(!s)return'';
    const chg=+s.Return_1D_pct||0;
    return`<div class="wrow" onclick="pick('${ticker}')">
      <span class="wtick">${ticker}</span>
      <span class="sig ${sigClass(s.Signal)}" style="font-size:9px;padding:1px 5px">${ic(s.Signal)} ${s.Signal||'NEUTRAL'}</span>
      <span class="${chg>=0?'up':'dn'}" style="font-size:11px;margin-left:auto;margin-right:5px">${chg>=0?'+':''}${chg.toFixed(2)}%</span>
      <button class="wrm" onclick="toggleWL(event,'${ticker}')">×</button></div>`;
  }).join('');
}

// ── Paper Trading ─────────────────────────────────────────
function executeTrade(action){
  if(!selected)return;
  const s=signals.find(x=>x.Ticker===selected);
  if(!s||!s.Close)return;
  const cmp=+s.Close, qty=parseInt(document.getElementById('trade-qty').value);
  const tf=document.getElementById('trade-tf').value;
  const notes=(document.getElementById('trade-notes').value||'').trim();
  const msgBox=document.getElementById('trade-msg');
  if(isNaN(qty)||qty<=0){msgBox.style.color='var(--amber)';msgBox.textContent='Enter valid qty.';return}
  const cost=cmp*qty;
  if(action==='BUY'){
    if(pt.cash<cost){msgBox.style.color='var(--red)';msgBox.textContent='Insufficient funds!';return}
    pt.cash-=cost;
    if(pt.positions[selected]){
      const o=pt.positions[selected];
      const nq=o.qty+qty, na=((o.qty*o.avg)+cost)/nq;
      pt.positions[selected]={qty:nq,avg:+na.toFixed(4),tf};
    }else{
      pt.positions[selected]={qty,avg:cmp,tf};
    }
    msgBox.style.color='var(--green)'; msgBox.textContent=`Bought ${qty} @ ₹${cmp.toFixed(2)}`;
    addJournalEntry('BUY',selected,qty,cmp,tf,s.Signal,+s.Score||0,+s.RSI||0,s.Rules_Fired||'',notes,null);
  }else if(action==='SELL'){
    const pos=pt.positions[selected];
    if(!pos||pos.qty<qty){msgBox.style.color='var(--red)';msgBox.textContent=`Only ${pos?pos.qty:0} shares held.`;return}
    const pnl=(cmp-pos.avg)*qty;
    pt.cash+=cost; pt.realised=(pt.realised||0)+pnl;
    pos.qty-=qty;
    if(pos.qty<=0)delete pt.positions[selected];
    const ps=pnl>=0?'+':'';
    msgBox.style.color=pnl>=0?'var(--green)':'var(--red)';
    msgBox.textContent=`Sold ${qty} @ ₹${cmp.toFixed(2)} | P&L: ${ps}₹${pnl.toFixed(0)}`;
    addJournalEntry('SELL',selected,qty,cmp,tf,s.Signal,+s.Score||0,+s.RSI||0,s.Rules_Fired||'',notes,pnl);
  }
  localStorage.setItem('nse_pt',JSON.stringify(pt));
  renderPortfolio(); renderJournal();
}

function resetPortfolio(){
  if(!confirm('Reset portfolio to ₹10,00,000? All positions will be cleared.'))return;
  pt={cash:1000000,positions:{},realised:0};
  localStorage.setItem('nse_pt',JSON.stringify(pt));
  renderPortfolio();
}

function renderPortfolio(){
  let totalCurr=pt.cash, unrealised=0;
  const posKeys=Object.keys(pt.positions||{});
  let html='';
  posKeys.forEach(ticker=>{
    const pos=pt.positions[ticker];
    const s=signals.find(x=>x.Ticker===ticker);
    const cmp=s&&+s.Close?+s.Close:pos.avg;
    const invest=pos.qty*pos.avg, curr=pos.qty*cmp, pnl=curr-invest, pp=(pnl/invest)*100;
    totalCurr+=curr; unrealised+=pnl;
    const pc=pnl>=0?'c-green':'c-red', sg=pnl>=0?'+':'';
    const tfbadge=pos.tf?`<span class="jtf ${pos.tf}" style="margin-right:2px">${pos.tf}</span>`:'';
    html+=`<div class="wrow" style="cursor:default">
      ${tfbadge}
      <span class="wtick" style="min-width:55px">${ticker}</span>
      <span class="nu" style="font-size:10px;min-width:28px">${pos.qty}×</span>
      <span class="c-dim" style="font-size:10px">avg ₹${pos.avg.toFixed(1)}</span>
      <span style="font-size:10px;margin-left:auto">₹${cmp.toFixed(1)}</span>
      <span class="${pc}" style="font-size:11px;font-weight:600;min-width:55px;text-align:right">${sg}₹${pnl.toFixed(0)}</span>
      <span class="${pc}" style="font-size:9px;min-width:38px;text-align:right">${sg}${pp.toFixed(1)}%</span>
      <button class="btn" style="padding:2px 5px;font-size:9px;margin-left:6px" onclick="pick('${ticker}')">TRADE</button>
    </div>`;
  });
  if(!posKeys.length)html='<div class="empty">No active positions.<br>Select a stock and click BUY to start.</div>';
  document.getElementById('pt-positions').innerHTML=html;
  const upc=unrealised>=0?'c-green':'c-red', rpc=(pt.realised||0)>=0?'c-green':'c-red';
  set('pt-cash',fmtINR(pt.cash));
  set('pt-total',fmtINR(totalCurr));
  const ue=document.getElementById('pt-upnl'); ue.textContent=(unrealised>=0?'+':'')+fmtINR(unrealised); ue.className='pt-val '+upc;
  const re=document.getElementById('pt-rpnl'); re.textContent=((pt.realised||0)>=0?'+':'')+fmtINR(pt.realised||0); re.className='pt-val '+rpc;
}

// ── Trade Journal ─────────────────────────────────────────
function addJournalEntry(action,ticker,qty,price,tf,signal,score,rsi,rules,notes,pnl){
  journal.unshift({
    id:Date.now(),
    date:new Date().toLocaleString('en-IN',{timeZone:'Asia/Kolkata',hour12:false}).replace(',',''),
    action,ticker,qty,price:+price.toFixed(2),tf:tf||'D',signal,score,rsi:+rsi.toFixed(1),
    rules:rules||'',notes:notes||'',
    pnl:pnl!==null&&pnl!==undefined?+pnl.toFixed(2):null,
  });
  if(journal.length>500)journal=journal.slice(0,500);
  localStorage.setItem('nse_journal',JSON.stringify(journal));
}

function renderJournal(){
  const closed=journal.filter(j=>j.pnl!==null);
  const wins=closed.filter(j=>j.pnl>0).length;
  const wr=closed.length?((wins/closed.length)*100).toFixed(0)+'%':'—';
  const totalPnl=closed.reduce((a,j)=>a+(j.pnl||0),0);
  const best=closed.length?Math.max(...closed.map(j=>j.pnl)):0;
  set('js-count',journal.length);
  set('js-wr',wr);
  const be=document.getElementById('js-best'); be.textContent=best>0?'+₹'+best.toFixed(0):'—'; be.className='js-val c-green';
  const pe=document.getElementById('js-pnl'); pe.textContent=(totalPnl>=0?'+':'')+fmtINR(totalPnl); pe.className='js-val '+(totalPnl>=0?'c-green':'c-red');
  const el=document.getElementById('jnl-body');
  if(!journal.length){el.innerHTML='<div class="empty">No journal entries yet.<br>Every paper trade is recorded here automatically.</div>';return}
  el.innerHTML=journal.map(j=>{
    const ac=j.action==='BUY'?'c-green':'c-red';
    const pc=j.pnl===null?'c-dim':(j.pnl>=0?'c-green':'c-red');
    const pv=j.pnl===null?'OPEN':(j.pnl>=0?'+₹'+j.pnl.toFixed(0):'₹'+j.pnl.toFixed(0));
    return`<div class="jrow">
      <span style="font-size:9px;color:var(--text3);min-width:95px;white-space:nowrap">${String(j.date||'').slice(0,16)}</span>
      <span class="jtf ${j.tf||'D'}">${j.tf||'D'}</span>
      <span class="wtick" style="min-width:55px;cursor:pointer" onclick="pick('${j.ticker}')">${j.ticker}</span>
      <span class="${ac}" style="font-weight:600;min-width:32px">${j.action}</span>
      <span class="nu" style="min-width:24px">${j.qty}×</span>
      <span class="c-dim">₹${j.price}</span>
      <span class="${pc}" style="font-weight:600;min-width:60px;text-align:right">${pv}</span>
      <span class="jnotes" title="${j.notes||''}">${j.notes||''}</span>
    </div>`;
  }).join('');
}

function exportJournal(){
  if(!journal.length)return;
  const keys=['date','action','ticker','qty','price','tf','signal','score','rsi','pnl','rules','notes'];
  const header=keys.join(',');
  const rows=journal.map(j=>keys.map(k=>{
    const v=(j[k]===null||j[k]===undefined)?'':String(j[k]);
    return'"'+v.replace(/"/g,'""')+'"';
  }).join(',')).join('\n');
  const blob=new Blob([header+'\n'+rows],{type:'text/csv'});
  const a=document.createElement('a');
  a.href=URL.createObjectURL(blob);
  a.download='nse_trade_journal_'+new Date().toISOString().slice(0,10)+'.csv';
  a.click(); URL.revokeObjectURL(a.href);
}

function clearJournal(){
  if(!confirm('Clear all journal entries? This cannot be undone.'))return;
  journal=[];
  localStorage.setItem('nse_journal','[]');
  renderJournal();
}

// ── Risk Calculator ───────────────────────────────────────
function calcRisk(){
  const cap=+document.getElementById('r-capital').value||1000000;
  const riskPct=+document.getElementById('r-riskpct').value||2;
  const entry=+document.getElementById('r-entry').value||0;
  const sl=+document.getElementById('r-sl').value||0;
  const tgt=+document.getElementById('r-target').value||0;
  set('r-riskpct-v',riskPct+'%');
  if(!entry||!sl||sl>=entry){
    set('r-shares','—'); set('r-capneeded','—'); set('r-maxrisk','—'); set('r-rr','—');
    set('r-advice','Enter a valid entry and stop-loss price (SL must be below entry for longs).');
    return;
  }
  const riskPerShare=entry-sl;
  const maxRisk=cap*riskPct/100;
  const shares=Math.floor(maxRisk/riskPerShare);
  const capNeeded=shares*entry;
  const rr=tgt>entry?((tgt-entry)/riskPerShare).toFixed(2):'—';
  const rrOk=tgt>entry&&(tgt-entry)/riskPerShare>=2;
  set('r-shares',shares>0?shares:'0');
  set('r-capneeded',shares>0?fmtINR(capNeeded):'—');
  set('r-maxrisk',fmtINR(maxRisk));
  document.getElementById('r-rr').textContent=rr==='—'?'—':'1 : '+rr;
  document.getElementById('r-rr').className='risk-val '+(rrOk?'c-green':rr!=='—'&&+rr<1.5?'c-red':'c-amber');
  const capPct=((capNeeded/cap)*100).toFixed(1);
  let advice=`Risk per trade: ${fmtINR(maxRisk)} (${riskPct}% of capital). `;
  advice+=`Position size: ${shares} shares = ${fmtINR(capNeeded)} (${capPct}% of capital). `;
  if(+capPct>20) advice+=`⚠ High concentration — consider reducing size. `;
  if(rrOk) advice+=`✓ R:R ratio ${rr} is favourable (≥ 2:1).`;
  else if(rr!=='—') advice+=`⚠ R:R ratio ${rr} is below the recommended 2:1 minimum.`;
  document.getElementById('r-advice').textContent=advice;
}

// ── Tabs ──────────────────────────────────────────────────
function showTab(name,btn){
  document.querySelectorAll('.tb').forEach(b=>b.classList.remove('on'));
  document.querySelectorAll('.tp').forEach(p=>p.classList.remove('on'));
  btn.classList.add('on');
  document.getElementById('tp-'+name).classList.add('on');
}

// ── Boot ──────────────────────────────────────────────────
loadAllData();
</script>
</body>
</html>
