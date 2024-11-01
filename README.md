> In situ fully integrated dysphagia assisted diagnostic platform

## 文件目录

* answer：存放每个数据集test结果
* bluetooth：网页连接蓝牙（作废）
* conclusion：几个重点数据集的结果
* config：存模型参数配置文件
* data：存数据集train/test文件
* exp：对比实验模型代码
* exp_csv：对比实验部分数据集
* picture：画图
* save_models：数据集训练出来的模型
* signal：原始信号及处理代码
* templates：网页（作废）
* training：训练集迭代实验
* web：网页
* mini-program：小程序

## 模型训练

模型训练及评估已经集成到main分支下的`patchTST.py`内

步骤：

1. 在signal文件夹下运行`train_test.py`，分割数据集

2. 把分割好的数据集放在data文件夹内

3. 在config目录下新建训练的配置文件（`.yaml`文件），填写分割的数据集csv文件名以及分类的类数

4. 回到最外层文件夹下，运行：

   ```bash
   python ./patchTST.py --config ./config/your_yaml.yaml
   ```

   会显示test集的结果，每一类的分类accuracy，生成的model存在save_model文件夹内，预测结果在answer文件夹内
