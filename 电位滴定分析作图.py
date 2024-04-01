import time,os
import numpy as np
import matplotlib.pyplot as plt
import sklearn.metrics,scipy.interpolate 

#from scipy.interpolate import scipy.interpolate.make_interp_spline    #原spline函数

x,y=[],[]       #原始数据
dy_x=[]     #1阶微商
v1=[]           #一阶微商对应的V3
x_new,y_new=[],[]    #插值后的x,y
insert_num=30        #插值数
k_value=3     #cubic 3次样条插值
highest_order=20    #多项式最高次数(可能的 ) 用于找到最好的多项式
mse,r2,max_err=[],[],[]   #MSE,R2,MAX_ERROR
deg_max=0       #确认的多项式最高次数
eva_l,eva_h=5,7     #估计的 化学计量点范围
point_size=12             #数据点大小



def print_info():       #打印信息
    print("pH-V曲线绘制软件   programed by 华东理工大学材料学院学生讲师团 23010341金哲宇")
    print("MIT开源协议,源代码:")
    print("https://github.com/jzy-byte-cmd/pH-Vand-pH_-V-V-curve-")
    print("https://gitee.com/jzy-computer/p-h_-vand_p-h__-v_-v_curve")
    print("-"*70)
    #print("默认参数:1.")
    return


def paint(x,y,x_new,y_new):
    global point_size
    # 绘制原始数据点和拟合的曲线
    # 显示中文
    plt.rcParams['font.sans-serif'] = [u'SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.scatter(x, y,  label='原始数据',color="red",s=point_size)
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

def input_data():       #手动输入数据
    global x,y
    while True:
        x,y=[],[]
        while True:
            reinput=False
            str_=input("请输入体积数据(单位mL),以逗号(英文)分隔,回车结束:e.g. 1.20,2.30,3.2,4.1{ENTER}\n").strip()
            for i in str_:
                if (i!='.' and i!=',') and (ord(i)<48 or ord(i)>57):   #非法数据
                    print("非法输入: ",i,"请重新输入数据\n")
                    reinput=True
            if reinput==True:
                continue
            nums=str_.split(',')
            for i in nums:
                x.append(float(i))
            break
        str_=""
        nums.clear()
        nums=[]
        while True:
            reinput=False
            str_=input("请输入pH数据,以逗号(英文)分隔,回车结束:e.g. 1.20,2.30,3.2,4.1{ENTER}\n").strip()
            for i in str_:
                if (i!='.' and i!=',') and (ord(i)<48 or ord(i)>57):   #非法数据
                    print("非法输入: ",i,"请重新输入数据")
                    reinput=True
            if reinput==True:
                continue
            nums=str_.split(',')
            for i in nums:
                y.append(float(i))
            break
        str_=""
        nums.clear()
        nums=[]
        if len(x)!=len(y):  #数据不配对
            print("输入的数据无法一一配对(数量不匹配)")
            print("请重新输入\n")
            continue
        print("输入的数据:\n")
        print("|V/mL       |pH         |")
        for i in range(0,len(x)):
            print("|%11lf|%11lf|"%(x[i],y[i]))
        confirm=input("确认? y/n:")
        if confirm=="N" or confirm=="n":
            continue
        elif confirm!="Y" and confirm!="y":
            print("乱输就把你叉出去.")
            time.sleep(3)
            os._exit(0)
        break
    return

def restore():
    global insert_num,k_value,highest_order,eva_l,eva_h,point_size #全局变量
    insert_num=50        #插值数
    k_value=3     #cubic 3次样条插值
    highest_order=20    #多项式最高次数(可能的 ) 用于找到最好的多项式
    eva_l,eva_h=5,7     #估计的 化学计量点范围
    point_size=12
    return

def init_data():        #重置数据
    global x,y,dy_x,v1,x_new,y_new,mse,r2,max_err
    mse,r2,max_err=[],[],[]   #MSE,R2,MAX_ERROR
    x,y=[],[]       #原始数据
    dy_x=[]     #1阶微商
    v1=[]           #一阶微商对应的V3
    x_new,y_new=[],[]    #插值后的x,y

    return


def modi_argu():
    global insert_num,k_value,highest_order,eva_l,eva_h,point_size #全局变量
    print("\n")
    names=["insert_num","k","h_order","eva_l","eva_h","point_size"]        #高级设置变量名称
    while True:
        print("高级设置","-"*62,"\n插值次数:insert_num=%d\n插值阶数:k=%d\n寻找的多项式的最高次数:h_order=%d\n预估的化学计量点下限eva_l:%d,预估的化学计量点上限eva_h:%d"%(insert_num,k_value,highest_order,eva_l,eva_h))
        print("原始数据点大小:point_size=%d"%(point_size))
        print("-"*70,"\n说明:高级设置内的参数会对结果产生影响,所有参数为整数,k只能取奇数\n插值次数(不建议低于20,高于100)越高,曲线越平滑\n插值阶数** (只能取奇数) **越高:曲线曲率越大")
        print("寻找的多项式最高次数:拟合出的最高阶多项式阶数越高(仍旧是曲率增大)[不建议高于30会出现过拟合]")
        print("预估的化学计量点下限与上限:会影响两根切线的位置,如果出现2条以上的切线,则需缩小范围\n","-"*70)
        print("修改示例 k=1{ENTER} 将插值阶数改为1, 输入save{ENTER} 保存修改并退出(仅在本次运行程序有效)\nq{ENTER}恢复默认值并退出","\n","-"*70,"\n请修改")
        while True:
            argu=[]
            modi=""
            value=0
            modi=input("").strip()
            if modi=='save':#保存修改
                print("-"*70)
                print("插值次数:insert_num=%d\n插值阶数:k=%d\n寻找的多项式的最高次数:h_order=%d\n预估的化学计量点下限:%d,预估的化学计量点上限:%d"%(insert_num,k_value,highest_order,eva_l,eva_h))
                print("原始数据点大小:point_size=%d"%(point_size))
                print("已保存.")
                print("-"*70)
                return
            elif modi=="q": #放弃修改
                restore()   #恢复默认
                print("-"*70)
                print("插值次数:insert_num=%d\n插值阶数:k=%d\n寻找的多项式的最高次数:h_order=%d\n预估的化学计量点下限eva_l:%d,预估的化学计量点上限eva_h:%d"%(insert_num,k_value,highest_order,eva_l,eva_h))
                print("原始数据点大小:point_size=%d"%(point_size))
                print("已恢复默认参数.")
                print("-"*70)
                return
            argu=modi.split('=')
            #print(argu)
            if len(argu)>2:#超过2个参数
                print("输入错误,请检查")
                print("-"*70,"\n请修改")
                continue
            if argu[0] not in names:    #修改的变量错误/不存在
                print("高级设置中不存在参数:",argu[0])    
                print("-"*70,"\n请修改")
                continue
            else :   
                for i in argu[1]:
                    if ord(i)>57 or ord(i)<48:    #修改的值不是整数 
                        print("值错误,不可修改参数为小数,k只能为奇数.")
                        print("-"*70,"\n请修改")
                        continue
                    value=value*10+int(i)
            if value<=0:    #值小于0
                print("修改的值不能小于0\n","-"*69,"\n请修改")
                continue
            if argu[0]==names[0]:   #修改插值数
                insert_num=value
                print(argu[0],"修改为",value)
                continue
            elif argu[0]==names[1]:     #修改k_value
                if value%2!=0:
                    k_value=value
                    print(argu[0],"修改为",value)
                    continue
                else:
                    print("-"*70,"\nk只能为奇数\n请修改")
                    continue
            elif argu[0]==names[2]: #修改多项式最高次数(可能的 )
                highest_order=value
                print(argu[0],"修改为",value)
                continue
            elif argu[0]==names[3]:#修改eva_l
                eva_l=value
                print(argu[0],"修改为",value)
                continue
            elif argu[0]==names[4]:   #修改eva_h
                eva_h=value
                print(argu[0],"修改为",value)
                continue
            else:   #修改数据点大小
                point_size=value
                print(argu[0],"修改为:",value)
                continue
    return

def process_data(): #数据处理
    global x,y,dy_x,v1
    dy_x,v1=[],[]
    if len(x)!=len(y):
        print("输入的数据不匹配.")
        time.sleep(3)
        os._exit(0)
    for i in range(0,len(x)-1):
        dy_x.append((y[i+1]-y[i])/(x[i+1]-x[i]))  #计算V的一阶微商
        v1.append((x[i+1]+x[i])/2)      #对应的V


    print("数据:\n|V/mL       |pH         |对应的V/mL |▲V/▲pH     |")

    for i in range(0,len(x)-1):
        print("|%11lf|%11lf|           |           |"%(x[i],y[i]))
        print("|           |           |%11lf|%11lf|"%(v1[i],dy_x[i]))

    print("|%11lf|%11lf|           |           |"%(x[len(x)-1],y[len(y)-1]))
    os.system("pause")
    return




def choice():       #选择
   
    while True:
        choice_=0
        print("-"*70)
        print("1.手动输入数据\n2.从文件(excel表格)读取数据    <暂时没时间写>\n3.高级设置\n4.退出")
        print("-"*70)
        choice_=input("请输入序号以选择...(ENTER结束):")
        if choice_=='4':
            print("退出中...")
            time.sleep(2)
            os._exit(0) #退出
        elif choice_=='1':      #手动输入数据
            input_data()    #输入
            insert_value()  #插值
            find_best_poly()    #拟合
            process_data()      #数据处理
            run_pH_V()       #计算,画图pH_V
            run_dpH_dV()        #一阶微商图
            break 
        elif choice_=='3':      #高级设置
            modi_argu()
    return


def insert_value():     #插值
    global insert_num,k_value,y_new,x_new
    y_new,x_new=[],[]   #初始化
    x_size=len(x)
    y_size=len(y)
    #插值   
    for i in range(1,x_size):   #对x进行插值
        arr=np.linspace(x[i-1],x[i],insert_num)          #插值越多曲线越平滑
        for k in arr:
            x_new.append(k)
        
    x_new=set(x_new)
    x_new=list(x_new)   #过滤重复元素
    x_new.sort()
    #print(len(x_new))
    #os._exit(0)

    y_new=scipy.interpolate.make_interp_spline(x,y,k_value)(x_new)    #对y插值
    #print(y_new,len(y_new))
    return 

def find_best_poly():       #找到最好的多项式
    global highest_order,deg_max,x_new,y_new,Fx,y_fit
    for i in range(0,highest_order+1):   #最高次数

        y_fit,Fx=fit(x_new,y_new,i)
        mse.append(sklearn.metrics.mean_squared_error(y_new,y_fit))
        r2.append(sklearn.metrics.r2_score(y_new,y_fit))
        max_err.append(sklearn.metrics.max_error(y_new,y_fit))

    min_max_error,deg_max=min(max_err),max_err.index(min(max_err))
    print("max_error最小:",min_max_error,"  此时多项式最高次为:",deg_max)

    return

def run_dpH_dV()    :   #一阶微商画图
    global deg_max,x_new,y_new,x_new,dy_x,v1,insert_num,highest_order

    x_new,y_new=[],[]    #插值后的x,y

    mse,r2,max_err=[],[],[]   #MSE,R2,MAX_ERROR


    x_size=len(v1)
    y_size=len(dy_x)

    #插值   


    for i in range(1,x_size):   #对x进行插值
        arr=np.linspace(v1[i-1],v1[i],insert_num)          #插值越多曲线越平滑   会对结果产生影响  
        for k in arr:
            x_new.append(k)

        
    x_new=set(x_new)
    x_new=list(x_new)   #过滤重复元素
    x_new.sort()
    #print(len(x_new))
    #os._exit(0)

    y_new=scipy.interpolate.make_interp_spline(v1,dy_x,k_value)(x_new)    #对y插值  使曲线平滑  会对结果产生影响  k过高会由龙格现象
    #print(y_new,len(y_new))
    #os._exit(0)

    # 使用numpy.polyfit进行多项式拟合
    # 输出为多项式的系数，其中第0个元素是常数项

    for i in range(0,highest_order+1):   #i是最高次数

        y_fit,Fx=fit(x_new,y_new,i)
        mse.append(sklearn.metrics.mean_squared_error(y_new,y_fit))
        r2.append(sklearn.metrics.r2_score(y_new,y_fit))
        max_err.append(sklearn.metrics.max_error(y_new,y_fit))
    print("\n\n▲pH/▲V-V曲线数据:\n","-"*70)
    min_max_error,deg_max=min(max_err),max_err.index(min(max_err))
    print("max_error最小:",min_max_error,"  最高次为:",deg_max)
    #os._exit(0)

    y_fit,Fx=fit(x_new,y_new,deg_max)   #返回最好的多项式函数,并计算相应的y值

    print("-"*70)
    print("MSE(均方误差):",sklearn.metrics.mean_squared_error(y_new,y_fit))      #打印MSE 均方误差
    print("R2(回归决定系数):",sklearn.metrics.r2_score(y_new,y_fit))    #r**2
    print("MAX_ERROR(最大误差):",sklearn.metrics.max_error(y_new,y_fit))
    print("\n拟合的多项式函数:",Fx)
    print("-"*70)


    plt.xlabel("V")
    plt.ylabel("pH")
    plt.title('ΔpH/ΔV-V曲线')
    #plt.xticks([0.00,1.00,2.00,3.00,4.00,5.00,6.00,7.00,8.00,9.00,10.00],['0.00','1.00','2.00','3.00','4.00','5.00','6.00','7.00','8.00','9.00','10.00'])
    #plt.yticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],['0.00','1.00','2.00','3.00','4.00','5.00','6.00','7.00','8.00','9.00','10.00','11.00','12.00','13.00','14.00'])


    y_find=list(y_new)
    x_find=[x_new[y_find.index(max(y_find))]]*10
    y_find=list(np.linspace(min(y_find),max(y_find),10))

    #print(x_find,y_find)
    print("Ve=%.3lfmL"%x_find[0])
    print("-"*70)
    plt.plot(x_find,y_find,"-.",label="Ve=%.3lf"%x_find[0])
    paint(v1,dy_x,x_new,y_new)  #画图

    print("画图完成...")
    plt.clf()   #清空坐标轴
    plt.cla()   #清空图形内容
    init_data()
    os.system("pause")

    return

def run_pH_V():      #pH-V计算,画图
    global deg_max,x_new,y_new,x_new,eva_h,eva_l
    y_fit,Fx=fit(x_new,y_new,deg_max)   #返回最好的多项式函数,并计算相应的y值
    F1x=Fx.deriv()  #多项式一阶导数
    F1x_target=F1x-np.poly1d([1])
    root_complex=F1x_target.roots
    root,F1x_points,Fx_points=[],{},{}


    for i in root_complex:
        if i.imag==0.0 and eva_l<=i.real<=eva_h:
            root.append(float(i))
            F1x_points[float(i)]=float(F1x(float(i)))
            Fx_points[float(i)]=float(Fx(float(i)))


    #print("原来的多项式:",F1x,"\n\n新多项式:",F1x_target,"\n\n5~7内的实根:",root,"\n\n导函数点:",F1x_points,"\n原函数点:",Fx_points)


    print("\n\npH-V曲线\n","-"*70)
    print("MSE(均方误差):",sklearn.metrics.mean_squared_error(y_new,y_fit))      #打印MSE 均方误差
    print("R2(回归决定系数):",sklearn.metrics.r2_score(y_new,y_fit))    #r**2
    print("MAX_ERROR(最大误差):",sklearn.metrics.max_error(y_new,y_fit))
    print("-"*70)
    print("拟合的多项式函数:",Fx)
    print("-"*70)
    av_x,av_y=0,0,
    for k in Fx_points:
        paint_line(k,Fx_points[k],"斜率为1的切线","blue","-")
        av_x+=k
        av_y+=Fx_points[k]

    av_x/=len(Fx_points)
    av_y/=len(Fx_points)
    paint_line(av_x,av_y,"等分线","red","-.")
    print("NaOH V/mL:%lf    化学计量点:%lfpH"%(av_x,av_y))
    print("-"*70)
    plt.scatter(av_x,av_y,label="化学计量点",s=25,color="green")
    plt.xlabel("V")
    plt.ylabel("pH")
    plt.title('pH-V曲线')
    plt.xticks([0.00,1.00,2.00,3.00,4.00,5.00,6.00,7.00,8.00,9.00,10.00],['0.00','1.00','2.00','3.00','4.00','5.00','6.00','7.00','8.00','9.00','10.00'])
    plt.yticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],['0.00','1.00','2.00','3.00','4.00','5.00','6.00','7.00','8.00','9.00','10.00','11.00','12.00','13.00','14.00'])
    plt.annotate('NaOH V=%.3lfmL  pH=%.3lf'%(av_x,av_y),
            xy=(av_x, av_y), xycoords='data',
            xytext=(+9, -8), textcoords='offset points', fontsize=10,
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
    plt.plot([av_x]*10,list(np.linspace(y_new.min(),av_y,10)),"-.",label="Ve=%.3lf"%av_x)
    paint(x,y,x_new,y_new)  #画图

    plt.clf()   #清空坐标轴
    plt.cla()   #清空图形内容

    return 





if __name__=="__main__":        #程序入口
    os.system("chcp 65001")     #设置代码活动页为utf8编码
    while True:
        print_info()
        choice()




# 生成样本数据
#x=[0.00,1.00,2.00,3.00,4.00,5.00,5.10,5.20,5.30,5.40,5.50,5.60,5.70,5.80,5.90,6.00,7.00,8.00,9.00,10.00]
#y=[3.35,4.07,4.45,4.67,5.12,5.58,5.73,5.85,5.94,6.05,6.19,6.35,6.54,6.67,6.79,7.89,10.87,11.43,11.67,11.83]




