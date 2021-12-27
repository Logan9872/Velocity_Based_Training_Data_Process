# 动捕数据和vbt数据的对比和图像绘制，使用12.22日预实验数据
import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np

# 读取原始数据
file = 'C:/Users/Administrator/Desktop/optical_track/1222bvt_002.csv'
file_vbt = "C:/Users/Administrator/Desktop/动捕预实验/vbt设备数据/12.22vbt原始数据/002.csv"

opti_track_data = pd.read_csv(file, skiprows=6, usecols=[2, 3, 4], encoding="unicode_escape")
opti_track_time = pd.read_csv(file, skiprows=6, usecols=[1], encoding="unicode_escape")
# 求两点间的差值
distance = opti_track_data.diff(axis=0, periods=1)
# 计算速度的方向
distance['direction'] = distance.apply(lambda x: 1 if x['Y'] > 0 else -1, axis=1)
# 计算两点间的距离
distance['velocity'] = distance.apply(lambda x: math.sqrt(x['X']**2 + x['Y']**2 + x['Z']**2)*100*x['direction'], axis=1)

# 绘图
plt.plot(opti_track_time, distance['velocity'], linewidth=0.4)
plt.xlim((4, 8))
plt.xlabel("time(s)")
plt.ylabel("velocity(m/s)")
plt.show()

# ————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
VBT_data = pd.read_csv(file_vbt, skiprows=2, usecols=[2, 3], header=None, names=['position', 'velocity'], encoding="unicode_escape")
VBT_data_time = pd.read_csv(file_vbt, skiprows=2, usecols=[0], header=None, names=['time'], encoding="unicode_escape")

# 初始时间
origin_time = VBT_data_time['time'].loc[0]
# vbt的时间
VBT_data['time'] = VBT_data_time.apply(lambda x: (x['time']-origin_time)/1000, axis=1)
# vbt的速度
VBT_data['velocity'] = VBT_data.apply(lambda x: (x['velocity']*0.00767), axis=1)
# 图表绘制
plt.plot(VBT_data['time'], VBT_data['velocity'], linewidth=0.4)
plt.xlabel("time(s)")
plt.ylabel("velocity(m/s)")
plt.show()
# —————————————————————————————————————————————————————————————————————————————————————————————————————————————
# Opti Track设备和VBT设备滤波

# —————————————————————————————————————————————————————————————————————————————————————————————————————————————
# 绘制两条曲线重叠图
VBT_data['timeD'] = VBT_data.apply(lambda x: x['time'], axis=1)
plt.plot(opti_track_time, distance['velocity'], linewidth=0.4, color='red', label='Opti Track')
plt.plot(VBT_data['timeD'], VBT_data['velocity'], linewidth=0.4, color='blue', label='VBT')
plt.xlabel("time(s)")
plt.ylabel("velocity(m/s)")
plt.legend(loc="best", fontsize=8)
plt.show()

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

# 平移的时间
Trans_time = (Convo_index*1 - len(Opti_array)*1 + 1)*0.01
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
plt.show()



