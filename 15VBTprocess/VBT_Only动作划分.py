
import numpy as np
import pandas as pd
import os

dirs = os.listdir("C:/Users/Administrator/Desktop/915velocity/915centric/")
for all_files in dirs:
    # 读取原始数据
    file = "C:/Users/Administrator/Desktop/915velocity/915centric/" + all_files + ""
    origin_data = pd.read_csv(file)
    print(file)
    print(origin_data)
    origin_data["velocity"] = np.nan_to_num(origin_data["velocity"])
    division1 = pd.DataFrame()
    division2 = pd.DataFrame()
    division3 = pd.DataFrame()
    VBT1 = []
    VBT2 = []
    VBT3 = []
    position1 = []
    position2 = []
    position3 = []

    i = 0
    k = 0

    # 判断当前是否为空，如果是则i+1继续遍历，同时记录遇到空的数值j+1
    # 如果不为空则将数据存入list，i+1,j+1
    # 同时判断遇到空的个数j，若j大于200则认为是第二个动作，将其存入新的list
    #
    for i in range(len(origin_data["velocity"])):
        if (origin_data["velocity"][i] == 0):
            i = i + 1
            print(i)
# 当有数值的时候进入，如果前一个数为0，则存入list1
        elif (origin_data["velocity"][i] != 0):
            print(i)
            if (origin_data["velocity"][i-1] == 0):
                # 如果前一个数是0，后一个数不是，则k+1,k为遇到峰的个数
                k = k+1
                if(k==1):
                    VBT1.append(origin_data["velocity"][i])
                    position1.append(origin_data["position"][i])
                    A = {"velocity": VBT1, "position": position1}
                    division1 = pd.DataFrame(A)
                    i = i + 1

                elif(k==2):
                    VBT2.append(origin_data["velocity"][i])
                    position2.append(origin_data["position"][i])
                    B = {"velocity": VBT2, "position": position2}
                    division2 = pd.DataFrame(B)
                    i = i + 1

                elif (k == 3):
                    VBT3.append(origin_data["velocity"][i])
                    position3.append(origin_data["position"][i])
                    C = {"velocity": VBT3, "position": position3}
                    division3 = pd.DataFrame(C)
                    i = i + 1

            elif (origin_data["velocity"][i-1] != 0):
                if (k == 1):
                    VBT1.append(origin_data["velocity"][i])
                    position1.append(origin_data["position"][i])
                    A = {"velocity": VBT1, "position": position1}
                    division1 = pd.DataFrame(A)
                    i = i + 1

                elif (k == 2):
                    VBT2.append(origin_data["velocity"][i])
                    position2.append(origin_data["position"][i])
                    B = {"velocity": VBT2, "position": position2}
                    division2 = pd.DataFrame(B)
                    i = i + 1

                elif (k == 3):
                    VBT3.append(origin_data["velocity"][i])
                    position3.append(origin_data["position"][i])
                    C = {"velocity": VBT3, "position": position3}
                    division3 = pd.DataFrame(C)

                    i = i + 1
        else:
            i = i + 1

# 计算平均值和最大值

    if (division2.empty):
        division1["V_Mean"] = division1["velocity"].mean()
        division1["V_Max"] = division1["velocity"].max()
        division1.to_csv("C:\\Users\\Administrator\\Desktop\\915velocity\\915result\\" + all_files + "_1.csv", index=False)
    else:
        division1["V_Mean"] = division1["velocity"].mean()
        division1["V_Max"] = division1["velocity"].max()
        division2["V_Mean"] = division2["velocity"].mean()
        division2["V_Max"] = division2["velocity"].max()
        division3["V_Mean"] = division3["velocity"].mean()
        division3["V_Max"] = division3["velocity"].max()
        division1.to_csv("C:\\Users\\Administrator\\Desktop\\915velocity\\915result\\" + all_files + "_1.csv", index=False)
        division2.to_csv("C:\\Users\\Administrator\\Desktop\\915velocity\\915result\\" + all_files + "_2.csv", index=False)
        division3.to_csv("C:\\Users\\Administrator\\Desktop\\915velocity\\915result\\" + all_files + "_3.csv", index=False)
