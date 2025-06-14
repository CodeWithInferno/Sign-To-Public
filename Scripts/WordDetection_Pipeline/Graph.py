import numpy as np
import matplotlib.pyplot as plt
import os

# Load the dataset
data = np.load('sign_data_final.npz')
X = data['X']  # Shape: (num_samples, 60, 126)
y = data['y']

# Class distribution
unique, counts = np.unique(y, return_counts=True)

# Plot class distribution
plt.figure(figsize=(10, 5))
plt.bar(unique, counts, color='skyblue')
plt.title("Gloss Class Distribution in sign_data_final.npz")
plt.xlabel("Class Index")
plt.ylabel("Number of Samples")
plt.xticks(unique)
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# Plot a heatmap of keypoints for a single video
sample_idx = 0
sample = X[sample_idx]  # Shape: (60, 126)

plt.figure(figsize=(12, 6))
plt.imshow(sample.T, aspect='auto', cmap='viridis')
plt.colorbar(label='Keypoint Value')
plt.title(f"Heatmap of Keypoints for Sample Index {sample_idx} (Class {y[sample_idx]})")
plt.xlabel("Frame")
plt.ylabel("Keypoint Index")
plt.tight_layout()
plt.show()
