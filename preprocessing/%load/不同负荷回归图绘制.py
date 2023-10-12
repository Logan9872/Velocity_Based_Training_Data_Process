import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
lr = LinearRegression()

# 绘制散点图和OLC拟合
file = "C:/Users/Administrator/Desktop/OLC/low_load.csv"
# file = "C:/Users/Administrator/Desktop/OLC/mid_load.csv"
# file = "C:/Users/Administrator/Desktop/OLC/high_load.csv"
# 绘制散点图以及线性回归
plt.rcParams['font.sans-serif'] = 'Microsoft YaHei'  # 设置中文编码和负号的正常显示

OLC = pd.read_csv(file)
print(OLC)
# OLC = pd.DataFrame()
X = np.array(OLC['x']).reshape(-1, 1)
Y = np.array(OLC['y']).reshape(-1, 1)

lr.fit(X, Y)
R = lr.score(X, Y)
R = round(R, 4)
print(R)
R = lr.score(X, Y)


Y_pred = lr.predict(X)
plt.scatter(X, Y, label='监测数据', marker='o',color='blue', s=16, alpha=0.2)  # VBT数据和Opti数据的散点图
plt.plot(X, Y_pred, 'r', lw=3, label='拟合线')
plt.xlabel("VBT速度(m/s)")
plt.ylabel("Opti速度(m/s)")
plt.title("Low Load拟合曲线", fontproperties='SimHei', fontsize=20)
# -1.4,1;-1.3,0.8;-1,0.7(R2的距离)
plt.text(-1.4, 1, "R² = "+str(R)+"", fontsize=15)
plt.legend(loc='best')
plt.show()
