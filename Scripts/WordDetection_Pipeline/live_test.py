import cv2
import numpy as np
import tensorflow as tf
import mediapipe as mp
from tensorflow.keras.models import load_model

# === Custom Attention Layer ===
class AttentionLayer(tf.keras.layers.Layer):
    def __init__(self, **kwargs):
        super(AttentionLayer, self).__init__(**kwargs)
        self.dense = tf.keras.layers.Dense(1)

    def call(self, inputs):
        score = self.dense(inputs)
        attention_weights = tf.nn.softmax(score, axis=1)
        context_vector = attention_weights * inputs
        context_vector = tf.reduce_sum(context_vector, axis=1)
        return context_vector

# === Load trained model ===
model = load_model("sign_model_attn.keras", custom_objects={"AttentionLayer": AttentionLayer})

# === MediaPipe Hands Setup ===
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)
HAND_CONNECTIONS = mp_hands.HAND_CONNECTIONS

# === Your actual target labels
TARGET_LABELS = ["book", "cheat", "play", "eat", "drink", "school", "computer", "name", "hello", "sleep"]

# === Live video capture
cap = cv2.VideoCapture(0)
sequence = []

# Hold last prediction
last_prediction = ""
last_confidence = 0.0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    keypoints = []

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, HAND_CONNECTIONS)
            for lm in hand_landmarks.landmark:
                keypoints.extend([lm.x, lm.y, lm.z])

        keypoints = keypoints[:126] + [0] * (126 - len(keypoints))
        sequence.append(keypoints)

        if len(sequence) == 60:
            input_data = np.expand_dims(np.array(sequence), axis=0)
            prediction = model.predict(input_data)[0]

            class_index = np.argmax(prediction)
            predicted_label = TARGET_LABELS[class_index]
            confidence = np.max(prediction) * 100

            last_prediction = predicted_label
            last_confidence = confidence

            # 🔥 Log to terminal
            print(f"[Prediction #{class_index}] {predicted_label} — {confidence:.2f}%")

            sequence = []

    # Display on frame
    display_text = f"{last_prediction} ({last_confidence:.1f}%)"
    cv2.putText(frame, display_text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Live Sign Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
