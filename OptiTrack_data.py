# 动捕数据和vbt数据的对比和图像绘制，使用12.22日预实验数据
import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error  # 均方误差|
from sklearn.metrics import mean_absolute_error  # 平方绝对误差
from sklearn.metrics import r2_score  # R square
import pingouin as pg

# 读取原始数据
file = 'C:/Users/Administrator/Desktop/optical_track/1222bvt_011.csv'
file_vbt = "C:/Users/Administrator/Desktop/动捕预实验/vbt设备数据/12.22vbt原始数据/011.csv"
# 读取Opti的原始数据
opti_track_data = pd.read_csv(file, skiprows=6, usecols=[2, 3, 4], encoding="unicode_escape")
opti_track_time = pd.read_csv(file, skiprows=6, usecols=[1], encoding="unicode_escape")
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
# # 绘制两条曲线重叠图(未截取)
# VBT_data['timeD'] = VBT_data.apply(lambda x: x['time'], axis=1)
# plt.plot(opti_track_time, distance['velocity'], linewidth=0.4, color='red', label='Opti Track')
# plt.plot(VBT_data['timeD'], VBT_data['velocity'], linewidth=0.4, color='blue', label='VBT')
# plt.xlabel("time(s)")
# plt.ylabel("velocity(m/s)")
# plt.legend(loc="best", fontsize=8)
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

# 计算卷积
Convo = np.convolve(VBT_array, Opti_array)

# 验证卷积后的数长度是否等于原数组长度相加-1
# Conve = VBT_array + Opti_array - 1
print(len(Convo))
print(len(VBT_array))
print(len(Opti_array))

# nan全部替换成0
Convo = np.nan_to_num(Convo)
Convo_max = max(Convo)
Convo_array = Convo.tolist()
# 找到两条函数相关性最大的index,两条曲线时间轴对齐的为(i-m+1)
Convo_index = Convo_array.index(max(Convo_array))

# 平移的时间(T = Convo - VBT + 1)
Trans_index = (Convo_index*1 - len(VBT_array)*1 + 1)
Trans_time = Trans_index*0.01
print(Trans_time)

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————
# 绘制计算卷积后的两条曲线的相关性曲线，峰值点即相关性最大点
plt.plot(Convo, linewidth=0.4, color='red', label='Relativity')
plt.ylabel("Relativity")
plt.legend(loc="best", fontsize=8)
plt.show()

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————
# 再次绘制 平移时间轴的两条曲线
VBT_data['timeD'] = VBT_data.apply(lambda x: x['time']+Trans_time, axis=1)
plt.plot(opti_track_time, distance['velocity'], linewidth=0.4, color='red', label='Opti Track')
plt.plot(VBT_data['timeD'], VBT_data['velocity'], linewidth=0.4, color='blue', label='VBT')
plt.xlabel("time(s)")
plt.ylabel("velocity(m/s)")
plt.legend(loc="best", fontsize=8)
# plt.savefig('C:/Users/Administrator/Desktop/动捕和vbt曲线/.png')
plt.show()

# ————————————————————————————————————————————————————————————————————————————————————————————————————————————————
# 求两个函数的决定系数R^2
velocity_data = pd.DataFrame()  # 新建一个速度对比的df

# 截取动捕的数据[i:len]段，再截取和VBT设备一样的长度
Opti_slice_data = distance['velocity'].iloc[Trans_index:len(distance['velocity'])]
# 重排截取后数据的index
Opti_slice_data.reset_index(drop=True, inplace=True)
# 将两组数据形成新的df，计算其P相关系数
velocity_data['Opti'] = Opti_slice_data.iloc[0:len(VBT_data['velocity'])]
velocity_data['VBT'] = VBT_data['velocity']
plt.plot(velocity_data['VBT'], linewidth=0.4, color='blue', label='VBT')
plt.plot(velocity_data['Opti'], linewidth=0.4, color='red', label='Opti Track')
plt.show()
# 计算相关系数，默认是‘pearson’线性相关;'kendall','spearman'
r = velocity_data.corr()
R = r*r
print("线性相关系数r", "\n", r)
# print(R)

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————
# 计算均方误差
MSE = mean_squared_error(velocity_data['Opti'], velocity_data['VBT'])
RMSE = math.sqrt(MSE)
MAE = mean_absolute_error(velocity_data['Opti'], velocity_data['VBT'])
R2 = r2_score(velocity_data['Opti'], velocity_data['VBT'])
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
# print(ICC_data)
# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————————
ICC_data.to_csv('C:\\Users\\Administrator\\Desktop\\动捕和vbt曲线\\ICC\\ICC_Data.csv', index=False)
# data = pd.read_csv('C:/Users/Administrator/Desktop/动捕和vbt曲线/ICC/ICC_Data.csv')

# targets 为目标数据的分类（每条数据一类），raters为评判人的分类，ratings为实际数据。
ICC = pg.intraclass_corr(data=ICC_data, targets="target", raters="reader", ratings="velocity")
print(ICC)

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————————
# # 计算CV变异系数(因为数据中存在大量负值,且均值为负的接近0的值，故不用变异系数)
# # 计算VBT的CV
# VBT_mean = np.mean(VBT_ICC["velocity"])  # 计算平均值
# VBT_std = np.std(VBT_ICC["velocity"], ddof=0)  # 计算标准差
# VBT_CV = VBT_std / VBT_mean
# # 计算Opti的CV
# Opti_mean = np.mean(Opti_ICC["velocity"])
# Opti_std = np.std(Opti_ICC["velocity"], ddof=0)  # 计算标准差
# Opti_CV = Opti_std/Opti_mean
# print(VBT_CV)
# print(Opti_CV)
# print(VBT_std)
# print(Opti_std)
# ————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

