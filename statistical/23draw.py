import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
import os
from sklearn.linear_model import LinearRegression
lr = LinearRegression()
import seaborn as sns

# 图表图例 / XY轴的范围 /

# 用于绘制所有动作的数据回归曲线图，并在此调整配色
# 读取原始数据
file = "C:/Users/Administrator/Desktop/redraw/23-004.csv"
data = pd.read_csv(file, encoding="unicode_escape")
# 绘图

# 绘制异常点图
plt.plot(data['INDEX']/100, data['Opti'], "#fa4343", alpha=0.7, lw=2, label='OptiTrack System') #59A95A
plt.plot(data['INDEX']/100, data['VBT'], "#0780cf", alpha=0.7, lw=2, label='Proposed System')
plt.legend(loc=4)

# 去除多余空白
ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
plt.xlim(0, 10)  # 设置x轴的数值显示范围
plt.ylim(-1, 1.25)  # 设置y轴的数值显示范围
ax = plt.gca()   # 相对位置设定

plt.title("Abnormal Data", fontsize=18)
sns.despine()  # 去边框
sns.set_context("paper", font_scale=1.5)
sns.set_style('ticks')   # 设置风格
plt.ylabel("Instantaneous Velocity [m/s]", fontsize=13)
plt.xlabel("Time [s]", fontsize=13)
plt.savefig("C:/Users/Administrator/Desktop/squat_reps/全波形结果图/Abnormal Data.png")
plt.show()


