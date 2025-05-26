import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Your API key and panel URL
API_KEY = 'fK6aGhCOXIxz0uRi7KbghLxAkP7z3DPJ'
PANEL_URL = 'https://ethioscan.com/api/v1'

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the EthioScan SMM Bot!\n\nCommands:\n/services - View services\n/balance - Check your balance")

# Command: /services
async def services(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = requests.post(PANEL_URL, data={
        'key': API_KEY,
        'action': 'services'
    })
    data = response.json()

    if isinstance(data, list):
        message = ""
        for service in data[:20]:  # Limit output for Telegram
            message += f"{service['service']}: {service['name']} - ${service['rate']} per 1000\n"
        await update.message.reply_text(message or "No services found.")
    else:
        await update.message.reply_text("Failed to fetch services.")

# Command: /balance
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = requests.post(PANEL_URL, data={
        'key': API_KEY,
        'action': 'balance'
    })
    data = response.json()

    if 'balance' in data:
        await update.message.reply_text(f"Balance: ${data['balance']}\nCurrency: {data['currency']}")
    else:
        await update.message.reply_text("Failed to retrieve balance.")

# Main
def main():
    app = ApplicationBuilder().token("YOUR_TELEGRAM_BOT_TOKEN").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("services", services))
    app.add_handler(CommandHandler("balance", balance))

    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
