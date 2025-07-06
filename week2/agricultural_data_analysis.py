import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# 设置中文显示
plt.rcParams["font.family"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

'''读取数据集'''
df = pd.read_csv('US-pumpkins.csv')
print(f"数据加载成功，共{df.shape[0]}行{df.shape[1]}列")
print(df.info())

'''数据预处理'''
# 1. 缺失值处理
# 删除非空字段数量低于总数量50%的字段
threshold = len(df) * 0.5
df = df.dropna(thresh=threshold, axis=1)

# 区分分类字段和数值字段
categorical_columns = df.select_dtypes(include=['object']).columns
numeric_columns = df.select_dtypes(include=['number']).columns
# 分类字段用众数填充缺失值
for col in categorical_columns:
    df.fillna({col: df[col].mode()[0]}, inplace=True)
# 数值字段用均值填充缺失值
for col in numeric_columns:
    df.fillna({col: df[col].mean()}, inplace=True)

# 2. 处理Date字段，将其转换为日期时间类型
df['Date'] = pd.to_datetime(df['Date'])

# 输出Date字段的基本统计信息
print('Date字段的基本统计信息：')
print(df['Date'].describe())

# 提取年份和月份，新增到数据集中
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month

# 查看不同年份的记录数
year_counts = df['Year'].value_counts().sort_index()
print('不同年份的记录数：')
print(year_counts)

# 查看不同月份的记录数
month_counts = df['Month'].value_counts().sort_index()
print('不同月份的记录数：')
print(month_counts)

# 将结果保存为csv文件
csv_path = 'US-pumpkins_preprocessed.csv'
df.to_csv(csv_path)

