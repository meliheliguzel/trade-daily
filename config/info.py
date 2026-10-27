class InfoConfig:
    TITLE: str = "About TradeDaily"
    APP_NAME: str = "TradeDaily"
    VERSION: str = "0.1.0"
    AUTHOR: str = "Melih Eliguzel"
    LICENSE: str = "MIT License"
    LICENSE_URL: str = "https://opensource.org/licenses/MIT"
    GITHUB_URL: str = "https://github.com/meliheliguzel/trade-daily"
    ISSUES_URL: str = "https://github.com/meliheliguzel/trade-daily/issues"

    @classmethod
    def get_html_content(cls) -> str:
        return f"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html>
<head>
<meta name="qrichtext" content="1" />
<meta charset="utf-8" />
<style type="text/css">
body {{
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    font-size: 10pt;
    color: #e0e0e0;
    line-height: 1.6;
    margin: 16px;
    background-color: #121212;
}}
h1 {{
    color: #00CED1;
    font-size: 18pt;
    margin-bottom: 2px;
    text-align: center;
}}
.subtitle {{
    color: #a0a0a0;
    font-size: 10pt;
    text-align: center;
    margin-top: 2px;
    margin-bottom: 18px;
}}
h2 {{
    color: #4CAF50;
    font-size: 12pt;
    border-bottom: 1px solid #333333;
    padding-bottom: 4px;
    margin-top: 18px;
    margin-bottom: 8px;
}}
p, li {{
    color: #cccccc;
    font-size: 9.5pt;
}}
ul {{
    margin-top: 4px;
    margin-bottom: 12px;
    padding-left: 20px;
}}
li {{
    margin-bottom: 4px;
}}
.badge {{
    background-color: #212121;
    color: #00CED1;
    padding: 2px 8px;
    border-radius: 4px;
    font-weight: bold;
    border: 1px solid #333333;
}}
.tag {{
    background-color: #263238;
    color: #80cbc4;
    padding: 1px 6px;
    border-radius: 3px;
    font-size: 8.5pt;
}}
a {{
    color: #64B5F6;
    text-decoration: underline;
}}
.box {{
    background-color: #1c1c1c;
    border-left: 4px solid #00CED1;
    padding: 12px 14px;
    margin: 14px 0;
    border-radius: 2px;
}}
.box-warning {{
    background-color: #1f1b14;
    border-left: 4px solid #ffb74d;
    padding: 12px 14px;
    margin: 14px 0;
    border-radius: 2px;
}}
</style>
</head>
<body>

<h1>{cls.APP_NAME}</h1>
<p class="subtitle">Modern Desktop Trading Journal, Risk Management &amp; Portfolio Analytics<br />
<span class="badge">Version {cls.VERSION}</span> &nbsp; <span class="badge">Python 3.12+</span> &nbsp; <span class="badge">PySide6 (Qt6)</span></p>

<div class="box">
<b>Developer's Note: Purpose &amp; Philosophy</b><br />
<p style="margin-top: 6px; margin-bottom: 6px;">
<b>The Problem &amp; Solution:</b><br />
Consistent trading demands strict risk management, emotional discipline, and systematic post-trade review. However, most commercial journals are cloud-based, subscription-heavy ($30-$50/month), and force traders to upload sensitive financial balances and execution data to third-party servers.
</p>
<p style="margin-top: 6px; margin-bottom: 6px;">
<b>TradeDaily</b> was engineered as a 100% <b>offline-first, zero-subscription, privacy-focused</b> desktop solution where all data resides securely on your local machine. Built with Python 3.12, PySide6 (Qt6), and Plotly, it combines disciplined risk calculation, segregated multi-account tracking, permanent in-database chart archiving, and interactive equity curve analytics—backed by an automated test suite of <b>237 tests (91% coverage)</b>.
</p>
<p style="margin-top: 6px; margin-bottom: 2px;">
Community feedback, feature discussions, and pull requests are warmly welcomed on GitHub!
</p>
</div>

<h2>Core Capabilities</h2>
<ul>
    <li><b>Disciplined Trading Journal:</b> Track trade parameters (Platform, Parity, Direction, Entry/Exit Dates, R:R, Position Size, Target/Stop/Exit Prices, Net P&amp;L) across Open, TP, and SL states.</li>
    <li><b>Multi-Strategy Tagging:</b> Associate multiple trading setups with each transaction to evaluate individual strategy profitability and win rates.</li>
    <li><b>Permanent In-Database Chart Archiving:</b> Store chart screenshots directly inside the SQLite database as binary blobs (BLOB) or attach external web links (e.g., TradingView) with native in-app preview.</li>
    <li><b>Interactive Visual Analytics:</b> Plotly &amp; QtWebEngine-powered dynamic charts including Long/Short distribution, Win/Loss ratios, Strategy usage, and R:R performance.</li>
    <li><b>Capital &amp; Equity Curve Tracking:</b> Monitor account progression and balance growth curves over time.</li>
    <li><b>Multi-Account Management:</b> Manage distinct profiles (Spot, Futures, Prop Firm / Funded) with fully segregated SQLite databases and logs.</li>
    <li><b>Integrated R:R Calculator:</b> Quickly compute optimal position sizing and risk-reward ratios.</li>
    <li><b>High-Performance Lazy Loading:</b> Smoothly browse extensive transaction histories with infinite scroll and dynamic sorting.</li>
</ul>

<h2>Planned Future Roadmap</h2>
<ul>
    <li><b>Import &amp; Export:</b> Support for CSV and Excel trade history import/export.</li>
    <li><b>Exchange API Synchronization:</b> Read-only sync for closed orders from major exchanges (e.g., Binance, Bybit).</li>
    <li><b>Advanced Time Analytics:</b> Performance breakdown by day of week, market session, and holding duration.</li>
    <li><b>Theme Customization:</b> Dynamic Dark and Light theme toggle.</li>
    <li><b>Multi-Currency Accounting:</b> Native multi-currency portfolio tracking (USD, EUR, USDT, BTC).</li>
</ul>

<h2>Architecture &amp; Tech Stack</h2>
<p>
Built with a clean, decoupled <b>Model-View-Controller (MVC)</b> architecture:<br />
<span class="tag">Python 3.12</span> &bull; <span class="tag">PySide6 (Qt6)</span> &bull; <span class="tag">Plotly 6</span> &bull; <span class="tag">SQLite3</span> &bull; <span class="tag">Ruff</span> &bull; <span class="tag">Pytest (237 Tests - 91% Coverage)</span>
</p>

<h2>Developer &amp; Community</h2>
<p>
Developed by <b>{cls.AUTHOR}</b>.<br />
GitHub Repository: <a href="{cls.GITHUB_URL}">{cls.GITHUB_URL}</a><br />
Issues &amp; Discussions: <a href="{cls.ISSUES_URL}">{cls.ISSUES_URL}</a>
</p>

<h2>License</h2>
<p>
This software is distributed under the <b>{cls.LICENSE}</b>.<br />
You are free to use, inspect, modify, and distribute this software in accordance with the terms of the license.
</p>

<div class="box-warning">
<b>⚠️ Financial Disclaimer</b><br />
TradeDaily is strictly an informational record-keeping, trade journaling, and quantitative risk calculation tool. It does <b>not</b> provide investment, financial, legal, or tax advice. Financial trading involves significant risk of capital loss. The author assumes no responsibility or liability for any financial decisions, trades, or losses incurred through the use of this software.
</div>

</body>
</html>
"""
