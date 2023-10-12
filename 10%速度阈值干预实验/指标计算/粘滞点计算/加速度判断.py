import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
import os

DiskPath = "PreTestConcentric"
# DiskPath = "MidTestConcentric"
# DiskPath = "PostTestConcentric"

dirs = os.listdir("C:/Users/Administrator/Desktop/滤波后数据结果/" + DiskPath + "/")

for all_files in dirs:
    # 读取原始数据
    file = "C:/Users/Administrator/Desktop/滤波后数据结果//" + DiskPath + "//" + all_files + ""

    title = all_files[:38]  # 读取文件名
    title_csv = title[:-4]

    # 读取速度和位置上数据
    VBT_data = pd.read_csv(file, encoding="unicode_escape")

    # Filter acceleration data
    b, a = signal.butter(4, 0.125, 'lowpass')
    VBT_data['Velocity'] = signal.filtfilt(b, a, VBT_data['Velocity'])

    # Calculate acceleration
    velocity_t = VBT_data['Velocity'].diff()
    distance = velocity_t / 0.01
    VBT_data['Acceleration'] = distance

    # Find time intervals where acceleration is less than 0
    negative_acceleration_intervals = []
    is_in_negative_interval = False
    start_time = None

    for index, row in VBT_data.iterrows():
        if row['Acceleration'] < 0:
            if not is_in_negative_interval:
                start_time = row['Time']  # Record the start time of the interval
                is_in_negative_interval = True
        else:
            if is_in_negative_interval:
                end_time = row['Time']  # Record the end time of the interval
                negative_acceleration_intervals.append((start_time, end_time))
                is_in_negative_interval = False

    # Print or use negative_acceleration_intervals as needed
    print("Negative Acceleration Intervals for", title_csv)
    for interval in negative_acceleration_intervals:
        print(f"Start Time: {interval[0]}, End Time: {interval[1]}")

    # Plot acceleration data
    plt.figure(1)
    plt.plot(VBT_data['Time'], VBT_data['Acceleration'], linewidth=4, color='blue', label='VBT')
    plt.axhline(y=0, linewidth=1, c="red")  # 添加水平直线
    plt.xlabel("Time (10ms)")
    plt.ylabel("Acceleration (m/s²)")
    plt.title(title_csv, fontsize=18)
    plt.show()
