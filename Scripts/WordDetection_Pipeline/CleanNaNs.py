import numpy as np

# Load corrupted data
data = np.load("sign_data_filtered.npz")
X, y = data["X"], data["y"]

# Replace NaNs with 0.0
X_cleaned = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)

print("✅ NaNs after cleaning:", np.isnan(X_cleaned).sum())

# Save cleaned data
np.savez("sign_data_cleaned.npz", X=X_cleaned, y=y)
print("✅ Saved cleaned data to sign_data_cleaned.npz")
