# 从%RM架中读取合并好的30%RM-90%RM和all的csv,计算指标，并用于回归图的绘制

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
# 读取分好的深蹲动作的数据，分别求出VBT和Opti的均值，并将这个均值放入表中

dirs = os.listdir("C:/Users/Administrator/Desktop/%rm/ALL")
for all_files in dirs:
    # 读取原始数据
    file = "C:/Users/Administrator/Desktop/%rm/ALL/" + all_files + ""
    data = pd.read_csv(file, encoding="unicode_escape")
    waveform = pd.DataFrame()
    print(data)
    waveform['VBT'] = data['VBT']
    waveform['OPTI'] = data['OPTI']
    file_vbt = data['VBT']
    file_opti = data['OPTI']
    X = np.array(file_vbt).reshape(-1, 1)
    Y = np.array(file_opti).reshape(-1, 1)
    # ————————————————————————————————————————
    # R
    lr.fit(X, Y)
    R = lr.score(X, Y)
    print("w值为:", lr.coef_)
    print("b截距值为:", lr.intercept_)
    # waveform['R'] = R
    # print(R)
    # ——————————————————————————————————————
    Y_pred = lr.predict(X)
    plt.scatter(X, Y, label='Data', marker='o', s=16)  # VBT数据和Opti数据的散点图
    plt.plot(X, Y_pred, 'r', lw=1, label='OLC')
    plt.xlabel("VBT(m/s)")
    plt.ylabel("Opti(m/s)")
    plt.legend(loc='best')
    plt.show()
    # plt.rcParams['font.sans-serif'] = 'Microsoft YaHei'  # 设置中文编码和负号的正常显示
    # ————————————————————————————————————————
    # ICC
    VBT_ICC = pd.DataFrame()
    Opti_ICC = pd.DataFrame()
    VBT_ICC["velocity"] = file_vbt
    VBT_ICC.insert(0, "reader", "A")
    VBT_ICC.insert(0, "target", range(VBT_ICC.shape[0]))

    Opti_ICC["velocity"] = file_opti
    Opti_ICC = Opti_ICC.replace(np.nan, 0)
    Opti_ICC.insert(0, "reader", "B")
    Opti_ICC.insert(0, "target", range(Opti_ICC.shape[0]))
    ICC_data = pd.concat([VBT_ICC, Opti_ICC])
    ICC = pg.intraclass_corr(data=ICC_data, targets="target", raters="reader", ratings="velocity")
    waveform['ICC'] = ICC["ICC"][3]
    # ————————————————————————————————————————
    # RMSE
    MSE = mean_squared_error(Y, X)
    RMSE = math.sqrt(MSE)
    waveform['RMSE'] = RMSE

    print("ICC", ICC)
    print("RMSE", RMSE)
    # ————————————————————————————————————————
    velocity_data = pd.DataFrame()
    velocity_data['VBT'] = data['VBT']
    velocity_data['OPTI'] = data['OPTI']
    r = velocity_data.corr()
    waveform['Person'] = r["VBT"][1]
    print("person",r)
    # ———————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 计算CMC相关系数
    CMC = pd.DataFrame()  # 新建CMC
    waveform["mean"] = (waveform["VBT"] + waveform["OPTI"]) / 2
    velocity_mean = np.mean(waveform["mean"])  # 两设备总的平均值
    CMC["OPTI"] = waveform['OPTI']
    CMC["VBT"] = waveform['VBT']
    CMC["f_mean"] = (waveform["VBT"] + waveform["OPTI"]) / 2  # 当前帧数下的平均值
    CMC["diff1"] = (CMC["VBT"] - CMC["f_mean"]) ** 2
    diff_sum1 = np.sum(CMC["diff1"])  # 分子
    CMC["diff2"] = (CMC["VBT"] - velocity_mean) ** 2
    diff_sum2 = np.sum(CMC["diff2"])  # 分母
    F = len(CMC["OPTI"])  # 总帧数
    # 带入计算公式
    CMC_val = math.sqrt(1 - ((diff_sum1 / F) / (diff_sum2 / (2 * F - 1))))

    waveform['CMC'] = CMC_val

    waveform.to_csv("C:\\Users\\Administrator\\Desktop\\squat_reps\\"+all_files+"", index=False)