import pandas as pd
from configuration import RAW_DATA_PATH

def load_data():
    df = pd.read_csv(RAW_DATA_PATH)
    print(f"数据加载成功，共{df.shape[0]}行{df.shape[1]}列")
    return df

def clean_data(df):
    # 缺失值处理
    th = len(df) * 0.5
    df = df.dropna(thresh=th, axis=1)

    cat_cols = df.select_dtypes(include=['object']).columns
    num_cols = df.select_dtypes(include=['number']).columns

    for c in cat_cols:
        df[c].fillna(df[c].mode()[0], inplace=True)
    for n in num_cols:
        df[n].fillna(df[n].mean(), inplace=True)

    # 时间特征
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year']  = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month

    print('不同年份的记录数：\n', df['Year'].value_counts().sort_index())
    print('不同月份的记录数：\n', df['Month'].value_counts().sort_index())
    return df