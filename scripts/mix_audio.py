import json, os, subprocess, tempfile

with open("tmp/segments.json", "r", encoding="utf-8") as f:
    segments = json.load(f)

sfx_file = "tmp/sfx_clean.mp3"
asset2_file = "tmp/asset2.mp3"
os.makedirs("tmp/mixed", exist_ok=True)

sfx_duration = float(subprocess.check_output(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration",
     "-of", "default=noprint_wrappers=1:nokey=1", sfx_file]
).decode().strip())

dialogue_segments = []
current_time = 2.0
for i, seg in enumerate(segments):
    mp3 = f"tmp/dialogue/seg_{i:04d}.mp3"
    if not os.path.exists(mp3):
        continue
    seg_dur = float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", mp3]
    ).decode().strip())

    pause = 1.5 if seg["character"] == "الرَّاوِي" else 0.8
    if "عَاصِفَة" in seg["text"] or "الْتَحَمَت" in seg["text"] or "انْهَارَت" in seg["text"]:
        pause = 3.0

    dialogue_segments.append({
        "start": current_time,
        "file": mp3,
        "duration": seg_dur,
        "character": seg["character"],
        "text": seg["text"]
    })
    current_time += seg_dur + pause

total_dialogue_dur = current_time
target_duration = max(total_dialogue_dur, sfx_duration)
total_duration = max(target_duration * 1.3, 600)
print(f"المدة الإجمالية المستهدفة: {total_duration:.1f} ثانية ({total_duration/60:.1f} دقيقة)")

# تكرار المؤثرات إذا كانت أقصر
if sfx_duration < total_duration:
    loops = int(total_duration / sfx_duration) + 1
    loop_file = "tmp/mixed/sfx_looped.mp3"
    subprocess.run([
        "ffmpeg", "-y",
        "-stream_loop", str(loops),
        "-i", sfx_file,
        "-t", str(total_duration),
        "-ac", "2",
        "-ar", "48000",
        loop_file
    ], check=True, capture_output=True)
    sfx_file = loop_file

# بناء filter_complex للـ mixing
filters = []
inputs = []
input_idx = 0

# SFX background track
inputs.extend(["-i", sfx_file])
sfx_idx = 0

# Audio ducking: حجم الخلفية ينخفض 20% أثناء الكلام
for ds in dialogue_segments:
    inputs.extend(["-i", ds["file"]])
    idx = input_idx + 1
    start = ds["start"]
    end = start + ds["duration"]

    filters.append(
        f"[{sfx_idx}:a] volume=1.0, "
        f"volume=enable='between(t,{start},{end})':volume=0.65 "
        f"[sfx_ducked_{input_idx}]"
    )

    filters.append(
        f"[{idx}:a]adelay={int(start*1000)}|{int(start*1000)}[delay_{input_idx}]"
    )

    input_idx += 1

# جمع كل المسارات
mix_parts = []
for i in range(input_idx):
    mix_parts.append(f"[sfx_ducked_{i}]")
    mix_parts.append(f"[delay_{i}]")

mix_input = "".join(mix_parts)
filters.append(f"{mix_input} amix=inputs={input_idx+1}:duration=first [audio]")

filter_complex = "; ".join(filters)

# تنفيذ الخلط
subprocess.run([
    "ffmpeg", "-y",
    *inputs,
    "-filter_complex", filter_complex,
    "-map", "[audio]",
    "-ac", "2",
    "-ar", "48000",
    "-b:a", "320k",
    "tmp/mixed/final_mix.wav"
], check=True)

print("تم خلط الصوت النهائي")

# تحويل إلى MP3 عالي الجودة
subprocess.run([
    "ffmpeg", "-y",
    "-i", "tmp/mixed/final_mix.wav",
    "-codec:a", "libmp3lame",
    "-b:a", "320k",
    "output/final_audio.mp3"
], check=True)
print("تم تصدير الملف الصوتي النهائي: output/final_audio.mp3")
