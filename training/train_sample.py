import numpy as np
import pandas as pd
import csv
from collections import Counter

csv_file_path = 'train1.csv'

values = [150]


# 读取CSV文件
df = pd.read_csv(csv_file_path)

# 确保标签列是分类类型
df['label'] = df['label'].astype('category')

for i in values:
    # 为每个标签类别随机抽取10个样本
    samples = []
    for label in df['label'].cat.categories:
        mask = df['label'] == label
        class_samples = df[mask]
        if len(class_samples) >= i:
            sampled = df[mask].sample(n=i, random_state=42)
        else:
            sampled = class_samples
        samples.append(sampled)

    # 合并所有样本
    result_df = pd.concat(samples)

    # 重置索引
    result_df = result_df.reset_index(drop=True)

    string_csv = str(i)+'.csv'
    # 保存到新的CSV文件
    result_df.to_csv(string_csv, index=False)
