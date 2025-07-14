from sklearn.metrics import mean_squared_error, r2_score

def regression_report(y_train, y_train_pred, y_test, y_test_pred):
    train_mse = mean_squared_error(y_train, y_train_pred)
    train_r2  = r2_score(y_train, y_train_pred)
    test_mse  = mean_squared_error(y_test, y_test_pred)
    test_r2   = r2_score(y_test, y_test_pred)

    print(f"训练集 MSE: {train_mse:.4f}  |  R²: {train_r2:.4f}")
    print(f"测试集  MSE: {test_mse:.4f}  |  R²: {test_r2:.4f}")