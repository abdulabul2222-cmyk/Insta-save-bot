import telebot
import os
import re
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import yt_dlp

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

    file_name = f"reel_{message.chat.id}.mp4"
    ydl_opts = {
        'format': 'best',
        'outtmpl': file_name,
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([clean_url])

        if os.path.exists(file_name):
            with open(file_name, 'rb') as video:
                bot.send_video(message.chat.id, video, caption="✅ Lo bhai, ho gayi download!")
            os.remove(file_name)
        else:
            bot.reply_to(message, "❌ Video download nahi ho payi.")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)[:100]}")
        if os.path.exists(file_name):
            os.remove(file_name)

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    bot.infinity_polling()
        
