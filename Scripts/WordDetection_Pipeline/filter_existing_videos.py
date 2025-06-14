import pandas as pd
import os

# Path to CSV and video folder
csv_path = 'wlasl_master_index.csv'
videos_folder = '/Users/pratham/Programming/Hackathon/data/videos'
output_csv = 'wlasl_filtered.csv'

# Load index CSV
df = pd.read_csv(csv_path)

# Append video path
def get_path(vid):
    path = os.path.join(videos_folder, f"{vid}.mp4")
    return path if os.path.exists(path) else None

df['video_path'] = df['video_id'].apply(get_path)

# Drop rows where video file is missing
df = df.dropna(subset=['video_path'])

# Save
df.to_csv(output_csv, index=False)
print(f"✅ Filtered index saved to {output_csv} with {len(df)} valid videos")
