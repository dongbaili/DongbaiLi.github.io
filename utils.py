from select import select
import numpy as np
import random
from math import ceil
import torch
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns
import logging
beta_base = [1/3, -2/3, 1, -1/3, 2/3, -1,] # hard-coded coefficients

def get_corr_pic(data,data_y,w,label):
    logging.basicConfig(level=logging.INFO)
    plt.figure()
    plt.title('The Corr')
    data_y = data_y.reshape(-1,1)
    w = w.reshape(-1,1)
    corr = weighted_corr(np.concatenate((data,data_y),axis=1),np.concatenate((data,data_y),axis=1),w)
    ax = plt.subplots(figsize=(16, 16))
    ax = sns.heatmap(np.abs(corr), cmap="YlGnBu")
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.savefig('./images/heatMap/'+str(label)+'_corr.jpg')
    plt.close()
    logging.basicConfig(level=logging.DEBUG)

def setup_seed(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    random.seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

def weighted_cov(X, W):
    '''
    X: numpy array, (n, p)
    W: numpy array, (n, 1), sum up to 1
    '''
    X_bar =  np.matmul(X.T, W) # shape: (p, 1)
    return np.matmul(X.T, W*X) - np.matmul(X_bar, X_bar.T)

def weighted_cov_torch(X, Y=None, W=None):
    if Y is None:
        X_bar = torch.matmul(X.T, W) # shape: (p, 1)
        return torch.matmul(X.T, W*X) - torch.matmul(X_bar, X_bar.T)
    else:
        X_bar = torch.matmul(X.T, W) # shape: (p, 1)
        Y_bar = torch.matmul(Y.T, W) # shape: (p, 1)
        return torch.matmul(X.T, W*Y) - torch.matmul(X_bar, Y_bar.T)


def weighted_corr(X, Y=None, W=None):
    '''
    X: numpy array, (n, p)
    W: numpy array, (n, 1), sum up to 1
    '''
    if Y is None:
        X_bar = np.matmul(X.T, W) # shape: (p, 1)
        X_2_bar = np.matmul((X**2).T, W) # shape: (p, 1)
        varX = X_2_bar - X_bar**2
        return (np.matmul(X.T, W*X) - np.matmul(X_bar, X_bar.T)) / np.sqrt(np.matmul(varX, varX.T))
    else:
        X_bar = np.matmul(X.T, W) # shape: (p, 1)
        Y_bar = np.matmul(Y.T, W)
        X_2_bar = np.matmul((X**2).T, W) # shape: (p, 1)
        Y_2_bar = np.matmul((Y**2).T, W)
        varX = X_2_bar - X_bar**2
        varY = Y_2_bar - Y_bar**2
        return (np.matmul(X.T, W*Y) - np.matmul(X_bar, Y_bar.T)) / np.sqrt(np.matmul(varX, varY.T))

def pretty(vector):
    if type(vector) is list:
        vlist = vector
    elif type(vector) is np.ndarray:
        vlist = vector.reshape(-1).tolist()
    else:
        vlist = vector.view(-1).tolist()
    return "[" + ", ".join("{:+.4f}".format(vi) for vi in vlist) + "]"

def get_cov_mask(select_ratio):
    select_ratio = np.reshape(select_ratio, (-1, 1))
    cov_mask = 1-np.matmul(select_ratio, select_ratio.T)
    return cov_mask 


def get_beta_s(p_s):
    beta_s = beta_base * (ceil(p_s/len(beta_base)))
    return np.array(beta_s[:p_s])

def get_beta_collinearity(p):
    beta_base = [1/5, -2/5, 3/5, -4/5, 1, -1/5, 2/5, -3/5, 4/5, -1,] # hard-coded coefficients
    beta = beta_base * (ceil(p/len(beta_base)))
    return np.array(beta[:p])

def get_expname(args):
    order = "-order=%d"%args.order if args.reweighting == "DWR" else ""
    MLP_gen = "-MLP_gen=%s" % "_".join([str(j) for j in args.hidden_units_gen]) if args.true_func == "MLP" else ""
    MLP_backend = "-MLP_backend=%s" % "_".join([str(j) for j in args.hidden_units_backend]) if args.backend == "MLP" else ""
    misspe = "-misspe=%s"%args.misspe if args.true_func == "linear" else ""
    paradigm = "" if args.true_func == "linear" else "-paradigm=%s"%args.paradigm
    backend = "fs=%s"%args.fs_type if args.paradigm == "fs" else "regr=%s" % args.backend
    return  "p=%d%s%s-n=%d-Vb_ratio=%.1f-%s%s-rtrain=%.1f-%s-%s-spurious=%s-%s%s%s"%(args.p, MLP_gen, MLP_backend, args.n, args.Vb_ratio, args.mode, misspe, args.r_train, args.reweighting, backend, args.spurious, args.decorrelation_type, order, paradigm)

def calc_var(beta, X, fx):
    beta = np.reshape(beta, (-1, 1))
    linear_term = np.matmul(X, beta)
    nonlinear_term = fx - linear_term
    return np.var(linear_term), np.var(nonlinear_term), np.var(fx)

def gen_Cov(p, rho):
    cov = np.ones((p, p))*rho
    for i in range(p):
        cov[i, i] = 1
    return cov

def gen_interaction_terms(X):
    X_mean = X.mean(axis=0)
    n, p = X.shape
    p_ia = (p*(p-1))//2
    X_ia = np.zeros((n, p_ia))
    cnt = 0
    for i in range(p):
        for j in range(i+1, p):
            X_ia[:, cnt] = (X[:,i]-X_mean[i])*(X[:, j]-X_mean[j])
            cnt += 1
    assert cnt == p_ia
    return X_ia

def GridSearch(args, model_name, X_train, Y_train, W, X_val, Y_val):
    model_func = get_algorithm_class(model_name)
    best_MSE = 1e10
    best_lam = -1.0
    best_model = None
    if model_name != "OLS":
        for lam in args.lambda_grid:
            model = model_func(args, X_train, Y_train, W, lam)
            MSE = mean_squared_error(Y_val, model.predict(X_val))
            if MSE < best_MSE:
                best_MSE = MSE
                best_lam = lam
                best_model = model
    else:
        best_model = model_func(args, X_train, Y_train, W)
    return best_model, best_lam

def BV_analysis(beta_hat_array, beta):
    beta_hat_mean = np.mean(beta_hat_array, axis=0)
    bias = np.sum((beta_hat_mean-beta)**2)
    var = np.sum(np.diag(np.cov(beta_hat_array, rowvar=False)))
    return bias, var

def update(W, delta, lambdaa = 1.1):
    W = W * ((delta - delta.min()) / (delta.max() - delta.min()) / 20 + 1)
    P = W / W.sum()
    D = delta.max()
    L = delta / D
    # L = (delta * delta) / D**2
    # L = 1 - np.exp(-delta / D)
    L_ = (L * P).sum()
    Beta = L_ / (1 - L_)
    W = W / W.sum()
    return W, Beta

def ada(W,true,predict):
    p = W/W.sum()
    d = max(abs(true-predict))
    L = np.square(abs(true-predict)/d)
    # L = 1-np.exp(-1*(abs(true-predict)/d))
    L_ = (np.sum(L*p))
    b = L_ / (1-L_)
    ans = W*b**(1-L)
    ans = ans/ans.sum()
    return ans
if __name__ == "__main__":
    X = torch.randn(2000, 10)
    print(weighted_cov(X.numpy(), W=np.ones((X.shape[0], 1))/X.shape[0]))
    print(weighted_cov_torch(X, W=torch.ones((X.shape[0], 1))/X.shape[0]))
    print(np.cov(X.numpy().T))