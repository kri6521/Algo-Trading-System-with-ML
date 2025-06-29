import pandas as pd

def calculate_indicators(df):
    df['20DMA'] = df['Close'].rolling(window=20).mean()
    df['50DMA'] = df['Close'].rolling(window=50).mean()
    delta = df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

def generate_signals(df):
    df = calculate_indicators(df)
    df['Buy_Signal'] = (df['RSI'] < 30) & (df['20DMA'] > df['50DMA'])
    df['Sell_Signal'] = (df['RSI'] > 70) & (df['20DMA'] < df['50DMA'])
    return df 