import json, os, requests, time, subprocess

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
MODEL = "eleven_multilingual_v3"

with open("tmp/segments.json", "r", encoding="utf-8") as f:
    segments = json.load(f)

os.makedirs("tmp/dialogue", exist_ok=True)

headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": ELEVENLABS_API_KEY
}

for i, seg in enumerate(segments):
    out_path = f"tmp/dialogue/seg_{i:04d}.mp3"
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
        print(f"  {i+1}/{len(segments)} موجود مسبقاً: {seg['character']}")
        continue

    print(f"  {i+1}/{len(segments)} جاري توليد: {seg['character']} - {seg['text'][:40]}...")

    payload = {
        "text": seg["text"],
        "model_id": MODEL,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.3,
            "use_speaker_boost": True
        }
    }

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{seg['voice_id']}"

    for attempt in range(5):
        try:
            r = requests.post(url, json=payload, headers=headers, timeout=120)
            if r.status_code == 200:
                with open(out_path, "wb") as f:
                    f.write(r.content)
                break
            elif r.status_code == 429:
                print(f"    معدل محدود، انتظار {attempt*5} ثانية...")
                time.sleep((attempt + 1) * 5)
            else:
                print(f"    خطأ {r.status_code}: {r.text[:100]}")
                time.sleep(3)
        except Exception as e:
            print(f"    استثناء: {e}")
            time.sleep(5)

print("تم توليد جميع المقاطع الصوتية")
