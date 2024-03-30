# pH-V-and-pH-V-V-curve
pH-V曲线和ΔpH/ΔV-V曲线，确定氢氧化钠滴定HAc终点和Ve

## pH-V曲线基本原理
```
from sklearn.metrics import mean_squared_error,r2_score,max_error
from scipy.interpolate import make_interp_spline    #原spline函数
```
利用spline对初始数据进行插值，使曲线平滑。
利用numpy的polyfit对插值后的数据进行多项式拟合，利用```MSE```,```R2```,```MAX_ERROR```
找出最高阶数为[0,20]内的MAX_ERROR最小的多项式，并用其拟合曲线。
计算斜率为1的切线和等分线以及
```化学计量点pH和滴定终点Ve```

## ▲pH/▲V-V曲线基本原理
利用spline对初始数据插值，使曲线平滑
利用spline对初始数据进行插值，使曲线平滑。
利用numpy的polyfit对插值后的数据进行多项式拟合，利用```MSE```,```R2```,```MAX_ERROR```
找出最高阶数为[0,20]内的MAX_ERROR最小的多项式，并用其拟合曲线。
找到拟合曲线的最大y值，确定最大y值时对应的x值为```滴定终点Ve```
