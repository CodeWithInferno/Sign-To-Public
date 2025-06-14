import numpy as np
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelBinarizer

# ✅ Fixed AttentionLayer with get_config for deserialization
class AttentionLayer(tf.keras.layers.Layer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dense = tf.keras.layers.Dense(1)

    def call(self, inputs):
        score = self.dense(inputs)
        attention_weights = tf.nn.softmax(score, axis=1)
        context_vector = attention_weights * inputs
        context_vector = tf.reduce_sum(context_vector, axis=1)
        return context_vector

    def get_config(self):
        config = super().get_config()
        return config

# Load dataset
data = np.load("sign_data_cleaned.npz")
X = data["X"]
y = data["y"]

# Encode labels
encoder = LabelBinarizer()
y_enc = encoder.fit_transform(y)
class_names = encoder.classes_

# Load model
model = tf.keras.models.load_model("sign_model_attn.keras", custom_objects={"AttentionLayer": AttentionLayer})

# Predict
y_pred = model.predict(X)
y_pred_labels = np.argmax(y_pred, axis=1)

# Report
print("Classification Report:")
print(classification_report(y, y_pred_labels, target_names=[str(c) for c in class_names]))

# Confusion Matrix
conf_mat = confusion_matrix(y, y_pred_labels)

plt.figure(figsize=(10, 8))
sns.heatmap(conf_mat, annot=True, fmt='d', cmap="Blues", xticklabels=class_names, yticklabels=class_names)
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Confusion Matrix")
plt.tight_layout()
plt.show()
