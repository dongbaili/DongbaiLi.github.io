## 使用MLP版本
### 结果
- 在一部分setting下我们的方法更好，例如S->V小样本量和collinearity。
- 在其余setting下表现比较接近，很难总结规律
- 我们的方法依然更稳定
## 一些想法
- 只有加fitting loss比不加要明显好，才有可能比加反过来的fitting loss明显好
- 和离散情况一致，我们的方法decorelation loss往往更大
 。fitting loss几乎在训练过程中不变/逐渐变大
- 看起来加入我们设计的fitting loss对于MLP版本提升比较小。而对于离散版本的提升更大。
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