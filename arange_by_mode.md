## 结果
- 在一部分setting下我们的方法更好，例如S->V小样本量和collinearity。
- 在其余setting下表现比较接近，很难总结规律
- 我们的方法的曲线波动会更小
## 一些想法
- 容易理解的是，好setting下往往加fitting loss比不加的明显好
- 如果没有明显比"double"好，那么就不应期望比fake dwr版本明显好
- 超参数相同的情况下，我们的方法decorelation loss往往更大
- 我们的方法fitting loss几乎在训练过程中不变/逐渐变大
### S->V

<div style="display: flex;">
    n = 100
    <img src="final/S->V_n=100.png" alt="" width="400">
    n = 200
    <img src="final/S->V_n=200.png" alt="" width="400">
</div>
<div style="display: flex;">
    n = 500
    <img src="final/S->V_n=500.png" alt="" width="400">
    n = 1000
    <img src="final/S->V_n=1000.png" alt="" width="400">
</div>
<div style="display: flex;">
    n = 1500
    <img src="final/S->V_n=1500.png" alt="" width="400">
    n = 2000
    <img src="final/S->V_n=2000.png" alt="" width="400">
</div>

### V->S
<div style="display: flex;">
    n = 100
    <img src="final/V->S_n=100.png" alt="" width="400">
    n = 200
    <img src="final/V->S_n=200.png" alt="" width="400">
</div>
<div style="display: flex;">
    n = 500
    <img src="final/V->S_n=500.png" alt="" width="400">
    n = 1000
    <img src="final/V->S_n=1000.png" alt="" width="400">
</div>
<div style="display: flex;">
    n = 1500
    <img src="final/V->S_n=1500.png" alt="" width="400">
    n = 2000
    <img src="final/V->S_n=2000.png" alt="" width="400">
</div>

### S_|_V
<div style="display: flex;">
    n = 100
    <img src="final/S_|_V_n=100.png" alt="" width="400">
    n = 200
    <img src="final/S_|_V_n=200.png" alt="" width="400">
</div>
<div style="display: flex;">
    n = 500
    <img src="final/S_|_V_n=500.png" alt="" width="400">
    n = 1000
    <img src="final/S_|_V_n=1000.png" alt="" width="400">
</div>
<div style="display: flex;">
    n = 1500
    <img src="final/S_|_V_n=1500.png" alt="" width="400">
    n = 2000
    <img src="final/S_|_V_n=2000.png" alt="" width="400">
</div>

### collinearity
<div style="display: flex;">
    n = 100
    <img src="final/collinearity_n=100.png" alt="" width="400">
    n = 200
    <img src="final/collinearity_n=200.png" alt="" width="400">
</div>
<div style="display: flex;">
    n = 500
    <img src="final/collinearity_n=500.png" alt="" width="400">
    n = 1000
    <img src="final/collinearity_n=1000.png" alt="" width="400">
</div>
<div style="display: flex;">
    n = 1500
    <img src="final/collinearity_n=1500.png" alt="" width="400">
    n = 2000
    <img src="final/collinearity_n=2000.png" alt="" width="400">
</div>