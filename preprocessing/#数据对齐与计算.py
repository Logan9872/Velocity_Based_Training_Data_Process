# 动捕数据和vbt数据的对比和图像绘制，使用12.22日预实验数据
# 于3.14日更新批处理计算21人数据
import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy import stats
from scipy import signal
from sklearn.metrics import mean_squared_error  # 均方误差|
from sklearn.metrics import mean_absolute_error  # 平方绝对误差
from sklearn.metrics import r2_score  # R square
import pingouin as pg
import os
from sklearn.linear_model import LinearRegression
lr = LinearRegression()

dirs = os.listdir("C:/Users/Administrator/Desktop/DataPreprocess/OPTI_data")
for all_files in dirs:
    # 读取原始数据
    file = "C:/Users/Administrator/Desktop/DataPreprocess/OPTI_data/" + all_files + ""
    file_vbt = "C:/Users/Administrator/Desktop/DataPreprocess/VBT_data/" + all_files + ""
    # 读取Opti的原始数据
    opti_track_data = pd.read_csv(file, skiprows=6, usecols=[2, 3, 4], encoding="unicode_escape")
    opti_track_time = pd.read_csv(file, skiprows=6, usecols=[1], encoding="unicode_escape")

    # 低通巴特沃斯滤波
    # 4 阶数 0.12=2*（截止频率6HZ/采样频率100HZ）
    b, a = signal.butter(4, 0.125, 'lowpass')
    opti_track_data['X'] = signal.filtfilt(b, a, opti_track_data['X'])
    opti_track_data['Y'] = signal.filtfilt(b, a, opti_track_data['Y'])
    opti_track_data['Z'] = signal.filtfilt(b, a, opti_track_data['Z'])

    # 求两点间的差值
    distance = opti_track_data.diff(axis=0, periods=1)
    # 计算速度的方向
    distance['direction'] = distance.apply(lambda x: 1 if x['Y'] > 0 else -1, axis=1)
    # 计算两点间的距离
    distance['velocity'] = distance.apply(lambda x: math.sqrt(x['X']**2 + x['Y']**2 + x['Z']**2)*100*x['direction'], axis=1)
    # ————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 绘图
    plt.plot(opti_track_time, distance['velocity'], linewidth=0.4)
    # plt.xlim((4, 8))
    plt.xlabel("time(s)")
    plt.ylabel("velocity(m/s)")
    plt.show()

    # ————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 读取VBT的原始数据
    VBT_data = pd.read_csv(file_vbt, skiprows=2, usecols=[2, 3], header=None, names=['position', 'velocity'], encoding="unicode_escape")
    VBT_data_time = pd.read_csv(file_vbt, skiprows=2, usecols=[0], header=None, names=['time'], encoding="unicode_escape")

    # 初始时间
    origin_time = VBT_data_time['time'].loc[0]
    # vbt的时间
    VBT_data['time'] = VBT_data_time.apply(lambda x: (x['time']-origin_time)/1000, axis=1)
    # vbt的速度
    VBT_data['velocity'] = VBT_data.apply(lambda x: (x['velocity']*0.00767), axis=1)
    # ————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 绘图
    plt.plot(VBT_data['time'], VBT_data['velocity'], linewidth=0.4)
    plt.xlabel("time(s)")
    plt.ylabel("velocity(m/s)")
    plt.show()
    # —————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # Opti Track设备和VBT设备滤波

    # —————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 绘制两条曲线重叠图(未截取)
    VBT_data['timeD'] = VBT_data.apply(lambda x: x['time'], axis=1)
    plt.plot(VBT_data['timeD'], VBT_data['velocity'], linewidth=0.4, color='blue', label='VBT')
    plt.plot(opti_track_time, distance['velocity'], linewidth=0.4, color='red', label='Opti Track')
    plt.xlabel("time(s)")
    plt.ylabel("velocity(m/s)")
    plt.legend(loc="best", fontsize=8)
    # plt.show()

    # ———————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 计算两条曲线的的相关函数，找到相关性最大的计算时间差

    # 反转VBT数据
    VBT_data_reverse = VBT_data['velocity'][::-1]
    Opti_data = distance['velocity']

    # 将df中的值类型转换成number
    VBT_data_reverse = VBT_data_reverse.apply(pd.to_numeric, errors='raise')
    Opti_data = Opti_data.apply(pd.to_numeric, errors='raise')

    # 转换成数组
    VBT_array = np.array(VBT_data_reverse)
    Opti_array = np.array(Opti_data)
    print("======================")
    # print(np.argwhere(np.isnan(VBT_array)))
    # print(np.argwhere(np.isnan(Opti_array)))
    Opti_array = np.nan_to_num(Opti_array)

    # 计算卷积
    Convo = np.convolve(VBT_array, Opti_array)

    # 验证卷积后的数长度是否等于原数组长度相加-1
    # Conve = VBT_array + Opti_array - 1
    print("卷积后的长度", len(Convo))
    print("VBT的长度", len(VBT_array))
    print("动捕的长度", len(Opti_array))

    # nan全部替换成0
    # Convo = np.nan_to_num(Convo)
    Convo_max = max(Convo)
    Convo_array = Convo.tolist()
    # 找到两条函数相关性最大的index,两条曲线时间轴对齐的为(i-m+1)
    Convo_index = Convo_array.index(max(Convo_array))

    # 平移的时间(T = Convo - VBT + 1)
    Trans_index = (Convo_index*1 - len(VBT_array)*1 + 1)
    Trans_time = Trans_index*0.01
    print('平移的时间', Trans_time)
    # ———————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 绘制计算卷积后的两条曲线的相关性曲线，峰值点即相关性最大点
    plt.plot(Convo, linewidth=0.4, color='red', label='Relativity')
    plt.ylabel("Relativity")
    plt.legend(loc="best", fontsize=8)
    plt.show()

    # ———————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 再次绘制平移时间轴的两条曲线
    VBT_data['timeD'] = VBT_data.apply(lambda x: x['time']+Trans_time, axis=1)
    plt.plot(opti_track_time, distance['velocity'], linewidth=0.4, color='red', label='Opti Track')
    plt.plot(VBT_data['timeD'], VBT_data['velocity'], linewidth=0.4, color='blue', label='VBT')

    plt.legend(loc="best", fontsize=8)

    plt.show()

    # ————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 求两个函数的决定系数R^2
    velocity_data = pd.DataFrame()  # 新建一个速度对比的df

    # 截取VBT和Opti数据的两端，使得两条曲线对齐
    # Opti和VBT数据截取的index
    Opti_Trans_index = Trans_index if Trans_index >= 0 else 0
    VBT_Trans_index = 0 if Trans_index >= 0 else -Trans_index
    # Opti和VBT数据截取的长度，取两曲线的交集
    Opti_len = len(VBT_data['velocity'])if Trans_index >= 0 else len(distance['velocity'])
    VBT_len = len(distance['velocity']) if Trans_index >= 0 else len(VBT_data['velocity'])

    # 重排截取后Opti数据的index，使其从0开始
    Opti_slice_data = distance['velocity'].iloc[Opti_Trans_index:len(distance['velocity'])]
    Opti_slice_data.reset_index(drop=True, inplace=True)
    velocity_data['Opti'] = Opti_slice_data.iloc[0:Opti_len]

    # 重排截取后VBT数据的index，使其从0开始
    VBT_slice_data = VBT_data['velocity'].iloc[VBT_Trans_index:len(VBT_data['velocity'])]
    VBT_slice_data.reset_index(drop=True, inplace=True)
    velocity_data['VBT'] = VBT_slice_data[0:VBT_len]

    # 绘制截取对齐后的数据
    plt.plot(velocity_data['VBT'], linewidth=0.4, color='blue', label='VBT')
    plt.plot(velocity_data['Opti'], linewidth=0.4, color='red', label='Opti Track')
    plt.legend(loc="best", fontsize=8)
    # 中文设置
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.xlabel("时间(10ms)")
    plt.ylabel("速度(m/s)")
    plt.title(all_files, loc='left', color='b')
    plt.title("设备数据对照图")
    filename = "C:/Users/Administrator/Desktop/动捕和vbt曲线/" + all_files + ".png"
    plt.savefig(filename)
    plt.show()
    # ———————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 绘制散点图以及线性回归
    plt.rcParams['font.sans-serif'] = 'Microsoft YaHei'  # 设置中文编码和负号的正常显示

    OLC = pd.DataFrame()
    OLC['x'] = velocity_data['VBT'].fillna(0)
    OLC['y'] = velocity_data['Opti'].fillna(0)
    X = np.array(OLC['x']).reshape(-1, 1)
    Y = np.array(OLC['y']).reshape(-1, 1)
   
    lr.fit(X, Y)
    R = lr.score(X, Y)
    print("w值为:", lr.coef_)
    print("b截距值为:", lr.intercept_)
    print(R)

    Y_pred = lr.predict(X)
    plt.scatter(X, Y, label='监测数据', marker='o', s=16)  # VBT数据和Opti数据的散点图
    plt.plot(X, Y_pred, 'r', lw=3, label='拟合线')
    # plt.plot([velocity_data['VBT'].min(), velocity_data['VBT'].max()],
    #          [velocity_data['Opti'].min(), velocity_data['Opti'].max()], 'r', lw=3, label='拟合线')
    plt.xlabel("VBT速度(m/s)")
    plt.ylabel("Opti速度(m/s)")
    plt.legend(loc='best')
    plt.show()
    # ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

    # 计算相关系数，默认是‘pearson’线性相关;'kendall','spearman'
    r = velocity_data.corr()
    print("线性相关系数r", "\n", r)
    # R = r*r
    # print(R)

    # ———————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 计算均方误差
    # 替换list中的nan
    nan = np.isnan(velocity_data)
    velocity_data[nan] = 0
    # MSE/RMSE/MAE/R2计算
    # standard error of the mean
    SEM_OPTI = scipy.stats.sem(velocity_data['Opti'], axis=0, ddof=0)
    SEM_VBT = scipy.stats.sem(velocity_data['VBT'], axis=0, ddof=0)
    MSE = mean_squared_error(velocity_data['Opti'], velocity_data['VBT'])
    RMSE = math.sqrt(MSE)
    MAE = mean_absolute_error(velocity_data['Opti'], velocity_data['VBT'])
    R2 = r2_score(velocity_data['Opti'], velocity_data['VBT'])
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
    VBT_ICC["velocity"] = velocity_data['VBT']
    VBT_ICC.insert(0, "reader", "A")
    VBT_ICC.insert(0, "target", range(VBT_ICC.shape[0]))

    # 生成Opti的list
    Opti_ICC["velocity"] = velocity_data['Opti']
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
    velocity_data["mean"] = (velocity_data["VBT"] + velocity_data["Opti"]) / 2
    velocity_mean = np.mean(velocity_data["mean"])  # 两设备总的平均值
    CMC["Opti"] = velocity_data['Opti']
    CMC["VBT"] = velocity_data['VBT']
    CMC["f_mean"] = (velocity_data["VBT"] + velocity_data["Opti"]) / 2  # 当前帧数下的平均值
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
    velocity_data["Pearson"] = r["VBT"][0]
    velocity_data["MSE"] = MSE
    velocity_data["RMSE"] = RMSE
    velocity_data["MAE"] = MAE
    velocity_data["R2"] = R2
    velocity_data["ICC"] = ICC["ICC"][3]
    velocity_data["CMC"] = CMC_val
    velocity_data["SEM_OPTI"] = SEM_OPTI
    velocity_data["SEM_VBT"] = SEM_VBT

    # 保存成csv文件

    velocity_data.to_csv("C:\\Users\\Administrator\\Desktop\\datapreprocess\\pre_result\\"+all_files+"", index=False)
    # data = pd.read_csv('C:/Users/Administrator/Desktop/动捕和vbt曲线/ICC/ICC_Data.csv')




