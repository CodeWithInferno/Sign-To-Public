import os
import numpy as np
import tensorflow as tf
import cv2
from collections import defaultdict
import matplotlib.pyplot as plt
from tqdm import tqdm

# === Parameters ===
SEQUENCE_LENGTH = 16
IMG_SIZE = (224, 224)
DATA_SPLITS = ['val', 'test']
BASE_PATH = '/Users/pratham/Programming/Hackathon/data/preprocessing'
MODEL_PATH = '/Users/pratham/Programming/Hackathon/Scripts/RNN/sign_model_final.h5'

# === Load model ===
model = tf.keras.models.load_model(MODEL_PATH)

# === Class map ===
SELECTED_CLASSES = sorted([
    "bed", "before", "blue", "book", "can", "candy", "chair", "clothes", "computer", "cousin",
    "deaf", "drink", "go", "hearing", "man", "many", "no", "study", "walk", "who"
])
inv_class_map = {i: cls for i, cls in enumerate(SELECTED_CLASSES)}

# === Tracking ===
correct_counts = defaultdict(int)
total_counts = defaultdict(int)
confidences = []

def preprocess_video_folder(folder):
    frames = sorted(os.listdir(folder))[:SEQUENCE_LENGTH]
    video = []
    for fname in frames:
        path = os.path.join(folder, fname)
        img = cv2.imread(path)
        if img is None:
            continue
        img = cv2.resize(img, IMG_SIZE)
        img = img / 255.0
        video.append(img)
    if len(video) == SEQUENCE_LENGTH:
        return np.expand_dims(np.array(video), axis=0)
    return None

# === Run blind prediction ===
for split in DATA_SPLITS:
    split_path = os.path.join(BASE_PATH, split, 'frames')
    for cls in tqdm(os.listdir(split_path), desc=f"Processing {split}"):
        cls_path = os.path.join(split_path, cls)
        for vid_folder in os.listdir(cls_path):
            vid_path = os.path.join(cls_path, vid_folder)
            video = preprocess_video_folder(vid_path)
            if video is None:
                continue
            pred = model.predict(video, verbose=0)[0]
            pred_idx = np.argmax(pred)
            pred_label = inv_class_map[pred_idx]
            confidence = pred[pred_idx]
            confidences.append(confidence)
            total_counts[cls] += 1
            if pred_label == cls:
                correct_counts[cls] += 1

# === Compute accuracy per class ===
accuracy_per_class = {cls: correct_counts[cls] / total_counts[cls] if total_counts[cls] else 0
                      for cls in SELECTED_CLASSES}

# === Plot accuracy bar chart ===
plt.figure(figsize=(12, 6))
plt.bar(accuracy_per_class.keys(), accuracy_per_class.values(), color='skyblue')
plt.xticks(rotation=45)
plt.ylabel('Accuracy')
plt.title('Per-Class Accuracy on val/test')
plt.tight_layout()
plt.savefig("per_class_accuracy_bar_chart.png")

# === Plot confidence histogram ===
plt.figure(figsize=(8, 5))
plt.hist(confidences, bins=20, color='orange', edgecolor='black')
plt.xlabel('Confidence')
plt.ylabel('Frequency')
plt.title('Confidence Distribution Across Predictions')
plt.tight_layout()
plt.savefig("confidence_distribution.png")

print("\n✅ Evaluation Complete. Saved:")
print("- per_class_accuracy_bar_chart.png")
print("- confidence_distribution.png")
