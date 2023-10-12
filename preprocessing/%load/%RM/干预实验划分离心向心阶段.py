import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import heapq

dirs = os.listdir("C:/Users/Administrator/Desktop/meanV/A/")
for all_files in dirs:
    # 读取原始数据
    file = "C:/Users/Administrator/Desktop/meanV/A/" + all_files + ""
    OLC1 = pd.read_csv(file)
    # OLC2 = pd.read_csv(file)
    OLC1[OLC1 <= 0.05] = 0  # 向心补零
    # OLC2[OLC2 >= -0.05] = 0  # 离心补零

    OLC1 = OLC1[OLC1 >= 0.05]  # 向心
    # OLC2 = OLC2[OLC2 <= -0.05]  # 离心
    plt.figure(1)
    plt.plot(OLC1['y'], linewidth=0.4, color='blue', label='OPTI')
    plt.plot(OLC1['x'], linewidth=0.4, color='red', label='VBT')
    # plt.figure(2)
    # plt.plot(OLC2['y'], linewidth=0.4, color='blue', label='OPTI')
    # plt.plot(OLC2['x'], linewidth=0.4, color='red', label='VBT')
    plt.show()


    # print(OLC)

    OLC1.to_csv("C:\\Users\\Administrator\\Desktop\\meanV\\centric\\" + all_files + "", index=False)
    # OLC2.to_csv("C:\\Users\\Administrator\\Desktop\\OLC\\%rm\\75%B\\" + all_files + "", index=False)
