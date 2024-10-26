from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import csv

# signal,0.9303,0.96,0.92,0.91,0.93,0.98
# 'Bow', 'Chew', 'Cough', 'Swallow', 'Belch'
# pro,0.9656,0.9483,0.9444,0.9583,0.9243,1.00
# 'A', 'E', 'I', 'O', 'U'
# eat,0.9569, 0.9815,0.9778,0.8235
# 'Drinking', 'Porridge', 'Bread'


def heat(key_name, key_values, accuracy, string_value):
    plt.figure()
    if len(key_values) == 4:
        data = [[key_name[0], key_name[0], key_values[0]*100], [key_name[1], key_name[1],  key_values[1]*100],
                [key_name[2], key_name[2],  key_values[2] *
                100], [key_name[3], key_name[3],  key_values[3]*100]]
    elif len(key_values) == 3:
        data = [[key_name[0], key_name[0], key_values[0]*100], [key_name[1], key_name[1],  key_values[1]*100],
                [key_name[2], key_name[2],  key_values[2] * 100]]
    else:
        data = [[key_name[0], key_name[0], key_values[0]*100], [key_name[1], key_name[1],  key_values[1]*100],
                [key_name[2], key_name[2],  key_values[2] *
                100], [key_name[3], key_name[3],  key_values[3]*100],
                [key_name[4], key_name[4],  key_values[4]*100]]

    # 提取热力图的行和列标签以及对应的值
    rows = key_name  # 行标签
    cols = key_name  # 列标签，这里假设列标签与行标签相同
    values = [item[2] for item in data]  # 热力图的数值

    # 创建一个二维数组，初始化为0
    matrix = np.zeros((len(rows), len(cols)))
    mask = np.ones((len(rows), len(cols)))
    # 填充矩阵，这里假设是对称矩阵，即行标签和列标签相同
    for i in range(len(rows)):
        matrix[i, i] = values[i]
        mask[i, i] = 0
    # 使用seaborn绘制热力图
    ax = sns.heatmap(matrix, annot=True, fmt=".2f", mask=mask, xticklabels=rows, yticklabels=rows,
                     cmap='coolwarm', annot_kws={'size': 14})

    # 添加黑色边框
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color('black')
        spine.set_linewidth(0.5)
    # 显示图表
    # 添加标题
    accuracy = accuracy*100
    accuracy_str = f'Overall Accuracy: {accuracy:.2f}%'
    plt.title(accuracy_str, fontsize=16)
    plt.xticks(fontsize=17)
    plt.yticks(fontsize=17)
    plt.xticks(rotation=0)
    plt.yticks(rotation=360)
    plt.tight_layout()
    plt.savefig(string_value+'_1.png')
    plt.savefig(string_value+'_1.pdf')
    plt.close()


def draw_bar(key_name, key_values, string_value):
    plt.figure()
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.family'] = 'Arial'

    def autolable(rects, ax):
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2.0, 1.002*height,
                    '%.3f' % height, ha='center', va='bottom')
    # 归一化
    norm = plt.Normalize(0.9, 1)
    norm_values = norm(key_values)
    # 定义自定义颜色映射
    colors = [(1, 1, 1),  # 白色（最浅灰色）
              (0.5, 0.5, 0.6)]  # 浅蓝色
    my_cmap = LinearSegmentedColormap.from_list('my_cmap', colors)
    map_vir = cm.get_cmap(name='viridis')
    # colors = my_cmap(norm_values)
    colors = map_vir(norm_values)
    fig = plt.figure()  # 调用figure创建一个绘图对象
    plt.subplot(111)
    ax = plt.bar(key_name, key_values, width=0.5, color=colors,
                 edgecolor='black')  # edgecolor边框颜色

    sm = cm.ScalarMappable(cmap=map_vir, norm=norm)  # norm设置最大最小值
    sm.set_array([])
    plt.colorbar(sm)
    autolable(ax, plt.gca())
    plt.ylabel('Test Accuracy', rotation=90,
               fontsize=12, fontname='Arial')
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.savefig(string_value+'_2.png')
    plt.close()


if __name__ == '__main__':
    with open('./answer.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            string_value = "./hot/"+row[0]
            acc = float(row[1])
            number_values = [float(value) for value in row[2:]]
            # multi_corr()
            key_name = ['A', 'E', 'I', 'O', 'U']
            key_values = number_values
            # draw_bar(key_name, key_values, string_value)
            heat(key_name, key_values, acc, string_value)
