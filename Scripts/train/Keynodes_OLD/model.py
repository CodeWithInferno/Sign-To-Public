import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv, global_mean_pool

class ASLGNN(torch.nn.Module):
    def __init__(self, in_features=3, hidden_dim=64, num_classes=29):
        super(ASLGNN, self).__init__()
        self.conv1 = GCNConv(in_features, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, hidden_dim)
        self.fc = torch.nn.Linear(hidden_dim, num_classes)

    def forward(self, data):
        x, edge_index, batch = data.x, data.edge_index, data.batch
        x = F.relu(self.conv1(x, edge_index))
        x = F.relu(self.conv2(x, edge_index))
        x = global_mean_pool(x, batch)
        return self.fc(x)
