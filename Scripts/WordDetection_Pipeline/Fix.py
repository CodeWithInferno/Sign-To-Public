import numpy as np
import pandas as pd
from collections import Counter

# Load original .npz
data = np.load('sign_data_final.npz', allow_pickle=True)
X, y = data['X'], data['y']

# Count class frequencies
counts = Counter(y)
print("Original class counts:", counts)

# Filter out classes with less than 2 samples
valid_classes = [label for label, count in counts.items() if count >= 2]
mask = np.isin(y, valid_classes)

X_filtered = X[mask]
y_filtered = y[mask]

# Re-index class labels
unique_labels = np.unique(y_filtered)
label_map = {old: new for new, old in enumerate(unique_labels)}
y_filtered = np.array([label_map[label] for label in y_filtered])

# Save
np.savez('sign_data_filtered.npz', X=X_filtered, y=y_filtered)
print("✅ Saved cleaned dataset to sign_data_filtered.npz")

# Print new class distribution
new_counts = Counter(y_filtered)
df = pd.DataFrame.from_dict(new_counts, orient='index', columns=['Samples'])
print("\nFiltered Class Distribution:")
print(df.sort_index())
