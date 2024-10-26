import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 读取CSV文件
df = pd.read_csv('wandb_export_2024-07-20T14_14_27.658+08_00 - 副本.csv')

# 确保'Step'列是数值型
df['Step'] = pd.to_numeric(df['Step'])

# 使用seaborn绘制折线图
sns.lineplot(data=df, x='Step', y='Train', color='#0058cc',
             label='Train', dashes=False, linewidth=2)
sns.lineplot(data=df, x='Step', y='Test', color='#cc5f00',
             label='Test',  dashes=False, linewidth=2)

plt.tick_params(axis='both', which='major', labelsize=14)
# 隐藏横轴的刻度标签
plt.xticks([])

# 添加图例
plt.legend(fontsize=16)

# 添加标题和轴标签
plt.xlabel('Step', fontsize=16)  # 纵轴标签，即使横轴刻度隐藏也可以保留
plt.ylabel('Physiological Signal Loss', fontsize=16)

# 可选：调整图表以适应内容
plt.tight_layout()
plt.savefig('loss.pdf')
plt.savefig('loss.png')
