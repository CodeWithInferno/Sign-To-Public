import os
import glob
import torch
import mediapipe as mp
import cv2

# Paths
train_dir = "/Users/pratham/Programming/Hackathon/data/asl_alphabet_train"
test_dir = "/Users/pratham/Programming/Hackathon/data/asl_alphabet_test"
output_train_dir = "/Users/pratham/Programming/Hackathon/keypoints_data/train"
output_test_dir = "/Users/pratham/Programming/Hackathon/keypoints_data/test"

# Setup Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1)

def process_dataset(input_dir, output_dir, is_test=False):
    os.makedirs(output_dir, exist_ok=True)

    if not is_test:
        # Training dataset: /A/A1.jpg, /B/B1.jpg...
        for class_name in os.listdir(input_dir):
            class_dir = os.path.join(input_dir, class_name)
            if not os.path.isdir(class_dir):
                continue
            
            output_class_dir = os.path.join(output_dir, class_name)
            os.makedirs(output_class_dir, exist_ok=True)

            for img_path in glob.glob(os.path.join(class_dir, "*.jpg")):
                process_image(img_path, output_class_dir, os.path.basename(img_path).replace(".jpg", ".pt"))
    else:
        # Test dataset: /A_test.jpg, /B_test.jpg...
        for img_path in glob.glob(os.path.join(input_dir, "*.jpg")):
            class_name = os.path.basename(img_path).split("_")[0]
            output_class_dir = os.path.join(output_dir, class_name)
            os.makedirs(output_class_dir, exist_ok=True)
            filename = os.path.basename(img_path).replace(".jpg", ".pt")
            process_image(img_path, output_class_dir, filename)

def process_image(img_path, output_dir, filename):
    image = cv2.imread(img_path)
    if image is None:
        print(f"Failed to load {img_path}")
        return
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = hands.process(image_rgb)
    if result.multi_hand_landmarks:
        hand_landmarks = result.multi_hand_landmarks[0]
        keypoints = [[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]
        keypoints_tensor = torch.tensor(keypoints, dtype=torch.float)
    else:
        print(f"No hand detected in {img_path}, saving zero tensor")
        keypoints_tensor = torch.zeros((21, 3), dtype=torch.float)
    
    save_path = os.path.join(output_dir, filename)
    torch.save(keypoints_tensor, save_path)
    print(f"Saved keypoints for {img_path} to {save_path}")

# Run for train and test
process_dataset(train_dir, output_train_dir, is_test=False)
process_dataset(test_dir, output_test_dir, is_test=True)

print("✅ Keypoint extraction complete for both training and test datasets!")
