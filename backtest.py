def backtest(df):
    buy_price = None
    returns = []
    for idx, row in df.iterrows():
        if row['Buy_Signal'] and not buy_price:
            buy_price = row['Close']
        elif row['Sell_Signal'] and buy_price:
            returns.append(row['Close'] - buy_price)
            buy_price = None
    total_trades = len(returns)
    wins = [r for r in returns if r > 0]
    win_ratio = len(wins) / total_trades if total_trades > 0 else 0
    return {
        "Total Trades": total_trades,
        "Win Ratio": win_ratio,
        "Net P&L": sum(returns)
    } 