import torch
from torch import optim
import numpy as np
from utils import weighted_cov_torch
from Prediction_Model import PredictionModel
import matplotlib.pyplot as plt
import torch.nn as nn
def decorr_loss(X, weight, cov_mask=None, order=1):
    n = X.shape[0]
    p = X.shape[1]
    balance_loss = 0.0 
    for a in range(1, order+1):
        for b in range(a, order+1):
            if a != b:
                cov_mat = weighted_cov_torch(X**a, X**b, W=weight**2/n)
            else:
                cov_mat = weighted_cov_torch(X**a, W=weight**2/n)
            cov_mat = cov_mat**2
            cov_mat = cov_mat * cov_mask
            balance_loss += torch.sum(torch.sqrt(torch.sum(cov_mat, dim=1)-torch.diag(cov_mat) +  1e-10))

    loss_weight_sum = (torch.sum(weight * weight) - n) ** 2
    loss_weight_l2 = torch.sum((weight * weight) ** 2)
    loss = 2000.0 / p * balance_loss + 0.5 * loss_weight_sum + 0.00005 * loss_weight_l2 # hard coding
    return loss, balance_loss, loss_weight_sum, loss_weight_l2

class MLP(nn.Module):
    def __init__(self, input_size, output_size, n):
        super(MLP, self).__init__()
        # hidden_size = int(n / (5 * (input_size + output_size)))
        hidden_size = 10
        # Define the layers
        self.fc1 = nn.Linear(input_size, hidden_size)
        # self.fc1 = nn.Linear(input_size, output_size)
        self.t1 = nn.Tanh()
        self.fc2 = nn.Linear(hidden_size, output_size)
        # self.t2 = nn.Tanh()
        # self.fc3 = nn.Linear(hidden_size, output_size)
        
    def forward(self, x):
        x = self.fc1(x)
        x = self.t1(x)
        x = self.fc2(x)
        # x = self.t2(x)
        # x = self.fc3(x)
        return x
    
def Weight_model(X, Y, epochs = 2, cov_mask=None, order=1, num_steps = 5000, lr = 0.02, tol=1e-8, loss_lb=0.001, iter_print=1000, logger=None, device=None,weight=None, k = 100):
    X = torch.tensor(X, dtype=torch.float, device=device)
    Y= torch.tensor(Y, dtype=torch.float, device=device)
    n, p = X.shape    
    if cov_mask is None:
        cov_mask = torch.ones((p, p), device=device)
    else:
        cov_mask = torch.tensor(cov_mask, dtype=torch.float, device=device)
    model = MLP(p, 1, n)
    optimizer = optim.Adam(model.parameters(), lr = lr)
    p_model = PredictionModel(epochs=epochs)
    weight_list = []
    corr_list = []
    for i in range(num_steps):
        optimizer.zero_grad()
        weight = model(X)
        
        independ_loss, balance_loss, loss_s, loss_2 = decorr_loss(X, weight, cov_mask, order=order)
        
        # predict_loss, r_loss, r_weight = p_model.train_and_test(X, Y, weight)
        # loss = independ_loss +  k * predict_loss
        
        loss = independ_loss
        loss.backward()
        optimizer.step()
        if (i+1) % iter_print == 0:
            record = (weight**2).cpu().detach().numpy()
            record /= np.sum(record) # normalize: weights sum up to 1
            weight_list.append(record)
            if (i+1) % (iter_print*10) == 0:
                print(f"iter{i+1}: Decorrelation loss:{independ_loss} Loss: {loss}")
                # print(f"iter{i+1}: Decorrelation loss:{independ_loss} predict_loss:{predict_loss} Loss: {loss}")
            # record the corr of loss and weight
            # correlation_coefficient = np.corrcoef(r_loss.detach().numpy().T, (r_weight**2).detach().numpy().T)[0,1]
            # corr_list.append(correlation_coefficient) 
    return weight_list, corr_list, independ_loss