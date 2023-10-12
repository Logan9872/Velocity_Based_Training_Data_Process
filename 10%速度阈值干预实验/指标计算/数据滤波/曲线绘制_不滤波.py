import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
import sympy
import os

dirs = os.listdir("C:/Users/Administrator/Desktop/10%VelocityData除信号/C&E/ConcentricResult/PreTestConcentric/")
# dirs = os.listdir("C:/Users/Administrator/Desktop/10%VelocityData除信号/C&E/ConcentricResult/MidTestConcentric/")
# dirs = os.listdir("C:/Users/Administrator/Desktop/10%VelocityData除信号/C&E/ConcentricResult/PostTestConcentric/")
for all_files in dirs:
    # 读取原始数据
    file = "C:/Users/Administrator/Desktop/10%VelocityData除信号/C&E/ConcentricResult/PreTestConcentric/" + all_files + ""
    # file = "C:/Users/Administrator/Desktop/10%VelocityData除信号/C&E/ConcentricResult/MidTestConcentric/" + all_files + ""
    # file = "C:/Users/Administrator/Desktop/10%VelocityData除信号/C&E/ConcentricResult/PostTestConcentric/" + all_files + ""

    title = all_files[:38]  # 读取文件名
    title_csv = title[:-4]

    # 读取速度和位置上数据
    VBT_data = pd.read_csv(file, encoding="unicode_escape")

    plt.figure(1)
    plt.plot(VBT_data['Velocity'], linewidth=4, color='blue', label='VBT')

    # plt.axhline(y=0, linewidth=1, c="red")  # 添加水平直线
    #
    plt.xlabel("Time(10ms)")
    plt.ylabel("Velocity(m/s)")
    plt.title(title_csv, fontproperties='SimHei', fontsize=18)

    plt.savefig("C:\\Users\\Administrator\\Desktop\\测试数据绘制\\单个深蹲曲线\\" + title_csv + ".png")

    plt.show()



    # 保存成csv文件
    VBT_data.to_csv("C:\\Users\\Administrator\\Desktop\\10%VelocityData除信号\\滤波后\\MidTestConcentric\\" + title_csv + ".csv", index=False)
