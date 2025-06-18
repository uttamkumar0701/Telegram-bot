
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

ADMIN_ID = 6241099044

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await context.bot.send_message(chat_id=update.effective_chat.id,
        text=f"Hello {user.first_name}, your message will be sent to the admin.")
    await context.bot.send_message(chat_id=ADMIN_ID,
        text=f"📥 New message from {user.full_name} (ID: {user.id})")

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    await context.bot.send_message(chat_id=ADMIN_ID,
        text = f"📨 Message from {user.first_name} (ID: {user.id}):\n\n{message.text}"

if __name__ == '__main__':
    app = ApplicationBuilder().token("7381963215:AAF5W1vWsNcoJgWKWpT0Na-kF5eIwpElxhM").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), message_handler))
    app.run_polling()
