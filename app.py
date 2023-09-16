import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from downloader import Downloader

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Congrats Umar on his new bike")

async def link(update: Update, context):
    link = " ".join(context.args)
    await update.message.reply_text("Downloading.... this may take a while")

    yt_downloader = Downloader(link)
    yt_downloader.download_video()

if __name__ == '__main__':
    application = ApplicationBuilder().token(
        '6371821489:AAGObhHZiXqvEgV-IQGtcBG_IdqE5aWMkBM').build()
    
    start_handler = CommandHandler('start', start)
    link_handler = CommandHandler('link', link)
    application.add_handler(start_handler)
    application.add_handler(link_handler)
    
    application.run_polling()