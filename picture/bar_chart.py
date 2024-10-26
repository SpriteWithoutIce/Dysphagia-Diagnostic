import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import cm


def draw_bar(key_name, key_values):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.family'] = 'Arial'
    # 标准柱状图的值

    # def autolable(rects):
    #     for rect in rects:
    #         height = rect.get_height()
    #         if height >= 0:
    #             plt.text(rect.get_x()+rect.get_width()/2.0 -
    #                      0.3, height+0.02, '%.3f' % height)
    #         else:
    #             plt.text(rect.get_x()+rect.get_width()/2.0 -
    #                      0.3, height-0.06, '%.3f' % height)
    #             # 如果存在小于0的数值，则画0刻度横向直线
    #             plt.axhline(y=0, color='black')
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
               fontsize=12, fontname='Times New Roman')
    plt.show()


if __name__ == '__main__':

    # multi_corr()
    key_name = ['Bow', 'Chew', 'Cough', 'Swallow']
    key_values = [1, 1, 0.692, 0.952]
    draw_bar(key_name, key_values)
