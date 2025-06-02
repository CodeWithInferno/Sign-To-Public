import torch
import torch.nn as nn
import torch.optim as optim
from dataset import get_data_loaders
from model import ASLCNN
import os

train_dir = "/Users/pratham/Programming/Hackathon/data/asl_alphabet_train"
test_dir = "/Users/pratham/Programming/Hackathon/data/asl_alphabet_test"
save_path = "/Users/pratham/Programming/Hackathon/models/asl_cnn.pth"

batch_size = 32
num_epochs = 10
learning_rate = 0.001
image_size = (64, 64)

train_loader, test_loader, classes = get_data_loaders(train_dir, test_dir, batch_size, image_size)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = ASLCNN(num_classes=len(classes)).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

for epoch in range(num_epochs):
    model.train()
    running_loss, correct, total = 0.0, 0, 0
    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
    print(f"Epoch {epoch+1}/{num_epochs}, Loss: {running_loss/len(train_loader):.4f}, Accuracy: {100*correct/total:.2f}%")

model.eval()
correct, total = 0, 0
with torch.no_grad():
    for inputs, labels in test_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        outputs = model(inputs)
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
print(f"Test Accuracy: {100*correct/total:.2f}%")

os.makedirs(os.path.dirname(save_path), exist_ok=True)
torch.save(model.state_dict(), save_path)
print(f"Model saved to {save_path}")
