from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import yt_dlp
import os

# ⚠️ لا تضع التوكن هنا — استخدم Environment Variable في Render
TOKEN = os.getenv("7999965874:AAE_A19r9cnuKAbDcYBKybEPZS-7MICTaXQ")

if not TOKEN:
    raise ValueError("No TOKEN provided. Set it in Render Environment Variables.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 أهلاً! أرسل لي رابط فيديو من يوتيوب لأستخرج لك الصوت كملف MP3 🎵"
    )

async def download_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if "youtube.com" not in url and "youtu.be" not in url:
        await update.message.reply_text("❌ من فضلك أرسل رابط يوتيوب صحيح.")
        return

    # تحقق من وجود ملف الكوكيز
    if not os.path.exists('cookies.txt'):
        await update.message.reply_text("❌ خطأ داخلي: ملف الكوكيز غير موجود على الخادم!")
        return

    await update.message.reply_text("⏳ جارٍ التحميل... قد يستغرق 10-30 ثانية.")

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(title)s.%(ext)s',
        'cookiefile': 'cookies.txt',  # 👈 ملف الكوكيز
        'quiet': True,
        'no_warnings': False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # التأكد من اسم الملف النهائي
            filename = ydl.prepare_filename(info).rsplit('.', 1)[0] + ".mp3"

        if not os.path.exists(filename):
            await update.message.reply_text("❌ فشل في إنشاء الملف الصوتي. جرب رابطاً آخر.")
            return

        with open(filename, 'rb') as audio_file:
            await update.message.reply_audio(
                audio=audio_file,
                caption="🎧 تم التحميل بنجاح! استمتع بالأغنية ❤️"
            )

        # حذف الملف بعد الإرسال
        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ أثناء التحميل:\n{str(e)}")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_audio))

    print("🚀 البوت يعمل...")
    app.run_polling()

if __name__ == '__main__':
    main()