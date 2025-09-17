from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp
import os

# ✏️ ضع توكن البوت هنا
TOKEN = "7999965874:AAE_A19r9cnuKAbDcYBKybEPZS-7MICTaXQ"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل لي رابط يوتيوب لأستخرج لك الصوت 🎵")

async def download_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "youtube.com" not in url and "youtu.be" not in url:
        await update.message.reply_text("الرجاء إرسال رابط يوتيوب صحيح.")
        return

    await update.message.reply_text("جارٍ التحميل... ⏳")

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(title)s.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")

        with open(filename, 'rb') as audio_file:
            await update.message.reply_audio(audio=audio_file, caption="هذا صوتك 🎧")

        os.remove(filename)  # حذف الملف بعد الإرسال

    except Exception as e:
        await update.message.reply_text(f"حدث خطأ: {str(e)}")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_audio))

    print("🚀 البوت يعمل...")
    app.run_polling()

if __name__ == '__main__':
    main()