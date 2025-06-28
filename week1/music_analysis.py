import pandas as pd
import seaborn as sns
import os
# 设置环境变量，限制 OpenMP 线程数为 3
os.environ['OMP_NUM_THREADS'] = '3'
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler
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
                  'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature']
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

# 5. 时间趋势分析
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

'''确定聚类数量'''
# 数据标准化
X = df[music_features]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 根据流派大致分类为节奏型、抒情型、说唱型、综合型，选择k=4
k = 4
print(f"\n基于流派分布和特征相似性，选择聚类数 k = {k}")

'''K-Means聚类'''
kmeans = KMeans(n_clusters=k, random_state=42)
df['cluster_label'] = kmeans.fit_predict(X_scaled)

'''聚类结果分析'''
# 1. 聚类内音乐特征分析
print("\n各聚类音乐特征均值：")
cluster_features = df.groupby('cluster_label')[music_features].mean()
print(cluster_features)

# 可视化聚类特征均值
plt.figure(figsize=(16, 8))
for i, feature in enumerate(music_features):
    plt.subplot(3, 3, i+1)
    sns.barplot(x=df['cluster_label'], y=df[feature], palette='viridis')
    plt.title(f'聚类 vs {feature}')
plt.tight_layout()
plt.savefig('cluster_features.png')
plt.show()

# 2. 聚类与音乐流派的关系
print("\n各聚类中流派分布（前5）：")
genre_distribution = df.groupby(['cluster_label', 'artist_top_genre'])['name'].count().unstack(fill_value=0)
print(genre_distribution)

# 可视化流派分布
plt.figure(figsize=(18, 10))
sns.heatmap(genre_distribution, annot=True, fmt='g', cmap='YlGnBu')
plt.title('各聚类中流派分布热图')
plt.tight_layout()
plt.savefig('genre_cluster_heatmap.png')
plt.show()

# 3. 聚类与歌曲流行度的关系
print("\n各聚类平均流行度：")
popularity_by_cluster = df.groupby('cluster_label')['popularity'].mean()
print(popularity_by_cluster)

# 可视化流行度分布
plt.figure(figsize=(10, 6))
sns.barplot(x=popularity_by_cluster.index, y=popularity_by_cluster.values, palette='magma')
plt.title('各聚类平均流行度')
plt.xlabel('聚类标签')
plt.ylabel('平均流行度')
plt.tight_layout()
plt.savefig('popularity_by_cluster.png')
plt.show()

# 4. 聚类与发布时间的关系
print("\n各聚类歌曲发布年份分布：")
# 转换为年份
df['release_year'] = df['release_date'].astype(str).str[:4].astype(int)
year_by_cluster = df.groupby(['cluster_label', 'release_year'])['name'].count().unstack(fill_value=0)
print(year_by_cluster)

# 可视化发布时间分布
plt.figure(figsize=(18, 10))
for cluster in range(k):
    cluster_data = year_by_cluster.loc[cluster].sort_index()
    plt.plot(cluster_data.index, cluster_data.values, label=f'聚类 {cluster}')
plt.title('各聚类歌曲发布年份分布')
plt.xlabel('年份')
plt.ylabel('歌曲数量')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('release_year_by_cluster.png')
plt.show()

'''聚类结果总结'''
print("\n聚类结果总结：")
for cluster in range(k):
    cluster_df = df[df['cluster_label'] == cluster]
    main_genre = cluster_df['artist_top_genre'].value_counts().idxmax()
    avg_popularity = cluster_df['popularity'].mean()
    avg_danceability = cluster_df['danceability'].mean()
    avg_energy = cluster_df['energy'].mean()
    print(f"聚类 {cluster}:")
    print(f"  主要流派: {main_genre}")
    print(f"  平均流行度: {avg_popularity:.2f}")
    print(f"  平均可舞性: {avg_danceability:.2f}")
    print(f"  平均活力: {avg_energy:.2f}")
    print(f"  歌曲数量: {len(cluster_df)}")
    print()