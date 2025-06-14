import json
import os
from collections import defaultdict

# Path to JSON and video folder
json_path = "/Users/pratham/Programming/Hackathon/data/WLASL_v0.3.json"
video_folder = "/Users/pratham/Programming/Hackathon/data/videos"
output_file = "gloss_counts.txt"

# Load the JSON
with open(json_path, 'r') as f:
    data = json.load(f)

# Count available video files per gloss
gloss_counts = defaultdict(int)

for entry in data:
    gloss = entry["gloss"]
    for instance in entry["instances"]:
        video_id = instance["video_id"]
        video_filename = f"{video_id}.mp4"
        if os.path.exists(os.path.join(video_folder, video_filename)):
            gloss_counts[gloss] += 1

# Sort results
sorted_counts = sorted(gloss_counts.items(), key=lambda x: -x[1])

# Write to file
with open(output_file, 'w') as f:
    f.write(f"{'Gloss':<20} | {'Available Videos'}\n")
    f.write("-" * 40 + "\n")
    for gloss, count in sorted_counts:
        f.write(f"{gloss:<20} | {count}\n")

print(f"✅ Saved gloss counts to {output_file}")
