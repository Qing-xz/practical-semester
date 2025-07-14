import xgboost as xgb
from sklearn.metrics import mean_squared_error, r2_score

def train_and_predict(X_train, y_train, X_test):
    model = xgb.XGBRegressor(random_state=42)
    model.fit(X_train, y_train)
    y_train_pred = model.predict(X_train)
    y_test_pred  = model.predict(X_test)
    return model, y_train_pred, y_test_pred