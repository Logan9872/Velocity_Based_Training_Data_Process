import os
import numpy as np
import pingouin as pg
import pandas as pd

dirs = os.listdir("C:/Users/Administrator/Desktop/WSY_ICC_data")
for all_files in dirs:
    # 读取原始数据
    file = "C:/Users/Administrator/Desktop/WSY_ICC_data/" + all_files + ""
    # file = "C:/Users/Administrator/Desktop/data/all.csv"

    origin = pd.read_excel(file)
    print(origin)
    VBT_ICC = pd.DataFrame()
    Opti_ICC = pd.DataFrame()
    # # 生成VBT的list
    VBT_ICC["velocity"] = origin['VBT']
    VBT_ICC.insert(0, "reader", "A")
    VBT_ICC.insert(0, "target", range(VBT_ICC.shape[0]))
    ICC_data = pd.concat([VBT_ICC, Opti_ICC])  # 将VBT和Opti两个速度列表合并成一个
    print(ICC_data)

    # 生成Opti的list
    Opti_ICC["velocity"] =origin['OPTI']
    Opti_ICC = Opti_ICC.replace(np.nan, 0)
    Opti_ICC.insert(0, "reader", "B")
    Opti_ICC.insert(0, "target", range(Opti_ICC.shape[0]))
    ICC_data = pd.concat([VBT_ICC, Opti_ICC])  # 将VBT和Opti两个速度列表合并成一个
    print(ICC_data)
    # ———————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # targets 为目标数据的分类（每条数据一类），raters为评判人的分类，ratings为实际数据。
    ICC = pg.intraclass_corr(data=ICC_data, targets="target", raters="reader", ratings="velocity")
    print(ICC)
    print(file)
    origin["ICC"] = ICC["ICC"][3]
    origin.to_csv("C:\\Users\\Administrator\\Desktop\\WSY_ICC_data\\"+all_files+"", index=False)