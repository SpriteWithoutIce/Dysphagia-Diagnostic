import pandas as pd

df = pd.read_csv('testA1.csv')

df_shuffled = df.sample(frac=1).reset_index(drop=True)

df_shuffled.to_csv('shuffled_testA1.csv', index=False)
