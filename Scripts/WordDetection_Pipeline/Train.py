import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Dense, Bidirectional, Masking
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer

# Load cleaned data
data = np.load("sign_data_cleaned.npz")
X = data["X"]
y = data["y"]

print("X shape:", X.shape)
print("y shape:", y.shape)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# One-hot encode labels
encoder = LabelBinarizer()
y_train_enc = encoder.fit_transform(y_train)
y_test_enc = encoder.transform(y_test)
num_classes = y_train_enc.shape[1]

# ✅ Fixed Attention Layer
class AttentionLayer(tf.keras.layers.Layer):
    def __init__(self):
        super().__init__()
        self.dense = Dense(1)

    def call(self, inputs):
        score = self.dense(inputs)                                 # (batch, 60, 1)
        attention_weights = tf.nn.softmax(score, axis=1)           # (batch, 60, 1)
        context_vector = attention_weights * inputs                # (batch, 60, 126)
        context_vector = tf.reduce_sum(context_vector, axis=1)     # (batch, 126)
        return context_vector

# Build model
inputs = Input(shape=(60, 126))
x = Masking()(inputs)
x = Bidirectional(LSTM(64, return_sequences=True))(x)
x = AttentionLayer()(x)
x = Dense(64, activation='relu')(x)
outputs = Dense(num_classes, activation='softmax')(x)

model = Model(inputs, outputs)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train model
model.fit(X_train, y_train_enc, validation_data=(X_test, y_test_enc), epochs=25, batch_size=16)

# ✅ Save in safe format
model.save("sign_model_attn.keras")
print("✅ Model saved to sign_model_attn.keras")
