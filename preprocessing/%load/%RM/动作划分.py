import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import heapq

dirs = os.listdir("C:/Users/Administrator/Desktop/meanV/divide/")
for all_files in dirs:
    # 读取原始数据
    file = "C:/Users/Administrator/Desktop/meanV/divide/" + all_files + ""
    origin_data = pd.read_csv(file)
    origin_data["x"] = np.nan_to_num(origin_data["x"])
    origin_data["y"] = np.nan_to_num(origin_data["y"])
    division1 = pd.DataFrame()
    division2 = pd.DataFrame()
    division3 = pd.DataFrame()
    VBT1 = []
    OPTI1 = []
    VBT2 = []
    OPTI2 = []
    VBT3 = []
    OPTI3 = []

    i = 0
    k = 0

    # 判断当前是否为空，如果是则i+1继续遍历，同时记录遇到空的数值j+1
    # 如果不为空则将数据存入list，i+1,j+1
    # 同时判断遇到空的个数j，若j大于200则认为是第二个动作，将其存入新的list
    #
    for i in range(len(origin_data["x"])):
        if (origin_data["x"][i] == 0):
            i = i + 1
# 当有数值的时候进入，如果前一个数为0，则存入list1
        elif (origin_data["x"][i] != 0):
            print(i)
            if (origin_data["x"][i-1] == 0):
                # 如果前一个数是0，后一个数不是，则k+1,k为遇到峰的个数
                k = k+1
                if(k==1):
                    VBT1.append(origin_data["x"][i])
                    OPTI1.append(origin_data["y"][i])
                    A = {"VBT": VBT1, "OPTI": OPTI1}
                    division1 = pd.DataFrame(A)
                    i = i + 1

                elif(k==2):
                    VBT2.append(origin_data["x"][i])
                    OPTI2.append(origin_data["y"][i])
                    B = {"VBT": VBT2, "OPTI": OPTI2}
                    division2 = pd.DataFrame(B)
                    i = i + 1

                elif (k == 3):
                    VBT3.append(origin_data["x"][i])
                    OPTI3.append(origin_data["y"][i])
                    c = {"VBT": VBT3, "OPTI": OPTI3}
                    division3 = pd.DataFrame(c)
                    i = i + 1

            elif (origin_data["x"][i-1] != 0):
                if (k == 1):
                    VBT1.append(origin_data["x"][i])
                    OPTI1.append(origin_data["y"][i])
                    A = {"VBT": VBT1, "OPTI": OPTI1}
                    division1 = pd.DataFrame(A)
                    i = i + 1

                elif (k == 2):
                    VBT2.append(origin_data["x"][i])
                    OPTI2.append(origin_data["y"][i])
                    B = {"VBT": VBT2, "OPTI": OPTI2}
                    division2 = pd.DataFrame(B)
                    i = i + 1

                elif (k == 3):
                    VBT3.append(origin_data["x"][i])
                    OPTI3.append(origin_data["y"][i])
                    C = {"VBT": VBT3, "OPTI": OPTI3}
                    division3 = pd.DataFrame(C)
                    i = i + 1
        else:
            i = i + 1

# 计算平均值和最大值


    if (division2.empty):
        division1["VBT_ Mean"] = division1["VBT"].mean()
        division1["OPTI_ Mean"] = division1["OPTI"].mean()
        division1["VBT_ Max"] = division1["VBT"].max()
        division1["OPTI_ Max"] = division1["OPTI"].max()
        division1.to_csv("C:\\Users\\Administrator\\Desktop\\meanV\\division\\" + all_files + "_1.csv", index=False)
    else:
        division1["VBT_ Mean"] = division1["VBT"].mean()
        division1["OPTI_ Mean"] = division1["OPTI"].mean()
        division1["VBT_ Max"] = division1["VBT"].max()
        division1["OPTI_ Max"] = division1["OPTI"].max()
        division2["VBT_ Mean"] = division1["VBT"].mean()
        division2["OPTI_ Mean"] = division1["OPTI"].mean()
        division2["VBT_ Max"] = division1["VBT"].max()
        division2["OPTI_ Max"] = division1["OPTI"].max()
        division3["VBT_ Mean"] = division1["VBT"].mean()
        division3["OPTI_ Mean"] = division1["OPTI"].mean()
        division3["VBT_ Max"] = division1["VBT"].max()
        division3["OPTI_ Max"] = division1["OPTI"].max()
        division1.to_csv("C:\\Users\\Administrator\\Desktop\\meanV\\division\\" + all_files + "_1.csv", index=False)
        division2.to_csv("C:\\Users\\Administrator\\Desktop\\meanV\\division\\" + all_files + "_2.csv", index=False)
        division3.to_csv("C:\\Users\\Administrator\\Desktop\\meanV\\division\\" + all_files + "_3.csv", index=False)
