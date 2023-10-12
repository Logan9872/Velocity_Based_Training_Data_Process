import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
import os
from sklearn.linear_model import LinearRegression
lr = LinearRegression()
import seaborn as sns

# 图表图例 / XY轴的范围 /

# 用于绘制所有动作的数据回归曲线图，并在此调整配色
dirs = os.listdir("C:/Users/Administrator/Desktop/redraw/chart_waveform")
for all_files in dirs:
    # 读取原始数据
    file = "C:/Users/Administrator/Desktop/redraw/chart_waveform/" + all_files + ""
    title = all_files[:-4]
    data = pd.read_csv(file, encoding="unicode_escape")
    # 拟合
    X = np.array(data['VBT']).reshape(-1, 1)
    Y = np.array(data['OPTI']).reshape(-1, 1)
    print(data)
    r = '{:.3f}'.format(data['Person'][0])

    lr.fit(X, Y)
    R = '{:.4f}'.format(lr.score(X, Y))
    W = '{:.4f}'.format(lr.coef_[0][0])
    b = '{:.4f}'.format(lr.intercept_[0])
    if(b[0:1] == "-"):
        K = ""
    else:
        K ="+"

    # 绘图
    Y_pred = lr.predict(X)

    # ————————————————————————————————————————————————————————————————————
    # seaboard 设置
    # 绘制拟合曲线


    # # 绘制异常点图
    # plt.scatter(data['VBT_23'], data['OPTI_23'], c="#59A95A", s=80, alpha=0.4, edgecolor="#F1FFFF")

    # 绘制除了异常点以外的图
    C = sns.regplot(
        x=data['VBT_off'],
        y=data['OPTI_off'],
        line_kws={"color": "#fa4343", "alpha": 0.8, "lw": 2},
        scatter_kws={"color": "#0780cf", 's': 80, "alpha": 0.4, "edgecolor": "#F1FFFF", "norm": 0.4},
    )
    # plt.legend(labels=["Abnornal", "Normal", "Fitted Curve"], loc=2)

    # # 绘制异常点图
    plt.scatter(data['VBT_23'], data['OPTI_23'], c="#0780cf", s=80, alpha=0.4, edgecolor="#F1FFFF")
    plt.legend(labels=["Raw Data", "Fitted Curve"], loc=2)


    # 去除多余空白
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.xlim(-1.5, 2)  # 设置x轴的数值显示范围
    plt.ylim(-1.5, 2)  # 设置y轴的数值显示范围
    ax = plt.gca()   # 相对位置设定

    plt.text(0.6, 0.3,
             "y = " + str(W)+"x"+ K +""+ str(b) +" ""\n" "R²  = " + str( R) + " ",
             fontsize=14,
             verticalalignment="top",
             transform=ax.transAxes)

    plt.title(title, fontsize=18)
    sns.despine()  # 去边框
    sns.set_context("paper", font_scale=1.5)
    sns.set_style('ticks')   # 设置风格
    plt.xlabel("Instantaneous Velocity of Proposed System [m/s]", fontsize=13)
    plt.ylabel("Instantaneous Velocity of OptiTrack System [m/s]", fontsize=13)
    filename = "C:/Users/Administrator/Desktop/squat_reps/全波形结果图/" + title + ".pdf"
    # filename = "C:/Users/Administrator/Desktop/squat_reps/异常值结果图/" + title + ".pdf"
    plt.savefig(filename)
    plt.show()

