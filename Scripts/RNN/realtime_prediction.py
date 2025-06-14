import tensorflow as tf
import numpy as np
import cv2
from collections import deque

# === Load model ===
model = tf.keras.models.load_model("sign_model_final.h5")

# === Class map ===
SELECTED_CLASSES = sorted([
    "bed", "before", "blue", "book", "can", "candy", "chair", "clothes", "computer", "cousin",
    "deaf", "drink", "go", "hearing", "man", "many", "no", "study", "walk", "who"
])
inv_class_map = {i: cls for i, cls in enumerate(SELECTED_CLASSES)}

# === Parameters ===
SEQUENCE_LENGTH = 16
IMG_SIZE = (224, 224)
frame_buffer = deque(maxlen=SEQUENCE_LENGTH)
video_path = "/Users/pratham/Programming/Hackathon/Bed_fixed.mp4"

# === Softmax sharpening function ===
def sharpen(pred, temperature=0.3):
    logits = np.log(pred + 1e-8)  # avoid log(0)
    scaled = logits / temperature
    exp_preds = np.exp(scaled - np.max(scaled))  # for numerical stability
    return exp_preds / np.sum(exp_preds)

# === Open video file ===
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("❌ Cannot open video file")
    exit()

# === Collect exactly SEQUENCE_LENGTH frames ===
print("🎞️ Collecting frames...")
while len(frame_buffer) < SEQUENCE_LENGTH:
    ret, frame = cap.read()
    if not ret:
        print("❌ Not enough frames in the video")
        exit()
    resized = cv2.resize(frame, IMG_SIZE)
    normalized = resized / 255.0
    frame_buffer.append(normalized)

cap.release()

# === Run prediction ===
video = np.array(frame_buffer)
video = np.expand_dims(video, axis=0)
raw_pred = model.predict(video, verbose=0)[0]
pred = sharpen(raw_pred, temperature=0.3)  # Sharpen prediction confidence

# === Get top 2 predictions ===
top_indices = np.argsort(pred)[-2:][::-1]
print("\n🔍 Top 2 Predictions:")
for rank, idx in enumerate(top_indices, 1):
    print(f"{rank}. {inv_class_map[idx]} (Confidence: {pred[idx]:.4f})")
