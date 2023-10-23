seed=42
times=5
p=10
r_train=2.5
iters_balance=15000
iter_print=100
k=100
n=100
mode="S_|_V"
python main.py --k $k --seed $seed --reweighting DWR --times $times --mode $mode --n $n --p $p --r_train $r_train --iters_balance $iters_balance --iter_print $iter_print --bv_analysis
mode="S->V"
python main.py --k $k --seed $seed --reweighting DWR --times $times --mode $mode --n $n --p $p --r_train $r_train --iters_balance $iters_balance --iter_print $iter_print --bv_analysis
mode="V->S"
python main.py --k $k --seed $seed --reweighting DWR --times $times --mode $mode --n $n --p $p --r_train $r_train --iters_balance $iters_balance --iter_print $iter_print --bv_analysis
mode="collinearity"
python main.py --k $k --seed $seed --reweighting DWR --times $times --mode $mode --n $n --p $p --r_train $r_train --iters_balance $iters_balance --iter_print $iter_print --bv_analysis
n=200
mode="S_|_V"
python main.py --k $k --seed $seed --reweighting DWR --times $times --mode $mode --n $n --p $p --r_train $r_train --iters_balance $iters_balance --iter_print $iter_print --bv_analysis
mode="S->V"
python main.py --k $k --seed $seed --reweighting DWR --times $times --mode $mode --n $n --p $p --r_train $r_train --iters_balance $iters_balance --iter_print $iter_print --bv_analysis
mode="V->S"
python main.py --k $k --seed $seed --reweighting DWR --times $times --mode $mode --n $n --p $p --r_train $r_train --iters_balance $iters_balance --iter_print $iter_print --bv_analysis
mode="collinearity"
python main.py --k $k --seed $seed --reweighting DWR --times $times --mode $mode --n $n --p $p --r_train $r_train --iters_balance $iters_balance --iter_print $iter_print --bv_analysis
n=500
mode="S_|_V"
python main.py --k $k --seed $seed --reweighting DWR --times $times --mode $mode --n $n --p $p --r_train $r_train --iters_balance $iters_balance --iter_print $iter_print --bv_analysis
mode="S->V"
python main.py --k $k --seed $seed --reweighting DWR --times $times --mode $mode --n $n --p $p --r_train $r_train --iters_balance $iters_balance --iter_print $iter_print --bv_analysis
mode="V->S"
python main.py --k $k --seed $seed --reweighting DWR --times $times --mode $mode --n $n --p $p --r_train $r_train --iters_balance $iters_balance --iter_print $iter_print --bv_analysis
mode="collinearity"
python main.py --k $k --seed $seed --reweighting DWR --times $times --mode $mode --n $n --p $p --r_train $r_train --iters_balance $iters_balance --iter_print $iter_print --bv_analysis
n=1000
mode="S_|_V"
python main.py --k $k --seed $seed --reweighting DWR --times $times --mode $mode --n $n --p $p --r_train $r_train --iters_balance $iters_balance --iter_print $iter_print --bv_analysis
mode="S->V"
python main.py --k $k --seed $seed --reweighting DWR --times $times --mode $mode --n $n --p $p --r_train $r_train --iters_balance $iters_balance --iter_print $iter_print --bv_analysis
mode="V->S"
python main.py --k $k --seed $seed --reweighting DWR --times $times --mode $mode --n $n --p $p --r_train $r_train --iters_balance $iters_balance --iter_print $iter_print --bv_analysis
mode="collinearity"
python main.py --k $k --seed $seed --reweighting DWR --times $times --mode $mode --n $n --p $p --r_train $r_train --iters_balance $iters_balance --iter_print $iter_print --bv_analysis
n=1500
mode="S_|_V"
python main.py --k $k --seed $seed --reweighting DWR --times $times --mode $mode --n $n --p $p --r_train $r_train --iters_balance $iters_balance --iter_print $iter_print --bv_analysis
mode="S->V"
python main.py --k $k --seed $seed --reweighting DWR --times $times --mode $mode --n $n --p $p --r_train $r_train --iters_balance $iters_balance --iter_print $iter_print --bv_analysis
mode="V->S"
python main.py --k $k --seed $seed --reweighting DWR --times $times --mode $mode --n $n --p $p --r_train $r_train --iters_balance $iters_balance --iter_print $iter_print --bv_analysis
mode="collinearity"
python main.py --k $k --seed $seed --reweighting DWR --times $times --mode $mode --n $n --p $p --r_train $r_train --iters_balance $iters_balance --iter_print $iter_print --bv_analysis
n=2000
mode="S_|_V"
python main.py --k $k --seed $seed --reweighting DWR --times $times --mode $mode --n $n --p $p --r_train $r_train --iters_balance $iters_balance --iter_print $iter_print --bv_analysis
mode="S->V"
python main.py --k $k --seed $seed --reweighting DWR --times $times --mode $mode --n $n --p $p --r_train $r_train --iters_balance $iters_balance --iter_print $iter_print --bv_analysis
mode="V->S"
python main.py --k $k --seed $seed --reweighting DWR --times $times --mode $mode --n $n --p $p --r_train $r_train --iters_balance $iters_balance --iter_print $iter_print --bv_analysis
mode="collinearity"
python main.py --k $k --seed $seed --reweighting DWR --times $times --mode $mode --n $n --p $p --r_train $r_train --iters_balance $iters_balance --iter_print $iter_print --bv_analysis