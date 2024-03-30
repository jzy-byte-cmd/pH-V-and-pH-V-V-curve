import sympy
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error,r2_score,max_error
from scipy.interpolate import make_interp_spline    #原spline函数

# 显示中文
plt.rcParams['font.sans-serif'] = [u'SimHei']
plt.rcParams['axes.unicode_minus'] = False

def paint(x,y,x_new,y_new):
    # 绘制原始数据点和拟合的曲线
    plt.scatter(x, y,  label='原始数据',color="red",s=10)
    plt.plot(x_new, y_new,label='拟合曲线', linewidth=2,color="black")
    plt.legend()
    plt.show()

def paint_line(x,y,label,color,line_style):   #传入点   #计算一次函数,并画图
    b=y-x   #截距
    points_x,points_y=[],[]
    for i in np.linspace(x-1.5,x+1.5,5):
        points_x.append(i)
        points_y.append(i+b)
    plt.plot(points_x,points_y,line_style,lw=2,color=color,label=label)
    return  


def fit(x_new,y_new,times):     #拟合
        coeff = np.polyfit(x_new, y_new, times)

        # 使用numpy.poly1d来创建多项式对象
        poly1d_obj = np.poly1d(coeff)

        #print(poly1d_obj) 
        # 使用多项式对象来计算拟合的y值
        y_fit = poly1d_obj(x_new)
        return y_fit,poly1d_obj


# 生成样本数据
x=[0.50,1.50,2.50,3.50,4.50,5.05,5.15,5.25,5.35,5.45,5.55,5.65,5.75,5.85,5.95,6.50,7.50,8.50,9.50]
y=[0.72,0.38,0.22,0.45,0.46,1.50,1.20,0.90,1.10,1.40,1.60,1.90,1.30,1.20,11.0,2.98,0.56,0.24,0.16]


x_new,y_new=[],[]    #插值后的x,y

mse,r2,max_err=[],[],[]   #MSE,R2,MAX_ERROR


x_size=len(x)
y_size=len(y)
insert_num=5        #插值数
#插值   
for i in range(1,x_size):   #对x进行插值
    arr=np.linspace(x[i-1],x[i],50)          #插值越多曲线越平滑
    for k in arr:
        x_new.append(k)
    
x_new=set(x_new)
x_new=list(x_new)   #过滤重复元素
x_new.sort()
print(len(x_new))
#exit(0)

y_new=make_interp_spline(x,y,k=1)(x_new)    #对y插值
print(y_new,len(y_new))
#exit(0)

# 使用numpy.polyfit进行多项式拟合
# 10是拟合的多项式的最高次数
# 输出为多项式的系数，其中第0个元素是常数项

for i in range(0,21):   #i是最高次数

    y_fit,Fx=fit(x_new,y_new,i)
    mse.append(mean_squared_error(y_new,y_fit))
    r2.append(r2_score(y_new,y_fit))
    max_err.append(max_error(y_new,y_fit))

min_max_error,deg_max=min(max_err),max_err.index(min(max_err))
print("max_error最小:",min_max_error,"  最高次为:",deg_max)
#exit(0)

y_fit,Fx=fit(x_new,y_new,deg_max)   #返回最好的多项式函数,并计算相应的y值

'''
for i in root_complex:
    if i.imag==0.0 and 5<=i.real<=7:
        root.append(float(i))
        F1x_points[float(i)]=float(F1x(float(i)))
        Fx_points[float(i)]=float(Fx(float(i)))


print("原来的多项式:",F1x,"\n\n新多项式:",F1x_target,"\n\n5~7内的实根:",root,"\n\n导函数点:",F1x_points,"\n原函数点:",Fx_points)

'''




print("MSE(均方误差):",mean_squared_error(y_new,y_fit))      #打印MSE 均方误差
print("R2(回归决定系数):",r2_score(y_new,y_fit))    #r**2
print("MAX_ERROR(最大误差):",max_error(y_new,y_fit))
print("\n函数:",Fx)


'''
av_x,av_y=0,0,
for k in Fx_points:
    paint_line(k,Fx_points[k],"斜率为1的切线","blue","-")
    av_x+=k
    av_y+=Fx_points[k]

av_x/=len(Fx_points)
av_y/=len(Fx_points)
paint_line(av_x,av_y,"等分线","red","-.")
print("\n\nNaOH V/mL:%lf    化学计量点:%lfpH"%(av_x,av_y))
plt.scatter(av_x,av_y,label="化学计量点",s=10,color="green")
'''
plt.xlabel("V")
plt.ylabel("pH")
plt.title('ΔpH/ΔV-V曲线')
plt.xticks([0.00,1.00,2.00,3.00,4.00,5.00,6.00,7.00,8.00,9.00,10.00],['0.00','1.00','2.00','3.00','4.00','5.00','6.00','7.00','8.00','9.00','10.00'])
plt.yticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],['0.00','1.00','2.00','3.00','4.00','5.00','6.00','7.00','8.00','9.00','10.00','11.00','12.00','13.00','14.00'])
'''
plt.annotate('NaOH V=%lfmL  pH=%lf'%(av_x,av_y),
         xy=(av_x, av_y), xycoords='data',
         xytext=(+9, -8), textcoords='offset points', fontsize=10,
         arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
'''

y_find=list(y_new)
x_find=[x_new[y_find.index(max(y_find))]]*10
y_find=list(np.linspace(0,max(y_find),10))

print(x_find,y_find)

plt.plot(x_find,y_find,"-.",label="Ve=%.3lf"%x_find[0])
paint(x,y,x_new,y_new)  #画图
