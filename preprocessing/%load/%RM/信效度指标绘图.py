import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import heapq


# 读取原始数据
file1 = "C:/Users/Administrator/Desktop/R&V/Reliability.csv"
file2 = "C:/Users/Administrator/Desktop/R&V/Validity.csv"
reliability = pd.read_csv(file1, encoding='utf-8')
validity = pd.read_csv(file2,encoding='utf-8')
plt.figure(1)
plt.plot(list(reliability['Load%']), list(reliability['Pearson(r)']), linewidth=0.4, color='red', label='Pearson（r）')
plt.plot(list(reliability['Load%']), list(reliability['R2']), linewidth=0.4, color='blue', label='R2')
plt.plot(list(reliability['Load%']), list(reliability['SEM1']), linewidth=0.4, color='blue', label='R2')
# plt.plot(list(reliability['Load%']), list(reliability['SEM2']), linewidth=0.4, color='blue', label='R2')
plt.show()
plt.figure(2)
plt.plot(list(validity['Load%']), list(validity['ICC']), linewidth=0.4, color='red', label='Pearson（r）')
plt.plot(list(validity['Load%']), list(validity['CMC']), linewidth=0.4, color='blue', label='R2')
plt.show()
