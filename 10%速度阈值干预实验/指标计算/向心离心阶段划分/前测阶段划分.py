# 1.08 以固定速度阈值划分向心离心的


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import heapq

dirs = os.listdir("C:/Users/Administrator/Desktop/10%VelocityData除信号/PreTest/")
for all_files in dirs:
    # 读取原始数据
    file = "C:/Users/Administrator/Desktop/10%VelocityData除信号/PreTest/" + all_files + ""
    #
    title = all_files[:38]  # 读取文件名
    title_png = title[:-4]
    filename = "C:/Users/Administrator/Desktop/测试数据绘制/前测/向心离心/" + title_png + ".png"
    # filename2 = "C:/Users/Administrator/Desktop/测试数据绘制/前测/离心/" + title_png + ".png"
    # 
    # 读取速度和位置上数据
    VBT_data = pd.read_csv(file, skiprows=2, usecols=[2, 3], header=None, names=['Position', 'Velocity'],encoding="unicode_escape")
    # 读取时间数据
    VBT_data_time = pd.read_csv(file, skiprows=2, usecols=[0], header=None, names=['Time'],encoding="unicode_escape")
    origin_time = VBT_data_time['Time'].loc[0]
    VBT_data['Time'] = VBT_data_time.apply(lambda x: (x['Time'] - origin_time) / 1000, axis=1)
    VBT_data['Velocity'] = VBT_data.apply(lambda x: (x['Velocity'] * 0.00767), axis=1)
    VBT_data['Position'] = VBT_data.apply(lambda x: (x['Position'] * 0.0000767), axis=1)
    #
    OLC1 = pd.DataFrame()
    OLC2 = pd.DataFrame()
    OLC1['Velocity'] = VBT_data['Velocity']
    OLC2['Velocity'] = VBT_data['Velocity']
    # OLC1['Time'] = VBT_data['Time']
    # OLC2['Time'] = VBT_data['Time']
    OLC2['Velocity'] = VBT_data['Velocity']
    OLC1["Velocity"][OLC1["Velocity"] <= 0.05] = 0  # 向心补零
    OLC2["Velocity"][OLC2["Velocity"] >= -0.05] = 0  # 离心补零
    # OLC2[OLC2 >= -0.05] = 0  # 离心补零

    OLC1["Velocity"] = OLC1["Velocity"][OLC1["Velocity"] > 0.05]  # 向心
    OLC2["Velocity"] = OLC2["Velocity"][OLC2["Velocity"] < -0.05]  # 离心
    # OLC2 = OLC2[OLC2 <= -0.05]  # 离心

    plt.figure(1)
    # plt.plot(OLC1['y'], linewidth=0.4, color='blue', label='OPTI')
    plt.plot(OLC1['Velocity'], linewidth=4, color='red', label='VBT')
    # plt.plot(OLC2['y'], linewidth=0.4, color='blue', label='OPTI')
    plt.plot(OLC2['Velocity'], linewidth=4, color='blue', label='VBT')
    plt.xlabel("Time(10ms)")
    plt.ylabel("Velocity(m/s)")
    plt.savefig(filename)
    plt.show()

    # plt.savefig(filename2)

    print(title)

    OLC1.to_csv("C:\\Users\\Administrator\\Desktop\\10%VelocityData除信号\\C&E\\PreTestConcentric\\" + all_files + "", index=False)
    OLC2.to_csv("C:\\Users\\Administrator\\Desktop\\10%VelocityData除信号\\C&E\\PreTestEccentric\\" + all_files + "", index=False)

