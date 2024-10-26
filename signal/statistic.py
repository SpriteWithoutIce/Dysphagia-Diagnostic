import pandas as pd

df = pd.read_csv('../data/testA_answer.csv')

category_counts = df.iloc[:, 2].value_counts()

# 按照类别值从小到大排序
sorted_category_counts = category_counts.sort_index()

# 打印结果
print(sorted_category_counts)
