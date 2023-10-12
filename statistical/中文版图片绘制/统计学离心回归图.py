import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
import os
from sklearn.linear_model import LinearRegression
lr = LinearRegression()
import seaborn as sns
import matplotlib.pyplot as plt



# 用于绘制所有动作的数据回归曲线图，并在此调整配色
dirs = os.listdir("C:/Users/Administrator/Desktop/squat_reps/chart/eccentric/")
for all_files in dirs:
    plt.rc("font", family='Adobe Heiti Std')
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负

    # 读取原始数据
    file = "C:/Users/Administrator/Desktop/squat_reps/chart/eccentric/" + all_files + ""
    title = all_files[:-19]
    data = pd.read_csv(file, encoding="unicode_escape")
    # 拟合
    X = np.array(data['VBT']).reshape(-1, 1)
    Y = np.array(data['OPTI']).reshape(-1, 1)
    lr.fit(X, Y)
    R = '{:.4f}'.format(lr.score(X, Y))

    W = '{:.4f}'.format(lr.coef_[0][0])
    b = '{:.4f}'.format(lr.intercept_[0])
    r = '{:.3f}'.format(data['Person'][0])
    if(b[0:1] == "-"):
        K = ""
    else:
        K ="+"

    # 绘图
    Y_pred = lr.predict(X)
    plt.xlim(-0.9, 0)  # 设置x轴的数值显示范围
    plt.ylim(-0.9, 0)  # 设置y轴的数值显示范围
    # ————————————————————————————————————————————————————————————————————
    # seaboard 设置
    sns.regplot(
        x=X,
        y=Y,
        line_kws={"color": "#fa4343", "alpha": 0.6, "lw": 2},
        scatter_kws={"color": "#0780cf", 's': 140, "alpha": 0.4, "edgecolor": "w", "norm": 0.4},

    )
    ax = plt.gca()   # 相对位置设定
    # 图例

    plt.legend(labels=["原始数据", "拟合曲线"], loc=2)
    plt.text(0.6, 0.3,
             "y = " + str(W)+"x"+ K +""+ str(b) +" ""\n" "R$^{2}$ = " + str(R) + " ",
             fontsize=14,
             verticalalignment="top",
             transform=ax.transAxes)
    # plt.legend(loc='best')
    plt.title(title, fontsize=18)
    sns.despine()  # 去边框
    sns.set_context("paper", font_scale=1.5)
    sns.set_style('ticks')   # 设置风格
    plt.xlabel("力量训练监测系统 平均速度 [m/s]", fontsize=13)
    plt.ylabel(" OptiTrack系统 平均速度[m/s]", fontsize=13)
    filename = "C:/Users/Administrator/Desktop/squat_reps/中文结果图/ecc/" + title + ".pdf"
    plt.savefig(filename)
    plt.show()
