# model.py

import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, TimeDistributed, LSTM, Dense, GlobalAveragePooling2D, Dropout

def build_model(input_shape=(16, 224, 224, 3), num_classes=100):
    """
    input_shape: (sequence_length, height, width, channels)
    num_classes: number of output classes (signs)
    """
    sequence_len = input_shape[0]

    # Input Layer
    inputs = Input(shape=input_shape)

    # Base CNN: MobileNetV2 (lightweight, good for real-time)
    base_cnn = MobileNetV2(include_top=False, weights='imagenet', pooling=None)
    for layer in base_cnn.layers:
        layer.trainable = False  # freeze base CNN

    # Wrap in TimeDistributed
    x = TimeDistributed(base_cnn)(inputs)
    x = TimeDistributed(GlobalAveragePooling2D())(x)  # shape: (batch, seq, features)

    # LSTM layer
    x = LSTM(256, return_sequences=False)(x)
    x = Dropout(0.5)(x)

    # Final Classifier
    outputs = Dense(num_classes, activation='softmax')(x)

    # Model
    model = Model(inputs, outputs)
    return model
