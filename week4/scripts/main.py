import pandas as pd
from data_analysis   import load_data, clean_data
from feature_processing import engineer_features, select_top_features
from model           import train_and_predict
from evaluate        import regression_report
from utility         import plot_correlation, plot_feature_importance
from sklearn.ensemble import RandomForestRegressor

def main():
    # 1. 读取 & 清洗
    df = load_data()
    df = clean_data(df)

    # 2. 特征工程
    df = engineer_features(df)

    # 3. 可视化
    plot_correlation(df)

    # 4. 特征选择
    X_train, X_test, y_train, y_test, selected = select_top_features(df)
    X_train_sel = X_train[selected]
    X_test_sel  = X_test[selected]

    # 5. 建模 & 评估
    model, y_tr_pred, y_te_pred = train_and_predict(X_train_sel, y_train, X_test_sel)
    regression_report(y_train, y_tr_pred, y_test, y_te_pred)

    # 6. 特征重要性图
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train_sel, y_train)
    imp_df = (pd.DataFrame({'Feature': selected,
                            'Importance': rf.feature_importances_})
              .sort_values('Importance', ascending=False))
    plot_feature_importance(imp_df)

if __name__ == '__main__':
    main()