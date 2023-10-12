import pandas as pd
from scipy import signal
import os
import matplotlib.pyplot as plt

DiskPath = "PreTestConcentric"  # Replace with your desired DiskPath

dirs = os.listdir("C:/Users/Administrator/Desktop/滤波后数据结果/" + DiskPath + "/")

for all_files in dirs:
    file = "C:/Users/Administrator/Desktop/滤波后数据结果//" + DiskPath + "//" + all_files + ""
    title = all_files[:38]

    VBT_data = pd.read_csv(file, encoding="unicode_escape")

    # Apply Butterworth filter
    b, a = signal.butter(4, 0.125, 'lowpass')
    VBT_data['Velocity'] = signal.filtfilt(b, a, VBT_data['Velocity'])

    # Calculate acceleration
    velocity_t = VBT_data['Velocity'].diff()
    VBT_data['Acceleration'] = velocity_t / 0.01

    # Initialize variables to track sticky region
    sticky_region_started = False
    sticky_region_indices = []

    # Initialize a list to store sticky region start and end points for plotting
    sticky_region_points = []

    for index, acceleration in VBT_data['Acceleration'].items():
        if acceleration < 0 and not sticky_region_started:
            sticky_region_started = True
            sticky_region_indices.append(index)
        elif acceleration > 0 and sticky_region_started:
            sticky_region_indices.append(index)
            sticky_region_points.extend(sticky_region_indices)  # Store start and end points
            sticky_region_indices = []  # Reset for the next sticky region
            sticky_region_started = False

    if len(sticky_region_points) < 2:
        print(f"Sticky Region{title}: No sticky region found")
    else:
        # Print the indices of sticky regions in the original file
        print(f"Sticky Region{title}: {sticky_region_points}")

        # 绘制加速度数据
        plt.figure(figsize=(10, 6))
        plt.plot(VBT_data.index, VBT_data['Acceleration'], linewidth=1, color='blue', label='Acceleration')
        plt.axhline(y=0, linewidth=1, c="red")  # Add horizontal line at y=0

        # 高光粘滞区间
        for i in range(0, len(sticky_region_points), 2):
            start_idx = sticky_region_points[i]
            end_idx = sticky_region_points[i + 1]
            plt.axvspan(start_idx, end_idx, color='yellow', alpha=0.3)

        plt.xlabel("Time (Index)")
        plt.ylabel("Acceleration (m/s²)")
        plt.title(title, fontproperties='SimHei', fontsize=18)
        plt.show()
