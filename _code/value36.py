# 创建36个站点和评价指标csv

import glob
import numpy as np
import pandas as pd
from sklearn.metrics.regression import r2_score, mean_squared_error, mean_absolute_error
from scipy.stats import gaussian_kde, pearsonr

folder_path = r"F:\precipitation\data2\combine_all_data\pre_gpm_trmm_cdr_tem_ndvi_cloud_day2_test_daily\*.csv"
path_list = glob.glob(folder_path)

table1 = pd.read_csv(r'F:\precipitation\data\all_station.csv')
table2 = pd.DataFrame(columns=['std_number', 'longitude', 'latitude', 'PCC', 'MSE', 'MAE', 'BIAS'])
print(table1)
table2[["std_number", 'longitude', 'latitude']] = table1[['station', 'lon', 'lat']]
print(table2)

for i, j in zip(path_list, list(range(0, 36))):
    # 散点密度图
    data = pd.read_csv(i)  # 读取数据
    data = data[~data["20_20pre"].isin([3276.6])]
    x_data = data['20_20pre'].values  # x坐标值
    y_data = data['daily_fusion_extract'].values  # y坐标值
    # 评价指标
    PCC = pearsonr(y_data, x_data)[0]  # 皮尔森相关系数
    MSE = mean_squared_error(x_data, y_data, squared=False)  # 均方误差
    MAE = mean_absolute_error(x_data, y_data)  # 平均绝对值误差
    BIAS = float(np.mean(x_data - y_data))  # 偏差
    value = pd.Series([PCC, MSE, MAE, BIAS], ['PCC', 'MSE', 'MAE', 'BIAS'])

    table2.loc[j, ['PCC', 'MSE', 'MAE', 'BIAS']] = value[['PCC', 'MSE', 'MAE', 'BIAS']].values

print(table2)
table2.to_csv(r'F:\precipitation\data2\paper\value362.csv', index=False)
