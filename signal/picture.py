import matplotlib.pyplot as plt
import numpy as np
import csv
from scipy.ndimage import gaussian_filter

time = []
vol = []


with open("干咽数据/7月3日/07032140干咽第十七组.data", "r") as datafile:
    for _ in range(9):
        next(datafile, None)

    for line in datafile:
        numbers = line.strip().split()
        # print(numbers)
        if len(numbers) == 2:
            try:
                time_val = float(numbers[0])
                vol_val = float(numbers[1])
                time.append(time_val)
                vol.append(vol_val)
            except ValueError:
                print(f"无法将 {numbers} 转换为浮点数")

# 绘制图形
plt.figure(figsize=(100, 6))  # 设置图形大小
plt.plot(time, vol, marker='o')  # 绘制折线图，并用'o'标记每个数据点
plt.xlabel('Time')  # 设置x轴标签
plt.ylabel('Volume')  # 设置y轴标签
plt.title('Time vs Volume')  # 设置图形标题
plt.grid(True)  # 显示网格线
plt.show()  # 显示图形
