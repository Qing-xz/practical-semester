# Pumpkin 数据集数据分析
## 数据说明
| 字段名 | 非空数量 | 数据类型 | 字段含义 |
| --- | --- | --- | --- |
| City Name | 1757 | object | 城市名称，记录南瓜交易或相关事件发生的城市 |
| Type | 45 | object | 南瓜类型 |
| Package | 1757 | object | 包装方式 |
| Variety | 1752 | object | 南瓜品种 |
| Sub Variety | 296 | object | 南瓜子品种 |
| Grade | 0 | float64 | 等级 |
| Date | 1757 | object | 交易日期 |
| Low Price | 1757 | float64 | 最低价格 |
| High Price | 1757 | float64 | 最高价格 |
| Mostly Low | 1654 | float64 | 多数情况下的最低价格 |
| Mostly High | 1654 | float64 | 多数情况下的最高价格 |
| Origin | 1754 | object | 产地 |
| Origin District | 131 | object | 产地所在区域 |
| Item Size | 1478 | object | 南瓜大小 |
| Color | 1141 | object | 颜色 |
| Environment | 0 | float64 | 环境相关 |
| Unit of Sale | 162 | object | 销售单位 |
| Quality | 0 | float64 | 质量 |
| Condition | 0 | float64 | 状况 |
| Appearance | 0 | float64 | 外观 |
| Storage | 0 | float64 | 存储情况 |
| Crop | 0 | float64 | 收成情况 |
| Repack | 1757 | object | 是否重新包装 |
| Trans Mode | 0 | float64 | 运输方式 |
| Unnamed: 24 | 0 | float64 | 未命名字段 24 |
| Unnamed: 25 | 103 | object | 未命名字段 25 |

该数据集共有 1757 行，26 列。
## 数据预处理
1. 缺失值处理

该数据集存在缺失值，为了分析的准确性，对数据集进行缺失值处理：
删除非空字段数量低于总数量 50% 的字段。
对于分类字段的缺失值，使用众数进行填充。
对于数值字段的缺失值，使用均值进行填充。


# 探索数据可视化

有好几个库都可以进行数据可视化。用 matplotlib 和 seaborn 对本课中涉及的 Pumpkin 数据集创建一些数据可视化的图标。并思考哪个库更容易使用？

## 评判标准

| 标准 | 优秀 | 中规中矩 | 仍需努力 |
| -------- | --------- | -------- | ----------------- |
|          | 提交了含有两种探索可视化方法的 notebook 工程文件         |   提交了只包含有一种探索可视化方法的 notebook 工程文件       |  没提交  notebook 工程文件                 |
