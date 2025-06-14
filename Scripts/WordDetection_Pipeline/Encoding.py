import numpy as np
from sklearn.preprocessing import LabelEncoder

# Load from previous step
data = np.load("raw_keypoints_unencoded.npz", allow_pickle=True)
X = data['X']
labels = data['labels']

# Label encode
le = LabelEncoder()
y = le.fit_transform(labels)

# Save final .npz
np.savez("sign_data_final.npz", X=X, y=y)
print("✅ Saved sign_data_final.npz")
print("Classes:", le.classes_)
