import telebot
import requests

BOT_TOKEN = "8713209453:AAEyFtGhTI54i9COQbIKlPoBVYD4lJLfYmA"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_msg(message):
    bot.reply_to(message, "👋 Welcome! Mujhe kisi bhi Instagram Reel ya Video ka link bhejo, main turant download karke dunga.")

@bot.message_handler(func=lambda message: True)
def download_reel(message):
    url = message.text.strip()
    if "instagram.com" not in url:
        bot.reply_to(message, "⚠️ Kripya valid Instagram reel ya post ka link bhejein.")
        return

    wait_msg = bot.reply_to(message, "⏳ Reel download ho rahi hai, kripya thoda intezar karein...")

    try:
        api_url = f"https://api.vkrdownloader.xyz/server?vkr={url}"
        res = requests.get(api_url).json()

        video_url = None
        if "data" in res and "downloadUrl" in res["data"]:
            video_url = res["data"]["downloadUrl"]
        elif "url" in res:
            video_url = res["url"]

        if video_url:
            bot.send_video(message.chat.id, video_url, caption="✅ Yeh rahi aapki Reel!\nPowered by Fast Downloader")
            bot.delete_message(message.chat.id, wait_msg.message_id)
        else:
            bot.edit_message_text("❌ Video link fetch nahi ho paya. Post private ho sakti hai.", message.chat.id, wait_msg.message_id)
    except Exception as e:
        bot.edit_message_text("⚠️ Download fail ho gaya. Kripya baad mein try karein.", message.chat.id, wait_msg.message_id)

bot.infinity_polling()
