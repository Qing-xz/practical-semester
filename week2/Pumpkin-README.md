# Pumpkin 数据集数据分析
## 数据说明
US-pumpkins数据集共有 1757 行，26 列。

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

## 数据预处理
1. 缺失值处理

该数据集存在缺失值，为了分析的准确性，对数据集进行缺失值处理：

删除非空字段数量低于总数量 50% 的字段；
对于分类字段的缺失值，使用众数进行填充；
对于数值字段的缺失值，使用均值进行填充。

2. Date字段处理

原始数据中Date字段的数据类型为object，为了便于进行基于日期的分析，
使用pd.to_datetime函数将Date字段转换为日期时间类型。
转换完成后，提取了年份和月份信息分别存储在新的列 Year 和 Month 中，
并统计了不同年份和不同月份的记录数。

预处理后字段概述如下：

| 字段名 | 数据类型 | 含义 |
| --- | --- | --- |
| City Name | object | 城市名称，记录南瓜交易或相关事件发生的城市 |
| Package | object | 包装方式 |
| Variety | object | 南瓜品种 |
| Date | datetime64[ns] | 交易日期 |
| Low Price | float64 | 最低价格 |
| High Price | float64 | 最高价格 |
| Mostly Low | float64 | 多数情况下的最低价格 |
| Mostly High | float64 | 多数情况下的最高价格 |
| Origin | object | 产地 | 
| Item Size | object | 南瓜大小 |
| Color | object | 颜色 |
| Repack | object | 是否重新包装 |

## 数据统计分析
计算平均价格：通过数据集的 Low Price 字段和 High Price 字段计算 Average Price。
价格统计：查看价格的基本统计信息、主要城市和品种的数量，找出价格最高和最低的前 10 个记录。
### 1. 价格分布特征

| 统计量 | 数值         |
|-----|------------|
|count | 1757.000000 |
|mean | 128.771138 |
|std | 86.426495 |
|min | 0.240000 |
|25% | 24.250000 |
|50% | 145.000000 |
|75% | 192.500000 |
|max | 480.000000 |
结果显示出美国南瓜市场价格整体均值约为 128.77，波动幅度较大；
中位数 145 高于均值 128.77，说明高价交易对均值的拉低作用，实际市场价格整体偏高。

### 2. 主要城市与品种

主要城市数量：共有13个主要城市参与南瓜交易。

主要品种数量：共有 10 种主要南瓜品种。
### 3. 价格极值分析

#### 价格最高的前10个记录
| City Name       | Package       | Variety      | Year | Month | Average Price |
|-----------------|---------------|--------------|------|-------|---------------|
| SAN FRANCISCO   | 24 inch bins   | PIE TYPE     | 2016 | 10    | 480.0         |
| SAN FRANCISCO   | 24 inch bins   | HOWDEN TYPE  | 2016 | 10    | 440.0         |
| SAN FRANCISCO   | 36 inch bins   | PIE TYPE     | 2017 | 9     | 440.0         |
| SAN FRANCISCO   | 36 inch bins   | PIE TYPE     | 2017 | 9     | 440.0         |
| COLUMBIA        | 24 inch bins   | MINIATURE    | 2017 | 9     | 400.0         |
| COLUMBIA        | 24 inch bins   | MINIATURE    | 2017 | 9     | 400.0         |
| COLUMBIA        | 24 inch bins   | MINIATURE    | 2017 | 9     | 400.0         |
| BALTIMORE       | 24 inch bins   | CINDERELLA   | 2017 | 6     | 380.0         |
| BALTIMORE       | 24 inch bins   | CINDERELLA   | 2017 | 6     | 380.0         |
| BALTIMORE       | 24 inch bins   | CINDERELLA   | 2017 | 6     | 380.0         |
高价南瓜集中在旧金山、哥伦比亚等城市，多为 PIE TYPE、迷你型等特殊品种，且交易时间集中在 2016-2017 年秋冬季节。
这可能与当地较高的消费水平、感恩节前后的烘焙需求（如制作南瓜派）及品种稀缺性有关，大规格包装（24/36 英寸箱）也反映了批发场景下的规模化交易特征。
#### 价格最低的前10个记录
| City Name   | Package       | Variety    | Year | Month | Average Price |
|-------------|---------------|------------|------|-------|---------------|
| LOS ANGELES | 24 inch bins  | FAIRYTALE  | 2016 | 9     | 0.24          |
| LOS ANGELES | 24 inch bins  | FAIRYTALE  | 2016 | 10    | 0.24          |
| LOS ANGELES | 24 inch bins  | FAIRYTALE  | 2016 | 10    | 0.24          |
| LOS ANGELES | 24 inch bins  | FAIRYTALE  | 2016 | 10    | 0.24          |
| LOS ANGELES | 24 inch bins  | FAIRYTALE  | 2016 | 10    | 0.24          |
| LOS ANGELES | 24 inch bins  | FAIRYTALE  | 2016 | 10    | 0.24          |
| LOS ANGELES | 24 inch bins  | CINDERELLA | 2017 | 8     | 0.30          |
| LOS ANGELES | 24 inch bins  | CINDERELLA | 2017 | 8     | 0.30          |
| LOS ANGELES | 24 inch bins  | CINDERELLA | 2017 | 9     | 0.30          |
| LOS ANGELES | 24 inch bins  | CINDERELLA | 2017 | 9     | 0.30          |
低价记录全部来自洛杉矶，涉及 FAIRYTALE 和 CINDERELLA 品种，
价格较旧金山低 1600 倍以上。可能与品种口感、市场需求度较低有关。
时间上集中在秋冬季节，与高价区交易时间重叠但价格表现迥异，凸显区域市场供需和消费能力的显著分化。
## 数据可视化分析

