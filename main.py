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
    raw_text = message.text.strip()
    
    # URL me se faltu tracking parameters (?stkn=... etc) saaf karna
    match = re.search(r'(https?://(?:www\.)?instagram\.com/(?:reel|p|share)/[a-zA-Z0-9_-]+)', raw_text)
    if not match:
        bot.reply_to(message, "⚠️ Kripya valid Instagram Reel URL bhejein.")
        return

    clean_url = match.group(1)
    wait_msg = bot.reply_to(message, "⏳ Reel download ho rahi hai, kripya intezar karein...")

    # Method 1: Primary API
    try:
        api_url = f"https://api.siputzx.my.id/api/d/igdl?url={clean_url}"
        res = requests.get(api_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15).json()
        if res.get("status") and res.get("data"):
            video_url = res["data"][0].get("url")
            bot.send_video(message.chat.id, video_url, caption="✅ Downloaded successfully!")
            return
    except Exception:
        pass

    # Method 2: Backup fast engine
    try:
        backup_url = f"https://widipe.com/download/ig?url={clean_url}"
        res2 = requests.get(backup_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15).json()
        if res2.get("status") and res2.get("result"):
            results = res2["result"]
            video_url = results[0]["url"] if isinstance(results, list) else results.get("url")
            if video_url:
                bot.send_video(message.chat.id, video_url, caption="✅ Downloaded successfully!")
                return
    except Exception:
        pass

    bot.reply_to(message, "❌ Video download nahi ho payi. Ek baar doosri reel ka link try karein.")

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    bot.infinity_polling()
            
