import tensorflow as tf
import numpy as np
import cv2
import os

# === Load model ===
model = tf.keras.models.load_model("sign_model_final.h5")

# === Preprocessing function ===
def preprocess_video(frames_folder, frame_count=16, img_size=(224, 224)):
    frames = sorted(os.listdir(frames_folder))[:frame_count]
    video = []
    for fname in frames:
        img = cv2.imread(os.path.join(frames_folder, fname))
        img = cv2.resize(img, img_size)
        img = img / 255.0
        video.append(img)
    video = np.array(video)
    return np.expand_dims(video, axis=0)  # shape: (1, 16, 224, 224, 3)

# === Class map loader ===
def get_class_map_from_directory(directory):
    classes = sorted(os.listdir(directory))
    return {cls_name: idx for idx, cls_name in enumerate(classes)}

# === Reverse class lookup ===
SELECTED_CLASSES = {
    "book", "drink", "computer", "go", "chair",
    "clothes", "who", "before", "candy", "deaf",
    "cousin", "man", "hearing", "can", "study",
    "walk", "bed", "many", "blue", "no"
}
class_map = {cls_name: idx for idx, cls_name in enumerate(sorted(SELECTED_CLASSES))}
inv_class_map = {v: k for k, v in class_map.items()}

# === Run inference ===
video = preprocess_video("/Users/pratham/Programming/Hackathon/data/preprocessing/test/frames/no/38525")
pred = model.predict(video)[0]  # shape: (num_classes,)
top_5_indices = np.argsort(pred)[-5:][::-1]

print("\n🔍 Top 5 Predictions:")
for i, idx in enumerate(top_5_indices):
    label = inv_class_map.get(idx, "Unknown")
    confidence = pred[idx]
    print(f"{i+1}. {label} (Confidence: {confidence:.4f})")
