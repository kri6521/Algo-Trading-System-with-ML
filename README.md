# Algo Trading System (RSI + MA Crossover, ML, Google Sheets, Telegram)

## Overview
A modular, production-ready algo-trading system for NIFTY stocks featuring:
- RSI + Moving Average (MA) crossover strategy
- Machine Learning (ML) predictions
- Google Sheets logging
- Telegram alerts
- CSV backup

## Project Structure
```
.
├── data/                  # Stock data (CSV)
├── models/                # Trained ML models (per stock)
├── results/               # CSV backups of trades and summaries
├── fetch_data.py          # Fetches historical stock data
├── strategy.py            # Implements RSI + MA crossover logic
├── backtest.py            # Backtests strategy on historical data
├── ml_model.py            # ML model training and prediction
├── google_sheets.py       # Google Sheets API integration
├── telegram_bot.py        # Telegram bot for alerts
├── main.py                # Main orchestration (strategy + Sheets)
├── complete_system_with_telegram.py # Full system: strategy + ML + Sheets + Telegram
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## File-by-File Explanation

### main.py
**Entry point for the basic system.**
- Fetches data for selected stocks
- Runs the RSI+MA strategy
- Logs trades and summary to Google Sheets
- (Optionally) sends Telegram alerts

### fetch_data.py
**Fetches historical stock data using yfinance.**
- Can be run standalone to save data to `data/stock_data.csv`
- Used by main.py and other modules

### strategy.py
**Implements the RSI + MA crossover strategy.**
- Calculates 20DMA, 50DMA, and RSI
- Generates buy/sell signals based on indicator logic

### backtest.py
**Backtests the strategy on historical data.**
- Evaluates performance: win ratio, P&L, etc.
- Used by main.py and the full system

### ml_model.py
**Trains and applies a simple ML model (Decision Tree) for next-day prediction.**
- Uses technical indicators as features
- Returns model and accuracy

### google_sheets.py
**Handles Google Sheets integration.**
- Connects to a Google Sheet (requires `creds.json`)
- Logs trades and summary to `Trade_Log` and `Summary` worksheets

### telegram_bot.py
**Sends alerts and summaries to Telegram.**
- Requires bot token and chat ID
- Used for real-time notifications

### complete_system_with_telegram.py
**Full-featured system runner.**
- Combines strategy, ML, Google Sheets, and Telegram alerts
- Produces CSV backups in `results/`
- Recommended for production/demo

## Setup
1. Clone the repo or copy files.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up Google Sheets API credentials as `creds.json` (see [gspread docs](https://gspread.readthedocs.io/en/latest/oauth2.html)).
4. (Optional) Set up Telegram bot token and chat ID in `telegram_bot.py`.

## Usage
- **Fetch data:**
  ```bash
  python fetch_data.py
  ```
- **Run basic system:**
  ```bash
  python main.py
  ```
- **Run full system (strategy + ML + Sheets + Telegram):**
  ```bash
  python complete_system_with_telegram.py
  ```

## Notes
- Google Sheet must have worksheets: `Trade_Log` and `Summary`.
- For ML, see `ml_model.py`.
- For Telegram alerts, see `telegram_bot.py`.
- CSV backups are saved in `results/`.

## Demo
- [Add Loom/OBS video link here]
- [Google Sheet link here](https://docs.google.com/spreadsheets/d/1XT_is_R2tR_qscBiSxie2PP5ZSfjNe1DqpScPoK-1Eo/edit?gid=1395192561#gid=1395192561)
