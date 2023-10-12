
import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy import stats
from sklearn.metrics import mean_squared_error  # 均方误差|
from sklearn.metrics import mean_absolute_error  # 平方绝对误差
from sklearn.metrics import r2_score  # R square
import pingouin as pg
import os
from sklearn.linear_model import LinearRegression
lr = LinearRegression()

dirs = os.listdir("C:/Users/Administrator/Desktop/OLC/%RM/pre_result/")
for all_files in dirs:
    # 读取原始数据
    file = "C:/Users/Administrator/Desktop/OLC/%RM/pre_result/" + all_files + ""
    OLC = pd.read_csv(file)
    # 读取原始数据

    # ———————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 绘制散点图以及线性回归
    plt.rcParams['font.sans-serif'] = 'Microsoft YaHei'  # 设置中文编码和负号的正常显示

    OLC['x'] = OLC['x'].fillna(0)
    OLC['y'] = OLC['y'].fillna(0)

    X = np.array(OLC['x']).reshape(-1, 1)
    Y = np.array(OLC['y']).reshape(-1, 1)
    lr.fit(X, Y)
    R = lr.score(X, Y)
    print(R)

    Y_pred = lr.predict(X)
    plt.scatter(X, Y, label='监测数据', marker='o', s=16)  # VBT数据和Opti数据的散点图
    plt.plot(X, Y_pred, 'r', lw=3, label='拟合线')
    # plt.plot([OLC['x'].min(), OLC['x'].max()],
    #          [OLC['y'].min(), OLC['y'].max()], 'r', lw=3, label='拟合线')
    plt.xlabel("VBT速度(m/s)")
    plt.ylabel("Opti速度(m/s)")
    plt.legend(loc='best')
    plt.show()
    # ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

    # 计算相关系数，默认是‘pearson’线性相关;'kendall','spearman'
    r = OLC.corr()
    print("线性相关系数r", "\n", r)
    # R = r*r
    # print(R)

    # ———————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 计算均方误差
    # 替换list中的nan
    nan = np.isnan(OLC)
    OLC[nan] = 0
    # MSE/RMSE/MAE/R2计算
    # standard error of the mean
    SEM_OPTI = scipy.stats.sem(OLC['y'], axis=0, ddof=0)
    SEM_VBT = scipy.stats.sem(OLC['x'], axis=0, ddof=0)
    MSE = mean_squared_error(OLC['y'], OLC['x'])
    RMSE = math.sqrt(MSE)
    MAE = mean_absolute_error(OLC['y'], OLC['x'])
    R2 = r2_score(OLC['y'], OLC['x'])
    print("OPTI估计的标准误差(SEM)", SEM_OPTI)
    print("VBT估计的标准误差(SEM)", SEM_VBT)
    print("均方误差(MSE)", MSE)
    print("均方根误差(RMSE)", RMSE)
    print("平均绝对误差(MAE)", MAE)
    print("决定系数(R^2)", R2)

    # ————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 计算ICC组内相关系数
    VBT_ICC = pd.DataFrame()
    Opti_ICC = pd.DataFrame()
    # # 生成VBT的list
    VBT_ICC["velocity"] = OLC['x']
    VBT_ICC.insert(0, "reader", "A")
    VBT_ICC.insert(0, "target", range(VBT_ICC.shape[0]))

    # 生成Opti的list
    Opti_ICC["velocity"] = OLC['y']
    Opti_ICC = Opti_ICC.replace(np.nan, 0)
    Opti_ICC.insert(0, "reader", "B")
    Opti_ICC.insert(0, "target", range(Opti_ICC.shape[0]))
    ICC_data = pd.concat([VBT_ICC, Opti_ICC])  # 将VBT和Opti两个速度列表合并成一个
    print(ICC_data)
    # ———————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # targets 为目标数据的分类（每条数据一类），raters为评判人的分类，ratings为实际数据。
    ICC = pg.intraclass_corr(data=ICC_data, targets="target", raters="reader", ratings="velocity")
    print(ICC)
    print(file)

    # ———————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 计算CMC相关系数
    CMC = pd.DataFrame()  # 新建CMC
    OLC["mean"] = (OLC["x"] + OLC["y"]) / 2
    velocity_mean = np.mean(OLC["mean"])  # 两设备总的平均值
    CMC["Opti"] = OLC['y']
    CMC["VBT"] = OLC['x']
    CMC["f_mean"] = (OLC["x"] + OLC["y"]) / 2  # 当前帧数下的平均值
    CMC["diff1"] = (CMC["VBT"] - CMC["f_mean"]) ** 2
    diff_sum1 = np.sum(CMC["diff1"])  # 分子
    CMC["diff2"] = (CMC["VBT"] - velocity_mean) ** 2
    diff_sum2 = np.sum(CMC["diff2"])  # 分母
    F = len(CMC["Opti"])  # 总帧数
    # 带入计算公式
    CMC_val = math.sqrt(1 - ((diff_sum1 / F) / (diff_sum2 / (2 * F - 1))))

    print(CMC_val)
    # ———————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 将两设备对其后的数据以及相关性指标结果保存为csv文件
    OLC["Pearson"] = format(r["y"][0], '3f')
    OLC["MSE"] = format(MSE, '3f')
    OLC["RMSE"] = format(RMSE, '3f')
    OLC["MAE"] = format(MAE, '3f')
    OLC["R2"] = format(R2, '3f')
    OLC["ICC"] = format(ICC["ICC"][3], '3f')
    OLC["CMC"] = format(CMC_val, '3f')
    OLC["SEM_OPTI"] = format(SEM_OPTI, '3f')
    OLC["SEM_VBT"] = format(SEM_VBT, '3f')
    # 保存成csv文件
    OLC.to_csv("C:\\Users\\Administrator\\Desktop\\OLC\\%RM\\pre_result\\result\\"+all_files+"", index=False)
    # data = pd.read_csv('C:/Users/Administrator/Desktop/动捕和vbt曲线/ICC/ICC_Data.csv')






