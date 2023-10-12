# 12.31将所有干预实验的数据遍历并绘制折线图，寻找多余信号并删除

import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
lr = LinearRegression()
import seaborn as sns

dirs = os.listdir("C:/Users/Administrator/Desktop/10%VelocityData除信号/PostTest/")
for all_files in dirs:
    # 读取原始数据
    file = "C:/Users/Administrator/Desktop/10%VelocityData除信号/PostTest/" + all_files + ""
    title = all_files[:38]  # 读取文件名
    # 读取速度和位置上数据
    VBT_data = pd.read_csv(file, skiprows=2, usecols=[2, 3], header=None, names=['Position', 'Velocity'],
                           encoding="unicode_escape")
    # 读取时间数据
    VBT_data_time = pd.read_csv(file, skiprows=2, usecols=[0], header=None, names=['Time'],
                                encoding="unicode_escape")

    origin_time = VBT_data_time['Time'].loc[0]
    VBT_data['Time'] = VBT_data_time.apply(lambda x: (x['Time'] - origin_time) / 1000, axis=1)
    VBT_data['Velocity'] = VBT_data.apply(lambda x: (x['Velocity'] * 0.00767), axis=1)
    VBT_data['Position'] = VBT_data.apply(lambda x: (x['Position'] * 0.0000767), axis=1)
    plt.title(title, fontsize=18)
    # ______________________________________________________
    # plt.plot(VBT_data['Time'], VBT_data['Velocity'], linewidth=4)
    # plt.xlabel("Time(s)")
    # plt.ylabel("Velocity(m/s)")
    # ______________________________________________________
    plt.plot(VBT_data['Time'], VBT_data['Position'], linewidth=4)
    plt.xlabel("Time(s)")
    plt.ylabel("Position(m)")
    # ______________________________________________________

    title_png = title[:-4]
    filename = "C:/Users/Administrator/Desktop/测试数据绘制/后测/" + title_png + ".png"
    # filename = "C:/Users/Administrator/Desktop/测试数据绘制/后测/速度/" + title_png + ".png"
    plt.savefig(filename)
    print(title)
    plt.show()

