import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
from sklearn.preprocessing import LabelEncoder
import numpy as np

# Load preprocessed data
input_csv = 'asl_keypoints_labels_processed.csv'
df = pd.read_csv(input_csv)

# Split features and labels
X = df.drop('label', axis=1)
y = df['label']

# Encode labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Save the LabelEncoder
joblib.dump(le, 'label_encoder.pkl')
print("💾 LabelEncoder saved as label_encoder.pkl")

# Save label encoder classes
with open('label_classes.txt', 'w') as f:
    for label in le.classes_:
        f.write(f"{label}\n")
print("💾 Label classes saved to label_classes.txt")

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Train RandomForest
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Predict on test set
y_pred = clf.predict(X_test)

# Evaluate
acc_train = accuracy_score(y_train, clf.predict(X_train))
acc_test = accuracy_score(y_test, y_pred)
print(f"🎯 Training Accuracy: {acc_train * 100:.2f}%")
print(f"✅ Test Accuracy: {acc_test * 100:.2f}%")
print("🔎 Classification Report on Test Data:")
unique_labels = np.unique(y_test)
target_names = le.inverse_transform(unique_labels)
print(classification_report(y_test, y_pred, labels=unique_labels, target_names=target_names))

# Save model
joblib.dump(clf, 'random_forest_model.pkl')
print("💾 Model saved as random_forest_model.pkl")
