from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestRegressor

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.regression import r2_score, mean_squared_error, mean_absolute_error
import joblib
from scipy.stats import pearsonr
from sklearn import metrics
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

"""
iris = load_iris()
print(iris['target'].shape)
rf1 = RandomForestClassifier()
rf2 = RandomForestClassifier(
    n_estimators=10,
    max_depth=None,
    min_samples_split=3,
    random_state=0
)
rf1.fit(iris.data[:130], iris.target[:130])
rf2.fit(iris.data[:130], iris.target[:130])
testset = iris.data[131:150]
y_true = iris.target[131:150]
y_pre1 = rf1.predict(testset)
y_pre2 = rf2.predict(testset)
print('rf1 prediction:', y_pre1)
print('rf2 prediction:', y_pre2)
mse1 = metrics.mean_squared_error(y_true, y_pre1)
mse2 = metrics.mean_squared_error(y_true, y_pre2)
print('MSE1: %.4f' % mse1)
print('MSE2: %.4f' % mse2)
"""

start = time.clock()

# 载入数据
data = pd.read_csv(
    r"F:\precipitation\data\train_model\all_data_del_abnormal.csv")  # error_bad_lines=False, encoding='ISO-8859-15')
# data = pd.read_csv(r"F:\precipitation\data\train_model\winter.csv")  # error_bad_lines=False, encoding='ISO-8859-15')

# 将多维数据转换为二维数据
predictors = data[["gpm", "trmm", "cdr", "cloud", "month", "day2"]].values
# predictors = data[["gpm", "trmm", "cdr", "ndvi", "ele"]].values
# predictors = data[["trmm","ele","month","day2","ndvi","cdr","gpm"]].values
# 获取Mean值并转换为一维数据
outputvar = data["std"].values
# datashuffle=shuffle(data1,random_state=888)a
# Data scaling
min_max_scaler = MinMaxScaler()
predictors = min_max_scaler.fit_transform(predictors)
# Splitting data
X_train, X_test, Y_train, Y_test = train_test_split(predictors, outputvar, test_size=0.2, random_state=888)

# print(min_max_scaler.fit(X_train))

# 导入模型
# regressor = RandomForestRegressor()
regressor = RandomForestRegressor(
    n_estimators=100,
    max_depth=20
)

# 数据导入模型进行训练
regressor.fit(X_train, Y_train)
# 保存模型
# joblib.dump(regressor,r"F:\precipitation\data\fusion_precipitation\gpm, trmm, cdr,cloud, month,day2.joblib")
# 调用保存的模型
# regressor=joblib.load(r"C:\Users\Casablanca\Desktop\model.joblib")


Y_pred = regressor.predict(X_test)
Y_pred2 = regressor.predict(X_train)

"""
print("1:",Y_pred)
# print("2:",Y_pred[:, 0])
print("3:",Y_pred2[:, 0])
input()
"""

print("Y_test:", Y_test)
print("Y_pred:", Y_pred)
# pd.DataFrame(Y_pred,Y_test).to_csv(r"C:\Users\Casablanca\Desktop\jieguo.csv")
end = time.clock()
print("运行耗时：", end - start)

# 绘制散点图
plt.scatter(Y_train, Y_pred2)
plt.title("train")
plt.show()
# plt.scatter(Y_test, Y_pred)
# plt.title("test")
# plt.show()
print("Y_train:", Y_train)
print("Y_pred2:", Y_pred2)
print('Done.\ntrain:\nR-squared: %f\nMSE: %f' % (r2_score(Y_train, Y_pred2), mean_squared_error(Y_train, Y_pred2)))
print('Done.\ntest:\nR-squared: %f\nMSE: %f' % (r2_score(Y_test, Y_pred), mean_squared_error(Y_test, Y_pred)))
print('RMSE: %f' % (mean_squared_error(Y_test, Y_pred, squared=False)))
print('MAE: %f' % (mean_absolute_error(Y_test, Y_pred)))
print('pearson:', pearsonr(Y_pred, Y_test))
print("gpm", pearsonr(data["std"], data["gpm"]))
print("trmm", pearsonr(data["std"], data["trmm"]))
print("cdr", pearsonr(data["std"], data["cdr"]))
print("ndvi", pearsonr(data["std"], data["ndvi"]))
print("ele", pearsonr(data["std"], data["ele"]))
print("month", pearsonr(data["std"], data["month"]))
print("day2", pearsonr(data["std"], data["day2"]))
print("cloud", pearsonr(data["std"], data["cloud"]))
# print(pearsonr(Y_pred[:, 0], Y_test))
# print(pearsonr(Y_pred2[:, 0], Y_train))

"""以下为相关性矩阵/热量图"""
import seaborn as sns

data1 = data[["gpm", "trmm", "cdr", "ndvi", "ele", "month", "day2", "cloud", "std"]]
plt.figure(figsize=(12, 10), dpi=80)
sns.heatmap(data1.corr(), xticklabels=data1.corr().columns, yticklabels=data1.corr().columns, cmap='RdYlBu_r', center=0,
            annot=True, fmt='.2f', annot_kws={'size': 15, 'weight': 'normal', 'color': 'black'})

# Decorations
plt.title('correlation_matrix', fontsize=22)
plt.xticks(fontsize=17)
plt.yticks(fontsize=17)

plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
plt.show()
print(data1.corr())

"""以下为散点密度图"""
# Calculate the point density
from scipy.stats import gaussian_kde

xy = np.vstack([Y_test, Y_pred])
z = gaussian_kde(xy)(xy)

# Sort the points by density, so that the densest points are plotted last
idx = z.argsort()
x, y, z = Y_test[idx], Y_pred[idx], z[idx]

fig, ax = plt.subplots()
y_lim = plt.ylim()
x_lim = plt.xlim()
plt.axis([-5, 150, -5, 150])
plt.plot(x_lim, y_lim, 'k-', color='r')
plt.scatter(x, y, c=z, s=20, cmap='Spectral_r')
plt.title('test', fontsize=22)
plt.colorbar()
plt.show()

# k折交叉验证
# scores = cross_val_score(regressor,X_train, Y_train,cv=5,scoring='r2')
# print("Cross validation scores:{}".format(scores))
# print("Mean cross validation score:{:2f}".format(scores.mean()))

# xy = np.vstack([Y_test, Y_pred])
# z = gaussian_kde(xy)(xy)
#
# # Sort the points by density, so that the densest points are plotted last
# idx = z.argsort()
# x, y, z = Y_test[idx], Y_pred[idx], z[idx]
#
# fig, ax = plt.subplots()
# plt.axis([-5, 150,-5, 150])
# y_lim = plt.ylim()
# x_lim = plt.xlim()
# plt.plot(x_lim, y_lim, 'k-', color = 'r')
# plt.scatter(x, y,c=z,  s=20,cmap='Spectral_r')
# plt.title('test', fontsize=22)
# plt.colorbar()
# plt.show()
