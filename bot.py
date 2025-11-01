 import os
import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ⚠️ আপনার বট টোকেনটি Render-এই থাকবে, এখানে নয়।
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# ⚠️ এইখানে @userinfobot থেকে পাওয়া আপনার নিজের আইডি'টি বসান
ADMIN_CHAT_ID = "123456789" # <--- আপনার আইডি এখানে বসান (string হিসেবে)


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
    user_id = contact.user_id
    username = update.message.from_user.username or "N/A" # ইউজারের @username
    
    logger.info(f"Contact received from {first_name}. Phone: {phone_number}")
    
    # ইউজারকে ধন্যবাদ মেসেজ
    await update.message.reply_text(
        f"ধন্যবাদ! আপনার নম্বর ({phone_number}) পেয়েছি।",
        reply_markup=ReplyKeyboardRemove()
    )
    
    # ⚠️ নতুন ধাপ: অ্যাডমিনকে মেসেজ পাঠানো
    admin_message = f"""
    🔔 নতুন কন্টাক্ট পাওয়া গেছে!
    
    নাম: {first_name}
    ফোন নম্বর: {phone_number}
    ইউজার আইডি: {user_id}
    ইউজারনেম: @{username}
    """
    
    if ADMIN_CHAT_ID:
        try:
            await context.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=admin_message
            )
        except Exception as e:
            logger.error(f"Error sending message to admin: {e}")

def main() -> None:
    if not BOT_TOKEN:
        logger.error("Error: BOT_TOKEN is not set!")
        return
    if not ADMIN_CHAT_ID:
        logger.error("Error: ADMIN_CHAT_ID is not set!")

    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    
    logger.info("Bot is starting (Admin Notify Version)...")
    application.run_polling()

if __name__ == "__main__":
    main()
