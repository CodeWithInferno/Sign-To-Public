import os
import json
import yt_dlp
import subprocess
from tqdm import tqdm
from time import sleep
from collections import defaultdict

# === Config ===
json_paths = {
    "train": "/Users/pratham/Programming/Hackathon/data/MSASL_train.json",
    "val": "/Users/pratham/Programming/Hackathon/data/MSASL_val.json",
    "test": "/Users/pratham/Programming/Hackathon/data/MSASL_test.json"
}
output_root = "/Users/pratham/Programming/Hackathon/data/MSASL_ALL"
failed_log = "failed_downloads.txt"

# === Helper: Download full video and trim ===
def download_and_trim(youtube_url, start_time, end_time, out_path):
    temp_path = out_path.replace(".mp4", "_raw.mp4")
    ydl_opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
        "quiet": True,
        "outtmpl": temp_path,
        "retries": 5,
        "noplaylist": True,
        "merge_output_format": "mp4",
        "user_agent": "Mozilla/5.0"
    }
    for attempt in range(3):
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])
            # Trim with ffmpeg
            cmd = [
                "ffmpeg", "-y", "-i", temp_path,
                "-ss", str(start_time), "-to", str(end_time),
                "-c:v", "libx264", "-an", out_path
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            os.remove(temp_path)
            return os.path.exists(out_path)
        except Exception as e:
            sleep(1)
            if attempt == 2:
                return f"{youtube_url} ❌ {str(e)}"
    return f"{youtube_url} ❌ Retry failed"

# === Collect all samples by label ===
label_samples = defaultdict(list)
for split, path in json_paths.items():
    with open(path, "r") as f:
        data = json.load(f)
    for entry in data:
        label = entry["clean_text"].lower()
        label_samples[label].append((split, entry))

# === Download all videos, class by class ===
with open(failed_log, "w") as flog:
    for label in tqdm(sorted(label_samples), desc="Words"):
        samples = label_samples[label]
        count = 0
        for split, entry in samples:
            url = entry["url"]
            start = entry["start_time"]
            end = entry["end_time"]
            name = entry["file"].replace("/", "_").replace(" ", "_").replace("(", "").replace(")", "")
            folder = os.path.join(output_root, label)
            os.makedirs(folder, exist_ok=True)
            out_path = os.path.join(folder, f"{name}.mp4")
            if os.path.exists(out_path):
                count += 1
                continue
            result = download_and_trim(url, start, end, out_path)
            if result is True:
                count += 1
            else:
                flog.write(f"{split}/{label} - {result}\n")
        print(f"{label}: Downloaded {count} videos.")

print("✅ All words processed. Check logs for failed downloads.")
