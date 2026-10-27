# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] - 2026-10-27

### 🎉 Initial Public Release (Beta)

Welcome to the first public, open-source release of **TradeDaily** — a local-first desktop trading journal, quantitative risk calculator, and portfolio analytics suite.

#### ✨ Core Capabilities
- **Disciplined Trading Journal:**
  - Log trade executions with Platform, Parity, Direction (Long/Short), R:R, Position Size, Entry/Exit Dates, Target/Stop/Exit Prices, and Net P&L.
  - Track Open, Take Profit (TP), and Stop Loss (SL) states with automated balance updates.
  - Multi-strategy tagging per transaction to isolate strategy win rates.
  - In-database chart screenshot archiving (`BLOB`) and TradingView URL attachment with in-app preview.
  - Dedicated contextual trade notes and execution reflections.
- **Risk / Reward (R:R) Calculator:**
  - Fast position sizing and risk factor calculations based on stop loss distance and account leverage.
- **Interactive Visual Analytics:**
  - Dark-mode Plotly analytics rendered via embedded `QtWebEngine`:
    - Long vs. Short distribution.
    - Win/Loss (TP vs. SL) ratio.
    - Strategy performance and frequency breakdown.
    - Cumulative balance growth (Equity Curve) over time.
    - Per-trade R:R distribution and net balance impacts.
    - One-click high-resolution chart export to Downloads folder.
- **Multi-Account / Segregated Profiles:**
  - Manage independent accounts (e.g., Spot, Futures, Prop Firm) with dedicated SQLite databases, logs, and analytics.
  - Instant account switching directly from the top menu bar.
- **High-Performance Lazy Loading Table:**
  - Infinite scroll transaction table with dynamic chronological sorting and real-time statistics summary bar.
- **Cross-Platform Standalone Packaging:**
  - Standalone packaging support for Linux, Windows, and macOS via PyInstaller and automated GitHub Actions workflows.

#### 🛠 Engineering & Reliability
- Built with **Python 3.12+**, **PySide6 (Qt6)**, and **Plotly 6**.
- Clean, decoupled **Model-View-Controller (MVC)** layered architecture.
- Thread-safe Singleton SQLite connection management with strict transaction safety.
- Cross-platform test suite of **237 unit and integration tests** passing with 0 errors (>90% test coverage).
- Strict Ruff linting and PEP 8 compliance.
- Modern Ubuntu 24.04 (Noble Numbat) and Windows NTFS file system compatibility.
