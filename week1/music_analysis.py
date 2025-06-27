import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

# 设置中文字体支持
plt.rcParams["font.family"] = ["SimHei"]
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 加载数据集
df = pd.read_csv('nigerian-songs.csv')

'''数据概述'''
print('数据基本信息：',df.info())

# 查看数据集行数和列数
rows, columns = df.shape
if rows < 100 and columns < 20:
    # 短表数据（行数少于100且列数少于20）查看全量数据信息
    print('数据全部内容信息：')
    print(df.to_csv(sep='\t', na_rep='nan'))
else:
    # 长表数据查看数据前几行信息
    print('数据前几行内容信息：')
    print(df.head().to_csv(sep='\t', na_rep='nan'))

'''数据分析'''
# 1. 流派分布分析
print("\n1. 流派分布分析：")
genre_counts = df['artist_top_genre'].value_counts()
print(genre_counts)

# 可视化流派分布
plt.figure(figsize=(12, 6))
sns.barplot(x=genre_counts.index, y=genre_counts.values)
plt.title('音乐流派分布')
plt.xlabel('流派')
plt.ylabel('数量')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# 2. 歌曲时长分析
print("\n2. 歌曲时长分析：")
# 转换时长为秒
df['duration_sec'] = df['length'] / 1000

# 计算基本统计量
duration_stats = df['duration_sec'].describe()
print("歌曲时长统计量：")
print(duration_stats)

# 检测异常值（使用IQR方法）
Q1 = df['duration_sec'].quantile(0.25)
Q3 = df['duration_sec'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = df[(df['duration_sec'] < lower_bound) | (df['duration_sec'] > upper_bound)]
print(f"检测到 {len(outliers)} 个时长异常值")

# 可视化歌曲时长分布
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
sns.histplot(df['duration_sec'], kde=True)
plt.title('歌曲时长分布')
plt.xlabel('时长(秒)')
plt.ylabel('频率')

plt.subplot(1, 2, 2)
sns.boxplot(y=df['duration_sec'])
plt.title('歌曲时长箱线图')
plt.tight_layout()
plt.show()

# 3. 歌手活跃度分析
print("\n3. 歌手活跃度分析：")
artist_counts = df['artist'].value_counts()
print("歌手歌曲数量排名（前10）：")
print(artist_counts.head(10))

# 可视化歌手活跃度（前10）
plt.figure(figsize=(12, 6))
sns.barplot(x=artist_counts.head(10).index, y=artist_counts.head(10).values)
plt.title('歌手活跃度排名（歌曲数量前10）')
plt.xlabel('歌手')
plt.ylabel('歌曲数量')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 4. 音乐属性相关性分析
print("\n4. 音乐属性相关性分析：")
# 选择数值型音乐属性列
music_features = ['danceability', 'acousticness', 'energy', 'instrumentalness',
                  'liveness', 'loudness', 'speechiness',
                  'tempo', 'time_signature']

# 计算相关系数矩阵
correlation = df[music_features].corr()
print("音乐属性相关系数矩阵：")
print(correlation)

# 可视化相关系数矩阵
plt.figure(figsize=(12, 10))
sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt='.2f', square=True)
plt.title('音乐属性相关性热图')
plt.tight_layout()
plt.show()

# 找出相关性最强的特征对
corr_pairs = correlation.unstack()
sorted_pairs = corr_pairs.sort_values(kind="quicksort", ascending=False)
strong_pairs = sorted_pairs[abs(sorted_pairs) > 0.5]
print("\n强相关特征对（相关系数绝对值>0.5）：")
print(strong_pairs[strong_pairs.index.get_level_values(0) != strong_pairs.index.get_level_values(1)])

# 5. 流行度与其他属性的关系
print("\n5. 流行度与其他属性的关系：")
# 计算流行度与其他属性的相关性
numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
popularity_corr = df[numeric_columns].corrwith(df['popularity']).sort_values(ascending=False)
print("流行度与其他属性的相关性：")
print(popularity_corr)

# 可视化流行度与舞蹈性、能量的关系
plt.figure(figsize=(15, 5))
plt.subplot(1, 2, 1)
sns.scatterplot(x='danceability', y='popularity', data=df)
plt.title('舞蹈性与流行度的关系')

plt.subplot(1, 2, 2)
sns.scatterplot(x='energy', y='popularity', data=df)
plt.title('能量与流行度的关系')
plt.tight_layout()
plt.show()

# 6. 时间趋势分析
print("\n6. 时间趋势分析：")
# 分析每年歌曲数量变化
yearly_counts = df['release_date'].value_counts().sort_index()
print("每年发布的歌曲数量：")
print(yearly_counts)

# 可视化每年歌曲数量和平均流行度变化
plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
sns.lineplot(x=yearly_counts.index, y=yearly_counts.values)
plt.title('每年发布的歌曲数量')
plt.xlabel('年份')
plt.ylabel('歌曲数量')

# 计算每年平均流行度
yearly_popularity = df.groupby('release_date')['popularity'].mean()
plt.subplot(1, 2, 2)
sns.lineplot(x=yearly_popularity.index, y=yearly_popularity.values)
plt.title('每年歌曲平均流行度')
plt.xlabel('年份')
plt.ylabel('平均流行度')
plt.tight_layout()
plt.show()