import matplotlib.pyplot as plt
import numpy as np
import csv
from scipy.ndimage import gaussian_filter

time = []
vol = []


with open("./打嗝补充2/打嗝第七组.data", "r") as datafile:
    for _ in range(9):
        next(datafile, None)

    # 从第10行开始读取
    for line in datafile:
        # 去除行尾的换行符并分割字符串,得到两个数
        numbers = line.strip().split()
        # print(numbers)
        # 检查是否确实有两个数,并且它们都是可转换为浮点数的
        if len(numbers) == 2:
            try:
                # 尝试将两个数转换为浮点数
                time_val = float(numbers[0])
                vol_val = float(numbers[1])
                # 添加到对应的列表中
                time.append(time_val)
                vol.append(vol_val)
            except ValueError:
                # 如果转换失败,则忽略这一行或打印错误消息
                print(f"无法将 {numbers} 转换为浮点数")

# # 绘制图形
# plt.figure(figsize=(100, 6))  # 设置图形大小
# plt.plot(time, vol, marker='o')  # 绘制折线图,并用'o'标记每个数据点
# plt.xlabel('Time')  # 设置x轴标签
# plt.ylabel('Volume')  # 设置y轴标签
# plt.title('Time vs Volume')  # 设置图形标题
# plt.grid(True)  # 显示网格线
# plt.show()  # 显示图形
# exit(0)

ranges = [1, 3, 6, 8.5, 13, 15, 18.5, 22, 25, 28, 31, 34, 37, 40.5,
          43.5, 47, 50, 53, 56, 59.5, 63, 66, 69.5, 72.5, 75, 78, 81]
cycle = 2
next_number = 1

# 尝试读取CSV文件的最后一行以获取最后一个编号
try:
    with open('signal_0815_yzt.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        # 读取所有行,但只保留最后一行
        rows = list(reader)
        if rows:
            # 假设编号在第一列,直接转换为整数
            last_number = int(rows[-1][0])
            next_number = last_number + 1
        else:
            next_number = 1
except FileNotFoundError:
    # 如果文件不存在,则使用初始编号
    pass
except (IndexError, ValueError):
    # 如果文件为空或格式不正确,也使用初始编号
    pass
# 遍历每个范围并绘制数据
for i, start in enumerate(ranges, 1):

    end = start+cycle
    # 初始化当前范围内的time和vol列表
    time_slice = []
    vol_slice = []

    # 遍历time和vol列表,截取当前范围内的数据
    for t, v in zip(time, vol):
        if start <= t <= end:
            time_slice.append(t)
            vol_slice.append(v)

    # 高斯滤波器参数
    sigma = 5  # 标准差,可以根据需要调整
    # 对vol_slice进行高斯滤波
    vol_slice_smoothed = gaussian_filter(vol_slice, sigma=sigma)

    # 降采样：每5/10个点求一个平均值,并舍弃最后一个点（如果不足5个）
    downsampled_time = []
    downsampled_vol = []
    down = (int)(2*cycle)
    for j in range(0, len(time_slice) - len(time_slice) % down, down):
        time_chunk = time_slice[j:j+down]
        vol_chunk = vol_slice_smoothed[j:j+down]
        downsampled_time.append(np.mean(time_chunk))
        downsampled_vol.append(np.mean(vol_chunk))

    # 0.5s
    if cycle == 0.5:
        downsampled_time = downsampled_time[:-1]  # 保留除最后一个元素之外的所有元素
        downsampled_vol = downsampled_vol[:-1]

    # # *-1
    # for j in range(len(downsampled_vol)):
    #     downsampled_vol[j] *= -1

    mean_value = np.mean(downsampled_vol)
    downsampled_vol = downsampled_vol-mean_value

    # 基线拉平
    p = np.polyfit(downsampled_time, downsampled_vol, 1)
    slope, intercept = p
    trend_values = np.polyval(p, downsampled_time)
    flattened_values = downsampled_vol - trend_values
    downsampled_vol = flattened_values

    # # 绘制图形
    # plt.figure(figsize=(10, 6))
    # plt.plot(downsampled_time, downsampled_vol, marker='o')
    # plt.xlabel('Time')
    # plt.ylabel('Volume')
    # plt.title(f'Time vs Volume for Range {i}: {start} to {end} (Downsampled)')
    # plt.grid(True)
    # plt.show()

    # 将降采样后的vol数组转换为以逗号分隔的字符串
    downsampled_vol_str = ','.join(map(str, downsampled_vol))

    # 写入CSV文件
    # 0e 1o 2u 3a 4i
    with open('signal_0815_yzt.csv', 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([str(next_number), downsampled_vol_str, 4])
        next_number += 1

    # 打印降采样后的点的数量
    print(
        f"Range {i}: Number of downsampled time points = {len(downsampled_time)}")
