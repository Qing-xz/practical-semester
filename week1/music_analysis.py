import pandas as pd

# 加载数据集
df = pd.read_csv('nigerian-songs.csv')

print('数据基本信息：')
df.info()

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

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

# 提取特征数据
features = df[['danceability', 'acousticness', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo']]

# 数据标准化
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# 初始化最佳簇数和最佳轮廓系数
best_clusters = 0
best_score = -1

# 尝试不同的簇数
for n_clusters in range(2, 11):
    kmeans = KMeans(n_clusters=n_clusters, random_state=2024)
    cluster_labels = kmeans.fit_predict(scaled_features)

    # 计算轮廓系数
    silhouette_avg = silhouette_score(scaled_features, cluster_labels)
    if silhouette_avg > best_score:
        best_score = silhouette_avg
        best_clusters = n_clusters

# 使用最佳簇数进行KMeans聚类
kmeans = KMeans(n_clusters=best_clusters, random_state=2024)
df['cluster_label'] = kmeans.fit_predict(scaled_features)

# 将结果保存为csv文件
csv_path = 'nigerian-songs_clustered.csv'
df.to_csv(csv_path, index=False)
print(f'最佳簇数为: {best_clusters}')