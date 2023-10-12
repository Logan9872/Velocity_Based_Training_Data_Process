import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
lr = LinearRegression()

# 绘制散点图和OLC拟合
file1 = "C:/Users/Administrator/Desktop/OLC/%RM/AB.csv"
file2 = "C:/Users/Administrator/Desktop/OLC/%RM/A.csv"
file3 = "C:/Users/Administrator/Desktop/OLC/%RM/B.csv"
# 绘制散点图以及线性回归
plt.rcParams['font.sans-serif'] = 'Microsoft YaHei'  # 设置中文编码和负号的正常显示

OLC = pd.read_csv(file1)
OLC2 = pd.read_csv(file2)
OLC3 = pd.read_csv(file3)


print(OLC)
# OLC = pd.DataFrame()
X = np.array(OLC['x']).reshape(-1, 1)
Y = np.array(OLC['y']).reshape(-1, 1)

lr.fit(X, Y)
R = lr.score(X, Y)
print("w值为:", lr.coef_)
print("b截距值为:", np.around(lr.intercept_, 4))
R = round(R, 4)
print(R)

# if Y >= 0:
#     color = 'r'
# else:
#     color = 'b'


Y_pred = lr.predict(X)
# plt.scatter(OLC2['x'], OLC2['y'], label='向心阶段监测数据', marker='o', s=16, c='r', alpha=0.2)  # VBT数据和Opti数据的散点图
# plt.scatter(OLC3['x'], OLC3['y'], label='离心阶段监测数据', marker='o', s=16, c='b', alpha=0.2)  # VBT数据和Opti数据的散点图
plt.scatter(X, Y, label='监测数据', marker='o', s=16, c='b', alpha=0.2)  # VBT数据和Opti数据的散点图
plt.plot(X, Y_pred, 'r', lw=3, label='拟合线')
plt.xlabel("VBT速度(m/s)")
plt.ylabel("Opti速度(m/s)")
plt.title("全数据拟合曲线", fontproperties='SimHei', fontsize=20)
# -1.4,1;-1.3,0.8;-1,0.7(R2的距离)
plt.text(-1.4, 0.8, "R² = "+str(R)+"", fontsize=13)
plt.text(-1.4, 0.8, "R² = "+str(R)+"", fontsize=13)
plt.legend(loc='best')
plt.show()

#
plt.plot(OLC['x'], linewidth=1, color='blue', label='VBT')
plt.plot(OLC['y'], linewidth=1, color='red', label='Opti Track')
plt.legend(loc='best')
plt.show()
