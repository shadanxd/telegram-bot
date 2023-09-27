import logging
import os
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from downloader import Downloader
import config

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Paste youtube video or instagram reel link to download it")
async def link(update: Update, context):
    link = update.message.text
    await update.message.reply_text("Downloading.... this may take a while")
    downloader = Downloader(link)
    status = False
    try:
        if link.find('instagram') != -1:
            print("dowloading insta")
            await downloader.download_instagram()
        elif link.find('youtu.be') != -1 or link.find('youtube'):
            print("downloading YT")
            await downloader.download_youtube()
    except Exception as e:
        logging.error("Invalid URL")
        await update.message.reply_text("Invalid URL")
    if downloader.downloaded_path is not None:
        await update.message.reply_text("Now Uploading....")
        
        # Upload the downloaded file
        await upload(update, context, path=downloader.downloaded_path)
        
        # Delete the downloaded file after uploading
        del downloader
    else:
        await update.message.reply_text("Uploading Failed")

async def upload(update: Update, context: ContextTypes.DEFAULT_TYPE, path):
    try:
        with open(path, 'rb') as file:
            await context.bot.send_document(chat_id=update.effective_chat.id, document=InputFile(file))
        
        # After successful upload, delete the file
        os.remove(path)
        
        await logging.INFO(f"File Uploaded: {path}")
    except Exception as e:
        logging.error(f"Error uploading or deleting file: {e}")
    
if __name__ == '__main__':
    application = ApplicationBuilder().token(config.bot_token).build()
    
    start_handler = CommandHandler('start', start)
    link_handler = MessageHandler(filters.TEXT & (filters.Entity("url") | filters.Entity("text_link")), link)
    application.add_handler(start_handler)
    application.add_handler(link_handler)
    application.run_polling(timeout= 600, write_timeout= 600)