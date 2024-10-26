import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def heat(key_name, key_values):
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
                     cmap='coolwarm')

    # 添加黑色边框
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color('black')
        spine.set_linewidth(0.5)
    # 显示图表
    # 添加标题
    plt.title('Overall Accuracy: 93.51%', fontsize=12)
    plt.show()


if __name__ == '__main__':
    heat()
