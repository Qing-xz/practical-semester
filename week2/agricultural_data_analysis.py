import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 设置中文显示
plt.rcParams["font.family"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

'''读取数据集'''
df = pd.read_csv('US-pumpkins.csv')
print(f"数据加载成功，共{df.shape[0]}行{df.shape[1]}列")
print(df.info())

'''数据处理阶段'''
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

# 3. 对分类字段进行编码
categorical_columns = categorical_columns.drop('Date', errors='ignore')
for col in categorical_columns:
    df[col] = df[col].astype('category').cat.codes

# 4. 计算平均价格，作为后续建模的目标变量
df['Average Price'] = (df['Low Price'] + df['High Price']) / 2

# 将结果保存为csv文件
# csv_path = 'US-pumpkins_preprocessed.csv'
# df.to_csv(csv_path)
print(df.info())

'''数据分析阶段'''
selected_columns = ['Year', 'Month', 'City Name', 'Variety', 'Item Size', 'Average Price']
model_df = df[selected_columns]

# 查看筛选后数据的基本信息
print('用于建模的数据基本信息：')
model_df.info()

# 查看各特征与平均价格的相关性（保留两位小数）
correlation = model_df.corr()['Average Price'].drop('Average Price').round(2)
print('各特征与平均价格的相关性：')
print(correlation)





# '''可视化'''
# # Matplotlib绘图部分
# # 绘制主要城市南瓜价格分布
# plt.figure(figsize=(12, 6))
# for city in df['City Name'].unique():
#     city_prices = df[df['City Name'] == city]['Average Price']
#     plt.hist(city_prices, bins=20, alpha=0.5, label=city)
# plt.title('主要城市南瓜价格分布（Matplotlib）')
# plt.xlabel('平均价格')
# plt.ylabel('频数')
# plt.legend()
# plt.savefig('matplotlib_city_price_distribution.png', dpi=300, bbox_inches='tight')
# plt.show()
#
# # 绘制不同品种南瓜价格分布
# plt.figure(figsize=(12, 6))
# for variety in df['Variety'].unique():
#     variety_prices = df[df['Variety'] == variety]['Average Price']
#     plt.hist(variety_prices, bins=20, alpha=0.5, label=variety)
# plt.title('不同品种南瓜价格分布（Matplotlib）')
# plt.xlabel('平均价格')
# plt.ylabel('频数')
# plt.legend()
# plt.savefig('matplotlib_variety_price_distribution.png', dpi=300, bbox_inches='tight')
# plt.show()
#
# # 绘制价格随时间变化趋势
# time_series = df.groupby('Date')['Average Price'].mean()
# plt.figure(figsize=(12, 6))
# plt.plot(time_series.index, time_series.values)
# plt.title('价格随时间变化趋势（Matplotlib）')
# plt.xlabel('日期')
# plt.ylabel('平均价格')
# plt.savefig('matplotlib_price_time_series.png', dpi=300, bbox_inches='tight')
# plt.show()
#
# # 绘制价格和尺寸的关系
# size_mapping = {size: idx for idx, size in enumerate(df['Item Size'].unique())}
# df['Size Num'] = df['Item Size'].map(size_mapping)
# plt.figure(figsize=(12, 6))
# plt.scatter(df['Size Num'], df['Average Price'])
# plt.title('价格和尺寸的关系（Matplotlib）')
# plt.xlabel('尺寸（数值编码）')
# plt.ylabel('平均价格')
# plt.savefig('matplotlib_price_size_relationship.png', dpi=300, bbox_inches='tight')
# plt.show()
#
# # Seaborn绘图部分
# # 绘制主要城市南瓜价格分布
# plt.figure(figsize=(12, 6))
# sns.histplot(data=df, x='Average Price', hue='City Name', multiple='stack')
# plt.title('主要城市南瓜价格分布（Seaborn）')
# plt.xlabel('平均价格')
# plt.ylabel('频数')
# plt.savefig('seaborn_city_price_distribution.png', dpi=300, bbox_inches='tight')
# plt.show()
#
# # 绘制不同品种南瓜价格分布
# plt.figure(figsize=(12, 6))
# sns.histplot(data=df, x='Average Price', hue='Variety', multiple='stack')
# plt.title('不同品种南瓜价格分布（Seaborn）')
# plt.xlabel('平均价格')
# plt.ylabel('频数')
# plt.savefig('seaborn_variety_price_distribution.png', dpi=300, bbox_inches='tight')
# plt.show()
#
# # 绘制价格随时间变化趋势
# plt.figure(figsize=(12, 6))
# sns.lineplot(data=df, x='Date', y='Average Price')
# plt.title('价格随时间变化趋势（Seaborn）')
# plt.xlabel('日期')
# plt.ylabel('平均价格')
# plt.savefig('seaborn_price_time_series.png', dpi=300, bbox_inches='tight')
# plt.show()
#
# # 绘制价格和尺寸的关系
# plt.figure(figsize=(12, 6))
# sns.scatterplot(data=df, x='Size Num', y='Average Price')
# plt.title('价格和尺寸的关系（Seaborn）')
# plt.xlabel('尺寸（数值编码）')
# plt.ylabel('平均价格')
# plt.savefig('seaborn_price_size_relationship.png', dpi=300, bbox_inches='tight')
# plt.show()