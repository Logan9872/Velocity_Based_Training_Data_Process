# 将批处理之后的数据进行平均计算
import os

import pandas as pd
import numpy as np
import scipy
from scipy import stats
dirs = os.listdir("C:/Users/Administrator/Desktop/LoadRank/pre_result_high")



filename_sum = []
ICC_sum = []
MSE_sum = []
RMSE_sum = []
MAE_sum = []
R2_sum = []
CMC_sum = []
SEM_OPTI_sum = []
SEM_VBT_sum = []

for all_files in dirs:
    file = "C:/Users/Administrator/Desktop/LoadRank/pre_result_high/" + all_files + ""

    data = pd.read_csv(file, encoding="unicode_escape")

    # standard error of the mean
    SEM_OPTI = scipy.stats.sem(data['Opti'], axis=0, ddof=0)
    SEM_VBT = scipy.stats.sem(data['VBT'], axis=0, ddof=0)
    SEM_OPTI_sum.append(SEM_OPTI)
    SEM_VBT_sum.append(SEM_VBT)

    CMC = data["CMC"][0]
    CMC_sum.append(CMC)

    ICC = data["ICC"][0]
    ICC_sum.append(ICC)

    MSE = data["MSE"][0]
    MSE_sum.append(MSE)

    RMSE = data["RMSE"][0]
    RMSE_sum.append(RMSE)

    MAE = data["MAE"][0]
    MAE_sum.append(MAE)

    R2 = data["R2"][0]
    R2_sum.append(R2)

    filename = all_files
    filename_sum.append(filename)

# 将list转为字典
    sum_data_dist = {"filename": filename_sum, "MSE_sum": MSE_sum, "RMSE_sum": RMSE_sum, "MAE_sum": MAE_sum, "R2_sum": R2_sum, "ICC_sum": ICC_sum, "SEM_OPTI_sum": SEM_OPTI_sum, "SEM_VBT_sum": SEM_VBT_sum}
    sum_data = pd.DataFrame(sum_data_dist)
# 当遍历完所有的数据后存为csv文件
    if (sum_data["filename"].shape[0] == 21):
        sum_data.to_csv("C:\\Users\\Administrator\\Desktop\\datapreprocess\\average_high.csv", index=False)

        SEM_OPTI_mean = round(np.mean(SEM_OPTI_sum), 8)
        SEM_VBT_mean = round(np.mean(SEM_VBT_sum), 8)
        CMC_mean = round(np.mean(CMC_sum), 4)
        ICC_mean = round(np.mean(ICC_sum), 4)
        MSE_mean = round(np.mean(MAE_sum), 4)
        RMSE_mean = round(np.mean(RMSE_sum), 4)
        MAE_mean = round(np.mean(MAE_sum), 4)
        R2_mean = round(np.mean(R2_sum), 4)

        print("复相关系数(CMC)：", CMC_mean)
        print("组内相关系数(ICC)：", ICC_mean)
        print("线性相关系数(R2)：", R2_mean)
        print("均方误差(MSE)：", MSE_mean)
        print("均方根误差(RMSE)：", RMSE_mean)
        print("平均绝对误差(MAE)：", MAE_mean)
        print("OPTI估计的标准误差(SEM)", SEM_OPTI_mean)
        print("VBT估计的标准误差(SEM)", SEM_VBT_mean)



