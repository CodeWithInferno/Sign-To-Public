import os
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, Dataset
from PIL import Image

class FlatImageDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.images = [f for f in os.listdir(root_dir) if f.endswith('.jpg') or f.endswith('.png')]
        self.class_names = sorted(set([img[0].upper() for img in self.images]))
        self.class_to_idx = {cls_name: idx for idx, cls_name in enumerate(self.class_names)}
        
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        img_name = self.images[idx]
        img_path = os.path.join(self.root_dir, img_name)
        image = Image.open(img_path).convert("RGB")
        label = self.class_to_idx[img_name[0].upper()]
        if self.transform:
            image = self.transform(image)
        return image, label

def get_data_loaders(train_dir, test_dir, batch_size=32, image_size=(64, 64)):
    transform = transforms.Compose([
        transforms.Resize(image_size),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5], std=[0.5])
    ])
    train_dataset = datasets.ImageFolder(root=train_dir, transform=transform)
    test_dataset = FlatImageDataset(root_dir=test_dir, transform=transform)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    return train_loader, test_loader, train_dataset.classes
