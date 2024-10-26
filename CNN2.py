import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import TensorDataset, DataLoader
from sklearn.neighbors import KNeighborsClassifier

data = pd.read_csv("./train1.csv")
data_test = pd.read_csv("./testA1.csv")
data.head()
data_1 = data["heartbeat_signals"].str.split(",", expand=True)
data_test_1 = data_test["heartbeat_signals"].str.split(",", expand=True)
np.array(data.label)
data_2 = np.array(data_1).astype("float32").reshape(-1, 1, 100)
data_test_2 = np.array(data_test_1).astype("float32").reshape(-1, 1, 100)
torch.set_printoptions(precision=7)
x_train = torch.tensor(data_2)
x_test = torch.tensor(data_test_2)
y_train = torch.tensor(data.label, dtype=int)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)

x_train = x_train.to(device)
y_train = y_train.to(device)
x_test = x_test.to(device)
dataset = TensorDataset(x_train, y_train)
train_loader = DataLoader(dataset, batch_size=128, shuffle=True)
test_loader = DataLoader(x_test, batch_size=128, shuffle=True)


class CNN_1(nn.Module):

    def __init__(self):
        super(CNN_1, self).__init__()
        self.conv1 = nn.Conv1d(
            in_channels=1, out_channels=64, kernel_size=7, stride=1, padding=3)
        self.conv2 = nn.Conv1d(
            in_channels=64, out_channels=128, kernel_size=5, stride=1, padding=2)
        self.conv3 = nn.Conv1d(
            in_channels=128, out_channels=256, kernel_size=3, stride=1, padding=1)
        self.conv4 = nn.Conv1d(
            in_channels=256, out_channels=256, kernel_size=3, stride=1, padding=1)
        self.maxpool = nn.MaxPool1d(kernel_size=2)
        self.sleakyrelu = nn.LeakyReLU(negative_slope=0.05)
        self.bn1 = nn.BatchNorm1d(64)
        self.bn2 = nn.BatchNorm1d(128)
        self.bn3 = nn.BatchNorm1d(256)
        self.bn4 = nn.BatchNorm1d(256)
        self.dropout = nn.Dropout(0.2)

        self.linear = nn.Sequential(
            nn.Linear(3072, 4096),
            nn.BatchNorm1d(4096),
            nn.LeakyReLU(negative_slope=0.05),
            nn.Linear(4096, 64),
            nn.BatchNorm1d(64),
            nn.LeakyReLU(negative_slope=0.05),
            nn.Linear(64, 3)
        )

    def forward(self, x):
        x = self.bn1(self.conv1(x))
        x = self.sleakyrelu(x)
        x = self.maxpool(x)
        x = self.bn2(self.conv2(x))
        x = self.sleakyrelu(x)
        x = self.maxpool(x)
        x = self.bn3(self.conv3(x))
        x = self.sleakyrelu(x)
        x = self.bn4(self.conv4(x))
        x = self.sleakyrelu(x)
        x = self.maxpool(x)
        x = self.dropout(x)
        x = torch.flatten(x, start_dim=1)
        x = self.linear(x)
        return x


class CNN_2(nn.Module):
    def __init__(self):
        super(CNN_2, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv1d(in_channels=1, out_channels=16,
                      kernel_size=11, stride=1, padding='same'),
            nn.BatchNorm1d(16),
            nn.LeakyReLU(),

            nn.Conv1d(in_channels=16, out_channels=32,
                      kernel_size=7, stride=1, padding='same'),
            nn.BatchNorm1d(32),
            nn.LeakyReLU(),

            nn.Conv1d(in_channels=32, out_channels=64,
                      kernel_size=5, stride=1, padding=1),
            nn.BatchNorm1d(64),
            nn.LeakyReLU(),
            nn.MaxPool1d(kernel_size=3, stride=2),

            nn.Conv1d(in_channels=64, out_channels=128,
                      kernel_size=3, stride=1, padding=1),
            nn.BatchNorm1d(128),
            nn.LeakyReLU(),

            nn.Conv1d(in_channels=128, out_channels=128,
                      kernel_size=3, stride=1, padding=1),
            nn.BatchNorm1d(128),
            nn.LeakyReLU(),
            nn.MaxPool1d(kernel_size=3, stride=2),
            nn.Dropout(0.2)
        )
        self.linear = nn.Sequential(
            nn.Linear(3072, 4096),
            nn.BatchNorm1d(4096),
            nn.LeakyReLU(),
            nn.Linear(4096, 64),
            nn.BatchNorm1d(64),
            nn.LeakyReLU(),
            nn.Linear(64, 3),
        )

    def forward(self, x):
        x = self.conv(x)
        x = torch.flatten(x, start_dim=1)
        x = self.linear(x)
        return x


# # 初始化模型、损失函数和优化器

# model_1 = CNN_1()
# model_2 = CNN_2()


# # 权值初始化
# for m in model_1.modules():
#     if isinstance(m, nn.Conv1d):
#         nn.init.kaiming_normal_(m.weight, nonlinearity='relu')
#     elif isinstance(m, nn.Linear):
#         nn.init.xavier_normal_(m.weight)

# criterion = nn.CrossEntropyLoss()
# optimizer = optim.Adam(model_1.parameters(), lr=0.00001)

# model_1.to(device)

# num_epochs = 100

# # 全训练集训练
# for epoch in range(num_epochs):
#     model_1.train()
#     running_loss = 0.0
#     for inputs, targets in train_loader:
#         # 前向传播
#         outputs = model_1(inputs)
#         loss = criterion(outputs, targets)
#         # 反向传播和优化
#         optimizer.zero_grad()
#         loss.backward()
#         optimizer.step()
#         running_loss += loss.item()
#     train_loss = running_loss / 100000

#     print('Epoch:{}, train_loss: {:.2e}'.format(epoch + 1, loss.item()))

# # 保存模型
# torch.save(model_1, 'model_1_0702.pkl')
# torch.save(model_2, 'model_2_0702.pkl')

model_1 = torch.load("model_1_0702.pkl")
model_2 = torch.load("model_2_0702.pkl")

model_1.to(device)
model_2.to(device)
# 模型预测
model_1.eval()
model_2.eval()
with torch.no_grad():
    output_1 = model_1(x_test)
    output_2 = model_2(x_test)
output_11 = torch.softmax(output_1, dim=1)
output_22 = torch.softmax(output_2, dim=1)
predict = 0.5 * output_11 + 0.5 * output_22
np.set_printoptions(suppress=True)
predict_cpu = predict.cpu().numpy()
# 预测概率低于0.5的样本处理
numpy_array = predict_cpu
for i in range(numpy_array.shape[0]):
    row = numpy_array[i]
    max_val = np.max(row)
    sorted_row = np.sort(row)
    second_max_val = sorted_row[-2]
    if max_val <= 0.5:
        if max_val - second_max_val >= 0.049:
            row[row != max_val] = 0
            row[row == max_val] = 1
            numpy_array[i] = row
        else:
            min_val = np.min(row)
            second_min_val = np.min(row[row != min_val])
            row[row == min_val] = 0
            row[row == second_min_val] = 0
            numpy_array[i] = row
np.set_printoptions(suppress=True)
numpy_array_1 = pd.DataFrame(numpy_array)
numpy_array_1.columns = ["label_0", "label_1", "label_2"]
numpy_array_1.index = list(range(1, 44))

numpy_array_1.to_csv("./numpy_array_0702.csv", index=True)
