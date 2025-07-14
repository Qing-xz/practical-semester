import pandas as pd
from configuration import TOP_N_IMPORTANCE
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

def engineer_features(df):
    # 类别编码
    cat_cols = df.select_dtypes(include=['object']).columns.drop('Date', errors='ignore')
    for col in cat_cols:
        df[col] = df[col].astype('category').cat.codes

    # 目标变量
    df['Average Price'] = (df['Low Price'] + df['High Price']) / 2
    return df

def select_top_features(df):
    y = df['Average Price']
    X = df.drop(columns=['Average Price', 'Date',
                         'Low Price', 'High Price',
                         'Mostly Low', 'Mostly High'])
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)

    feat_imp = (pd.DataFrame({'Feature': X.columns,
                              'Importance': rf.feature_importances_})
                .sort_values('Importance', ascending=False))
    selected = feat_imp.head(TOP_N_IMPORTANCE)['Feature'].tolist()
    print('选择的特征:', selected)
    return X_train, X_test, y_train, y_test, selected