import cv2
import os
import shutil

def is_blurry(image_path, threshold=100.0):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        return True  # Treat unreadable images as blurry
    variance = cv2.Laplacian(image, cv2.CV_64F).var()
    return variance < threshold

def process_recordings(recordings_folder, blurry_folder, threshold=100.0):
    os.makedirs(blurry_folder, exist_ok=True)
    for filename in os.listdir(recordings_folder):
        file_path = os.path.join(recordings_folder, filename)
        if is_blurry(file_path, threshold):
            print(f"Blurry: {filename}")
            shutil.move(file_path, os.path.join(blurry_folder, filename))
        else:
            print(f"Sharp: {filename}")
            # Run YOLO detection here or queue for further processing

def is_blurry(image, threshold=100.0):
    """Detect if an image is blurry using Laplacian variance.
    
    Args:
        image: OpenCV image in BGR format or path to an image file
        threshold: Variance threshold below which an image is considered blurry
        
    Returns:
        bool: True if the image is blurry, False otherwise
    
    Raises:
        ValueError: If the image is None or invalid
        Exception: For other processing errors
    """
    try:
        # Handle case where image is a file path
        if isinstance(image, str):
            img = cv2.imread(image, cv2.IMREAD_COLOR)
            if img is None:
                raise ValueError(f"Could not read image from path: {image}")
            image = img
            
        # Check if image is valid
        if image is None or image.size == 0:
            raise ValueError("Invalid image: Image is None or empty")
            
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Calculate Laplacian variance
        variance = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # Return blur status
        return variance < threshold
        
    except Exception as e:
        print(f"Error in blur detection: {type(e).__name__} - {str(e)}")
        raise

