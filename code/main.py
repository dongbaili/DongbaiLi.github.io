from utils import setup_seed, get_beta_s, get_expname, calc_var, pretty, get_cov_mask, BV_analysis, get_corr_pic
from sklearn.metrics import mean_squared_error
from data.selection_bias import gen_selection_bias_data
import numpy as np
import argparse
import os
import torch
from Logger import Logger
from collections import defaultdict as dd
from MLP import Weight_model
from DWR import DWR
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

def get_args():
    parser = argparse.ArgumentParser(description="Script to launch sample reweighting experiments", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    # data generation
    parser.add_argument("--p", type=int, default=10, help="Input dim")
    parser.add_argument("--n", type=int, default=2000, help="Sample size")
    parser.add_argument("--V_ratio", type=float, default=0.5)
    parser.add_argument("--Vb_ratio", type=float, default=0.1)
    parser.add_argument("--true_func", choices=["linear",], default="linear")
    parser.add_argument("--mode", choices=["S_|_V", "S->V", "V->S", "collinearity"], default="S_|_V")
    parser.add_argument("--misspe", choices=["poly", "exp", "None"], default="poly")
    parser.add_argument("--corr_s", type=float, default=0.9)
    parser.add_argument("--corr_v", type=float, default=0.1)
    parser.add_argument("--mms_strength", type=float, default=1.0, help="model misspecifction strength")
    parser.add_argument("--spurious", choices=["nonlinear", "linear"], default="nonlinear")
    parser.add_argument("--r_train", type=float, default=2.5, help="Input dim")
    parser.add_argument("--r_list", type=float, nargs="+", default=[-3, -2, -1.7, -1.5, -1.3, 1.3, 1.5, 1.7, 2, 3])
    parser.add_argument("--noise_variance", type=float, default=0.3)

    # frontend reweighting 
    parser.add_argument("--reweighting", choices=["None", "DWR", "SRDO"], default="DWR")
    parser.add_argument("--decorrelation_type", choices=["global", "group"], default="global")
    parser.add_argument("--order", type=int, default=1)
    parser.add_argument("--iters_balance", type=int, default=10000)

    # backend model 
    parser.add_argument("--backend", choices=["OLS", "Lasso", "Ridge"], default="OLS")
    parser.add_argument("--paradigm", choices=["regr", "fs",], default="regr")
    parser.add_argument("--iters_train", type=int, default=1000)
    parser.add_argument("--lam_backend", type=float, default=0.01) # regularizer coefficient
    parser.add_argument("--fs_type", choices=["oracle", "None", "given", "STG"], default="STG")
    parser.add_argument("--mask_given", type=int, nargs="+", default=[1,1,1,1,1,0,0,0,0,0])
    parser.add_argument("--mask_threshold", type=float, default=0.2)
    parser.add_argument("--lam_STG", type=float, default=3)
    parser.add_argument("--sigma_STG", type=float, default=0.1)
    parser.add_argument("--metrics", nargs="+", default=["L1_beta_error", "L2_beta_error"])
    parser.add_argument("--bv_analysis", action="store_true")

    # others
    parser.add_argument("--seed", type=int, default=3)
    parser.add_argument("--times", type=int, default=10)
    parser.add_argument("--result_dir", default="results")

    # 10.12 add
    parser.add_argument("--epochs", type=int, default=1)
    parser.add_argument("--iter_print", type=int, default=1000)
    parser.add_argument("--k", type=int, default=1000)

    return parser.parse_args()

def main(args, round, logger):
    setup_seed(args.seed + round)
    p = args.p
    p_v = int(p*args.V_ratio)
    p_s = p-p_v
    n = args.n
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # generate train data
    X_train, S_train, V_train, fs_train, Y_train = gen_selection_bias_data({**vars(args),**{"r": args.r_train}})
    W = np.ones((n, 1))/n

    beta_s = get_beta_s(p_s)
    beta_v = np.zeros(p_v)
    beta = np.concatenate([beta_s, beta_v])
    
    linear_var, nonlinear_var, total_var = calc_var(beta_s, S_train, fs_train)
    logger.info("Linear term var: %.3f, Nonlinear term var: %.3f, total var: %.3f" % (linear_var, nonlinear_var, total_var))
    
    # generate test data
    test_data = dict()
    for r_test in args.r_list:
        X_test, S_test, V_test, fs_test, Y_test = gen_selection_bias_data({**vars(args),**{"r": r_test}})
        test_data[r_test] = (X_test, S_test, V_test, fs_test, Y_test)

    # Main train process
    cov_mask = get_cov_mask(np.zeros(p))
    weight = torch.ones(n, 1, device=device)
    W_list, rev_corr_list, decorr_loss = Weight_model(X_train, Y_train, epochs = args.epochs, cov_mask = cov_mask, order=args.order, num_steps=args.iters_balance, logger=logger, device=device, weight=weight, iter_print=args.iter_print, k = args.k)

    # Test the weight we get from Weight_model
    ans, corr_list = [], []
    i = 0
    for W in W_list:
        model = LinearRegression()
        model.fit(X_train, Y_train, W.reshape(-1))
        b = []
        for r_test in args.r_list:
            X_test, S_test, V_test, fs_test, Y_test = test_data[r_test]
            Yp = model.predict(X_test)
            b.append(mean_squared_error(Y_test, Yp))
        ans.append(b)
        i += 1
        
    # See the correlation between loss and weight from the reversed model 
    """
    print(rev_corr_list)
    plt.figure(dpi = 240)
    plt.plot([(i+1) * args.iter_print for i in range(len(rev_corr_list))], rev_corr_list)
    plt.title('rev_correlation: loss & weight')
    plt.savefig(f'./images/{args.mode}_rev_corr{round}.png')
    plt.close()
    """
    # baseline1: linear model
    model = LinearRegression()
    model.fit(X_train, Y_train)
    linear_ans = []
    for r_test in args.r_list:
        X_test, S_test, V_test, fs_test, Y_test = test_data[r_test]
        Yp = model.predict(X_test)
        linear_ans.append(mean_squared_error(Y_test, Yp))
    
    # baseline2: DWR
    dwr_ans = []
    """
    logger.info('Start training DWR...')
    model = LinearRegression()
    weight = torch.ones(n, 1, device=device)        
    W_list = DWR(X_train, cov_mask=cov_mask, order=args.order,logger = logger,num_steps=args.iters_balance,device=device,weight=weight)
    # save the weight we get from DWR
    # np.save(f"weights/k={args.k}/n={args.n}/dwr_{args.mode}_{args.iters_balance}_{round}_r={args.r_train}",W_list)
    for W in W_list:
        model.fit(X_train, Y_train, W.reshape(-1))
        b = []
        for r_test in args.r_list:
            X_test, S_test, V_test, fs_test, Y_test = test_data[r_test]
            Yp = model.predict(X_test)
            b.append(mean_squared_error(Y_test, Yp))
        dwr_ans.append(b)
    """
    return ans, linear_ans, dwr_ans

if __name__ == "__main__":
    args = get_args()
    logger = Logger(args)
    logger.log_args(args)
    neg_RMSE_list = []
    linear_list= []
    dwr_list = []

    for i in range(args.times):
        logger.info("Round %d" % i)
        results, linear_ans, dwr_ans= main(args, i, logger)
        neg_RMSE = [np.mean(b[:5]) for b in results]
        neg_DWR = [np.mean(b[:5]) for b in dwr_ans]
        neg_RMSE_list.append(neg_RMSE)
        dwr_list.append(neg_DWR)

        linear_list.append(np.mean(linear_ans[:5]))

    logger.info("-------Final Result:--------")
    mean_neg_RMSE = np.mean(neg_RMSE_list, axis = 0)
    mean_dwr = np.mean(dwr_list, axis = 0)
    mean_linear = np.mean(linear_list)
    x = [(i+1) * args.iter_print for i in range(len(mean_neg_RMSE))]
    for iter, ans in zip(x, mean_neg_RMSE):
        print(f"iter{iter}: neg_RMSE = {ans}")
    print(f"linear neg_RMSE = {mean_linear}")
    np.save(f'./RMSEs/combine/{args.mode}/n={args.n}_k={args.k}',mean_neg_RMSE)
    # np.save(f'./RMSEs/combine/{args.mode}/DWR_n={args.n}_r={args.r_train}',mean_dwr)
    # np.save(f'./RMSEs/combine/{args.mode}/linear_n={args.n}_r={args.r_train}',[mean_linear]*len(x))
    # plt.figure(dpi = 240)
    # plt.plot(x, mean_neg_RMSE, label = 'new method')
    # plt.plot(x, mean_dwr, label = 'dwr')
    # plt.plot(x, [mean_linear]*len(x), label = 'linear')
    # plt.legend()
    # plt.title('neg_RMSE')
    # plt.savefig(f'./images/MLP/n={args.n}_{args.mode}_{args.iters_balance}_r={args.r_train}.png')