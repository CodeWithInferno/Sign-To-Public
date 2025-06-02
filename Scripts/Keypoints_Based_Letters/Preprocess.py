import numpy as np
import csv

def preprocess_keypoints(keypoints_batch):
    processed_batch = []
    for keypoints in keypoints_batch:
        keypoints = np.array(keypoints)
        mean_point = np.mean(keypoints, axis=0)
        centralized = keypoints - mean_point
        max_abs = np.max(np.abs(centralized))
        normalized = centralized / max_abs if max_abs != 0 else centralized
        flattened = normalized.flatten()
        processed_batch.append(flattened)
    return processed_batch

input_csv = 'asl_keypoints_labels.csv'
output_csv = 'asl_keypoints_labels_processed.csv'

keypoints_batch = []
labels = []

# Read CSV file
with open(input_csv, newline='') as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader)  # Skip header
    for row in reader:
        label = row[-1]
        keypoints = [float(val) for val in row[:-1]]
        # Reshape into (num_points, dims) -- adjust dims (2 or 3)
        keypoints = np.array(keypoints).reshape(-1, 3)
        keypoints_batch.append(keypoints)
        labels.append(label)

# Process keypoints
processed_batch = preprocess_keypoints(keypoints_batch)

# Write to new CSV
with open(output_csv, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    header = [f'proc_kp_{i}' for i in range(len(processed_batch[0]))] + ['label']
    writer.writerow(header)
    for proc_kp, label in zip(processed_batch, labels):
        writer.writerow(proc_kp.tolist() + [label])

print(f"✅ Processed data saved to {output_csv}")
