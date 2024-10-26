import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import torch.nn as nn
import torch.utils.data as Data
import torch.optim as optim
import torch
# 加载原始数据
class MyData(Data.Dataset):
    def __init__(self, feature, label):
        self.feature = feature # 特征
        self.label = label # 标签

    def __len__(self):
        return len(self.feature)

    def __getitem__(self, idx):
        return self.feature[idx], self.label[idx]

def load_data(batch_size):
    # 加载原始数据
    df_train = pd.read_csv('./train.csv')
    # 拆解heartbeat_signals
    train_signals = np.array(df_train['heartbeat_signals'].apply(lambda x: np.array(list(map(float, x.split(','))),dtype=np.float32)))
    train_labels = np.array(df_train['label'].apply(lambda x:float(x)),dtype=np.float32)
    # 构建pytorch数据类
    train_data = MyData(train_signals,train_labels)
    # 构建pytorch数据集Dataloader
    train_loader = Data.DataLoader(dataset = train_data,batch_size=batch_size,shuffle=True)
    return train_data,train_loader


class model_CNN_1(nn.Module):
    def __init__(self):
        super(model_CNN_1, self).__init__()
        self.conv_unit = nn.Sequential(
            nn.BatchNorm1d(1),
            nn.Conv1d(in_channels=1, out_channels=32, kernel_size=11, stride=1, padding=5),
            nn.LeakyReLU(),
            nn.BatchNorm1d(32),
            nn.Conv1d(in_channels=32, out_channels=64, kernel_size=11, stride=1, padding=5),
            nn.LeakyReLU(),
            nn.BatchNorm1d(64),
            nn.MaxPool1d(4),
            nn.Conv1d(in_channels=64, out_channels=128, kernel_size=3, stride=1, padding=1),
            nn.LeakyReLU(),
            nn.BatchNorm1d(128),
            nn.Conv1d(in_channels=128, out_channels=256, kernel_size=3, stride=1, padding=1),
            nn.LeakyReLU(),
            nn.MaxPool1d(4),
            nn.Dropout(0.1),
        )
        self.dense_unit = nn.Sequential(
            nn.Linear(3072, 1024),
            nn.LeakyReLU(),
            nn.Linear(1024, 128),
            nn.LeakyReLU(),
            nn.Linear(128, 4),
            nn.Softmax(dim=1)
        )

    def forward(self, inputs):
        inputs = inputs.view(inputs.size()[0], 1, inputs.size()[1])
        inputs = self.conv_unit(inputs)
        inputs = inputs.view(inputs.size()[0], -1)
        inputs = self.dense_unit(inputs)
        return inputs


def train_model(model, train_loader):
    model.train()
    running_loss = 0.0
    running_acc = 0.0
    for i, data in enumerate(train_loader):
        inputs, labels = data
        predictions = model(inputs)
        loss = criterion(predictions, labels.long())
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        running_loss += loss.item() * labels.size()[0]
        _, pred = torch.max(predictions, 1)
        num_correct = (pred == labels).sum()
        running_acc += num_correct.item()
    return running_loss, running_acc


def loss_curve(list_loss, list_acc):
    epochs = np.arange(1, len(list_loss) + 1)
    fig, ax = plt.subplots()
    ax.plot(epochs, list_loss, label='loss')
    ax.plot(epochs, list_acc, label='accuracy')
    ax.set_xlabel('epoch')
    ax.set_ylabel('%')
    ax.set_title('loss & accuray ')
    ax.legend()
# 调用定义的加载函数进行数据加载
batch_size = 64
train_data,train_loader = load_data(batch_size)

# 定义模型、loss function
model = model_CNN_1()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(),lr=0.0001)

# 循环20个epoch进行数据训练
list_loss,list_acc = [],[]
for epoch in range(5):
    running_loss,running_acc=train_model(model,train_loader)
    list_loss.append(running_loss/train_data.__len__())
    list_acc.append(running_acc/train_data.__len__())
    print('Train {} epoch, Loss: {:.6f}, Acc:{:.6f}'.format(epoch+1,running_loss/train_data.__len__(),running_acc/train_data.__len__()))

# 绘图查看loss 和 accuracy曲线
loss_curve(list_loss,list_acc)
predict_data=pd.read_csv("./testA.csv")
# 拆解heartbeat_signals
train_signals = np.array(predict_data['heartbeat_signals'].apply(lambda x: np.array(list(map(float, x.split(','))),dtype=np.float32)))

# 构建pytorch数据集Dataloader
train_loader = Data.DataLoader(dataset = train_data,batch_size=batch_size,shuffle=True)
