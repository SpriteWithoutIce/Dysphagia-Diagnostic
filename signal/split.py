import pandas as pd
from sklearn.model_selection import train_test_split

# 读取CSV文件
df = pd.read_csv('signal_0815_yzt.csv')

# 确保label列是分类变量
df['label'] = df['label'].astype('category')

# 分割数据，确保每个类别均匀分配
splits = train_test_split(
    df, test_size=0.5, stratify=df['label'], random_state=42)

# 分别写入两个新的CSV文件
splits[0].to_csv('signal_yzt_1.csv', index=False)
splits[1].to_csv('signal_yzt_2.csv', index=False)

# 重置id列，从0开始编号
splits[0]['id'] = range(len(splits[0]))
splits[1]['id'] = range(len(splits[1]))

# 再次写入新的CSV文件
splits[0].to_csv('signal_yzt_1.csv', index=False)
splits[1].to_csv('signal_yzt_2.csv', index=False)
