import os
import csv
import mediapipe as mp
import cv2

# 🔧 SETTINGS
data_dir = '/Users/pratham/Programming/Hackathon/data/asl_dataset_renamed'
output_csv = 'asl_keypoints_labels.csv'
show_keypoints = True  # Set to False to skip visualization

# Setup MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5)

# Initialize drawing utils
mp_drawing = mp.solutions.drawing_utils

# Open CSV file
with open(output_csv, 'w', newline='') as f:
    writer = csv.writer(f)
    header = [f'kp_{i}' for i in range(21*3)] + ['label']
    writer.writerow(header)

    # Loop through folders
    for label_folder in os.listdir(data_dir):
        folder_path = os.path.join(data_dir, label_folder)
        if os.path.isdir(folder_path):
            label = label_folder.upper()
            
            for filename in os.listdir(folder_path):
                if filename.lower().endswith(('.jpeg', '.jpg', '.png')):
                    file_path = os.path.join(folder_path, filename)
                    image = cv2.imread(file_path)
                    if image is None:
                        print(f"❌ Could not read {file_path}")
                        continue

                    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    results = hands.process(image_rgb)

                    if results.multi_hand_landmarks:
                        hand_landmarks = results.multi_hand_landmarks[0]
                        keypoints = []
                        for lm in hand_landmarks.landmark:
                            keypoints.extend([lm.x, lm.y, lm.z])  # Normalized coords
                        
                        writer.writerow(keypoints + [label])
                        print(f"✅ Saved keypoints for {file_path}")

                        # Optional Visualization
                        if show_keypoints:
                            annotated_image = image.copy()
                            mp_drawing.draw_landmarks(annotated_image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                            cv2.imshow('Keypoints Visualization', annotated_image)
                            cv2.waitKey(500)  # Show for 500ms
                            cv2.destroyAllWindows()

                    else:
                        print(f"⚠️ No hand detected in {file_path}")

hands.close()
print(f"✅ Finished processing. Keypoints saved to {output_csv}")
