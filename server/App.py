from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import base64
import numpy as np
import cv2
import time
import json
from collections import deque
from tensorflow.keras.models import load_model
from blur_detection import is_blurry

app = Flask(__name__)
CORS(app)

# Constants
RECORDINGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'recordings')
SEQUENCE_LENGTH = 60

# State
os.makedirs(RECORDINGS_DIR, exist_ok=True)
active_recordings = {}
keypoint_buffers = {}
# model = load_model('asl_lstm_attention_model.h5')
import random

class FakeModel:
    def predict(self, x):
        # Simulate a class prediction from your label set (e.g., 0–9 or ['hello', 'thanks', ...])
        mock_classes = ['hello', 'thanks', 'yes', 'no', 'iloveyou']
        return [[random.random() for _ in mock_classes]]

model = FakeModel()


# MediaPipe setup
import mediapipe as mp
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)

def extract_keypoints(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = hands.process(image_rgb)
    left = [0]*63
    right = [0]*63

    if result.multi_hand_landmarks and result.multi_handedness:
        for i, hand in enumerate(result.multi_hand_landmarks):
            handedness = result.multi_handedness[i].classification[0].label
            keypoints = [lm.x for lm in hand.landmark] + \
                        [lm.y for lm in hand.landmark] + \
                        [lm.z for lm in hand.landmark]
            if handedness == "Left":
                left = keypoints
            else:
                right = keypoints
    return left, right

@app.route('/start-recording', methods=['POST'])
def start_recording():
    session_id = str(int(time.time()))
    session_dir = os.path.join(RECORDINGS_DIR, session_id)
    os.makedirs(session_dir, exist_ok=True)
    active_recordings[session_id] = {
        'frame_count': 0,
        'directory': session_dir,
        'start_time': time.time(),
        'metadata': request.json.get('metadata', {})
    }
    keypoint_buffers[session_id] = {'left': deque(maxlen=SEQUENCE_LENGTH), 'right': deque(maxlen=SEQUENCE_LENGTH)}
    return jsonify({'success': True, 'session_id': session_id, 'message': 'Recording session started'})

@app.route('/process-frame', methods=['POST'])
def process_frame():
    if 'frame' not in request.json:
        return jsonify({'error': 'No frame data provided'}), 400

    session_id = request.json.get('session_id')
    frame_data = request.json['frame']
    if not session_id or session_id not in active_recordings:
        session_id = str(int(time.time()))
        session_dir = os.path.join(RECORDINGS_DIR, session_id)
        os.makedirs(session_dir, exist_ok=True)
        active_recordings[session_id] = {
            'frame_count': 0,
            'directory': session_dir,
            'start_time': time.time(),
            'metadata': request.json.get('metadata', {})
        }
        keypoint_buffers[session_id] = {'left': deque(maxlen=SEQUENCE_LENGTH), 'right': deque(maxlen=SEQUENCE_LENGTH)}

    session = active_recordings[session_id]
    frame_count = session['frame_count']
    try:
        img_bytes = base64.b64decode(frame_data.split(',')[1])
        nparr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        is_blur = is_blurry(frame, threshold=100.0)

        save_dir = os.path.join(session['directory'], 'blurry' if is_blur else '')
        os.makedirs(save_dir, exist_ok=True)
        frame_filename = os.path.join(save_dir, f'frame_{frame_count:06d}.jpg')
        cv2.imwrite(frame_filename, frame)

        # Extract keypoints
        left, right = extract_keypoints(frame)
        keypoint_buffers[session_id]['left'].append(left)
        keypoint_buffers[session_id]['right'].append(right)

        prediction = None
        confidence = None
        if len(keypoint_buffers[session_id]['left']) == SEQUENCE_LENGTH:
            left_seq = np.array(keypoint_buffers[session_id]['left'])[None, :, :]
            right_seq = np.array(keypoint_buffers[session_id]['right'])[None, :, :]
            pred = model.predict([left_seq, right_seq])[0]
            prediction = int(np.argmax(pred))
            confidence = float(np.max(pred))

        session['frame_count'] += 1
        return jsonify({
            'success': True,
            'session_id': session_id,
            'frame_number': frame_count,
            'blurry': is_blur,
            'prediction': prediction,
            'confidence': confidence,
            'message': 'Frame processed successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to process frame'}), 500

@app.route('/stop-recording', methods=['POST'])
def stop_recording():
    session_id = request.json.get('session_id')
    if not session_id or session_id not in active_recordings:
        return jsonify({'error': 'Invalid session ID'}), 400

    session = active_recordings[session_id]
    duration = time.time() - session['start_time']
    metadata = {
        'session_id': session_id,
        'frame_count': session['frame_count'],
        'duration_seconds': duration,
        'start_time': session['start_time'],
        'end_time': time.time(),
        'user_metadata': session['metadata']
    }
    with open(os.path.join(session['directory'], 'metadata.json'), 'w') as f:
        json.dump(metadata, f, indent=2)

    del active_recordings[session_id]
    del keypoint_buffers[session_id]

    return jsonify({
        'success': True,
        'session_id': session_id,
        'frame_count': metadata['frame_count'],
        'duration_seconds': duration,
        'message': 'Recording stopped successfully'
    })

@app.route('/recordings', methods=['GET'])
def list_recordings():
    recordings = []
    for item in os.listdir(RECORDINGS_DIR):
        item_path = os.path.join(RECORDINGS_DIR, item)
        if os.path.isdir(item_path):
            metadata_path = os.path.join(item_path, 'metadata.json')
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                recordings.append(metadata)
            else:
                frame_count = len([f for f in os.listdir(item_path) if f.endswith('.jpg')])
                recordings.append({
                    'session_id': item,
                    'frame_count': frame_count,
                    'incomplete': True
                })
    return jsonify({'recordings': recordings})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
