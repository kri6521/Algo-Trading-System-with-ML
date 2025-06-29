import yfinance as yf
import pandas as pd
import os

def fetch_stock_data(ticker, period='6mo', interval='1d'):
    stock = yf.Ticker(ticker)
    df = stock.history(period=period, interval=interval)
    df.reset_index(inplace=True)
    df['Ticker'] = ticker
    return df

if __name__ == "__main__":
    stocks = ['RELIANCE.NS', 'INFY.NS', 'HDFCBANK.NS']
    all_data = pd.concat([fetch_stock_data(t) for t in stocks])
    os.makedirs('data', exist_ok=True)
    all_data.to_csv('data/stock_data.csv', index=False) 