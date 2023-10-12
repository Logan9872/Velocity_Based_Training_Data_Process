
import numpy as np
import pandas as pd
import os

from xarray.plot.utils import plt

dirs = os.listdir("C:/Users/Administrator/Desktop/915velocity/915origin/")
for all_files in dirs:
    # 读取原始数据
    file_vbt = "C:/Users/Administrator/Desktop/915velocity/915origin/" + all_files + ""
    VBT_data_time = pd.read_csv(file_vbt, skiprows=2, usecols=[0], header=None, names=['time'],encoding="unicode_escape")
    VBT_data = pd.read_csv(file_vbt, skiprows=2, usecols=[2, 3], header=None, names=['position', 'velocity'],encoding="unicode_escape")
    VBT_velocity = pd.DataFrame()
    origin_time = VBT_data_time['time'].loc[0]
    # vbt的时间
    VBT_data['time'] = VBT_data_time.apply(lambda x: (x['time'] - origin_time) / 1000, axis=1)
    # vbt的速度
    VBT_data['velocity'] = VBT_data.apply(lambda x: (x['velocity'] * 0.00767), axis=1)
    # vbt的位置
    VBT_data['position'] = VBT_data.apply(lambda x: (x['position'] * 0.0000767), axis=1)
    # ————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 绘图
    plt.plot(VBT_data['time'], VBT_data['velocity'], linewidth=0.4)
    plt.xlabel("time(s)")
    plt.ylabel("velocity(m/s)")
    plt.title(all_files, loc = 'left',color = 'b')
    plt.show()
    # ————————————————————————————————————————————————————————————————————————————————————————————————————————————

    VBT_velocity["position"] = VBT_data["position"]
    VBT_velocity["velocity"] = VBT_data["velocity"]
    VBT_velocity.to_csv("C:\\Users\\Administrator\\Desktop\\915velocity\\915VBT\\" + all_files + "", index=False)
