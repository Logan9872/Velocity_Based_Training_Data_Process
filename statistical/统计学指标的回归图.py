import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
import os
from sklearn.linear_model import LinearRegression
lr = LinearRegression()
import seaborn as sns


# 用于绘制所有动作的数据回归曲线图，并在此调整配色
dirs = os.listdir("C:/Users/Administrator/Desktop/squat_reps/chart/")
for all_files in dirs:
    # 读取原始数据
    file = "C:/Users/Administrator/Desktop/squat_reps/chart/" + all_files + ""
    title = all_files[:-4]
    data = pd.read_csv(file, encoding="unicode_escape")
    # 拟合
    X = np.array(data['VBT']).reshape(-1, 1)
    Y = np.array(data['OPTI']).reshape(-1, 1)
    lr.fit(X, Y)
    R = '{:.3f}'.format(lr.score(X, Y))

    W = '{:.5f}'.format(lr.coef_[0][0])
    b = '{:.5f}'.format(lr.intercept_[0])
    r = '{:.3f}'.format(data['Person'][0])
    if(b[0:1] == "-"):
        K = ""
    else:
        K ="+"

    # 绘图
    Y_pred = lr.predict(X)

    # ————————————————————————————————————————————————————————————————————
    # seaboard 设置
    sns.regplot(
        x=X,
        y=Y,
        line_kws={"color": "#fa4343", "alpha": 0.4, "lw": 3},
        scatter_kws={"color": "#0e72cc", 's': 100, "alpha": 0.4, "edgecolor": "w", "norm": 0.4},

    )
    ax = plt.gca()   # 相对位置设定
    plt.text(0.1, 0.85,
             "y = " + str(W)+"x"+ K +""+ str(b) +" ""\n" "r = " + str(r) + " ",
             fontsize=14,
             verticalalignment="top",
             transform=ax.transAxes)
    # plt.legend(loc='best')
    plt.title(title, fontsize=20)
    sns.despine()  # 去边框
    sns.set_context("paper", font_scale=1.5)
    sns.set_style('ticks')   # 设置风格
    plt.xlabel("Average Velocity of Monitoring System (m/s)", fontsize=14)
    plt.ylabel("Average Velocity of OptiTrack System(m/s)", fontsize=14)
    filename = "C:/Users/Administrator/Desktop/squat_reps/结果图/" + title + ".png"
    plt.savefig(filename)
    plt.show()
