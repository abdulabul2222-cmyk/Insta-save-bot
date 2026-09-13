import telebot
import requests
import re
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import os

BOT_TOKEN = "8713209453:AAEyFtGhTI54i9COQbIKlPoBVYD4lJLfYmA"
bot = telebot.TeleBot(BOT_TOKEN)

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

@bot.message_handler(commands=['start'])
def start_msg(message):
    bot.reply_to(message, "👋 Welcome! Mujhe Instagram Reel ka link bhejo, main video download kar dunga.")

@bot.message_handler(func=lambda message: True)
def download_reel(message):
    url = message.text.strip()
    if "instagram.com" not in url:
        bot.reply_to(message, "⚠️ Kripya valid Instagram URL bhejein.")
        return

    wait_msg = bot.reply_to(message, "⏳ Reel download ho rahi hai, kripya intezar karein...")
    try:
        api_url = f"https://api.vkrdownloader.xyz/v1/dl?url={url}"
        res = requests.get(api_url).json()
        if res.get("status") and res.get("data", {}).get("downloads"):
            video_url = res["data"]["downloads"][0]["url"]
            bot.send_video(message.chat.id, video_url, caption="✅ Here is your reel!")
        else:
            bot.reply_to(message, "❌ Video download nahi ho payi. Reel private ho sakti hai ya link expired hai.")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    bot.infinity_polling()
                     
