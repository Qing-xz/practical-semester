import matplotlib.pyplot as plt
import seaborn as sns
from configuration import FIG_DIR

plt.rcParams["font.family"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

def plot_correlation(df):
    plt.figure(figsize=(14, 10))
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('特征相关性热力图')
    plt.tight_layout()
    plt.savefig(f"{FIG_DIR}/correlation_heatmap.png")
    plt.show()

def plot_feature_importance(importance_df):
    plt.figure(figsize=(12, 8))
    sns.barplot(x='Importance', y='Feature', data=importance_df)
    plt.title('特征重要性排名')
    plt.tight_layout()
    plt.savefig(f"{FIG_DIR}/feature_importance.png")
    plt.show()