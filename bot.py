import os
import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# টোকেনটি আমরা সার্ভার থেকে নেবো
BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    contact_button = KeyboardButton(text="Click Here to Share Your Contact", request_contact=True)
    keyboard = [[contact_button]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    
    welcome_note = "স্বাগতম! আপনার কন্টাক্ট শেয়ার করতে নিচের বাটনে ক্লিক করুন।"
    await update.message.reply_text(welcome_note, reply_markup=reply_markup)

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    contact = update.message.contact
    phone_number = contact.phone_number
    first_name = contact.first_name
    
    logger.info(f"Contact received from {first_name}. Phone: {phone_number}")
    await update.message.reply_text(
        f"ধন্যবাদ! আপনার নম্বর ({phone_number}) পেয়েছি।",
        reply_markup=ReplyKeyboardRemove()
    )

def main() -> None:
    if not BOT_TOKEN:
        logger.error("Error: BOT_TOKEN is not set!")
        return

    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    
    logger.info("Bot is starting...")
    application.run_polling()

if __name__ == "__main__":
    main()
