import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import torch.nn.functional as F
class PredictionModel(nn.Module):
    def __init__(self, epochs = 2, p = 10):
        super(PredictionModel, self).__init__()
        self.linear = nn.Linear(p, 1)
        self.epochs = epochs
        self.optimizer = optim.Adam(self.linear.parameters(), lr=0.01)
        self.criterion = F.mse_loss
    def forward(self, x):
        return self.linear(x)
    
    def train_and_test(self, X, Y, weight):
        weight_clone =  weight.detach().clone()
        weight_clone = (weight_clone**2) / (weight_clone**2).sum()
        self.train()
        # train {epochs} steps
        for epoch in range(self.epochs):
            output = self.forward(X)
            loss = self.criterion(output, Y, reduction='none')
            weighted_loss = (loss*weight_clone).mean()
            self.optimizer.zero_grad()
            weighted_loss.backward()
            self.optimizer.step()
        # return prediction loss
        output = self.forward(X)
        loss = self.criterion(output, Y, reduction='none')
        weighted_loss = (loss * torch.max(weight_clone) - loss * weight_clone).mean()
        return weighted_loss, loss, weight
    