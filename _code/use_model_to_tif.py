import os
import re
from tqdm import tqdm
import pandas as pd
from osgeo import gdal
import glob
import numpy as np


# 定义读取tiff文件函数
def read_tiff(file_path):
    # 打开GeoTIFF波段1，索引为1
    # 波段索引从1开始，而不是0
    tiff = gdal.Open(file_path)
    tiff_width = tiff.RasterXSize  # 栅格矩阵的列数
    tiff_height = tiff.RasterYSize  # 栅格矩阵的行数
    # tiff_bands = tiff.RasterCount  # 波段数
    if tiff_width == 437 and tiff_height == 340:
        tiff_data = tiff.ReadAsArray(0, 0, tiff_width, tiff_height)  # 获取数据
    elif tiff_width == 438 and tiff_height == 340:
        tiff_data = tiff.ReadAsArray(0, 0, tiff_width - 1, tiff_height)  # 获取数据
    else:
        print("这个文件大小既不是340*437，也不是340*438：", file_path, "。请检查代码以及文件。")
        tiff_data = None
    # tiff_geotrans = tiff.GetGeoTransform()  # 获取仿射矩阵信息
    # tiff_proj = tiff.GetProjection()  # 获取投影信息
    return tiff, tiff_data


"""
实验所需数据为：["gpm","trmm","cdr","ndvi","month","ele","day2"],经过相关性分析，最终选取["gpm", "trmm", "cdr","cloud", "month","day2"]
"""

# 确定各个文件路径
# gpm_folder_path = r"F:\precipitation\data\GPM\GPM_2019_cut\*.tif"
# trmm_folder_path = r"F:\precipitation\data\TRMM\trmm_2019_cut\*.tif"
# cdr_folder_path = r"F:\precipitation\data\persiann_CDR\cdr_2019_cut\*.tif"
# ndvi_folder_path = r"F:\precipitation\data\modis_10000\modis_ndvi_resmple_cut\*.tif"
# ele_folder_path = r"F:\precipitation\data\DEM\dem_30m_1000m_cut.tif"
# cloud_folder_path = r"F:\precipitation\data\cloud\cloud_tif_cut\*.tif"
# 确定各个文件路径
gpm_folder_path = r"F:\precipitation\data\GPM\GPM_2019_cut_matrix\*.tif"
trmm_folder_path = r"F:\precipitation\data\TRMM\trmm_2019_cut_matrix\*.tif"
cdr_folder_path = r"F:\precipitation\data\persiann_CDR\cdr_2019_cut_matrix\*.tif"
ndvi_folder_path = r"F:\precipitation\data\modis_10000\modis_ndvi_resmple_cut\*.tif"
ele_folder_path = r"F:\precipitation\data\DEM\dem_30m_1000m_cut.tif"
cloud_folder_path = r"F:\precipitation\data\cloud\cloud_tif_cut_matrix\*.tif"

gpm_path_list = glob.glob(gpm_folder_path)
trmm_path_list = glob.glob(trmm_folder_path)
cdr_path_list = glob.glob(cdr_folder_path)
cloud_path_list = glob.glob(cloud_folder_path)
# NDVI和ele最终不参与融合,加入cloud
ndvi_path_list = glob.glob(ndvi_folder_path)  # NDVI为16天分辨率，因此需要延长16倍,即总共23个文件*16=368个文件，再去掉最后多余的三个
ndvi_path_list16 = sorted(ndvi_path_list * 16)[:-3]  # 将NDVI进行延长并去掉最后三个
ele_path_list = glob.glob(ele_folder_path) * 365  # 高程固定不变，因此只有一份，需要延长365倍

day2_list = list(range(1, 366))
month_list = []
for i in gpm_path_list:
    regx = "2019-(.*)-"
    a = re.findall(regx, i)
    month_list.append(int(a[0]))


# 调用模型生成融合值
def model(data):
    from sklearn.preprocessing import MinMaxScaler
    import joblib

    data_1 = pd.read_csv(
        r"F:\precipitation\data2\train_model\all_data_train_del_abnormal.csv")

    predictors = data_1[["gpm", "trmm", "cdr", "cloud", "month", "day2"]].values

    min_max_scaler = MinMaxScaler()

    predictors = min_max_scaler.fit_transform(predictors)
    in_data = min_max_scaler.transform(data)

    # 调用保存的模型
    regressor = joblib.load(
        r"F:\precipitation\data2\fusion_precipitation\gpm, trmm, cdr,cloud, month,day2.joblib")  # 此处需与输入变量个数相同
    out_data = regressor.predict(in_data)

    return out_data


# 定义创建tif的函数
def create_tif(tif_path, tif_name, row, col, geotransform, projection, matrix_name):
    # 生成tif
    out_file_tif_path = os.path.join(tif_path, tif_name)
    # row = 437
    # col = 340

    driver = gdal.GetDriverByName("GTiff")
    out_tif = driver.Create(out_file_tif_path, col, row, 1, gdal.GDT_Float64)

    out_tif.SetGeoTransform(geotransform)
    out_tif.SetProjection(projection)
    out_tif.GetRasterBand(1).WriteArray(np.where(matrix_name < 0, 0, matrix_name))
    # out_tif.GetRasterBand(1).WriteArray(matrix_name)
    del out_tif


# 主函数，调用模型批量生成融合数据
def use_model_to_tif():
    for gpm_path, trmm_path, cdr_path, cloud_path, month, day2 in tqdm(zip(
            gpm_path_list, trmm_path_list, cdr_path_list, cloud_path_list, month_list, day2_list
    )):
        gpm_tiff, gpm_tiff_data = read_tiff(gpm_path)
        trmm_tiff, trmm_tiff_data = read_tiff(trmm_path)
        cdr_tiff, cdr_tiff_data = read_tiff(cdr_path)
        cloud_tiff, cloud_tiff_data = read_tiff(cloud_path)

        all_tiff = np.stack(
            (gpm_tiff_data, trmm_tiff_data, cdr_tiff_data, cloud_tiff_data)
        )  # 将多个tif矩阵进行叠加

        all_tiff_1 = all_tiff.reshape((4, -1))  # 将叠加后矩阵转换为二维
        # print("转置：", all_tiff_1.T)
        # print(all_tiff_1.T.shape)
        month_day2 = (np.array([month, day2] * 148580)).reshape((148580, 2))
        in_matrix = np.concatenate((all_tiff_1.T, month_day2), axis=1)
        # print(in_matrix)
        predict_data = model(in_matrix)
        # print("预测数据:", predict_data)
        # print("预测数据形状", predict_data.shape)
        # print("预测数据类型", type(predict_data))

        predict_data_tif = predict_data.reshape((340, 437))

        tif_name = os.path.basename(gpm_path)[:-4]  # 通过gpm数据文件名为生成的tif数据命名

        create_tif(
            tif_path=r"F:\precipitation\data2\fusion_precipitation\daily_success", tif_name=tif_name,
            row=gpm_tiff.RasterYSize,
            col=gpm_tiff.RasterXSize,
            geotransform=gpm_tiff.GetGeoTransform(), projection=gpm_tiff.GetProjection(), matrix_name=predict_data_tif
        )  # 调用创建tif文件函数，将gpm数据的大小、仿射信息、投影信息运用到生成的tif


# if __name__ == "__main__":
#     use_model_to_tif()
