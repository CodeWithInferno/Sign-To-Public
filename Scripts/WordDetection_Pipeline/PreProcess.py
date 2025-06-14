import os
import pandas as pd
import numpy as np
from tqdm import tqdm

KEYPOINTS_DIR = "/Users/pratham/Programming/Hackathon/Scripts/WordDetection_Pipeline/keypoints_csv"
MAX_FRAMES = 60
OUTPUT_NPY = "processed_keypoints.npz"

# Step 1: Collect all CSVs
all_files = [f for f in os.listdir(KEYPOINTS_DIR) if f.endswith(".csv")]

X_data = []
y_labels = []

for file in tqdm(all_files, desc="Merging keypoint CSVs"):
    path = os.path.join(KEYPOINTS_DIR, file)
    df = pd.read_csv(path)

    # Drop frames where all keypoints are NaN
    kp_cols = df.columns[3:]  # Skip video_id, label, frame
    df = df.dropna(subset=kp_cols, how="all")

    if df.empty:
        continue

    # Keep only video_id, label, keypoints (drop frame)
    video_id = df['video_id'].iloc[0]
    label = df['label'].iloc[0]
    df = df.drop(columns=['frame'])

    # Pad/truncate to MAX_FRAMES
    if len(df) < MAX_FRAMES:
        pad_len = MAX_FRAMES - len(df)
        pad_df = pd.DataFrame(np.nan, index=range(pad_len), columns=df.columns)
        pad_df[['video_id', 'label']] = [video_id, label]
        df = pd.concat([df, pad_df], ignore_index=True)
    elif len(df) > MAX_FRAMES:
        df = df.iloc[:MAX_FRAMES]

    # Final: get only keypoints array
    kp_array = df.iloc[:, 2:].to_numpy()  # drop video_id and label
    X_data.append(kp_array)
    y_labels.append(label)

X = np.array(X_data)  # shape: (n_videos, 60, 126)
labels = np.array(y_labels)

# Save intermediate (before label encoding)
np.savez("raw_keypoints_unencoded.npz", X=X, labels=labels)
print("✅ Saved raw_keypoints_unencoded.npz")
