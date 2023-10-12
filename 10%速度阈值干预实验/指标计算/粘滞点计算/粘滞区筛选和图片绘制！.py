import pandas as pd
from scipy import signal
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Set Seaborn style
sns.set_theme(style="whitegrid", font_scale=2, font="SimHei")

plt.rcParams['axes.unicode_minus']=False

DiskPath = "PreTestConcentric"
# DiskPath = "MidTestConcentric"
# DiskPath = "PostTestConcentric"


dirs = os.listdir("C:/Users/Administrator/Desktop/滤波后数据结果/" + DiskPath + "/")


# 生成csv文件存储粘滞期数据
sticky_region_csv = pd.DataFrame()
file_name = []
sticky_region_time = []

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

    # Initialize variables to track sticky regions
    sticky_regions = []
    sticky_region = []

    for index, acceleration in VBT_data['Acceleration'].items():
        if acceleration < 0 and not sticky_region:
            sticky_region.append(index)
        elif acceleration > 0 and sticky_region:
            sticky_region.append(index)
            sticky_regions.append(sticky_region)
            sticky_region = []


    if len(sticky_regions) <= 1:
        print("No sticky regions found")
        # sticky_region_time.append(0)
    else:
        # Combine the first and last sticky regions
        combined_sticky_region = list(range(sticky_regions[0][0], sticky_regions[-1][-1] + 1))

        # Print the indices of the combined sticky region in the original file
        print(f"Sticky Region Indices in {title}: {combined_sticky_region}")
        print(sticky_regions)
        sticky_time = (sticky_regions[-1][-1]*1-sticky_regions[0][0]*1) * 0.01

        # 添加文件名
        file_name.append(title)
        sticky_region_time.append(sticky_time)

        # Create a square plot with uniform axes and y=0 at the center

        plt.figure(figsize=(10, 10))
        ax1 = sns.lineplot(data=VBT_data, x=VBT_data.index, y='Acceleration', linewidth=2, color='blue', zorder=3)
        sns.lineplot(data=VBT_data, x=VBT_data.index, y='Velocity', linewidth=2, color='green', ax=ax1)
        ax1.set_ylabel('加速度(m/$\mathregular{s^2}$)', color='black')
        ax1.set_xlabel("时间(10ms)", color='black')
        plt.axhline(y=0, linewidth=2, c="red")
        plt.legend(labels=["加速度", "速度"], loc=3)

        # 设置双Y轴
        ax2 = ax1.twinx()
        # ---
        sns.lineplot(data=VBT_data, x=VBT_data.index, y='Acceleration', linewidth=2, color='blue', ax=ax2)
        sns.lineplot(data=VBT_data, x=VBT_data.index, y='Velocity', linewidth=2, color='green', ax=ax1)
        ax1.set_ylabel('加速度(m/$\mathregular{s^2}$)', color='black')
        ax1.set_xlabel("时间(10ms)", color='black')
        plt.axhline(y=0, linewidth=2, c="red")
        # ---
        ax2.set_ylabel('速度(m/s)', color="black")

        # 高亮粘滞区
        plt.axvspan(combined_sticky_region[0], combined_sticky_region[-1], color='grey', alpha=0.3)

# ----
        # Set uniform x axis limits to make it square
        # plt.xlim(VBT_data.index.min(), VBT_data.index.max())

        # min_y = min(VBT_data[['Acceleration', 'Velocity']].min().min(), 0)
        # max_y = max(VBT_data[['Acceleration', 'Velocity']].max().max(), 0)
        # ax1.set_ylim(min_y, max_y)
        # ax2.set_ylim(min_y, max_y)
# ------
#         ax1.set_ylim(15,-15)
#         ax2.set_ylim(15,-15)
# -----

       # 设置绘图的区域
        plt.xlim(VBT_data.index.min(), VBT_data.index.max())
        y_min = min(VBT_data[['Acceleration', 'Velocity']].min())
        y_max = max(VBT_data[['Acceleration', 'Velocity']].max())
        if y_min * y_max < 0:
            ax1.set_ylim(-max(abs(y_min), abs(y_max)), max(abs(y_min), abs(y_max)))
            ax2.set_ylim(-max(abs(y_min), abs(y_max)), max(abs(y_min), abs(y_max)))
        else:
            ax1.set_ylim(y_min, y_max)
            ax2.set_ylim(y_min, y_max)
# ----

        ax1.set_ylim(-8, 8)
        ax2.set_ylim(-8, 8)
        # plt.title(title, fontsize=18)
        plt.savefig("C:\\Users\\Administrator\\Desktop\\粘滞点结果\\"+DiskPath + "\\" + title + ".png")
        plt.show()
        # ---

        print(file_name)
        print(sticky_region_time)

sticky_region_csv["file_name"] = file_name
sticky_region_csv["stick_region_time"] = sticky_region_time
sticky_region_csv.to_csv("C:\\Users\\Administrator\\Desktop\\粘滞点结果\\" +DiskPath+ ".csv", index=False)

print(sticky_region_csv)
