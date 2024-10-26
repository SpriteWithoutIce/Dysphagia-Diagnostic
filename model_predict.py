import torch
import numpy as np
import pandas as pd
import torch.nn.functional as F
import torch.nn as nn
# Load the model
model = torch.load("model_0725_yzt_2.pkl")

data_test = pd.read_csv("./testAyzt.csv")

data_test_1 = data_test["heartbeat_signals"].str.split(",", expand=True)
ids = data_test["id"].values
data_test_2 = np.array(data_test_1).astype("float32").reshape(-1, 100, 1)
torch.set_printoptions(precision=7)

x_test = torch.tensor(data_test_2)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)

x_test = x_test.to(device)
# 设置批处理大小
batch_size = 128

# 将 x_test 分成多个小批次
num_samples = len(x_test)
num_batches = (num_samples + batch_size - 1) // batch_size

# 初始化一个空列表来存储所有批次的模型输出
all_outputs = []

# 将模型设为评估模式，这会关闭模型中的 Dropout 和 BatchNorm 层
model.eval()

# 在没有梯度计算的情况下，对每个批次进行推理
with torch.no_grad():
    for i in range(num_batches):
        start_idx = i * batch_size
        end_idx = min((i + 1) * batch_size, num_samples)
        inputs_batch = x_test[start_idx:end_idx]

        # 对当前批次的数据进行推理
        outputs_batch = model(inputs_batch)

        # 将当前批次的模型输出添加到列表中
        all_outputs.append(outputs_batch.prediction_logits)

# 将所有批次的模型输出拼接成一个张量
all_outputs_tensor = torch.cat(all_outputs, dim=0)
normalized_outputs = F.softmax(all_outputs_tensor, dim=1)
# 将模型输出从GPU移动到CPU
predicted_labels_cpu = normalized_outputs.cpu()

# 将CPU上的张量转换为NumPy数组
predicted_labels_np = predicted_labels_cpu.numpy()
torch.set_printoptions(precision=8)
numpy_array_1 = pd.DataFrame(predicted_labels_np)
numpy_array_1.columns = ["label_0", "label_1", "label_2", "label_3"]
numpy_array_1.index = ids

numpy_array_1.to_csv("./0709_model_2.csv", index=True)
