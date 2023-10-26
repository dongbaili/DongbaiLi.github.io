## See the coefficients of lienar model
### conclusions:
1. Average Negative RMSE最小 对应 模型参数对v的权重小
2. Decorrelation loss越小并不保证模型参数对v的权重更小
   - 甚至所有情况下Best case都有较大的Decorrelation loss
### S->V
n=100
<div style="display: flex;">
    <img src="params/S->V/n=100_best.png" alt="" width="300">
    <img src="params/S->V/n=100_4000.png" alt="" width="300">
    <img src="params/S->V/n=100_12000.png" alt="" width="300">
</div>
n=200
<div style="display: flex;">
    <img src="params/S->V/n=200_best.png" alt="" width="300">
    <img src="params/S->V/n=200_4000.png" alt="" width="300">
    <img src="params/S->V/n=200_12000.png" alt="" width="300">
</div>
n=500
<div style="display: flex;">
    <img src="params/S->V/n=500_best.png" alt="" width="300">
    <img src="params/S->V/n=500_4000.png" alt="" width="300">
    <img src="params/S->V/n=500_12000.png" alt="" width="300">
</div>

### S_|_V
n=100
<div style="display: flex;">
    <img src="params/S_|_V/n=100_best.png" alt="" width="300">
    <img src="params/S_|_V/n=100_4000.png" alt="" width="300">
    <img src="params/S_|_V/n=100_12000.png" alt="" width="300">
</div>
n=200
<div style="display: flex;">
    <img src="params/S_|_V/n=200_best.png" alt="" width="300">
    <img src="params/S_|_V/n=200_4000.png" alt="" width="300">
    <img src="params/S_|_V/n=200_12000.png" alt="" width="300">
</div>
n=500
<div style="display: flex;">
    <img src="params/S_|_V/n=500_best.png" alt="" width="300">
    <img src="params/S_|_V/n=500_4000.png" alt="" width="300">
    <img src="params/S_|_V/n=500_12000.png" alt="" width="300">
</div>

### collinearity
n=100
<div style="display: flex;">
    <img src="params/collinearity/n=100_best.png" alt="" width="300">
    <img src="params/collinearity/n=100_4000.png" alt="" width="300">
    <img src="params/collinearity/n=100_12000.png" alt="" width="300">
</div>
n=200
<div style="display: flex;">
    <img src="params/collinearity/n=200_best.png" alt="" width="300">
    <img src="params/collinearity/n=200_4000.png" alt="" width="300">
    <img src="params/collinearity/n=200_12000.png" alt="" width="300">
</div>
n=500
<div style="display: flex;">
    <img src="params/collinearity/n=500_best.png" alt="" width="300">
    <img src="params/collinearity/n=500_4000.png" alt="" width="300">
    <img src="params/collinearity/n=500_12000.png" alt="" width="300">
</div>