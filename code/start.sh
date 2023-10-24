seed=42
times=5
p=10
r_train=2.5
iters_balance=15000
iter_print=100
k=2000
n=500
mode="V->S"
python main.py --k $k --seed $seed --reweighting DWR --times $times --mode $mode --n $n --p $p --r_train $r_train --iters_balance $iters_balance --iter_print $iter_print --bv_analysis
mode="collinearity"
python main.py --k $k --seed $seed --reweighting DWR --times $times --mode $mode --n $n --p $p --r_train $r_train --iters_balance $iters_balance --iter_print $iter_print --bv_analysis