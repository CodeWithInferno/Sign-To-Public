from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import base64
import numpy as np
import cv2
import time
import json
from blur_detection import is_blurry
from blur_detection import process_recordings

app = Flask(__name__)
CORS(app)

# Create directories for storing recordings if they don't exist
RECORDINGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'recordings')
os.makedirs(RECORDINGS_DIR, exist_ok=True)

# Dictionary to store active recording sessions
active_recordings = {}

@app.route('/start-recording', methods=['POST'])
def start_recording():
    """Start a new recording session"""
    session_id = str(int(time.time()))
    session_dir = os.path.join(RECORDINGS_DIR, session_id)
    os.makedirs(session_dir, exist_ok=True)
    
    active_recordings[session_id] = {
        'frame_count': 0,
        'directory': session_dir,
        'start_time': time.time(),
        'metadata': request.json.get('metadata', {})
    }
    
    return jsonify({
        'success': True,
        'session_id': session_id,
        'message': 'Recording session started'
    })

@app.route('/process-frame', methods=['POST'])
def process_frame():
    """Process and save a frame from the frontend"""
    if 'frame' not in request.json:
        return jsonify({'error': 'No frame data provided'}), 400
    
    session_id = request.json.get('session_id')
    frame_data = request.json['frame']
    
    # If no session_id provided or session doesn't exist, create a new one
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
    
    # Get the session info
    session = active_recordings[session_id]
    frame_count = session['frame_count']
    
    try:
        # Decode base64 image
        img_bytes = base64.b64decode(frame_data.split(',')[1])
        nparr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Save the frame as an image
        frame_filename = os.path.join(session['directory'], f'frame_{frame_count:06d}.jpg')
        cv2.imwrite(frame_filename, frame)
        
        # Update frame count
        session['frame_count'] += 1
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'frame_number': frame_count,
            'message': 'Frame processed successfully'
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'Failed to process frame'
        }), 500

@app.route('/stop-recording', methods=['POST'])
def stop_recording():
    """Stop an active recording session"""
    session_id = request.json.get('session_id')
    
    if not session_id or session_id not in active_recordings:
        return jsonify({'error': 'Invalid session ID'}), 400
    
    session = active_recordings[session_id]
    duration = time.time() - session['start_time']
    
    # Save metadata
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
    
    # Remove from active recordings
    del active_recordings[session_id]
    
    return jsonify({
        'success': True,
        'session_id': session_id,
        'frame_count': metadata['frame_count'],
        'duration_seconds': duration,
        'message': 'Recording stopped successfully'
    })

@app.route('/recordings', methods=['GET'])
def list_recordings():
    """List all available recordings"""
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
                # For recordings without metadata (possibly interrupted)
                frame_count = len([f for f in os.listdir(item_path) if f.endswith('.jpg')])
                recordings.append({
                    'session_id': item,
                    'frame_count': frame_count,
                    'incomplete': True
                })
    
    return jsonify({
        'recordings': recordings
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
    

@app.route('/process-frame', methods=['POST'])
def process_frame():
    """Process and save a frame from the frontend"""
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
    
    session = active_recordings[session_id]
    frame_count = session['frame_count']
    
    try:
        # Decode base64 image
        img_bytes = base64.b64decode(frame_data.split(',')[1])
        nparr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Check for blurriness
        is_blur = is_blurry(frame, threshold=100.0)
        if is_blur:
            blurry_dir = os.path.join(session['directory'], 'blurry')
            os.makedirs(blurry_dir, exist_ok=True)
            blurry_filename = os.path.join(blurry_dir, f'frame_{frame_count:06d}.jpg')
            cv2.imwrite(blurry_filename, frame)
            print(f"Saved blurry frame: {blurry_filename}")
        else:
            frame_filename = os.path.join(session['directory'], f'frame_{frame_count:06d}.jpg')
            cv2.imwrite(frame_filename, frame)
            print(f"Saved sharp frame: {frame_filename}")
        
        session['frame_count'] += 1
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'frame_number': frame_count,
            'blurry': is_blur,
            'message': 'Frame processed successfully'
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'Failed to process frame'
        }), 500
