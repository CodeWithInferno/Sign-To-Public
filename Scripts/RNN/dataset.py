# dataset.py

import os
import numpy as np
import cv2
import tensorflow as tf

class SignDataset(tf.keras.utils.Sequence):
    def __init__(self, root_dir, class_map, sequence_len=16, batch_size=8, shuffle=True):
        self.root_dir = root_dir
        self.class_map = class_map
        self.sequence_len = sequence_len
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.video_paths = self._gather_video_paths()
        self.on_epoch_end()

    def _gather_video_paths(self):
        video_dirs = []
        for class_name in os.listdir(self.root_dir):
            class_path = os.path.join(self.root_dir, class_name)
            if not os.path.isdir(class_path):
                continue
            for video_id in os.listdir(class_path):
                video_dir = os.path.join(class_path, video_id)
                if os.path.isdir(video_dir):
                    video_dirs.append((video_dir, self.class_map[class_name]))
        return video_dirs

    def __len__(self):
        return len(self.video_paths) // self.batch_size

    def __getitem__(self, idx):
        batch_paths = self.video_paths[idx * self.batch_size:(idx + 1) * self.batch_size]
        batch_x, batch_y = [], []
        for video_dir, label in batch_paths:
            frames = self._load_frames(video_dir)
            batch_x.append(frames)
            batch_y.append(label)
        return np.array(batch_x), np.array(batch_y)

    def on_epoch_end(self):
        if self.shuffle:
            np.random.shuffle(self.video_paths)

    def _load_frames(self, video_dir):
        frame_files = sorted(os.listdir(video_dir))
        total = len(frame_files)

        if total >= self.sequence_len:
            indices = np.linspace(0, total - 1, self.sequence_len).astype(int)
        else:
            indices = np.concatenate([np.arange(total)] + [np.full((self.sequence_len - total,), total - 1)])

        frames = []
        for idx in indices:
            img_path = os.path.join(video_dir, frame_files[idx])
            img = cv2.imread(img_path)
            img = cv2.resize(img, (224, 224))
            img = img.astype(np.float32) / 255.0
            frames.append(img)
        return np.array(frames)

def get_class_map(data_root):
    """Utility to generate class name → index mapping based on training set"""
    class_names = sorted(os.listdir(data_root))
    class_map = {name: idx for idx, name in enumerate(class_names) if os.path.isdir(os.path.join(data_root, name))}
    return class_map
