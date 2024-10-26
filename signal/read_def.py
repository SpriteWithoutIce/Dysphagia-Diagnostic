import matplotlib.pyplot as plt
import numpy as np
import csv
from scipy.ndimage import gaussian_filter

paths = ["meas_plotter_20240913_185344.txt",
         "meas_plotter_20240913_185512.txt",
         "meas_plotter_20240913_185641.txt",
         "meas_plotter_20240913_185812.txt"
         ]


def read_csv(path):
    time = []
    vol = []
    path = "./data/第四个/lyh咀嚼/"+path
    ranges = []
    with open(path, "r", encoding='utf-8') as datafile:
        first_line = True
        for line in datafile:
            line = line.strip()
            if first_line:  # 处理第一行
                pairs = line.split('，')  # 使用中文逗号分割
                for pair in pairs:
                    pair = pair.strip()
                    print(pair)
                    if '（' in pair and '）' in pair:
                        if ',' in pair:
                            start, end = pair[1:-1].split(',')  # 使用中文逗号分割
                        try:
                            start_val = float(start)
                            end_val = float(end)
                            ranges.append((start_val, end_val))
                        except ValueError:
                            print(f"无法将 {pair} 转换为浮点数")
                first_line = False
            else:  # 处理第二行及以后的数据
                numbers = line.split()
                if len(numbers) == 2:
                    try:
                        time_val = float(numbers[0])
                        vol_val = float(numbers[1])
                        time.append(time_val)
                        vol.append(vol_val)
                    except ValueError:
                        print(f"无法将 {numbers} 转换为浮点数")

    for j in range(len(time)):
        time[j] += 60
    mean_value = np.mean(vol)
    for i in range(len(vol)):
        vol[i] -= mean_value

    # # 绘制图形
    # plt.figure(figsize=(100, 6))  # 设置图形大小
    # plt.plot(time, vol, marker='o')  # 绘制折线图,并用'o'标记每个数据点
    # plt.xlabel('Time')  # 设置x轴标签
    # plt.ylabel('Volume')  # 设置y轴标签
    # plt.title('Time vs Volume')  # 设置图形标题
    # plt.grid(True)  # 显示网格线
    # plt.show()
    # exit(0)

    # ranges = [(-9.71481, 1), (-8.24902, 1.5), (-3.15131, 1)]

    next_number = 1

    # 尝试读取CSV文件的最后一行以获取最后一个编号
    try:
        with open('signal_1007_lyh.csv', 'r', newline='') as csvfile:
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
    for i, (start, length) in enumerate(ranges, 1):
        start_index = None
        # start += 60
        for j, t in enumerate(time):
            if t >= start:
                start_index = j
                break
        end = min(int(start_index + 200*length+1), len(time))

        time_slice = time[start_index:end]  # 直接使用切片来获取数据
        vol_slice = vol[start_index:end]

        # 高斯滤波器参数
        sigma = 5  # 标准差,可以根据需要调整
        # 对vol_slice进行高斯滤波
        vol_slice_smoothed = gaussian_filter(vol_slice, sigma=sigma)

        # 降采样：每5/10个点求一个平均值,并舍弃最后一个点(如果不足5个)
        downsampled_time = []
        downsampled_vol = []
        for j in range(0, len(time_slice) - len(time_slice) % int(2*length), int(2*length)):
            time_chunk = time_slice[j:j+int(2*length)]
            vol_chunk = vol_slice_smoothed[j:j+int(2*length)]
            downsampled_time.append(np.mean(time_chunk))
            downsampled_vol.append(np.mean(vol_chunk))

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
        downsampled_vol = downsampled_vol[:100]
        downsampled_vol_str = ','.join(map(str, downsampled_vol))

        # 写入CSV文件
        # 0e 1o 2u
        # 0a 1e 2i 3o 4u
        # 0绿豆糕 1面包 2喝水
        # 0喝水 1八宝粥 2cmb 3喝水
        with open('signal_1007_lyh.csv', 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([str(next_number), downsampled_vol_str, 1])
            next_number += 1

        # 打印降采样后的点的数量
        print(
            f"Range {i}: Number of downsampled time points = {len(downsampled_vol)}")


if __name__ == "__main__":
    for path in paths:
        print(path)
        read_csv(path=path)
