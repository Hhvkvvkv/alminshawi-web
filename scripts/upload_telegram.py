import os, requests, mimetypes

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

if not BOT_TOKEN or not CHAT_ID:
    print("❌ مفاتيح Telegram غير موجودة")
    exit(1)

def send_file(file_path, method, caption=""):
    if not os.path.exists(file_path):
        print(f"❌ الملف غير موجود: {file_path}")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"
    size_mb = os.path.getsize(file_path) / 1024 / 1024
    print(f"رفع {file_path} ({size_mb:.1f} MB) إلى Telegram...")

    with open(file_path, "rb") as f:
        files = {method.replace("send", "").lower(): f}
        data = {"chat_id": CHAT_ID, "caption": caption}
        r = requests.post(url, data=data, files=files, timeout=600)
        if r.status_code == 200:
            print(f"✅ تم رفع {file_path}")
        else:
            print(f"❌ فشل: {r.status_code} - {r.text[:200]}")

# إرسال الفيديو
caption_video = (
    "القرآن الكريم - القارئ الشيخ محمد صديق المنشاوي\n"
    "إنتاج سينمائي: ملحمة النخيلة\n"
    "رابط التحميل: https://github.com/Hhvkvvkv/alminshawi-web/releases"
)
send_file("output/final_video.mp4", "sendVideo", caption_video)

# إرسال الصوت
send_file("output/final_audio.mp3", "sendAudio")

print("تم إرسال جميع الملفات إلى Telegram")
