import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy import stats
from scipy import signal
from sklearn.metrics import mean_squared_error  # 均方误差|
from sklearn.metrics import mean_absolute_error  # 平方绝对误差
from sklearn.metrics import r2_score  # R square
import pingouin as pg
import os

dirs = os.listdir("C:/Users/Administrator/Desktop/DataPreprocess/OPTI_data")
for all_files in dirs:
    # 读取原始数据
    file = "C:/Users/Administrator/Desktop/DataPreprocess/OPTI_data/" + all_files + ""
    # 读取Opti的原始数据
    opti_track_data = pd.read_csv(file, skiprows=6, usecols=[2, 3, 4], encoding="unicode_escape")
    opti_track_time = pd.read_csv(file, skiprows=6, usecols=[1], encoding="unicode_escape")

    # 4 阶数 0.12=2*（截止频率6HZ/采样频率100HZ）
    b, a = signal.butter(4, 0.125, 'lowpass')
    opti_track_data['X'] = signal.filtfilt(b, a, opti_track_data['X'])
    opti_track_data['Y'] = signal.filtfilt(b, a, opti_track_data['Y'])
    opti_track_data['Z'] = signal.filtfilt(b, a, opti_track_data['Z'])


    print(opti_track_data)

