from sklearn.ensemble import RandomForestRegressor
from lightgbm import LGBMRegressor
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, root_mean_squared_error
import pandas as pd
import joblib
from sklearn.preprocessing import MinMaxScaler


def loadData(path):
    scalor = MinMaxScaler(feature_range=(0, 1))
    df = pd.read_csv(path)
    X = df.iloc[:, 3:-1]
    columns = X.columns
    X = scalor.fit_transform(X)
    X = pd.DataFrame(X, columns=columns)
    y = df.iloc[:, 2]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    return X_train, X_test, y_train, y_test


def train(dataPath, output, flg=False):
    X_train, X_test, y_train, y_test = loadData(path=dataPath)
    lgbmCls = LGBMRegressor() 
    lgbmCls.fit(X_train, y_train)
    y_prd = lgbmCls.predict(X_test)

    r2 = r2_score(y_test, y_prd)
    mse = mean_squared_error(y_test, y_prd)
    rmse = root_mean_squared_error(y_test, y_prd)
    print(f'r2:{r2}, mse:{mse}, rmse:{rmse}')
    if flg:
        joblib.dump(lgbmCls, output)


def train_rf(dataPath, output, flg=False):
    X_train, X_test, y_train, y_test = loadData(path=dataPath)
    lgbmCls = RandomForestRegressor()
    lgbmCls.fit(X_train, y_train)
    y_prd = lgbmCls.predict(X_test)

    r2 = r2_score(y_test, y_prd)
    mse = mean_squared_error(y_test, y_prd)
    rmse = root_mean_squared_error(y_test, y_prd)
    print(f'r2:{r2}, mse:{mse}, rmse:{rmse}')
    # joblib.dump(lgbmCls, output)
    if flg:
        joblib.dump(lgbmCls, output)


def train_xg(dataPath, output, flg=False):
    X_train, X_test, y_train, y_test = loadData(path=dataPath)
    lgbmCls = XGBRegressor()
    lgbmCls.fit(X_train, y_train)
    y_prd = lgbmCls.predict(X_test)

    r2 = r2_score(y_test, y_prd)
    mse = mean_squared_error(y_test, y_prd)
    rmse = root_mean_squared_error(y_test, y_prd)
    print(f'r2:{r2}, mse:{mse}, rmse:{rmse}')
    # joblib.dump(lgbmCls, output) 
    if flg:
        joblib.dump(lgbmCls, output)


if __name__ == '__main__':
    train(dataPath=r'data\data.csv', output=r'models/lgbmV1.pkl', flg=True)
    train_rf(dataPath=r'data\data.csv', output=r'models/rfV1.pkl', flg=True)
    train_xg(dataPath=r'data\data.csv', output=r'models/xgV1.pkl', flg=True)

