import pandas as pd

df_predictions = pd.read_csv("./conclusion/0811_model_摩擦电发音(3).csv")
df_answers = pd.read_csv("./data/test_dataset_摩擦电发音.csv")

df_predictions['id'] = pd.to_numeric(
    df_predictions['id'], errors='coerce').dropna().astype(int)
df_answers['id'] = pd.to_numeric(
    df_answers['id'], errors='coerce').dropna().astype(int)

df_predictions['Predicted_Label'] = df_predictions.iloc[:, 1:].idxmax(
    axis=1).apply(lambda x: int(x.lstrip('label_')))

df_answers['answer'] = pd.to_numeric(
    df_answers['answer'], errors='coerce').dropna().astype(int)

# 合并两个DataFrame以比较预测结果和实际结果
merged_df = pd.merge(df_predictions[['id', 'Predicted_Label']], df_answers[[
                     'id', 'answer']], on='id', how='left')

# 计算正确率
accuracy = merged_df[merged_df['answer'].notna()]['Predicted_Label'].eq(
    merged_df['answer']).mean()

print(f"accuracy: {accuracy:.4f}")

# 假设 'answer' 是实际类别列，'Predicted_Label' 是预测类别列
accuracy_by_class = (merged_df['Predicted_Label'] == merged_df['answer'])
accuracy_by_class = accuracy_by_class.groupby(merged_df['answer']).mean()

# 打印每一类的准确率
print(accuracy_by_class)

# 创建一个只包含id和Predicted_Label的新DataFrame
result_df = df_predictions[['id', 'Predicted_Label']]

# 将这个新DataFrame保存到一个新的CSV文件中
# 使用index=False来避免将索引保存为文件的一列
# result_df.to_csv("0709_model_2_with_labels.csv", index=False)

# 打印一条消息确认文件已保存
print("Predicted labels have been saved")
