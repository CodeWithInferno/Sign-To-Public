import requests
import base64
import json
import time
import os

# Server URL
SERVER_URL = 'http://localhost:5001'

# Test image path - replace with an actual image path on your system
# For this test, we'll create a simple black image if no test image is available
def create_test_image(filename='test_image.jpg'):
    try:
        import numpy as np
        import cv2
        # Create a simple black image (100x100)
        img = np.zeros((100, 100, 3), np.uint8)
        # Add some text to the image
        cv2.putText(img, 'Test', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imwrite(filename, img)
        print(f"Created test image: {filename}")
        return filename
    except Exception as e:
        print(f"Error creating test image: {e}")
        return None

# Convert image to base64
def image_to_base64(image_path):
    with open(image_path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:image/jpeg;base64,{encoded_string}"

# Test start recording endpoint
def test_start_recording():
    print("\n1. Testing start recording endpoint...")
    try:
        response = requests.post(
            f"{SERVER_URL}/start-recording",
            json={
                'metadata': {
                    'test': True,
                    'timestamp': time.time(),
                    'device': 'test_device'
                }
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success! Session ID: {data.get('session_id')}")
            return data.get('session_id')
        else:
            print(f"Failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Test process frame endpoint
def test_process_frame(session_id, image_path):
    print("\n2. Testing process frame endpoint...")
    try:
        # Convert image to base64
        base64_image = image_to_base64(image_path)
        
        response = requests.post(
            f"{SERVER_URL}/process-frame",
            json={
                'session_id': session_id,
                'frame': base64_image
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success! Frame processed: {data}")
            return True
        else:
            print(f"Failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

# Test stop recording endpoint
def test_stop_recording(session_id):
    print("\n3. Testing stop recording endpoint...")
    try:
        response = requests.post(
            f"{SERVER_URL}/stop-recording",
            json={
                'session_id': session_id
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success! Recording stopped: {data}")
            return True
        else:
            print(f"Failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

# Test list recordings endpoint
def test_list_recordings():
    print("\n4. Testing list recordings endpoint...")
    try:
        response = requests.get(f"{SERVER_URL}/recordings")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success! Found {len(data.get('recordings', []))} recordings")
            return data.get('recordings', [])
        else:
            print(f"Failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []

# Run all tests
def run_tests():
    print("Starting Flask server tests...")
    
    # Create a test image
    test_image = create_test_image()
    if not test_image:
        print("Failed to create test image. Exiting.")
        return
    
    # Start a recording session
    session_id = test_start_recording()
    if not session_id:
        print("Failed to start recording session. Exiting.")
        return
    
    # Process a few frames
    for i in range(3):
        print(f"\nProcessing frame {i+1}/3...")
        if not test_process_frame(session_id, test_image):
            print(f"Failed to process frame {i+1}. Continuing...")
        time.sleep(0.5)  # Small delay between frames
    
    # Stop the recording
    test_stop_recording(session_id)
    
    # List all recordings
    recordings = test_list_recordings()
    
    print("\nTest Summary:")
    print(f"- Created test image: {test_image}")
    print(f"- Session ID: {session_id}")
    print(f"- Total recordings: {len(recordings)}")
    
    # Clean up test image
    try:
        os.remove(test_image)
        print(f"- Cleaned up test image: {test_image}")
    except Exception as e:
        print(f"- Failed to clean up test image: {e}")

if __name__ == "__main__":
    run_tests()