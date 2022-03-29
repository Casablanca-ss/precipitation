"""以下为散点密度图"""
# Calculate the point density
import glob
import os.path
import numpy as np
import pandas as pd
from sklearn.metrics.regression import r2_score, mean_squared_error, mean_absolute_error
from matplotlib import pyplot as plt
from scipy.stats import gaussian_kde, pearsonr
from tqdm import tqdm

folder_path = r"F:\precipitation\data2\combine_all_data\pre_gpm_trmm_cdr_tem_ndvi_cloud_day2_test_daily\*.csv"
path_list = glob.glob(folder_path)


def point_density():  # 绘制散点密度图
    for i in tqdm(path_list):
        # 散点密度图
        data = pd.read_csv(i)  # 读取数据
        data = data[~data["20_20pre"].isin([3276.6])]
        x_data = data['20_20pre'].values  # x坐标值
        y_data = data['daily_fusion_extract'].values  # y坐标值
        # print('Done.\ntest:\nR-squared: %f\nMSE: %f' % (r2_score(x_data, y_data), mean_squared_error(x_data, y_data)))
        # print('RMSE: %f' % (mean_squared_error(x_data, y_data, squared=False)))
        # print('MAE: %f' % (mean_absolute_error(x_data, y_data)))
        # print('pearson:', pearsonr(y_data, x_data))

        # 评价指标
        PCC = pearsonr(y_data, x_data)[0]  # 皮尔森相关系数
        MSE = mean_squared_error(x_data, y_data, squared=False)  # 均方误差
        MAE = mean_absolute_error(x_data, y_data)  # 平均绝对值误差
        BIAS = float(np.mean(x_data - y_data))  # 偏差
        N = len(x_data)  # 统计数量
        figure_name = os.path.basename(i)[:-4]  # 从文件名中提取图表名称
        plt.figure(figsize=(6.5, 6))  # 设置图表长宽比
        # 进行点密度计算
        xy = np.vstack([x_data, y_data])
        z = gaussian_kde(xy)(xy)
        # Sort the points by density, so that the densest points are plotted last
        idx = z.argsort()
        x, y, z = x_data[idx], y_data[idx], z[idx]
        plt.scatter(x, y, c=z, s=130, cmap='Spectral_r')  # 设置散点大小

        # 绘制1：1直线
        y_lim = plt.ylim(-1, 28)  # 设置x范围
        x_lim = plt.xlim(-1, 28)  # 设置y范围
        plt.plot(x_lim, y_lim, '--', color='k')  # 设置线类型、颜色

        # 坐标元素设置
        plt.axis([-2, 25, -2, 25])  # 设置xy轴显示范围
        plt.xticks(list(range(0, 31, 10)), fontproperties='Times New Roman', size=30)  # 设置x轴坐标刻度
        plt.yticks(list(range(0, 31, 10)), fontproperties='Times New Roman', size=30)  # 设置y轴坐标刻度
        plt.xlabel("gauge precipitation",fontproperties='Times New Roman', size=40)
        plt.ylabel("fusion precipitation",fontproperties='Times New Roman', size=40)
        plt.title(f'Station-{figure_name}', fontproperties='Times New Roman', fontsize=35)  # 设置标题名称及字号
        plt.grid(b=True, which='major', axis='both', linestyle='--')  # 设置网格线
        plt.text(x=0, y=20, fontsize=30, s='PCC=%.2f\nRMSE=%.2fmm\nMAE=%.2fmm' % (PCC, MSE, MAE),
                 fontdict={'family': 'Times New Roman'})  # 加入评价指标
        plt.text(x=12, y=1, fontsize=30, s='BIAS=%.2fmm\nN=%d' % (BIAS, N),
                 fontdict={'family': 'Times New Roman'})  # 加入评价指标

        # plt.colorbar()  # 显示色带
        # 保存图表
        # plt.savefig(fr"C:\Users\Casablanca\Desktop\新建文件夹\{figure_name}.png", dpi=100, bbox_inches='tight')
        # plt.show()
        plt.close()
        # break


