
import numpy as np
import pandas as pd
import os


dirs = os.listdir("C:/Users/Administrator/Desktop/10%VelocityData除信号/C&E/Concentric/PreTestConcentric/")

for all_files in dirs:
    # 读取原始数据
    file = "C:/Users/Administrator/Desktop/10%VelocityData除信号/C&E/Concentric/PreTestConcentric/" + all_files + ""
    origin_data = pd.read_csv(file, skip_blank_lines=False)
    print(origin_data)
    origin_data["Velocity"] = np.nan_to_num(origin_data["Velocity"])
    print(origin_data)

    title = all_files[:38]  # 读取文件名
    title_csv = title[:-4]

    division1 = pd.DataFrame()
    division2 = pd.DataFrame()
    division3 = pd.DataFrame()
    Velocity1 = []
    Velocity2 = []
    Velocity3 = []

    i = 0
    k = 0

    # 判断当前是否为空，如果是则i+1继续遍历，同时记录遇到空的数值j+1
    # 如果不为空则将数据存入list，i+1,j+1
    # 同时判断遇到空的个数j，若j大于200则认为是第二个动作，将其存入新的list
    #

    for i in range(len(origin_data["Velocity"])):

        if (origin_data["Velocity"][i] == 0):
            i = i + 1
# 当有数值的时候进入，如果前一个数为0，则存入list1
        elif (origin_data["Velocity"][i] != 0):
            if(i == 0):
                k = k+1
                if (k == 1):
                    Velocity1.append(origin_data["Velocity"][i])
                    A = {"Velocity": Velocity1}
                    division1 = pd.DataFrame(A)
                    i = i + 1

                elif (k == 2):
                    Velocity2.append(origin_data["Velocity"][i])
                    B = {"Velocity": Velocity2}
                    division2 = pd.DataFrame(B)
                    i = i + 1

                elif (k == 3):
                    Velocity3.append(origin_data["Velocity"][i])
                    C = {"Velocity": Velocity3}
                    division3 = pd.DataFrame(C)
                    i = i + 1
            elif (origin_data["Velocity"][i-1] == 0):
                # 如果前一个数是0，后一个数不是，则k+1,k为遇到峰的个数
                k = k+1
                if(k == 1):
                    Velocity1.append(origin_data["Velocity"][i])
                    A = {"Velocity": Velocity1}
                    division1 = pd.DataFrame(A)
                    i = i + 1

                elif(k == 2):
                    Velocity2.append(origin_data["Velocity"][i])
                    B = {"Velocity": Velocity2}
                    division2 = pd.DataFrame(B)
                    i = i + 1

                elif (k == 3):
                    Velocity3.append(origin_data["Velocity"][i])
                    C = {"Velocity": Velocity3}
                    division3 = pd.DataFrame(C)
                    i = i + 1
            elif (origin_data["Velocity"][i-1] != 0):
                if (k == 1):
                    Velocity1.append(origin_data["Velocity"][i])
                    A = {"Velocity": Velocity1}
                    division1 = pd.DataFrame(A)
                    i = i + 1

                elif (k == 2):
                    Velocity2.append(origin_data["Velocity"][i])
                    B = {"Velocity": Velocity2}
                    division2 = pd.DataFrame(B)
                    i = i + 1

                elif (k == 3):
                    Velocity3.append(origin_data["Velocity"][i])
                    C = {"Velocity": Velocity3}
                    division3 = pd.DataFrame(C)
                    i = i + 1
        else:
            i = i + 1
        # print(k)
        print(title_csv)
# 计算平均值和最大值

    if (division2.empty):
        # division1["Velocity_Mean"] = division1["Velocity"].mean()
        # division1["Velocity_Max"] = division1["Velocity"].max()
        division1.to_csv("C:\\Users\\Administrator\\Desktop\\10%VelocityData除信号\\C&E\\ConcentricResult\\PreTestConcentric\\" + title_csv + "-01.csv", index=False)

    elif(division3.empty):
        # division1["Velocity_Mean"] = division1["Velocity"].mean()
        # division1["Velocity_Max"] = division1["Velocity"].max()
        # division2["Velocity_Mean"] = division2["Velocity"].mean()
        # division2["Velocity_Max"] = division2["Velocity"].max()

        division1.to_csv("C:\\Users\\Administrator\\Desktop\\10%VelocityData除信号\\C&E\\ConcentricResult\\PreTestConcentric\\" + title_csv + "-01.csv", index=False)
        division2.to_csv("C:\\Users\\Administrator\\Desktop\\10%VelocityData除信号\\C&E\\ConcentricResult\\PreTestConcentric\\" + title_csv + "-02.csv", index=False)
    else:
        # division1["Velocity_Mean"] = division1["Velocity"].mean()
        # division1["Velocity_Max"] = division1["Velocity"].max()
        # division2["Velocity_Mean"] = division2["Velocity"].mean()
        # division2["Velocity_Max"] = division2["Velocity"].max()
        # division3["Velocity_Mean"] = division3["Velocity"].mean()
        # division3["Velocity_Max"] = division3["Velocity"].max()
   
        division1.to_csv("C:\\Users\\Administrator\\Desktop\\10%VelocityData除信号\\C&E\\ConcentricResult\\PreTestConcentric\\" + title_csv + "-01.csv", index=False)
        division2.to_csv("C:\\Users\\Administrator\\Desktop\\10%VelocityData除信号\\C&E\\ConcentricResult\\PreTestConcentric\\" + title_csv + "-02.csv", index=False)
        division3.to_csv("C:\\Users\\Administrator\\Desktop\\10%VelocityData除信号\\C&E\\ConcentricResult\\PreTestConcentric\\" + title_csv + "-03.csv", index=False)