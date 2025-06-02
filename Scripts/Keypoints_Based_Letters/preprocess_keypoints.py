import numpy as np

def preprocess_keypoints(keypoints_batch):
    processed_batch = []
    for keypoints in keypoints_batch:
        keypoints = np.array(keypoints)
        mean_point = np.mean(keypoints, axis=0)
        centralized = keypoints - mean_point
        max_abs = np.max(np.abs(centralized))
        if max_abs != 0:
            normalized = centralized / max_abs
        else:
            normalized = centralized
        flattened = normalized.flatten()
        processed_batch.append(flattened)
    return processed_batch
