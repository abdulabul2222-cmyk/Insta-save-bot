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
    match = re.search(r'(https?://(?:www\.)?instagram\.com/(?:reel|p|share)/[a-zA-Z0-9_-]+)', raw_text)
    if not match:
        bot.reply_to(message, "⚠️ Kripya valid Instagram Reel URL bhejein.")
        return

    clean_url = match.group(1)
    wait_msg = bot.reply_to(message, "⏳ Reel download ho rahi hai, thoda intezar karein...")

    # Method: Cobalt public instance (Most stable Instagram parser)
    try:
        cobalt_payload = {
            "url": clean_url,
            "videoQuality": "720"
        }
        cobalt_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        res = requests.post("https://cobalt-backend.canine.tools/", json=cobalt_payload, headers=cobalt_headers, timeout=20).json()
        
        video_url = res.get("url")
        if video_url:
            bot.send_video(message.chat.id, video_url, caption="✅ Lo bhai, ho gayi download!")
            return
    except Exception:
        pass

    # Fallback Direct Mirror
    try:
        mirror_url = f"https://api.tiklydown.eu.org/api/download?url={clean_url}"
        res2 = requests.get(mirror_url, timeout=15).json()
        video_url2 = res2.get("videoUrl") or res2.get("url")
        if video_url2:
            bot.send_video(message.chat.id, video_url2, caption="✅ Lo bhai, ho gayi download!")
            return
    except Exception:
        pass

    bot.reply_to(message, "❌ Video download nahi ho payi. Ek baar koi doosri reel ka link bhej kar check karein.")

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    bot.infinity_polling()
    
