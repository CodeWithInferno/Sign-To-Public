import os
from collections import defaultdict

DATASET_PATH = "/Users/pratham/Programming/Hackathon/data/preprocessing/train/frames"
min_required = 12  # Change this if you want to keep only classes with more samples

class_counts = defaultdict(int)

for class_name in os.listdir(DATASET_PATH):
    class_path = os.path.join(DATASET_PATH, class_name)
    if os.path.isdir(class_path):
        video_folders = [f for f in os.listdir(class_path) if os.path.isdir(os.path.join(class_path, f))]
        count = len(video_folders)
        class_counts[class_name] = count

# Sort by count descending
sorted_counts = sorted(class_counts.items(), key=lambda x: x[1], reverse=True)

# Print all
print("\n🔢 Sample counts per class:")
for cls, count in sorted_counts:
    print(f"{cls:<20}: {count}")

# Filter and print top ones (>= min_required)
print(f"\n✅ Classes with at least {min_required} samples:")
filtered = [(cls, c) for cls, c in sorted_counts if c >= min_required]
for cls, count in filtered:
    print(f"{cls:<20}: {count}")

print(f"\nTotal classes with ≥{min_required} samples: {len(filtered)}")
