import os
import glob
import torch
from torch_geometric.data import Dataset, Data

class KeyPointDataset(Dataset):
    def __init__(self, root_dir):
        super(KeyPointDataset, self).__init__()
        self.root_dir = root_dir
        self.samples = self._load_samples()

        # Mediapipe hand connections (edge list)
        self.edge_index = torch.tensor([
            [0,1],[1,2],[2,3],[3,4],
            [0,5],[5,6],[6,7],[7,8],
            [0,9],[9,10],[10,11],[11,12],
            [0,13],[13,14],[14,15],[15,16],
            [0,17],[17,18],[18,19],[19,20],
            [5,9],[9,13],[13,17],[17,5]
        ], dtype=torch.long).t().contiguous()

        # Class mapping
        self.classes = sorted(os.listdir(root_dir))
        self.class_to_idx = {cls_name: idx for idx, cls_name in enumerate(self.classes)}

    def _load_samples(self):
        samples = []
        for class_name in os.listdir(self.root_dir):
            class_dir = os.path.join(self.root_dir, class_name)
            if not os.path.isdir(class_dir):
                continue
            for pt_file in glob.glob(os.path.join(class_dir, "*.pt")):
                samples.append((pt_file, class_name))
        return samples

    def len(self):
        return len(self.samples)

    def get(self, idx):
        pt_file, class_name = self.samples[idx]
        x = torch.load(pt_file)
        y = torch.tensor(self.class_to_idx[class_name], dtype=torch.long)
        data = Data(x=x, edge_index=self.edge_index, y=y)
        return data
