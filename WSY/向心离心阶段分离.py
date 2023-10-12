import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import heapq

dirs = os.listdir("C:/Users/Administrator/Desktop/WSY_data/origin")
for all_files in dirs:
    # 读取原始数据
    file = "C:/Users/Administrator/Desktop/WSY_data/origin/" + all_files + ""
    OLC1 = pd.read_csv(file)
    OLC2 = pd.read_csv(file)
    OLC1["VBT"][OLC1["VBT"] <= 0.05] = 0  # 向心补零
    OLC2["VBT"][OLC2["VBT"] >= -0.05] = 0  # 向心补零
    OLC2[OLC2 >= -0.05] = 0  # 离心补零

    OLC1["VBT"] = OLC1["VBT"][OLC1["VBT"] >= 0.05]  # 向心
    OLC2["VBT"] = OLC2["VBT"][OLC2["VBT"] <= -0.05]  # 向心
    # OLC2 = OLC2[OLC2 <= -0.05]  # 离心
    plt.figure(1)
    # plt.plot(OLC1['y'], linewidth=0.4, color='blue', label='OPTI')
    plt.plot(OLC1['VBT'], linewidth=0.4, color='red', label='VBT')
    plt.show()
    # plt.figure(2)
    # plt.plot(OLC2['y'], linewidth=0.4, color='blue', label='OPTI')
    plt.plot(OLC2['VBT'], linewidth=0.4, color='blue', label='VBT')
    plt.show()

    centric = pd.DataFrame()
    eccentric = pd.DataFrame()
    centric["Opti"] = OLC1["Opti"]
    centric["VBT"] = OLC1["VBT"]
    eccentric["Opti"] = OLC2["Opti"]
    eccentric["VBT"] = OLC2["VBT"]

    # print(OLC)

    centric.to_csv("C:\\Users\\Administrator\\Desktop\\WSY_data\\concentric\\" + all_files + "", index=False)
    eccentric.to_csv("C:\\Users\\Administrator\\Desktop\\WSY_data\\eccentric\\" + all_files + "", index=False)
    # OLC2.to_csv("C:\\Users\\Administrator\\Desktop\\OLC\\%rm\\75%B\\" + all_files + "", index=False)
