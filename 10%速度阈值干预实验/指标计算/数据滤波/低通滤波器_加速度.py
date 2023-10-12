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
    # 读取时间数据
    print(title_csv)
    # 4 阶数 0.12=2*（截止频率6HZ/采样频率100HZ）
    b, a = signal.butter(4, 0.125, 'lowpass')
    VBT_data['Velocity'] = signal.filtfilt(b, a, VBT_data['Velocity'])
    # 已知速度求加速度
    velocity_t = VBT_data['Velocity'].diff()
    print(velocity_t)
    distance = velocity_t/0.01
    VBT_data['Acceleration'] = distance


    plt.figure(1)
    # plt.plot(VBT_data['Velocity'], linewidth=4, color='blue', label='VBT')
    #
    plt.plot(VBT_data['Acceleration'], linewidth=4, color='blue', label='VBT')
    plt.axhline(y=0, linewidth=1, c="red")  # 添加水平直线
    #
    plt.xlabel("Time(10ms)")
    # plt.ylabel("Velocity(m/s)")
    plt.ylabel("Acceleration(m/s²)")
    plt.title(title_csv, fontproperties='SimHei', fontsize=18)


    # plt.savefig("C:\\Users\\Administrator\\Desktop\\10%VelocityData除信号\\滤波后\\MidTestConcentric绘制\\速度\\" + title_csv + ".png")
    plt.savefig("C:\\Users\\Administrator\\Desktop\\10%VelocityData除信号\\滤波后\\PreTestConcentric绘制\\加速度\\" + title_csv + ".png")

    plt.show()



    # 保存成csv文件
    VBT_data.to_csv("C:\\Users\\Administrator\\Desktop\\10%VelocityData除信号\\滤波后\\PreTestConcentric\\" + title_csv + ".csv", index=False)
