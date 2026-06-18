import os, subprocess, json, math

os.makedirs("tmp/frames", exist_ok=True)

audio_duration = float(subprocess.check_output(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration",
     "-of", "default=noprint_wrappers=1:nokey=1", "tmp/mixed/final_mix.wav"]
).decode().strip())

if not os.path.exists("tmp/segments.json"):
    segments = []
else:
    with open("tmp/segments.json", "r", encoding="utf-8") as f:
        segments = json.load(f)

w, h = 3840, 2160
fps = 24
total_frames = int(audio_duration * fps)

print(f"توليد فيديو: {audio_duration:.1f} ثانية × {fps} إطار/ثانية = {total_frames} إطار")

scene_timestamps = []
scene_files = []

# توليد صور للمشاهد
scenes = [
    {"start": 0, "end": 30, "color": "darkgreen", "label": "وصف القرية"},
    {"start": 30, "end": 60, "color": "darkred", "label": "الهجوم الليلي"},
    {"start": 60, "end": 90, "color": "crimson", "label": "المعركة في الأزقة"},
    {"start": 90, "end": 130, "color": "darkgoldenrod", "label": "خطاب عساف"},
    {"start": 130, "end": 170, "color": "saddlebrown", "label": "الحصار والمؤامرة"},
    {"start": 170, "end": 220, "color": "midnightblue", "label": "راشد وليلى في الصحراء"},
    {"start": 220, "end": 260, "color": "goldenrod", "label": "عاصفة رملية"},
    {"start": 260, "end": 310, "color": "darkolivegreen", "label": "مجلس شيوخ القبائل"},
    {"start": 310, "end": 360, "color": "darkred", "label": "اقتحام القرية"},
    {"start": 360, "end": 420, "color": "darkorange", "label": "معركة الفجر"},
    {"start": 420, "end": 470, "color": "darkred", "label": "المبارزة النهائية"},
    {"start": 470, "end": 530, "color": "gold", "label": "سقوط الطاغية"},
    {"start": 530, "end": 570, "color": "darkgreen", "label": "النصر"},
    {"start": 570, "end": audio_duration, "color": "forestgreen", "label": "الخاتمة"}
]

for i, sc in enumerate(scenes):
    out = f"tmp/frames/scene_{i:03d}.png"
    color = sc["color"]
    label = sc["label"]

    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"color=c={color}:s={w}x{h}:d=1",
        "-vf", f"drawtext=text='{label}':fontsize=80:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:enable='between(t,0,1)'",
        "-frames:v", "1",
        out
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    scene_files.append(out)
    print(f"  مشهد {i+1}/{len(scenes)}: {label} ({sc['start']}-{sc['end']}ث)")

# إنشاء concat file للفيديو مع Ken Burns effect
concat_file = "tmp/concat.txt"
with open(concat_file, "w") as f:
    f.write("ffconcat version 1.0\n")

for i, sc in enumerate(scenes):
    dur = min(sc["end"], audio_duration) - sc["start"]
    if dur <= 0:
        continue
    # استخدام نفس الصورة مع zoom
    for chunk_start in range(0, int(dur), 5):
        chunk_dur = min(5, dur - chunk_start)
        if chunk_dur < 0.5:
            continue
        zoom = 1.0 + (chunk_start / dur) * 0.3
        img = scene_files[i]
        out_chunk = f"tmp/frames/chunk_{i}_{chunk_start}.mp4"
        if not os.path.exists(out_chunk):
            subprocess.run([
                "ffmpeg", "-y",
                "-loop", "1",
                "-i", img,
                "-vf", f"scale={w}:{h},zoompan=z={zoom}:d={int(chunk_dur*fps)}:s={w}x{h}",
                "-t", str(chunk_dur),
                "-c:v", "libx264",
                "-preset", "ultrafast",
                "-pix_fmt", "yuv420p",
                "-r", str(fps),
                out_chunk
            ], check=True, capture_output=True)
        with open(concat_file, "a") as f:
            f.write(f"file '{os.path.abspath(out_chunk)}'\n")

print("دمج المقاطع...")
final_video = "output/final_video.mp4"
subprocess.run([
    "ffmpeg", "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", concat_file,
    "-i", "tmp/mixed/final_mix.wav",
    "-c:v", "libx264",
    "-preset", "medium",
    "-crf", "18",
    "-profile:v", "high",
    "-pix_fmt", "yuv420p",
    "-r", str(fps),
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    "-movflags", "+faststart",
    final_video
], check=True)

size_mb = os.path.getsize(final_video) / 1024 / 1024
print(f"تم إنشاء الفيديو: {final_video} ({size_mb:.1f} MB)")
