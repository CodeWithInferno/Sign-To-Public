import os
import shutil

# Original and destination directories
src_base = '/Users/pratham/Programming/Hackathon/data/asl_dataset'
dst_base = '/Users/pratham/Programming/Hackathon/data/asl_dataset_renamed'

# Loop through label folders
for label_folder in os.listdir(src_base):
    src_folder = os.path.join(src_base, label_folder)
    if os.path.isdir(src_folder):
        label = label_folder.upper()  # Use 'R' instead of 'r'
        
        # Create destination folder
        dst_folder = os.path.join(dst_base, label)
        os.makedirs(dst_folder, exist_ok=True)
        
        count = 1  # Start counter for renaming
        
        # Loop through images
        for filename in os.listdir(src_folder):
            if filename.lower().endswith(('.jpeg', '.jpg', '.png')):
                src_file = os.path.join(src_folder, filename)
                
                # New filename: e.g., R_1.jpeg, R_2.jpeg
                new_filename = f"{label}_{count}.jpeg"
                dst_file = os.path.join(dst_folder, new_filename)
                
                # Copy file with new name
                shutil.copy2(src_file, dst_file)
                print(f"Copied {src_file} to {dst_file}")
                
                count += 1

print("✅ Dataset cloned and renamed successfully!")
