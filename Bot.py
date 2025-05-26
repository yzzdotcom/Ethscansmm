import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Telegram bot token and SMM panel config
BOT_TOKEN = '8136824737:AAENPUi-XV9-hjKAyMInDFLjaHdhefmncZk'
API_KEY = 'fK6aGhCOXIxz0uRi7KbghLxAkP7z3DPJ'
PANEL_URL = 'https://ethioscan.com/api/v1'

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to the EthioScan SMM Bot!\n\n"
        "Commands:\n"
        "/services - View services\n"
        "/balance - Check balance\n"
        "/order <service_id> <link> <quantity>\n"
        "/status <order_id>"
    )

# /services
async def services(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = requests.post(PANEL_URL, data={"key": API_KEY, "action": "services"})
    data = response.json()

    if isinstance(data, list):
        message = ""
        for service in data[:20]:  # Limit to 20 for Telegram message limit
            message += f"ID: {service['service']}\nName: {service['name']}\nRate: ${service['rate']}/1000\n\n"
        await update.message.reply_text(message or "No services found.")
    else:
        await update.message.reply_text("Failed to fetch services.")

# /balance
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = requests.post(PANEL_URL, data={"key": API_KEY, "action": "balance"})
    data = response.json()

    if 'balance' in data:
        await update.message.reply_text(f"Balance: ${data['balance']}\nCurrency: {data['currency']}")
    else:
        await update.message.reply_text("Failed to retrieve balance.")

# /order
async def order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 3:
        await update.message.reply_text("Usage:\n/order <service_id> <link> <quantity>")
        return

    service_id, link, quantity = args[0], args[1], args[2]

    payload = {
        "key": API_KEY,
        "action": "add",
        "service": service_id,
        "link": link,
        "quantity": quantity
    }

    response = requests.post(PANEL_URL, data=payload)
    data = response.json()

    if 'order' in data:
        await update.message.reply_text(f"Order placed successfully!\nOrder ID: {data['order']}")
    else:
        await update.message.reply_text(f"Error placing order:\n{data}")

# /status
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 1:
        await update.message.reply_text("Usage:\n/status <order_id>")
        return

    order_id = args[0]

    payload = {
        "key": API_KEY,
        "action": "status",
        "order": order_id
    }

    response = requests.post(PANEL_URL, data=payload)
    data = response.json()

    if 'status' in data:
        status_msg = "\n".join(f"{k}: {v}" for k, v in data.items())
        await update.message.reply_text(f"Order Status:\n{status_msg}")
    else:
        await update.message.reply_text("Failed to retrieve order status.")

# Main bot runner
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("services", services))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("order", order))
    app.add_handler(CommandHandler("status", status))

    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
