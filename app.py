import numpy as np
from flask import Flask, request, jsonify, render_template
import torch
import torch.nn.functional as F
import pandas as pd
app = Flask(__name__, template_folder='templates')
model = torch.load('model_patch.pkl')
model.eval()


@app.route('/')
def home():
    return render_template('page.html')


@app.route('/predict', methods=['POST'])
def predict():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    features_list = list(request.form.values())
    features_list = [value.split(",") for value in features_list]
    features = np.array(features_list).astype("float32").reshape(-1, 205, 1)
    torch.set_printoptions(precision=7)
    features = torch.tensor(features)
    features=features.to(device)
    with torch.no_grad():
        predict_outcome_list = model(features)
    predict_outcome = F.softmax(predict_outcome_list.prediction_logits, dim=1)
    predicted_labels_cpu = predict_outcome.cpu()
    predicted_labels_np = predicted_labels_cpu.numpy()
    torch.set_printoptions(precision=8)
    labels = ['干咽', '喝水', '吃面包', '吃水果']
    data = predicted_labels_np[0].tolist()  # 假设你想要获取第一行数据
    data_formatted = [round(value, 4) for value in data]
    # 渲染模板，并传递数据到HTML页面
    max_value=max(data)
    max_index = data.index(max_value)
    return render_template('page.html', labels=labels, data=data, max_index=max_index)
    # numpy_array_1=pd.DataFrame(predicted_labels_np)
    # return render_template('page.html', prediction_display_area='分类概率为：{}'.format(predicted_labels_np))


if __name__ == "__main__":
    app.run(port=80, debug=True)
