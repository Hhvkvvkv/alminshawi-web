import subprocess, os

INPUT = "tmp/asset3.mp3"
OUTPUT = "tmp/sfx_clean.mp3"

if not os.path.exists(INPUT):
    print("الملف غير موجود")
    exit(1)

duration = float(subprocess.check_output(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration",
     "-of", "default=noprint_wrappers=1:nokey=1", INPUT]
).decode().strip())
print(f"مدة الملف: {duration:.1f} ثانية")

cmd = [
    "ffmpeg", "-y", "-i", INPUT,
    "-af",
    "highpass=f=80," +
    "lowpass=f=8000," +
    "afftdn=nf=-25," +
    "deesser," +
    "volume=2.0",
    "-ac", "2",
    "-ar", "48000",
    "-b:a", "256k",
    OUTPUT
]
subprocess.run(cmd, check=True)
print(f"تم التنظيف: {OUTPUT}")
