import json
import csv
import os

# Path to WLASL JSON
wlasl_json_path = '/Users/pratham/Programming/Hackathon/data/WLASL_v0.3.json'
output_csv = 'wlasl_master_index.csv'

# Load WLASL data
with open(wlasl_json_path, 'r') as f:
    data = json.load(f)

# Write to CSV
with open(output_csv, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['video_id', 'gloss', 'split', 'url', 'bbox', 'fps', 'frame_start', 'frame_end', 'source'])

    for entry in data:
        gloss = entry['gloss']
        for inst in entry['instances']:
            writer.writerow([
                inst['video_id'],
                gloss,
                inst.get('split', 'unknown'),
                inst.get('url', 'unknown'),
                inst.get('bbox', ''),
                inst.get('fps', ''),
                inst.get('frame_start', ''),
                inst.get('frame_end', ''),
                inst.get('source', '')
            ])

print(f"✅ WLASL master index created: {output_csv}")
