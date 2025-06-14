# train.py

import os
import tensorflow as tf
from dataset import SignDataset, get_class_map
from model import build_model
from datetime import datetime

# === Paths ===
train_root = "/Users/pratham/Programming/Hackathon/data/preprocessing/train/frames"
val_root = "/Users/pratham/Programming/Hackathon/data/preprocessing/val/frames"
test_root = "/Users/pratham/Programming/Hackathon/data/preprocessing/test/frames"

# === Class Mapping ===
class_map = get_class_map(train_root)
num_classes = len(class_map)
print(f"🧠 Total classes: {num_classes}")

# === Load Datasets ===
sequence_len = 16
batch_size = 8

train_dataset = SignDataset(train_root, class_map, sequence_len=sequence_len, batch_size=batch_size)
val_dataset = SignDataset(val_root, class_map, sequence_len=sequence_len, batch_size=batch_size)
test_dataset = SignDataset(test_root, class_map, sequence_len=sequence_len, batch_size=batch_size, shuffle=False)

# === Build Model ===
model = build_model(input_shape=(sequence_len, 224, 224, 3), num_classes=num_classes)
model.summary()

# === Compile ===
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# === TensorBoard Logging ===
log_dir = os.path.join("logs", datetime.now().strftime("%Y%m%d-%H%M%S"))
tensorboard_cb = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

# === Callbacks ===
callbacks = [
    tf.keras.callbacks.ModelCheckpoint(
        filepath="sign_model_best.h5",
        monitor="val_accuracy",
        save_best_only=True,
        verbose=1
    ),
    tf.keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.5,
        patience=2,
        verbose=1
    ),
    tf.keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True
    ),
    tensorboard_cb
]

# === Train ===
epochs = 10

model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=epochs,
    callbacks=callbacks
)

# === Evaluate ===
test_loss, test_acc = model.evaluate(test_dataset)
print(f"\n✅ Test Accuracy: {test_acc:.2%}")
