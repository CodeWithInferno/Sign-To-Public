import json
import csv
import os

# Paths to files (update if needed)
json_path = '/Users/pratham/Programming/Hackathon/data/nslt_100.json'
class_list_path = '/Users/pratham/Programming/Hackathon/data/WLASL_v0.3.json'
videos_folder = '/Users/pratham/Programming/Hackathon/data/videos'

# Load class ID to word mapping from WLASL_v0.3.json
with open(class_list_path, 'r') as f:
    class_data = json.load(f)
class_id_to_label = {entry['id']: entry['gloss'] for entry in class_data}

# Load video info from nslt_100.json
with open(json_path, 'r') as f:
    video_data = json.load(f)

# Prepare CSV output
index_file = 'wlasl_index.csv'
with open(index_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['video_id', 'video_path', 'class_id', 'label', 'subset'])

    for video_id, info in video_data.items():
        subset = info['subset']
        action_info = info['action']
        class_id = action_info[0]
        label = class_id_to_label.get(class_id, 'UNKNOWN')
        video_filename = f"{video_id}.mp4"
        video_path = os.path.join(videos_folder, video_filename)

        writer.writerow([video_id, video_path, class_id, label, subset])

print(f"✅ Index file created: {index_file}")
