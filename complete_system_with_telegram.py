import pandas as pd
import os
from datetime import datetime
from integrated_system import run_integrated_system
from working_google_sheets_fixed import GoogleSheetsLogger
from telegram_bot import TelegramBot
from telegram_config import load_telegram_config

def run_complete_system_with_telegram():
    """Run complete algo-trading system with Google Sheets and Telegram integration"""
    print("🚀 COMPLETE ALGO-TRADING SYSTEM")
    print("=" * 60)
    print("Strategy + ML + Google Sheets + Telegram Alerts")
    print("=" * 60)
    
    # Step 1: Initialize Telegram Bot
    print("\n🤖 Initializing Telegram Bot...")
    bot_token, chat_id = load_telegram_config()
    
    telegram_bot = None
    if bot_token and chat_id:
        telegram_bot = TelegramBot(bot_token, chat_id)
        if telegram_bot.test_connection():
            print("✅ Telegram bot connected!")
            telegram_bot.send_system_status("STARTING")
        else:
            print("⚠️  Telegram bot connection failed")
            telegram_bot = None
    else:
        print("⚠️  Telegram bot not configured")
    
    # Step 2: Run the integrated analysis
    print("\n📊 Running Integrated Analysis...")
    results = run_integrated_system()
    
    if not results:
        print("❌ No results to process")
        if telegram_bot:
            telegram_bot.send_message("❌ System Error: No results generated")
        return
    
    # Step 3: Initialize Google Sheets logger
    print("\n🔗 Setting up Google Sheets...")
    logger = GoogleSheetsLogger()
    
    sheets_success = False
    if logger.connect() and logger.find_or_create_sheet():
        sheets_success = True
        print("✅ Google Sheets connected!")
    else:
        print("❌ Google Sheets connection failed")
    
    # Step 4: Prepare data for Google Sheets
    print("\n📝 Preparing data for Google Sheets...")
    
    # Prepare trades data
    trades_data = []
    for result in results:
        trades_data.append({
            'Date': datetime.now().strftime('%Y-%m-%d'),
            'Stock': result['stock'],
            'Price': result.get('current_price', 'N/A'),
            'RSI': result.get('current_rsi', 'N/A'),
            'Strategy_Signal': result['recommendation'],
            'ML_Prediction': result['ml_prediction']['direction'],
            'Recommendation': result['recommendation']
        })
    
    # Prepare summary data
    total_trades = sum(r['strategy_stats']['Total Trades'] for r in results)
    total_pl = sum(r['strategy_stats']['Net P&L'] for r in results)
    ml_confidence = sum(r['ml_prediction']['confidence'] for r in results) / len(results)
    
    summary_data = {
        'Total Strategy Trades': str(total_trades),
        'Total Strategy P&L': f"₹{total_pl:.2f}",
        'Average ML Confidence': f"{ml_confidence:.2%}",
        'Analysis Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Stocks Analyzed': str(len(results)),
        'System Status': 'ACTIVE'
    }
    
    # Step 5: Log to Google Sheets
    if sheets_success:
        print("\n📊 Logging to Google Sheets...")
        trades_success = logger.log_trades(trades_data)
        summary_success = logger.log_summary(summary_data)
        sheets_success = trades_success and summary_success
    
    # Step 6: Send Telegram Alerts
    if telegram_bot:
        print("\n📱 Sending Telegram Alerts...")
        
        # Send individual trading alerts for each stock
        for result in results:
            telegram_bot.send_trading_alert(
                stock=result['stock'],
                price=result.get('current_price', 'N/A'),
                rsi=result.get('current_rsi', 'N/A'),
                strategy_signal=result['recommendation'],
                ml_prediction=result['ml_prediction']['direction'],
                recommendation=result['recommendation']
            )
        
        # Send system summary
        telegram_bot.send_system_summary(
            total_trades=total_trades,
            total_pl=total_pl,
            ml_confidence=ml_confidence,
            stocks_analyzed=len(results)
        )
        
        # Send final status
        telegram_bot.send_system_status("COMPLETED")
    
    # Step 7: Save to CSV as backup
    print("\n💾 Saving backup to CSV...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs('results', exist_ok=True)
    
    # Save detailed CSV
    detailed_data = []
    for result in results:
        detailed_data.append({
            'Stock': result['stock'],
            'Date': datetime.now().strftime("%Y-%m-%d"),
            'Current_Price': result.get('current_price', 'N/A'),
            'Current_RSI': result.get('current_rsi', 'N/A'),
            'Strategy_Buy_Signals': result['strategy_signals']['buy'],
            'Strategy_Sell_Signals': result['strategy_signals']['sell'],
            'Strategy_Total_Trades': result['strategy_stats']['Total Trades'],
            'Strategy_Win_Ratio': result['strategy_stats']['Win Ratio'],
            'Strategy_Net_PL': result['strategy_stats']['Net P&L'],
            'ML_Prediction': result['ml_prediction']['direction'],
            'ML_Confidence': result['ml_prediction']['confidence'],
            'Recommendation': result['recommendation'],
            'Reason': result['reason']
        })
    
    detailed_df = pd.DataFrame(detailed_data)
    detailed_file = f'results/detailed_analysis_{timestamp}.csv'
    detailed_df.to_csv(detailed_file, index=False)
    
    # Save summary CSV
    summary_df = pd.DataFrame(list(summary_data.items()), columns=['Metric', 'Value'])
    summary_file = f'results/summary_{timestamp}.csv'
    summary_df.to_csv(summary_file, index=False)
    
    # Step 8: Final Results
    print(f"\n🎉 SYSTEM EXECUTION COMPLETE!")
    print(f"=" * 60)
    
    if sheets_success:
        print(f"✅ Google Sheets integration: SUCCESS")
        print(f"📊 View your sheet: {logger.get_sheet_url()}")
    else:
        print(f"❌ Google Sheets integration: FAILED")
    
    if telegram_bot:
        print(f"✅ Telegram alerts: SUCCESS")
    else:
        print(f"⚠️  Telegram alerts: NOT CONFIGURED")
    
    print(f"✅ CSV backup: SUCCESS")
    print(f"📁 CSV files: {detailed_file}, {summary_file}")
    
    print(f"\n📈 PERFORMANCE SUMMARY:")
    print(f"   Total trades: {total_trades}")
    print(f"   Total P&L: ₹{total_pl:.2f}")
    print(f"   ML confidence: {ml_confidence:.2%}")
    
    print(f"\n🎯 CURRENT RECOMMENDATIONS:")
    for result in results:
        print(f"   {result['stock']}: {result['recommendation']} - {result['reason']}")
    
    print(f"\n🔗 Data saved to:")
    if sheets_success:
        print(f"   📊 Google Sheets: {logger.get_sheet_url()}")
    print(f"   📁 Local CSV: results/ folder")
    if telegram_bot:
        print(f"   📱 Telegram: Alerts sent")
    
    return True

if __name__ == "__main__":
    run_complete_system_with_telegram() 