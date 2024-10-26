# 导入必要的库
from pyecharts import options as opts
from pyecharts.charts import HeatMap
import random

# 生成示例数据
data = [["bow", "bow", 100], ["chew", "chew", 94], [
    "cough", "cough", 95], ["swallow", "swallow", 100]]
# print(data)
list1 = ["bow", "chew", "cough", "swallow"]
# 创建基础热力图
heatmap_basic = (
    HeatMap()
    .add_xaxis(list1)
    .add_yaxis(
        series_name="",
        yaxis_data=list1,
        value=data,
        label_opts=opts.LabelOpts(is_show=True, position="inside"),
    )
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(
            is_piecewise=False,
            max_=100,
            min_=0,
            range_color=['#fffb00', '#1b3090'],
            pos_bottom="0%",  # 设置图例底部位置
            pos_top="50%",
        ),
        xaxis_opts=opts.AxisOpts(
            axisline_opts=opts.AxisLineOpts(is_show=False)),  # 隐藏x轴轴线
        yaxis_opts=opts.AxisOpts(
            axisline_opts=opts.AxisLineOpts(is_show=False))
    )

)
# 渲染图表
heatmap_basic.render("heatmap_basic.html")
