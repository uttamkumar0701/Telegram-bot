import logging
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler

import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await context.bot.send_message(
        chat_id=user.id,
        text="👋 Welcome! Your message will be sent to the admin."
    )


async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.message

    if message.text:
        text = f"📨 Message from {user.first_name} (ID: {user.id}):\n{message.text}"
        await context.bot.send_message(chat_id=ADMIN_ID, text=text)

    elif message.photo:
        photo_file = await message.photo[-1].get_file()
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo_file.file_id,
            caption=f"📷 Photo from {user.first_name} (ID: {user.id})"
        )

    elif message.document:
        doc = await message.document.get_file()
        await context.bot.send_document(
            chat_id=ADMIN_ID,
            document=InputFile(doc.file_path),
            caption=f"📄 Document from {user.first_name} (ID: {user.id})"
        )

    else:
        await context.bot.send_message(chat_id=ADMIN_ID, text="⚠️ Unsupported message type.")


async def reply_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        try:
            user_id = int(update.message.reply_to_message.text.split("ID: ")[1].split(")")[0])
            await context.bot.send_message(chat_id=user_id, text=update.message.text)
        except Exception as e:
            await context.bot.send_message(chat_id=ADMIN_ID, text="❌ Failed to reply to user.")


if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.REPLY & filters.TEXT, reply_to_user))
    app.add_handler(MessageHandler(filters.ALL, forward_to_admin))

    print("✅ Bot is running...")
    app.run_polling()
