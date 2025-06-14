import numpy as np
from sklearn.preprocessing import LabelBinarizer

# Load your dataset
data = np.load("sign_data_cleaned.npz")
y = data["y"]

# Fit label encoder
encoder = LabelBinarizer()
encoder.fit(y)

# Save encoded class labels
np.save("labels.npy", encoder.classes_)
print("✅ Saved labels.npy:", encoder.classes_)
