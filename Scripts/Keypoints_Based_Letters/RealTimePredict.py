import cv2
import mediapipe as mp
import numpy as np
import joblib

from preprocess_keypoints import preprocess_keypoints

# Load trained model
clf = joblib.load('random_forest_model.pkl')

# Load label classes
with open('label_classes.txt', 'r') as f:
    label_classes = [line.strip() for line in f]

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

# Open webcam
cap = cv2.VideoCapture(0)
print("🎥 Starting real-time prediction... Press 'q' to quit.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Flip and convert to RGB
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process frame
    result = hands.process(rgb)
    
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Extract keypoints
            keypoints = []
            for lm in hand_landmarks.landmark:
                keypoints.append([lm.x, lm.y, lm.z])
            
            # Preprocess keypoints
            processed = preprocess_keypoints([keypoints])[0].reshape(1, -1)
            
            # Predict
            pred_idx = clf.predict(processed)[0]
            
            if pred_idx < len(label_classes):
                pred_label = label_classes[pred_idx]
            else:
                pred_label = "Unknown"
            
            # Draw prediction with larger font and black color
            cv2.putText(frame, f'Prediction: {pred_label}', (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 4)  # Bigger text, black color, thicker
            
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
    cv2.imshow('Real-time Sign Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
