import csv
import matplotlib.pyplot as plt

# 打开CSV文件
with open('./signal_摩擦电发音_1.csv', 'r', newline='') as csvfile:
    reader = csv.reader(csvfile)
    rows = list(reader)[1:]
    data = []

    for i, row in enumerate(rows):
        third_column = row[2]
        if third_column != '4':
            continue
        second_column = row[1].split(',')
        second_column = [float(num) for num in second_column]
        data.append(second_column)
        plt.figure(figsize=(10, 6))  # 设置图表大小
        plt.plot(second_column, label=f'Signal {i + 1}')  # 绘制折线图
        plt.xlabel('Data')  # 设置x轴标签
        plt.ylabel('Value')  # 设置y轴标签
        plt.grid(True)  # 显示网格
        # plt.show()  # 显示图形
        plt.savefig("1-U.png")
        exit(0)
