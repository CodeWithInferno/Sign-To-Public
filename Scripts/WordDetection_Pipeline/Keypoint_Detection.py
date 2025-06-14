import cv2
import mediapipe as mp
import os
import pandas as pd
import numpy as np

# ====================
# ✅ Setup
# ====================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# ====================
# ✅ Target Glosses
# ====================
TARGET_LABELS = ["book", "cheat", "play", "eat", "drink", "school", "computer", "name", "hello", "sleep"]

# ====================
# ✅ Load and Filter CSV
# ====================
csv_path = "wlasl_filtered.csv"
df = pd.read_csv(csv_path)

# Only rows where gloss is in selected labels
df = df[df['gloss'].isin(TARGET_LABELS)]

# ====================
# ✅ Output Directory
# ====================
output_dir = "keypoints_csv"
os.makedirs(output_dir, exist_ok=True)

# ====================
# ✅ Keypoint Extraction
# ====================
def extract_hand_keypoints(landmarks):
    return [coord for lm in landmarks.landmark for coord in (lm.x, lm.y, lm.z)]

# ====================
# ✅ Process Videos
# ====================
for idx, row in df.iterrows():
    video_path = row['video_path']
    label = row['gloss']
    video_id = row['video_id']
    output_csv = os.path.join(output_dir, f"{video_id}.csv")

    if os.path.exists(output_csv):
        print(f"✅ Already processed: {video_id}")
        continue

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"❌ Failed to open: {video_path}")
        continue

    rows = []
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret or frame_count >= 60:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        # Start with NaNs
        left_hand = [np.nan] * 63
        right_hand = [np.nan] * 63

        if result.multi_hand_landmarks and result.multi_handedness:
            for landmarks, handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
                keypoints = extract_hand_keypoints(landmarks)
                hand_type = handedness.classification[0].label  # "Left" or "Right"
                if hand_type == "Left":
                    left_hand = keypoints
                elif hand_type == "Right":
                    right_hand = keypoints
                mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

        row_data = [video_id, label, frame_count] + left_hand + right_hand
        rows.append(row_data)

        # Preview
        frame_resized = cv2.resize(frame, (640, 480))
        cv2.imshow("Preview", frame_resized)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()

    if rows:
        columns = (
            ['video_id', 'label', 'frame'] +
            [f'lh_kp_{i}' for i in range(63)] +
            [f'rh_kp_{i}' for i in range(63)]
        )
        pd.DataFrame(rows, columns=columns).to_csv(output_csv, index=False)
        print(f"✅ Saved: {output_csv}")
    else:
        print(f"⚠️ No hands found in: {video_id}")
