
import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy import stats
from sklearn.metrics import mean_squared_error  # 均方误差|
from sklearn.metrics import mean_absolute_error  # 平方绝对误差
from sklearn.metrics import r2_score  # R square
import pingouin as pg
import os
from sklearn.linear_model import LinearRegression
lr = LinearRegression()
# 读取分好的深蹲动作的数据，分别求出VBT和Opti的均值，并将这个均值放入表中

fileName = []
vbt_mean = []
opti_mean = []

# dirs = os.listdir("C:/Users/Administrator/Desktop/squat_reps/load/30%load/ecce")
# dirs = os.listdir("C:/Users/Administrator/Desktop/squat_reps/load/45%load/ecce")
# dirs = os.listdir("C:/Users/Administrator/Desktop/squat_reps/load/60%load/ecce")
# dirs = os.listdir("C:/Users/Administrator/Desktop/squat_reps/load/75%load/ecce")
# dirs = os.listdir("C:/Users/Administrator/Desktop/squat_reps/load/90%load/ecce")
# # -----
# dirs = os.listdir("C:/Users/Administrator/Desktop/squat_reps/load/30%load/conc")
# dirs = os.listdir("C:/Users/Administrator/Desktop/squat_reps/load/45%load/conc")
# dirs = os.listdir("C:/Users/Administrator/Desktop/squat_reps/load/60%load/conc")
# dirs = os.listdir("C:/Users/Administrator/Desktop/squat_reps/load/75%load/conc")
# dirs = os.listdir("C:/Users/Administrator/Desktop/squat_reps/load/90%load/conc")
# # -----
dirs = os.listdir("C:/Users/Administrator/Desktop/squat_reps/con_div")
# dirs = os.listdir("C:/Users/Administrator/Desktop/squat_reps/ecc_div")

for all_files in dirs:
    # 读取原始数据
    # file = "C:/Users/Administrator/Desktop/squat_reps/load/30%load/ecce/" + all_files + ""
    # file = "C:/Users/Administrator/Desktop/squat_reps/load/45%load/ecce/" + all_files + ""
    # file = "C:/Users/Administrator/Desktop/squat_reps/load/60%load/ecce/" + all_files + ""
    # file = "C:/Users/Administrator/Desktop/squat_reps/load/75%load/ecce/" + all_files + ""
    # file = "C:/Users/Administrator/Desktop/squat_reps/load/90%load/ecce/" + all_files + ""
    # # -----
    # file = "C:/Users/Administrator/Desktop/squat_reps/load/30%load/conc/" + all_files + ""
    # file = "C:/Users/Administrator/Desktop/squat_reps/load/45%load/conc/" + all_files + ""
    # file = "C:/Users/Administrator/Desktop/squat_reps/load/60%load/conc/" + all_files + ""
    # file = "C:/Users/Administrator/Desktop/squat_reps/load/75%load/conc/" + all_files + ""
    # file = "C:/Users/Administrator/Desktop/squat_reps/load/90%load/conc/" + all_files + ""
    # # -----
    file = "C:/Users/Administrator/Desktop/squat_reps/con_div/" + all_files + ""
    # file = "C:/Users/Administrator/Desktop/squat_reps/ecc_div/" + all_files + ""
    data = pd.read_csv(file, encoding="unicode_escape")
    # 均值为mean
    file_vbt = data['VBT_Mean']
    file_opti = data['OPTI_Mean']
    # 非均值为
    # file_vbt = data['VBT']
    # file_opti = data['OPTI']
    fileName.append(all_files)
    vbt_mean.append(file_vbt[0])
    opti_mean.append(file_opti[0])
    A = {"FileName": fileName, "VBT": vbt_mean, "OPTI": opti_mean}
data_mean = pd.DataFrame(A)

X = np.array(data_mean['VBT']).reshape(-1, 1)
Y = np.array(data_mean['OPTI']).reshape(-1, 1)
# ————————————————————————————————————————
# R
lr.fit(X, Y)
R = lr.score(X, Y)
print("w值为:", lr.coef_)
print("b截距值为:", lr.intercept_)
data_mean['R'] = R
print(R)
# ——————————————————————————————————————
velocity_data = pd.DataFrame()
velocity_data['VBT'] = data['VBT']
velocity_data['OPTI'] = data['OPTI']
r = velocity_data.corr()
data_mean['Person'] = r["VBT"][1]
print("person", r)
# ——————————————————————————————————————
# 绘制
Y_pred = lr.predict(X)
plt.scatter(X, Y, label='Data', marker='o', s=16)  # VBT数据和Opti数据的散点图
plt.plot(X, Y_pred, 'r', lw=1, label='OLC')
plt.xlabel("VBT(m/s)")
plt.ylabel("Opti(m/s)")
plt.legend(loc='best')
plt.show()
# plt.rcParams['font.sans-serif'] = 'Microsoft YaHei'  # 设置中文编码和负号的正常显示
# ————————————————————————————————————————
# ICC
VBT_ICC = pd.DataFrame()
Opti_ICC = pd.DataFrame()
VBT_ICC["velocity"] = data_mean['VBT']
VBT_ICC.insert(0, "reader", "A")
VBT_ICC.insert(0, "target", range(VBT_ICC.shape[0]))

Opti_ICC["velocity"] = data_mean['OPTI']
Opti_ICC = Opti_ICC.replace(np.nan, 0)
Opti_ICC.insert(0, "reader", "B")
Opti_ICC.insert(0, "target", range(Opti_ICC.shape[0]))
ICC_data = pd.concat([VBT_ICC, Opti_ICC])
ICC = pg.intraclass_corr(data=ICC_data, targets="target", raters="reader", ratings="velocity")
data_mean['ICC'] = ICC["ICC"][3]
# ————————————————————————————————————————
# RMSE
MSE = mean_squared_error(Y, X)
RMSE = math.sqrt(MSE)
data_mean['RMSE'] = RMSE

print("ICC", ICC)
print("RMSE", RMSE)

# data_mean.to_csv("C:\\Users\\Administrator\\Desktop\\squat_reps\\90%RM Eccentric Phase.csv", index=False)
# data_mean.to_csv("C:\\Users\\Administrator\\Desktop\\squat_reps\\75%RM Eccentric Phase.csv", index=False)
# data_mean.to_csv("C:\\Users\\Administrator\\Desktop\\squat_reps\\60%RM Eccentric Phase.csv", index=False)
# data_mean.to_csv("C:\\Users\\Administrator\\Desktop\\squat_reps\\45%RM Eccentric Phase.csv", index=False)
# data_mean.to_csv("C:\\Users\\Administrator\\Desktop\\squat_reps\\30%RM Eccentric Phase.csv", index=False)
# # ——————
# data_mean.to_csv("C:\\Users\\Administrator\\Desktop\\squat_reps\\90%RM Cocentric Phase.csv", index=False)
# data_mean.to_csv("C:\\Users\\Administrator\\Desktop\\squat_reps\\75%RM Cocentric Phase.csv", index=False)
# data_mean.to_csv("C:\\Users\\Administrator\\Desktop\\squat_reps\\60%RM Cocentric Phase.csv", index=False)
# data_mean.to_csv("C:\\Users\\Administrator\\Desktop\\squat_reps\\45%RM Cocentric Phase.csv", index=False)
# data_mean.to_csv("C:\\Users\\Administrator\\Desktop\\squat_reps\\30%RM Cocentric Phase.csv", index=False)
# # ——————
data_mean.to_csv("C:\\Users\\Administrator\\Desktop\\squat_reps\\Full Loads Concentric Phase.csv", index=False)
# data_mean.to_csv("C:\\Users\\Administrator\\Desktop\\squat_reps\\Full Loads Eccentric Phase.csv", index=False)





