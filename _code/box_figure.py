# 创建绘制箱型图所需csv
import pandas as pd
import os
import glob
import numpy as np
from sklearn.metrics.regression import mean_squared_error, mean_absolute_error
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
from tqdm import tqdm

# 下面函数都基于此
foder_path = r"F:\precipitation\data2\combine_all_data\pre_gpm_trmm_cdr_tem_ndvi_cloud_day2_test_daily - 副本\*.csv"
path_list = glob.glob(foder_path)
list36 = []  # 用来存储36个站点所有数据
number_list = []  # 用来存储站点编号


# 定义指标函数
def value(x_data, y_data):
    pcc = pearsonr(x_data, y_data)[0]  # 皮尔森相关系数
    mse = mean_squared_error(x_data, y_data, squared=False)  # 均方误差
    mae = mean_absolute_error(x_data, y_data)  # 平均绝对值误差
    bias = float(np.mean(x_data - y_data))  # 偏差
    return pcc, mse, mae, bias


# 月份、站点四个指标
def box_figure():
    print("Waiting...")
    for i in path_list:
        number_list.append(int(os.path.basename(i)[:-4]))  # 提取站点编号
        table = pd.read_csv(i)
        table = table[~table["20_20pre"].isin([3276.6])]  # 去除异常值
        # table["20_20pre"].replace(0, 0.001,inplace=True)# 将降雨0值替换为0.001防止计算出错

        value_list = []  # 创建一个存储一个站点12个月四个指标的空列表
        for month in list(range(1, 13)):
            table_month = table[table["month"].isin([month])]  # 提取其中一个月
            if len(table_month) > 1:  # 某个月可能只有一组数据，无法进行计算，此处将此行删除
                pcc, mse, mae, bias = value(table_month["daily_fusion_extract"], table_month["20_20pre"])  # 计算
                value_list.append([pcc, mse, mae, bias])
            print(f"{i, month},ok!")

        # 列表解压重组
        new_value_list = np.array(value_list).T.tolist()
        list36.append(new_value_list)

    pcc = pd.DataFrame(np.array(pd.DataFrame(list36)[0]).tolist())
    mse = pd.DataFrame(np.array(pd.DataFrame(list36)[1]).tolist())
    mae = pd.DataFrame(np.array(pd.DataFrame(list36)[2]).tolist())
    bias = pd.DataFrame(np.array(pd.DataFrame(list36)[3]).tolist())

    pcc["number"] = pd.Series(number_list)
    mse["number"] = pd.Series(number_list)
    mae["number"] = pd.Series(number_list)
    bias["number"] = pd.Series(number_list)
    pcc.set_index("number").to_csv(r"C:\Users\Casablanca\Desktop\新建文件夹\pcc.csv",
                                   header=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    mse.set_index("number").to_csv(r"C:\Users\Casablanca\Desktop\新建文件夹\mse.csv",
                                   header=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    mae.set_index("number").to_csv(r"C:\Users\Casablanca\Desktop\新建文件夹\mae.csv",
                                   header=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    bias.set_index("number").to_csv(r"C:\Users\Casablanca\Desktop\新建文件夹\bias.csv",
                                    header=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    print("All Right!")


# 下面是站点、降雨产品四个指标
# 创建空列表存放四个指标
pcc_list = []
mse_list = []
mae_list = []
bias_list = []


def value_station36():
    print("Waiting...")
    for i in path_list:
        number_list.append(int(os.path.basename(i)[:-4]))  # 提取站点编号
        table = pd.read_csv(i)
        table = table[~table["20_20pre"].isin([3276.6])]  # 去除异常值
        pcc_list1 = []
        mse_list1 = []
        mae_list1 = []
        bias_list1 = []
        for j in ["gpm", "trmm", "cdr", "daily_fusion_extract"]:
            pcc, mse, mae, bias = value(table[j], table["20_20pre"])  # 计算
            pcc_list1.append(pcc)
            mse_list1.append(mse)
            mae_list1.append(mae)
            bias_list1.append(bias)
        pcc_list.append(pcc_list1)
        mse_list.append(mse_list1)
        mae_list.append(mae_list1)
        bias_list.append(bias_list1)
    table_pcc = pd.DataFrame(pcc_list)
    table_mse = pd.DataFrame(mse_list)
    table_mae = pd.DataFrame(mae_list)
    table_bias = pd.DataFrame(bias_list)
    table_pcc["number"] = pd.Series(number_list)
    table_mse["number"] = pd.Series(number_list)
    table_mae["number"] = pd.Series(number_list)
    table_bias["number"] = pd.Series(number_list)
    table_pcc.set_index("number").to_csv(r"C:\Users\Casablanca\Desktop\新建文件夹\PCC.csv",
                                         header=["gpm", "trmm", "cdr", "daily_fusion_extract"])
    table_mse.set_index("number").to_csv(r"C:\Users\Casablanca\Desktop\新建文件夹\MSE.csv",
                                         header=["gpm", "trmm", "cdr", "daily_fusion_extract"])
    table_mae.set_index("number").to_csv(r"C:\Users\Casablanca\Desktop\新建文件夹\MAE.csv",
                                         header=["gpm", "trmm", "cdr", "daily_fusion_extract"])
    table_bias.set_index("number").to_csv(r"C:\Users\Casablanca\Desktop\新建文件夹\BIAS.csv",
                                          header=["gpm", "trmm", "cdr", "daily_fusion_extract"])
    print("All Right!")


def value36_station4():
    print("Waiting...")
    for i in tqdm(path_list):
        file_name = os.path.basename(i)[:-4]  # 提取指标名称作为图表名称
        table = pd.read_csv(i)

        plt.figure(figsize=(20, 8), dpi=80)  # 设置图表长宽比
        x = list(range(36))
        y1 = table["daily_fusion_extract"]  # 融合数据
        y2 = table["gpm"]  # gpm数据
        y3 = table["trmm"]  # trmm数据
        y4 = table["cdr"]  # cdr数据
        plt.rcParams.update({'font.size': 18})
        # plt.plot(x, y, ".", color="k", markersize=10, label="gauge precipitation")
        plt.plot(x, y1, "-", color="r", lw=2, label="Fusinon precipitation")
        plt.plot(x, y2, "-.", color="y", lw=2, label="GPM")
        plt.plot(x, y3, "--", color="blue", lw=2, label="TRMM")
        plt.plot(x, y4, ":", color="purple", lw=2, label="PERSIANN-CDR")
        x_ticks = (table["number"][j] for j in x)

        plt.xticks(x, x_ticks, fontproperties='Times New Roman', size=15, rotation=45)  # 设置x轴刻度
        plt.xlabel("Site Number", fontproperties='Times New Roman', size=20)  # 设置x轴标签
        if file_name == "PCC":
            plt.axis([-0.5, 36.5, -0.1, 1])  # 设置xy轴显示范围
            plt.title(f"(a){file_name}", fontproperties='Times New Roman', size=30)  # 设置图表标题格式
            plt.ylabel("PCC", fontproperties='Times New Roman', size=20)  # 设置y轴标签
        elif file_name == "MSE":
            plt.axis([-0.5, 36.5, 2, 26])  # 设置xy轴显示范围

            plt.title(f"(b){file_name}", fontproperties='Times New Roman', size=30)  # 设置图表标题格式
            plt.ylabel("MSE(mm)", fontproperties='Times New Roman', size=20)  # 设置y轴标签
        elif file_name == "MAE":
            plt.axis([-0.5, 36.5, 1, 8])  # 设置xy轴显示范围

            plt.title(f"(c){file_name}", fontproperties='Times New Roman', size=30)  # 设置图表标题格式
            plt.ylabel("MAE(mm)", fontproperties='Times New Roman', size=20)  # 设置y轴标签
        elif file_name == "BIAS":
            plt.axis([-0.5, 36.5, -4.2, 4.6])  # 设置xy轴显示范围

            plt.title(f"(d){file_name}", fontproperties='Times New Roman', size=30)  # 设置图表标题格式
            plt.ylabel("BIAS(mm)", fontproperties='Times New Roman', size=20)  # 设置y轴标签

        plt.legend(loc="upper left")  # 显示图例
        plt.grid(b=True, which='major', axis='both', linestyle='--')  # 设置网格线

        # plt.savefig(fr"C:\Users\Casablanca\Desktop\新建文件夹\{file_name}.png", dpi=1500, bbox_inches='tight')  # 保存文件

        plt.show()
        plt.close()
        break
    print("All Right!")


# 绘制箱型图
def box():
    foder_path2 = r"C:\Users\Casablanca\Desktop\box\*.csv"
    path_list2 = glob.glob(foder_path2)
    month_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "July", "Aug", "Sep", "Oct", "Nov", "Dec"]
    abcd = ["d", "c", "b", "a"]
    for i, _abcd in zip(path_list2, abcd):
        file_name = os.path.basename(i)[:-4]
        file = pd.read_csv(i).iloc[:, 1:]
        print(file)

        plt.figure(figsize=(8, 5), dpi=100)  # 设置图表长宽比
        plt.boxplot(file, patch_artist=True, boxprops={'color': 'black', 'facecolor': 'lightgreen'}, sym='g.')

        plt.title(f"({_abcd}) {file_name}", fontproperties='Times New Roman', size=30)  # 设置图表标题格式
        x = list(range(1, 13))
        xticks = [month_list[j - 1] for j in x]
        plt.grid(b=True, which='major', axis='both', linestyle='--')  # 设置网格线

        # plt.xticks(x,month_list)
        plt.xticks(x, month_list)
        plt.xlabel("Month", fontproperties='Times New Roman', size=20)  # 设置x轴标签
        if file_name == "PCC":
            plt.title(f"(a){file_name}", fontproperties='Times New Roman', size=30)  # 设置图表标题格式
            plt.ylabel("PCC", fontproperties='Times New Roman', size=20)  # 设置y轴标签
        elif file_name == "MSE":
            plt.title(f"(b){file_name}", fontproperties='Times New Roman', size=30)  # 设置图表标题格式
            plt.ylabel("MSE(mm)", fontproperties='Times New Roman', size=20)  # 设置y轴标签
        elif file_name == "MAE":
            plt.title(f"(c){file_name}", fontproperties='Times New Roman', size=30)  # 设置图表标题格式
            plt.ylabel("MAE(mm)", fontproperties='Times New Roman', size=20)  # 设置y轴标签
        elif file_name == "BIAS":
            plt.title(f"(d){file_name}", fontproperties='Times New Roman', size=30)  # 设置图表标题格式
            plt.ylabel("BIAS(mm)", fontproperties='Times New Roman', size=20)  # 设置y轴标签

        # plt.savefig(fr"C:\Users\Casablanca\Desktop\新建文件夹\{file_name}.png", dpi=1500, bbox_inches='tight')  # 保存文件
        plt.show()
        break

