import numpy as np
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6, 6))

ax.pie([3.8, 6.8, 5.3, 7.9, 9.5, 6.1, 8.7, 5.6, 5, 8, 17.4, 11.5, 4.4],
       wedgeprops={'width': 0.5},
       startangle=90,
       colors=['#7c55c8', '#6e96c9', '#c58cd3', '#bf599b', '#f39557', '#fbb1a2', '#ffde02', '#a6d608', '#cbb9ab', '#998e8f', '#ffb59a', '#c1f9a2', '#a1d7ef'])

plt.show()

# # library
# import matplotlib.pyplot as plt

# # create data
# # 创建数据
# names = '0.85', '0.83', '0.91', '0.90', '0.98',
# size = [11, 21, 16, 24, 28]


# # Label distance: gives the space between labels and the center of the pie
# # labeldistance给出标签和饼图中心之间的间距
# plt.pie(size, labels=names, labeldistance=0.75,
#         wedgeprops=dict(width=0.3, edgecolor='w'))

# # 设置等比例轴，x和y轴等比例
# plt.axis('equal')
# plt.show()
