import requests
import json
from datetime import datetime

class TelegramBot:
    def __init__(self, bot_token=None, chat_id=None):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}" if bot_token else None
        
    def test_connection(self):
        """Test if the bot can connect and send messages"""
        if not self.bot_token or not self.chat_id:
            print("❌ Bot token or chat ID not configured")
            return False
            
        try:
            url = f"{self.base_url}/getMe"
            response = requests.get(url)
            if response.status_code == 200:
                bot_info = response.json()
                print(f"✅ Bot connected: @{bot_info['result']['username']}")
                return True
            else:
                print(f"❌ Bot connection failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error testing bot: {e}")
            return False
    
    def send_message(self, message):
        """Send a message to the configured chat"""
        if not self.bot_token or not self.chat_id:
            print("❌ Bot not configured")
            return False
            
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, data=data)
            if response.status_code == 200:
                print(f"✅ Message sent to Telegram")
                return True
            else:
                print(f"❌ Failed to send message: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error sending message: {e}")
            return False
    
    def send_trading_alert(self, stock, price, rsi, strategy_signal, ml_prediction, recommendation):
        """Send a formatted trading alert"""
        # Handle RSI formatting
        try:
            rsi_value = float(rsi) if rsi != 'N/A' else 0
            rsi_str = f"{rsi_value:.2f}" if rsi != 'N/A' else "N/A"
        except:
            rsi_str = str(rsi)
        
        message = f"""
🚨 <b>TRADING ALERT</b> 🚨

📊 <b>Stock:</b> {stock}
💰 <b>Price:</b> ₹{price}
📈 <b>RSI:</b> {rsi_str}
🎯 <b>Strategy:</b> {strategy_signal}
🤖 <b>ML Prediction:</b> {ml_prediction}
💡 <b>Recommendation:</b> {recommendation}

⏰ <i>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>
        """
        return self.send_message(message.strip())
    
    def send_system_summary(self, total_trades, total_pl, ml_confidence, stocks_analyzed):
        """Send system performance summary"""
        message = f"""
📊 <b>SYSTEM SUMMARY</b> 📊

📈 <b>Total Trades:</b> {total_trades}
💰 <b>Total P&L:</b> ₹{total_pl:.2f}
🤖 <b>ML Confidence:</b> {ml_confidence:.2%}
📋 <b>Stocks Analyzed:</b> {stocks_analyzed}

⏰ <i>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>
        """
        return self.send_message(message.strip())
    
    def send_system_status(self, status="ACTIVE"):
        """Send system status update"""
        emoji = "🟢" if status == "ACTIVE" else "🔴"
        message = f"""
{emoji} <b>SYSTEM STATUS</b> {emoji}

🔄 <b>Status:</b> {status}
📊 <b>Google Sheets:</b> Connected
🤖 <b>ML Models:</b> Loaded
📈 <b>Strategy:</b> Running

⏰ <i>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>
        """
        return self.send_message(message.strip())

def setup_telegram_bot():
    """Interactive setup for Telegram bot"""
    print("🤖 Setting up Telegram Bot")
    print("=" * 40)
    
    print("📋 Instructions:")
    print("1. Create a bot with @BotFather on Telegram")
    print("2. Get your bot token")
    print("3. Get your chat ID")
    print("4. Enter the details below")
    print()
    
    bot_token = input("🔑 Enter your bot token: ").strip()
    chat_id = input("💬 Enter your chat ID: ").strip()
    
    if not bot_token or not chat_id:
        print("❌ Bot token or chat ID not provided")
        return None
    
    # Test the bot
    bot = TelegramBot(bot_token, chat_id)
    if bot.test_connection():
        print("✅ Bot setup successful!")
        
        # Send test message
        test_message = f"""
🤖 <b>BOT CONNECTED!</b> 🤖

✅ Your algo-trading Telegram bot is now active!
📊 You'll receive alerts when trading signals are generated.
🤖 ML predictions and system updates will be sent here.

⏰ <i>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>
        """
        
        if bot.send_message(test_message.strip()):
            print("✅ Test message sent successfully!")
            return bot
        else:
            print("❌ Failed to send test message")
            return None
    else:
        print("❌ Bot setup failed")
        return None

def test_telegram_bot():
    """Test the Telegram bot functionality"""
    print("🧪 Testing Telegram Bot")
    print("=" * 40)
    
    bot = setup_telegram_bot()
    if not bot:
        return False
    
    # Test different message types
    print("\n📤 Testing message types...")
    
    # Test trading alert
    bot.send_trading_alert(
        stock="RELIANCE.NS",
        price="1515.40",
        rsi=68.99,
        strategy_signal="HOLD",
        ml_prediction="DOWN",
        recommendation="HOLD"
    )
    
    # Test system summary
    bot.send_system_summary(
        total_trades=2,
        total_pl=-429.47,
        ml_confidence=0.5602,
        stocks_analyzed=3
    )
    
    # Test system status
    bot.send_system_status("ACTIVE")
    
    print("\n✅ Telegram bot testing complete!")
    return True

if __name__ == "__main__":
    test_telegram_bot() 