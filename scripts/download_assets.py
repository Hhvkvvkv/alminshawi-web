import os, requests

os.makedirs("tmp", exist_ok=True)
os.makedirs("output", exist_ok=True)

ASSETS = {
    "asset1.mp3": os.environ.get("ASSET1", "https://clck.ru/3U8ST9"),
    "asset2.mp3": os.environ.get("ASSET2", "https://clck.ru/3UF2Uk"),
    "asset3.mp3": os.environ.get("ASSET3", "https://clck.ru/3UF2Xv")
}

for name, url in ASSETS.items():
    path = f"tmp/{name}"
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        print(f"{name} موجود مسبقاً")
        continue
    print(f"جاري تحميل {name}...")
    r = requests.get(url, stream=True, timeout=300)
    r.raise_for_status()
    with open(path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"  تم: {os.path.getsize(path)} bytes")
