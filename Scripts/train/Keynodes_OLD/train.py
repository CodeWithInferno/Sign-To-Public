import torch
from torch_geometric.loader import DataLoader
from model import ASLGNN
from dataset import KeyPointDataset
import yaml
import os
import random

# Load config
with open("config.yaml") as f:
    config = yaml.safe_load(f)

# Prepare datasets with train/val split
full_dataset = KeyPointDataset(config['dataset']['train_dir'])
dataset_size = len(full_dataset)
val_size = int(0.2 * dataset_size)
train_size = dataset_size - val_size
train_dataset, val_dataset = torch.utils.data.random_split(full_dataset, [train_size, val_size], generator=torch.Generator().manual_seed(42))
test_dataset = KeyPointDataset(config['dataset']['test_dir'])

train_loader = DataLoader(train_dataset, batch_size=config['dataset']['batch_size'], shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=config['dataset']['batch_size'], shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=config['dataset']['batch_size'], shuffle=False)

# Setup model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = ASLGNN(in_features=3, hidden_dim=config['model']['hidden_dim'], num_classes=config['model']['num_classes']).to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=config['training']['lr'], weight_decay=1e-4)
criterion = torch.nn.CrossEntropyLoss()
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=20, gamma=0.5)  # Reduce LR by half every 20 epochs

# Early stopping setup
best_val_acc = 0.0
patience = 10
patience_counter = 0

for epoch in range(1, config['training']['epochs'] + 1):
    model.train()
    total_loss, correct, total = 0, 0, 0
    for batch in train_loader:
        batch = batch.to(device)
        batch.x = (batch.x - batch.x.mean(dim=0)) / (batch.x.std(dim=0) + 1e-6)  # Normalize keypoints
        optimizer.zero_grad()
        out = model(batch)
        loss = criterion(out, batch.y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
        pred = out.argmax(dim=1)
        correct += (pred == batch.y).sum().item()
        total += batch.y.size(0)
    train_acc = 100 * correct / total
    scheduler.step()

    # Validation
    model.eval()
    val_correct, val_total = 0, 0
    val_loss = 0
    with torch.no_grad():
        for batch in val_loader:
            batch = batch.to(device)
            batch.x = (batch.x - batch.x.mean(dim=0)) / (batch.x.std(dim=0) + 1e-6)
            out = model(batch)
            val_loss += criterion(out, batch.y).item()
            pred = out.argmax(dim=1)
            val_correct += (pred == batch.y).sum().item()
            val_total += batch.y.size(0)
    val_acc = 100 * val_correct / val_total
    print(f"Epoch {epoch}, Loss: {total_loss/len(train_loader):.4f}, Acc: {train_acc:.2f}%, Val Acc: {val_acc:.2f}%")

    # Early stopping and checkpointing
    if val_acc > best_val_acc:
        best_val_acc = val_acc
        patience_counter = 0
        torch.save(model.state_dict(), config['training']['checkpoint_path'])
        print(f"🔥 Best model saved at epoch {epoch} with val acc {val_acc:.2f}%")
    else:
        patience_counter += 1
        if patience_counter >= patience:
            print("⏹️ Early stopping triggered.")
            break

# Load best model for test evaluation
model.load_state_dict(torch.load(config['training']['checkpoint_path']))
model.eval()
test_correct, test_total = 0, 0
with torch.no_grad():
    for batch in test_loader:
        batch = batch.to(device)
        batch.x = (batch.x - batch.x.mean(dim=0)) / (batch.x.std(dim=0) + 1e-6)
        out = model(batch)
        pred = out.argmax(dim=1)
        test_correct += (pred == batch.y).sum().item()
        test_total += batch.y.size(0)
print(f"✅ Final Test Accuracy: {100 * test_correct / test_total:.2f}%")
