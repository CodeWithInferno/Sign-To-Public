import cv2
import torch
import torch.nn.functional as F
from torchvision import transforms
from model import ASLCNN
from PIL import Image
import numpy as np

model_path = "/Users/pratham/Programming/Hackathon/models/asl_cnn.pth"
classes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'del', 'nothing', 'space']
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = ASLCNN(num_classes=len(classes)).to(device)
model.load_state_dict(torch.load(model_path, map_location=device))
model.eval()

# Enhanced preprocessing with data normalization
transform = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),  # Add some robustness to lighting changes
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])  # Proper RGB normalization
])

def preprocess_frame(frame):
    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Convert to PIL Image
    img_pil = Image.fromarray(rgb_frame)
    # Apply transformations
    img_tensor = transform(img_pil).unsqueeze(0).to(device)
    return img_tensor, rgb_frame

def get_prediction(img_tensor):
    with torch.no_grad():
        output = model(img_tensor)
        probs = F.softmax(output, dim=1)
        pred = torch.argmax(probs, 1).item()
        confidence = probs[0, pred].item()
    return pred, confidence

def draw_text(frame, text, position=(10, 30), color=(0, 255, 0)):
    cv2.putText(frame, text, position, cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

cap = cv2.VideoCapture(0)
print("Press 'q' to quit, 'p' to pause/unpause")

paused = False
while True:
    ret, frame = cap.read()
    if not ret:
        continue
        
    # Flip frame horizontally for mirror effect
    frame = cv2.flip(frame, 1)
    
    if not paused:
        # Preprocess the frame
        img_tensor, rgb_frame = preprocess_frame(frame)
        
        # Get prediction
        pred, confidence = get_prediction(img_tensor)
        label = classes[pred]
        
        # Display prediction based on confidence
        if confidence > 0.7:  # High confidence threshold
            text = f"{label} ({confidence*100:.1f}%)"
            color = (0, 255, 0)  # Green for high confidence
        else:
            text = "Uncertain"
            color = (0, 165, 255)  # Orange for low confidence
        
        draw_text(frame, text, color=color)
    
    # Show preprocessed frame (what the model sees)
    preprocessed_display = cv2.resize(rgb_frame, (320, 240))
    cv2.imshow("Preprocessed View", preprocessed_display)
    
    # Show main frame
    cv2.imshow("ASL Live Detection", frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('p'):
        paused = not paused

cap.release()
cv2.destroyAllWindows()
