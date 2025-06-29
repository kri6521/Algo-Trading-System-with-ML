from fetch_data import fetch_stock_data
from strategy import generate_signals
from backtest import backtest
from google_sheets import connect_to_sheet, log_trades, log_summary
import pandas as pd
# from telegram_bot import send_telegram_message  # Uncomment if using Telegram

def run_algo():
    stocks = ['RELIANCE.NS', 'INFY.NS', 'HDFCBANK.NS']
    all_data = []
    for s in stocks:
        df = fetch_stock_data(s)
        df = generate_signals(df)
        df['Ticker'] = s
        all_data.append(df)
    final_df = pd.concat(all_data)
    trades = final_df[final_df['Buy_Signal'] | final_df['Sell_Signal']][['Date', 'Ticker', 'Close', 'RSI', 'Buy_Signal', 'Sell_Signal']]
    stats = backtest(final_df)
    sheet = connect_to_sheet("Algo_Trading_Log")
    log_trades(trades, sheet)
    log_summary(stats, sheet)
    # if not trades.empty:
    #     send_telegram_message("New trade signals generated. Check Google Sheets.")

if __name__ == "__main__":
    run_algo() 