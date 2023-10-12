import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

file = "C:/Users/Administrator/Desktop/subject/PLT/movement_cycle.csv"

# 绘制散点图以及线性回归
plt.rcParams['font.sans-serif'] = 'Microsoft YaHei'  # 设置中文编码和负号的正常显示

OLC = pd.read_csv(file)
plt.figure(1)
plt.subplot(411)
plt.plot(OLC['x1'], linewidth=0.1, color='blue')
plt.plot(OLC['y1'], linewidth=0.1, color='red')
plt.subplot(412)
plt.plot(OLC['x2'], linewidth=0.1, color='blue')
plt.plot(OLC['y2'], linewidth=0.1, color='red')
plt.subplot(413)
plt.plot(OLC['x3'], linewidth=0.1, color='blue')
plt.plot(OLC['y3'], linewidth=0.1, color='red')
plt.subplot(414)
plt.plot(OLC['x4'], linewidth=0.1, color='blue')
plt.plot(OLC['y4'], linewidth=0.1, color='red')

plt.figure(2)
plt.subplot(411)
plt.plot(OLC['x5'], linewidth=0.1, color='blue')
plt.plot(OLC['y5'], linewidth=0.1, color='red')
plt.subplot(412)
plt.plot(OLC['x6'], linewidth=0.1, color='blue')
plt.plot(OLC['y6'], linewidth=0.1, color='red')
plt.subplot(413)
plt.plot(OLC['x7'], linewidth=0.1, color='blue')
plt.plot(OLC['y7'], linewidth=0.1, color='red')
plt.subplot(414)
plt.plot(OLC['x8'], linewidth=0.1, color='blue')
plt.plot(OLC['y8'], linewidth=0.1, color='red')
plt.figure(3)
plt.subplot(411)
plt.plot(OLC['x9'], linewidth=0.1, color='blue')
plt.plot(OLC['y9'], linewidth=0.1, color='red')
plt.subplot(412)
plt.plot(OLC['x10'], linewidth=0.1, color='blue')
plt.plot(OLC['y10'], linewidth=0.1, color='red')
plt.subplot(413)
plt.plot(OLC['x11'], linewidth=0.1, color='blue')
plt.plot(OLC['y11'], linewidth=0.1, color='red')
plt.subplot(414)
plt.plot(OLC['x12'], linewidth=0.1, color='blue')
plt.plot(OLC['y12'], linewidth=0.1, color='red')
plt.figure(4)
plt.subplot(411)
plt.plot(OLC['x13'], linewidth=0.1, color='blue')
plt.plot(OLC['y13'], linewidth=0.1, color='red')
plt.subplot(412)
plt.plot(OLC['x14'], linewidth=0.1, color='blue')
plt.plot(OLC['y14'], linewidth=0.1, color='red')
plt.subplot(413)
plt.plot(OLC['x15'], linewidth=0.1, color='blue')
plt.plot(OLC['y15'], linewidth=0.1, color='red')
plt.subplot(414)
plt.plot(OLC['x16'], linewidth=0.1, color='blue')
plt.plot(OLC['y16'], linewidth=0.1, color='red')
plt.figure(5)
plt.subplot(411)
plt.plot(OLC['x17'], linewidth=0.1, color='blue')
plt.plot(OLC['y17'], linewidth=0.1, color='red')
plt.subplot(412)
plt.plot(OLC['x18'], linewidth=0.1, color='blue')
plt.plot(OLC['y18'], linewidth=0.1, color='red')
plt.subplot(413)
plt.plot(OLC['x19'], linewidth=0.1, color='blue')
plt.plot(OLC['y19'], linewidth=0.1, color='red')
plt.subplot(414)
plt.plot(OLC['x20'], linewidth=0.1, color='blue')
plt.plot(OLC['y20'], linewidth=0.1, color='red')
plt.figure(6)
plt.subplot(414)
plt.plot(OLC['x21'], linewidth=0.1, color='blue')
plt.plot(OLC['y21'], linewidth=0.1, color='red')

# plt.legend(loc='best')
# plt.xlim(0,1800)#X轴范围
# plt.ylim(-1,1)#显示y轴范围
plt.rcParams['figure.figsize']= (6.0, 4.0)
plt.rcParams['savefig.dpi'] = 400 #图片像素
plt.rcParams['figure.dpi'] = 400 #分辨率

ax = plt.gca()  # 获取当前X和Y的比列
ax.set_aspect(400)  # 按比例缩放
# plt.savefig('01.jpg', bbox_inches='tight')

plt.show()

